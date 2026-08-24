"""Exact-scope consent and minimum-necessary egress compilation."""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .validate import (
    ValidationError,
    strict_json_loads,
    validate_consent,
    validate_egress,
    validate_ledger_event,
)
from .vault import subject_dir


EVENT_DATA_CLASSES = {
    "meal": "wellness_logs",
    "meal_photo": "meal_photos",
    "hrv_rollup": "wearable_rollups",
    "wearable_rollup": "wearable_rollups",
    "supplement_intake": "supplement_stack",
    "lab_index": "clinical_records_index",
    "visit": "clinical_records_index",
    "symptom": "clinical_records_content",
    "medication_intake": "clinical_records_content",
    "protocol_outcome": "protocol_outcomes_deid",
}


def event_data_class(event: dict[str, Any]) -> str:
    if event.get("sensitivity_class") == "genomic":
        return "genomic"
    if event.get("sensitivity_class") == "clinical":
        if event.get("kind") in {"lab_index", "visit"}:
            return "clinical_records_index"
        return "clinical_records_content"
    return EVENT_DATA_CLASSES.get(str(event.get("kind")), "wellness_logs")


def _load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = strict_json_loads(path.read_text(encoding="utf-8"), label)
    except FileNotFoundError as exc:
        raise ValidationError(f"missing {label}: {path.name}") from exc
    except ValidationError:
        raise
    if not isinstance(value, dict):
        raise ValidationError(f"{label} must be an object: {path.name}")
    return value


def load_egress_policy(vault: Path, household_id: str, subject_id: str) -> dict[str, Any]:
    policy = _load_json(subject_dir(vault, subject_id) / "egress.json", "egress policy")
    validate_egress(policy)
    if policy["household_id"] != household_id or policy["subject_id"] != subject_id:
        raise ValidationError("egress policy belongs to another household or subject")
    return policy


def _validate_consent_chain(grants: list[dict[str, Any]]) -> None:
    by_id: dict[str, dict[str, Any]] = {}
    for grant in grants:
        consent_id = grant["consent_id"]
        if consent_id in by_id:
            raise ValidationError(f"duplicate consent_id is ambiguous and denied: {consent_id}")
        by_id[consent_id] = grant

    successor_by_predecessor: dict[str, str] = {}
    for grant in grants:
        predecessor_id = grant.get("supersedes_consent_id")
        if not predecessor_id:
            if grant["revision"] != 1:
                raise ValidationError(f"root consent {grant['consent_id']} must have revision 1")
            continue
        predecessor = by_id.get(predecessor_id)
        if predecessor is None:
            raise ValidationError(f"consent {grant['consent_id']} supersedes an unknown consent")
        if predecessor_id in successor_by_predecessor:
            raise ValidationError(f"consent {predecessor_id} has multiple successors; deny ambiguous precedence")
        successor_by_predecessor[predecessor_id] = grant["consent_id"]
        if grant["revision"] != predecessor["revision"] + 1:
            raise ValidationError(f"consent {grant['consent_id']} revision is not predecessor + 1")
        granted = datetime.fromisoformat(grant["granted_at"].replace("Z", "+00:00"))
        predecessor_granted = datetime.fromisoformat(predecessor["granted_at"].replace("Z", "+00:00"))
        if granted < predecessor_granted:
            raise ValidationError(f"consent {grant['consent_id']} predates its predecessor")
        predecessor_withdrawn_at = predecessor.get("withdrawn_at")
        if predecessor_withdrawn_at:
            withdrawn = datetime.fromisoformat(str(predecessor_withdrawn_at).replace("Z", "+00:00"))
            if granted <= withdrawn:
                raise ValidationError(
                    f"consent {grant['consent_id']} must postdate its predecessor withdrawal"
                )

    for start in by_id:
        seen: set[str] = set()
        cursor = start
        while cursor in successor_by_predecessor:
            if cursor in seen:
                raise ValidationError("consent supersession cycle detected")
            seen.add(cursor)
            cursor = successor_by_predecessor[cursor]


