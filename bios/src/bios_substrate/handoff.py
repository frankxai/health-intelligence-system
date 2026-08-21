"""Clinician handoff one-pager generator."""

from __future__ import annotations

from pathlib import Path

from . import ledger as ledger_mod
from .phenotype import rebuild_phenotype
from .protocol_ops import list_active_runs
from .vault import load_household, resolve_subject_id, subject_dir, utc_now


DISCLAIMER = (
    "This export is a patient-organized summary for clinical conversation. "
    "It is not a diagnosis, not a prescription, and not an interpretation of labs or imaging. "
    "All medical decisions remain with the licensed clinician and the patient."
)


def build_handoff(vault: Path, subject: str) -> str:
    household = load_household(vault)
    subject_id = resolve_subject_id(household, subject)
    sub = next(s for s in household["subjects"] if s["subject_id"] == subject_id)
    phenotype = rebuild_phenotype(vault, subject_id)
    events = ledger_mod.read_events(vault, subject_id)
    runs = list_active_runs(vault, subject_id)
    recent = events[-15:]

    lines = [
        f"# Clinician handoff — {sub['display_name']}",
        "",
        f"_Generated: {utc_now()} · BIOS v0.1 · household `{household['household_id']}`_",
        "",
        f"> {DISCLAIMER}",
        "",
        "## Identity (minimum)",
        "",
        f"- Subject label: {sub['display_name']}",
        f"- Subject id (local): `{subject_id}`",
        f"- Timezone: {sub.get('timezone', 'unspecified')}",
        "",
        "## Why we are here",
        "",
        "_Patient/steward: replace this line with the appointment purpose in your own words._",
        "",
        "## Current ordinary-wellness stack (self-reported)",
        "",
    ]
    if phenotype.get("current_stack"):
        for item in phenotype["current_stack"]:
            lines.append(f"- {item['kind']}: {item['name']}" + (f" ({item.get('timing_note')})" if item.get("timing_note") else ""))
    else:
        lines.append("- (none logged yet)")

    lines += ["", "## Active n-of-1 protocols (ordinary wellness unless noted)", ""]
    if runs:
        for r in runs:
            title = r.get("protocol_snapshot", {}).get("title", r["protocol_id"])
            lines.append(f"- {title} — started {r['started_at']} — run `{r['run_id']}`")
    else:
        lines.append("- (none)")

    lines += ["", "## Recent observations (facts only)", ""]
    if recent:
        for e in recent:
            note = (e.get("note") or "").replace("\n", " ")
            lines.append(f"- {e.get('recorded_at')} · `{e.get('kind')}` · {note[:200]}")
    else:
        lines.append("- (none)")

    lines += [
        "",
        "## Constraints / allergies (self-reported)",
        "",
    ]
    constraints = phenotype.get("constraints") or []
    if constraints:
        for c in constraints:
            lines.append(f"- {c.get('label')} (source: {c.get('source')})")
    else:
        lines.append("- (none logged — confirm verbally)")

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
        "---",
        "",
        f"_Event count in local ledger: {phenotype.get('ledger_event_count', 0)}_",
        "",
    ]
    text = "\n".join(lines)
    out_dir = subject_dir(vault, subject_id) / "exports"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"clinician-handoff-{utc_now().replace(':', '').replace('-', '')[:15]}.md"
    out_path.write_text(text, encoding="utf-8")
    return text
