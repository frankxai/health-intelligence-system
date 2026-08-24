"""Consent- and egress-compiled clinician handoff generator."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from . import ledger as ledger_mod
from .audit import build_handoff_receipt
from .privacy import (
    authorize_export_identity,
    compile_export_events,
    load_consents,
    load_egress_policy,
    require_export_consent,
)
from .protocol_ops import list_active_runs
from .validate import MODEL_TIERS, RECIPIENT_KINDS, ValidationError
from .vault import load_household, resolve_subject_id, subject_dir, utc_now


DISCLAIMER = (
    "This export is a patient-organized summary for clinical conversation. "
    "It is not a diagnosis, not a prescription, and not an interpretation of labs or imaging. "
    "All medical decisions remain with the licensed clinician and the patient."
)


def _wellness_stack(events: list[dict[str, Any]]) -> list[dict[str, str]]:
    stack: list[dict[str, str]] = []
    for event in events:
        note = str(event.get("note") or "").strip()
        if not note:
            continue
        if event.get("kind") in {"tea", "supplement_intake", "breath_session"}:
            stack.append({"kind": str(event["kind"]), "name": note[:80]})
    seen: set[tuple[str, str]] = set()
    result: list[dict[str, str]] = []
    for item in reversed(stack):
        key = (item["kind"], item["name"].lower())
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return list(reversed(result))[-20:]


def build_handoff(
    vault: Path,
    subject: str,
    *,
    recipient_id: str | None = None,
    recipient_kind: str = "self",
    processor_id: str = "bios_local_runtime",
    processor_kind: str = "local_runtime",
    target_tier: str = "local",
    persist_internal: bool = True,
) -> str:
    """Compile a local, user-reviewable handoff through consent and egress.

    This function does not send data. A clinician recipient requires an explicit
    active grant matching that recipient id. The default compiles for the subject
    themself on the local tier so they can review before any separate sharing.
    """

    if recipient_kind not in RECIPIENT_KINDS:
        raise ValidationError(f"unsupported recipient kind: {recipient_kind}")
    if target_tier not in MODEL_TIERS or target_tier == "none":
        raise ValidationError(f"unsupported export target tier: {target_tier}")

    household = load_household(vault)
    subject_id = resolve_subject_id(household, subject)
    recipient_id = recipient_id or subject_id
    sub = next(item for item in household["subjects"] if item["subject_id"] == subject_id)
    grants = load_consents(vault, household["household_id"], subject_id)
    policy = load_egress_policy(vault, household["household_id"], subject_id)
    base_consent_ids = require_export_consent(
        grants,
        recipient_id=recipient_id,
        recipient_kind=recipient_kind,
        processor_id=processor_id,
        processor_kind=processor_kind,
        target_tier=target_tier,
        purpose="clinician_handoff",
    )

    events = ledger_mod.read_events(vault, subject_id)
    compiled = compile_export_events(
        events,
        grants=grants,
        policy=policy,
        recipient_id=recipient_id,
        recipient_kind=recipient_kind,
        processor_id=processor_id,
        processor_kind=processor_kind,
        target_tier=target_tier,
    )
    safe_events = compiled["included"]
    recent = safe_events[-15:]
    identity_allowed = authorize_export_identity(
        grants=grants,
        recipient_id=recipient_id,
        recipient_kind=recipient_kind,
        processor_id=processor_id,
        processor_kind=processor_kind,
        policy=policy,
        target_tier=target_tier,
    )

    visible_protocol_ids = {
        event.get("protocol_id")
        for event in safe_events
        if event.get("kind") == "protocol_start" and event.get("protocol_id")
    }
    visible_run_ids = {
        event.get("protocol_run_id")
        for event in safe_events
        if event.get("protocol_run_id")
    }
    runs: list[dict[str, Any]] = [
        run
        for run in list_active_runs(vault, subject_id)
        if run["protocol_id"] in visible_protocol_ids and run["run_id"] in visible_run_ids
    ]

    subject_label = sub["display_name"] if identity_allowed else "Subject (identity withheld by consent)"
    lines = [
        f"# Clinician handoff — {subject_label}",
        "",
        f"_Generated: {utc_now()} · BIOS v0.1 · target tier `{target_tier}`_",
        "",
        f"> {DISCLAIMER}",
        "",
        "## Export boundary",
        "",
        f"- Intended recipient: `{recipient_id if (identity_allowed or recipient_id != subject_id) else 'withheld-self-id'}` (`{recipient_kind}`)",
        f"- Authorized processor: `{processor_id}` (`{processor_kind}`)",
        "- This file was compiled locally and was not sent by BIOS.",
        "- The person/steward must review it before sharing.",
        f"- Included ledger events: {len(safe_events)}",
        "",
        "## Identity (minimum)",
        "",
    ]
    if identity_allowed:
        lines.extend([
            f"- Subject label: {sub['display_name']}",
            f"- Subject id (local): `{subject_id}`",
            f"- Timezone: {sub.get('timezone', 'unspecified')}",
        ])
    else:
        lines.append("- Withheld: no active identifiers consent for this recipient.")

    lines += [
        "",
        "## Why we are here",
        "",
        "_Patient/steward: replace this line with the appointment purpose in your own words._",
        "",
        "## Current ordinary-wellness stack (self-reported)",
        "",
    ]
    stack = _wellness_stack(safe_events)
    if stack:
        lines.extend(f"- {item['kind']}: {item['name']}" for item in stack)
    else:
        lines.append("- (none permitted by the active export policy)")

    lines += ["", "## Active n-of-1 protocols (ordinary wellness unless noted)", ""]
    if runs:
        for run in runs:
            title = run.get("protocol_snapshot", {}).get("title", run["protocol_id"])
            lines.append(f"- {title} — started {run['started_at']} — run `{run['run_id']}`")
    else:
        lines.append("- (none permitted by the active export policy)")

    lines += ["", "## Recent observations (facts only)", ""]
    if recent:
        for event in recent:
            note = str(event.get("note") or "").replace("\n", " ")
            detail = note[:200] if note else f"[{event.get('redaction_profile', 'structured data only')}]"
            lines.append(f"- {event.get('recorded_at')} · `{event.get('kind')}` · {detail}")
    else:
        lines.append("- (none permitted by the active export policy)")

    lines += [
        "",
        "## Three questions for the clinician",
        "",
        "1. _…_",
        "2. _…_",
        "3. _…_",
        "",
        "## Data request template (for clinic / portal)",
        "",
        "Please provide copies or portal access for:",
        "",
        "- problem list and visit notes from the last 12 months",
        "- current medication and allergy list",
        "- lab results and imaging reports relevant to today’s visit",
        "- care plan / follow-up instructions in writing",
        "",
        "## Red flags acknowledged",
        "",
        "If emergency symptoms occur (chest pain, trouble breathing, stroke signs, severe bleeding, "
        "suicidal crisis, etc.), call local emergency services — do not wait on this document or any AI.",
        "",
    ]
    body = "\n".join(lines + ["", "---", ""])
    receipt = build_handoff_receipt(
        vault,
        household_id=household["household_id"],
        subject_id=subject_id,
        recipient_id=recipient_id,
        recipient_kind=recipient_kind,
        processor_id=processor_id,
        processor_kind=processor_kind,
        target_tier=target_tier,
        included_event_ids=[event["event_id"] for event in safe_events],
        included_protocol_run_ids=[run["run_id"] for run in runs],
        consent_ids=sorted(set(base_consent_ids) | set(compiled["consent_ids"])),
        egress_policy=policy,
        content=body,
    )
    text = body + "\n".join(
        [
            "## Privacy receipt",
            "",
            f"- Receipt: `{receipt['receipt_id']}`",
            f"- Content SHA-256: `{receipt['content_sha256']}`",
            f"- HMAC signature: `{receipt['signature']['value']}`",
            "- Local audit receipt retained inside the synthetic vault; BIOS did not transmit this file.",
            "",
        ]
    )
    if persist_internal:
        out_dir = subject_dir(vault, subject_id) / "exports"
        out_dir.mkdir(parents=True, exist_ok=True)
        timestamp = utc_now().replace(":", "").replace("-", "")[:15]
        (out_dir / f"clinician-handoff-{timestamp}.md").write_text(text, encoding="utf-8")
    return text