def load_consents(vault: Path, household_id: str, subject_id: str) -> list[dict[str, Any]]:
    root = subject_dir(vault, subject_id) / "consent"
    if not root.exists():
        raise ValidationError("consent directory is missing")
    paths = sorted(root.glob("*.json"))
    if not paths:
        raise ValidationError("no consent grants exist for this subject")
    grants: list[dict[str, Any]] = []
    for path in paths:
        consent = _load_json(path, "consent grant")
        validate_consent(consent)
        if consent["household_id"] != household_id or consent["subject_id"] != subject_id:
            raise ValidationError(f"consent grant {path.name} belongs to another household or subject")
        grants.append(consent)
    _validate_consent_chain(grants)
    return grants


def _is_active(consent: dict[str, Any], superseded_ids: set[str]) -> bool:
    if consent["consent_id"] in superseded_ids or consent["status"] != "active":
        return False
    expires_at = consent.get("expires_at")
    if not expires_at:
        return True
    expires = datetime.fromisoformat(str(expires_at).replace("Z", "+00:00"))
    return expires > datetime.now(timezone.utc)


def _active_grants(grants: list[dict[str, Any]]) -> list[dict[str, Any]]:
    superseded = {
        grant["supersedes_consent_id"]
        for grant in grants
        if grant.get("supersedes_consent_id")
    }
    return [grant for grant in grants if _is_active(grant, superseded)]


def _base_scope_matches(
    grant: dict[str, Any],
    *,
    recipient_id: str,
    recipient_kind: str,
    processor_id: str,
    processor_kind: str,
    target_tier: str,
    purpose: str,
    action: str,
) -> bool:
    if grant.get("field_allowlist"):
        # Field-level compilation is intentionally not implemented. Ignore would broaden consent.
        return False
    recipient_match = any(
        item["recipient_id"] == recipient_id and item["kind"] == recipient_kind
        for item in grant["recipients"]
    )
    processor_match = any(
        item["processor_id"] == processor_id
        and item["kind"] == processor_kind
        and target_tier in item["allowed_tiers"]
        for item in grant["processors"]
    )
    return (
        recipient_match
        and processor_match
        and purpose in grant["purposes"]
        and action in grant["actions"]
    )


def matching_consent_ids(
    grants: list[dict[str, Any]],
    *,
    recipient_id: str,
    recipient_kind: str,
    processor_id: str,
    processor_kind: str,
    target_tier: str,
    purpose: str,
    action: str,
    data_class: str,
    event_id: str | None = None,
    protocol_run_id: str | None = None,
) -> list[str]:
    matched: list[str] = []
    for grant in _active_grants(grants):
        if not _base_scope_matches(
            grant,
            recipient_id=recipient_id,
            recipient_kind=recipient_kind,
            processor_id=processor_id,
            processor_kind=processor_kind,
            target_tier=target_tier,
            purpose=purpose,
            action=action,
        ):
            continue
        if data_class not in grant["data_classes"]:
            continue
        scope = grant["record_scope"]
        if event_id is not None and event_id not in scope["event_ids"]:
            continue
        if event_id is None and data_class != "identifiers":
            # Data-bearing records always need an exact event scope.
            continue
        if protocol_run_id is not None and protocol_run_id not in scope["protocol_run_ids"]:
            continue
        if data_class == "protocol_outcomes_deid" and protocol_run_id is None:
            continue
        matched.append(grant["consent_id"])
    return sorted(set(matched))


def consent_allows(
    grants: list[dict[str, Any]],
    **scope: Any,
) -> bool:
    return bool(matching_consent_ids(grants, **scope))


def require_export_consent(
    grants: list[dict[str, Any]],
    *,
    recipient_id: str,
    recipient_kind: str,
    processor_id: str,
    processor_kind: str,
    target_tier: str,
    purpose: str,
) -> list[str]:
    matches = sorted(
        grant["consent_id"]
        for grant in _active_grants(grants)
        if _base_scope_matches(
            grant,
            recipient_id=recipient_id,
            recipient_kind=recipient_kind,
            processor_id=processor_id,
            processor_kind=processor_kind,
            target_tier=target_tier,
            purpose=purpose,
            action="export",
        )
    )
    if matches:
        return matches
    raise ValidationError(
        "no active exact-scope export consent for the recipient, processor, purpose, action, and tier"
    )


def _egress_rule(policy: dict[str, Any], sensitivity_class: str) -> dict[str, Any]:
    matches = [rule for rule in policy["rules"] if rule["sensitivity_class"] == sensitivity_class]
    if len(matches) != 1:
        raise ValidationError(f"egress policy must have exactly one rule for {sensitivity_class}")
    return matches[0]


def _redact_event(
    event: dict[str, Any], profile: str, *, include_identifiers: bool
) -> dict[str, Any] | None:
    if profile == "none":
        result = deepcopy(event)
        result.pop("media_refs", None)
        result.pop("consent_ids", None)
        result["source"] = {"channel": (event.get("source") or {}).get("channel", "unknown")}
        if not include_identifiers:
            for key in ("household_id", "subject_id", "operator_id"):
                result.pop(key, None)
        return result
    if profile in {"block", "aggregate_only"}:
        return None
    redacted: dict[str, Any] = {
        "event_id": event["event_id"],
        "recorded_at": event["recorded_at"],
        "kind": event["kind"],
        "sensitivity_class": event["sensitivity_class"],
        "redaction_profile": profile,
    }
    for key in ("protocol_id", "protocol_run_id"):
        if event.get(key):
            redacted[key] = event[key]
    numeric_metrics = {
        key: value
        for key, value in (event.get("metrics") or {}).items()
        if isinstance(value, (int, float, bool))
    }
    if profile == "identifiers_only" and numeric_metrics:
        redacted["metrics"] = numeric_metrics
    return redacted


def authorize_export_identity(
    *,
    grants: list[dict[str, Any]],
    recipient_id: str,
    recipient_kind: str,
    processor_id: str,
    processor_kind: str,
    policy: dict[str, Any],
    target_tier: str,
    purpose: str = "clinician_handoff",
) -> bool:
    if not consent_allows(
        grants,
        recipient_id=recipient_id,
        recipient_kind=recipient_kind,
        processor_id=processor_id,
        processor_kind=processor_kind,
        target_tier=target_tier,
        purpose=purpose,
        action="export",
        data_class="identifiers",
    ):
        return False
    rule = _egress_rule(policy, "personal")
    return target_tier in rule["allowed_tiers"] and rule["redaction_profile"] == "none"


def compile_export_events(
    events: list[dict[str, Any]],
    *,
    grants: list[dict[str, Any]],
    policy: dict[str, Any],
    recipient_id: str,
    recipient_kind: str,
    processor_id: str,
    processor_kind: str,
    target_tier: str,
    purpose: str = "clinician_handoff",
) -> dict[str, Any]:
    included: list[dict[str, Any]] = []
    consent_ids: set[str] = set()
    seen_event_ids: set[str] = set()
    include_identifiers = authorize_export_identity(
        grants=grants,
        recipient_id=recipient_id,
        recipient_kind=recipient_kind,
        processor_id=processor_id,
        processor_kind=processor_kind,
        policy=policy,
        target_tier=target_tier,
        purpose=purpose,
    )
    for event in events:
        # compile_export_events is a public boundary and must not trust an in-memory caller to have
        # loaded the event through the ledger validator first.
        validate_ledger_event(event)
        event_id = event["event_id"]
        if event_id in seen_event_ids:
            raise ValidationError(f"export input contains duplicate event_id {event_id}")
        seen_event_ids.add(event_id)
        matches = matching_consent_ids(
            grants,
            recipient_id=recipient_id,
            recipient_kind=recipient_kind,
            processor_id=processor_id,
            processor_kind=processor_kind,
            target_tier=target_tier,
            purpose=purpose,
            action="export",
            data_class=event_data_class(event),
            event_id=event_id,
            protocol_run_id=event.get("protocol_run_id"),
        )
        if not matches:
            continue
        rule = _egress_rule(policy, event["sensitivity_class"])
        if target_tier not in rule["allowed_tiers"] or "none" in rule["allowed_tiers"]:
            continue
        redacted = _redact_event(
            event,
            rule["redaction_profile"],
            include_identifiers=include_identifiers,
        )
        if redacted is None:
            continue
        included.append(redacted)
        consent_ids.update(matches)
    return {
        "included": included,
        "consent_ids": sorted(consent_ids),
    }
