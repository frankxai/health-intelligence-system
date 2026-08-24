"""Draft 2020-12 schema validation plus fail-closed BIOS semantic gates."""

from __future__ import annotations

import json
import re
from datetime import date, datetime, timedelta, timezone
from functools import lru_cache
from typing import Any
from urllib.parse import urlparse

from jsonschema import Draft202012Validator, FormatChecker

from .paths import SCHEMAS


FORMAT_CHECKER = FormatChecker()


@FORMAT_CHECKER.checks("date-time")
def _format_date_time(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


@FORMAT_CHECKER.checks("uri")
def _format_uri(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return bool(parsed.scheme and parsed.netloc)


class ValidationError(ValueError):
    """A BIOS document was malformed or unsafe to consume."""


SCHEMA_VERSION = "0.1.0"
CLAIM_SCHEMA_VERSION = "0.1.1"
SENSITIVITY_CLASSES = {"public", "personal", "clinical", "genomic"}
SENSITIVITY_RANK = {"public": 0, "personal": 1, "clinical": 2, "genomic": 3}
MODEL_TIERS = {"local", "tee_or_venice", "frontier", "none"}
REDACTION_PROFILES = {"none", "identifiers_only", "clinical_strip", "aggregate_only", "block"}
EVIDENCE_TIERS = {"A", "B", "C", "D", "E", "Q"}
CITABLE_EVIDENCE_TIERS = {"A", "B", "C", "D"}
CERTAINTY_LEVELS = {"high", "moderate", "low", "very_low", "uncertain"}
CLAIM_STATUSES = {"draft", "active", "disputed", "withdrawn", "superseded", "retracted"}
SOURCE_KINDS = {
    "grade_guideline", "systematic_review_guideline", "systematic_review",
    "living_review", "umbrella_review", "registered_rct", "observational",
    "diagnostic", "implementation", "mechanistic", "authority_education",
    "book", "podcast", "preprint", "animal", "testimonial", "marketing",
    "traditional_source", "url",
}
DISCOVERY_ONLY_SOURCE_KINDS = {
    "authority_education", "book", "podcast", "preprint", "animal", "testimonial",
    "marketing", "traditional_source", "url",
}
SOURCE_LICENSES = {"cc0", "cc_by_4_0", "cc_by_nc_4_0", "public_domain", "publisher_terms", "authority_site_terms", "unknown"}
SOURCE_USE_PERMISSIONS = {"metadata_only", "open_access_full_text", "public_domain_full_text", "licensed_excerpt"}
CORRECTION_STATUSES = {"not_checked", "none_found", "corrected", "retracted", "expression_of_concern"}
CONFLICT_STATUSES = {"none_declared", "declared", "unknown", "not_applicable"}
PROTOCOL_CLASSES = {"ordinary_wellness", "habit_tracking", "education", "clinician_supervised_only", "jurisdiction_restricted"}
PROTOCOL_DOMAINS = {"circadian", "breath", "nutrition", "tea", "mind", "movement", "sleep", "custom"}
EVENT_KINDS = {
    "note", "symptom", "mood", "sleep", "breath_session", "meal", "meal_photo",
    "hydration", "tea", "supplement_intake", "medication_intake", "movement", "training",
    "hrv_rollup", "wearable_rollup", "lab_index", "visit", "protocol_start",
    "protocol_checkin", "protocol_stop", "protocol_outcome", "consent_grant",
    "consent_revoke", "export", "red_flag_ack",
}
PROTOCOL_EVENT_KINDS = {"protocol_start", "protocol_checkin", "protocol_stop", "protocol_outcome"}
CLINICAL_EVENT_KINDS = {"symptom", "medication_intake", "lab_index", "visit"}
SOURCE_CHANNELS = {"human", "phone", "wearable", "import", "agent", "clinician_export", "photo"}
CONSENT_PURPOSES = {"self_tracking", "family_stewardship", "clinician_handoff", "agent_assist", "research_contribution", "backup", "education"}
CONSENT_DATA_CLASSES = {
    "wellness_logs", "meal_photos", "wearable_rollups", "supplement_stack",
    "clinical_records_index", "clinical_records_content", "genomic", "identifiers",
    "protocol_outcomes_deid",
}
CONSENT_ACTIONS = {"collect", "store", "summarize", "ai_process", "export", "share", "contribute_deid"}
RECIPIENT_KINDS = {"self", "steward", "household_member", "clinician", "local_agent", "frontier_model", "commons", "backup_target"}
PROCESSOR_KINDS = {"local_runtime", "local_human_tool", "hosted_model", "backup_service"}
PROTOCOL_RELEASE_STATUSES = {"draft_synthetic", "reviewed"}
CONTRAINDICATION_SEVERITIES = {"review", "high", "critical"}
CONTRAINDICATION_ACTIONS = {
    "block_pending_human_review",
    "block_and_require_verified_signed_clearance",
    "permanent_runtime_block",
}
RESERVED_PUBLIC_NAMES = {"vitalis", "velora"}
TIER_SOURCE_KINDS = {
    "A": {"grade_guideline", "systematic_review_guideline"},
    "B": {"systematic_review", "living_review", "umbrella_review"},
    "C": {"registered_rct"},
    "D": {"observational", "diagnostic", "implementation", "mechanistic"},
}
EVIDENCE_RANK = {
    "Q": 0,
    "E": 1,
    "D": 2,
    "C": 3,
    "B": 4,
    "A": 5,
}


def strict_json_loads(text: str, label: str) -> Any:
    """Parse JSON while rejecting duplicate object keys."""

    def pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValidationError(f"{label} contains duplicate key {key!r}")
            result[key] = value
        return result

    try:
        return json.loads(text, object_pairs_hook=pairs_hook)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{label} is not valid JSON") from exc


@lru_cache(maxsize=None)
def _schema_validator(schema_name: str) -> Draft202012Validator:
    path = SCHEMAS / schema_name
    try:
        schema = strict_json_loads(path.read_text(encoding="utf-8"), f"schema {schema_name}")
    except FileNotFoundError as exc:
        raise ValidationError(f"published schema is missing: {schema_name}") from exc
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:  # jsonschema raises version-specific SchemaError
        raise ValidationError(f"published schema is invalid: {schema_name}: {exc}") from exc
    return Draft202012Validator(schema, format_checker=FORMAT_CHECKER)


def validate_published_schema(value: Any, schema_name: str, label: str) -> None:
    """Validate against the shipped schema before applying stricter semantics."""

    errors = sorted(_schema_validator(schema_name).iter_errors(value), key=lambda err: list(err.path))
    if not errors:
        return
    error = errors[0]
    location = ".".join(str(part) for part in error.path)
    suffix = f" at {location}" if location else ""
    raise ValidationError(f"{label} violates {schema_name}{suffix}: {error.message}")


def _parsed_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _not_future_datetime(value: str, label: str) -> None:
    if _parsed_datetime(value) > datetime.now(timezone.utc) + timedelta(minutes=5):
        raise ValidationError(f"{label} cannot be in the future")


def _not_future_date(value: str, label: str) -> None:
    if date.fromisoformat(value) > datetime.now(timezone.utc).date():
        raise ValidationError(f"{label} cannot be in the future")


def require(obj: dict[str, Any], fields: list[str], label: str) -> None:
    missing = [field for field in fields if field not in obj or obj[field] in (None, "")]
    if missing:
        raise ValidationError(f"{label} missing required fields: {', '.join(missing)}")


def _object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValidationError(f"{label} must be an object")
    return value


def _array(value: Any, label: str, *, nonempty: bool = False) -> list[Any]:
    if not isinstance(value, list) or (nonempty and not value):
        raise ValidationError(f"{label} must be a{' non-empty' if nonempty else 'n'} array")
    return value


def _text(value: Any, label: str, *, minimum: int = 1, maximum: int | None = None) -> str:
    if not isinstance(value, str) or len(value.strip()) < minimum:
        raise ValidationError(f"{label} must be a non-empty string")
    if maximum is not None and len(value) > maximum:
        raise ValidationError(f"{label} exceeds {maximum} characters")
    return value


def _strings(value: Any, label: str, *, nonempty: bool = False, allowed: set[str] | None = None) -> list[str]:
    rows = _array(value, label, nonempty=nonempty)
    if any(not isinstance(row, str) or not row.strip() for row in rows):
        raise ValidationError(f"{label} must contain non-empty strings")
    if len(rows) != len(set(rows)):
        raise ValidationError(f"{label} must contain unique values")
    if allowed is not None and not set(rows).issubset(allowed):
        raise ValidationError(f"{label} contains unsupported values: {sorted(set(rows) - allowed)}")
    return rows


def _enum(value: Any, allowed: set[str], label: str) -> str:
    if not isinstance(value, str) or value not in allowed:
        raise ValidationError(f"{label} must be one of {sorted(allowed)}")
    return value


def _closed(obj: dict[str, Any], allowed: set[str], label: str) -> None:
    unknown = sorted(set(obj) - allowed)
    if unknown:
        raise ValidationError(f"{label} contains unknown fields: {unknown}")


def _identifier(value: Any, prefix: str, label: str) -> str:
    text = _text(value, label)
    if not re.fullmatch(rf"{re.escape(prefix)}[A-Za-z0-9_-]+", text):
        raise ValidationError(f"{label} must match {prefix}[A-Za-z0-9_-]+")
    return text


def _iso_date(value: Any, label: str) -> str:
    text = _text(value, label)
    try:
        date.fromisoformat(text)
    except ValueError as exc:
        raise ValidationError(f"{label} must be an ISO date") from exc
    return text


def _iso_datetime(value: Any, label: str) -> str:
    text = _text(value, label)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValidationError(f"{label} must be an ISO date-time") from exc
    if parsed.tzinfo is None:
        raise ValidationError(f"{label} must include a timezone")
    return text


def _https(value: Any, label: str) -> str:
    text = _text(value, label)
    parsed = urlparse(text)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValidationError(f"{label} must be an https URL")
    return text


def _version(obj: dict[str, Any], label: str) -> None:
    if obj.get("schema_version") != SCHEMA_VERSION:
        raise ValidationError(f"{label}.schema_version must be {SCHEMA_VERSION}")


def validate_ledger_event(event: dict[str, Any]) -> None:
    validate_published_schema(event, "ledger-event.schema.json", "ledger_event")
    event = _object(event, "ledger_event")
    _closed(event, {"event_id", "schema_version", "household_id", "subject_id", "operator_id", "recorded_at", "occurred_at", "kind", "sensitivity_class", "source", "tags", "note", "metrics", "protocol_id", "protocol_run_id", "media_refs", "supersedes", "consent_ids"}, "ledger_event")
    require(event, ["event_id", "schema_version", "household_id", "subject_id", "recorded_at", "kind", "sensitivity_class", "source"], "ledger_event")
    _version(event, "ledger_event")
    _identifier(event["event_id"], "evt_", "ledger_event.event_id")
    _identifier(event["household_id"], "hh_", "ledger_event.household_id")
    _identifier(event["subject_id"], "sub_", "ledger_event.subject_id")
    _iso_datetime(event["recorded_at"], "ledger_event.recorded_at")
    if "occurred_at" in event:
        _iso_datetime(event["occurred_at"], "ledger_event.occurred_at")
    kind = _enum(event["kind"], EVENT_KINDS, "ledger_event.kind")
    sensitivity = _enum(event["sensitivity_class"], SENSITIVITY_CLASSES, "ledger_event.sensitivity_class")
    minimum_sensitivity = "clinical" if kind in CLINICAL_EVENT_KINDS else "personal"
    if SENSITIVITY_RANK[sensitivity] < SENSITIVITY_RANK[minimum_sensitivity]:
        raise ValidationError(
            f"ledger_event kind {kind} requires at least {minimum_sensitivity} sensitivity"
        )
    if kind in PROTOCOL_EVENT_KINDS:
        require(event, ["protocol_id", "protocol_run_id"], "protocol ledger_event")
    if "protocol_id" in event:
        _identifier(event["protocol_id"], "proto_", "ledger_event.protocol_id")
    if "protocol_run_id" in event:
        _identifier(event["protocol_run_id"], "run_", "ledger_event.protocol_run_id")
    source = _object(event["source"], "ledger_event.source")
    _closed(source, {"channel", "device", "agent_id", "import_ref"}, "ledger_event.source")
    require(source, ["channel"], "ledger_event.source")
    _enum(source["channel"], SOURCE_CHANNELS, "ledger_event.source.channel")
    if "tags" in event:
        _strings(event["tags"], "ledger_event.tags")
    if "note" in event:
        _text(event["note"], "ledger_event.note", maximum=4000)
    if "metrics" in event:
        metrics = _object(event["metrics"], "ledger_event.metrics")
        if any(not isinstance(key, str) or not key.strip() for key in metrics):
            raise ValidationError("ledger_event.metrics keys must be non-empty strings")
        if any(isinstance(value, (dict, list)) or value is None for value in metrics.values()):
            raise ValidationError("ledger_event.metrics values must be scalar")
    if "operator_id" in event:
        _identifier(event["operator_id"], "op_", "ledger_event.operator_id")
    if "supersedes" in event:
        _identifier(event["supersedes"], "evt_", "ledger_event.supersedes")
    if "consent_ids" in event:
        for consent_id in _strings(event["consent_ids"], "ledger_event.consent_ids"):
            _identifier(consent_id, "consent_", "ledger_event.consent_ids[]")
    if "media_refs" in event:
        for index, raw in enumerate(_array(event["media_refs"], "ledger_event.media_refs")):
            ref = _object(raw, f"ledger_event.media_refs[{index}]")
            _closed(ref, {"path", "sha256", "mime"}, f"ledger_event.media_refs[{index}]")
            require(ref, ["path", "sha256"], f"ledger_event.media_refs[{index}]")
            if not re.fullmatch(r"[a-f0-9]{64}", _text(ref["sha256"], f"ledger_event.media_refs[{index}].sha256")):
                raise ValidationError("ledger_event media sha256 must be lowercase hexadecimal")


def validate_protocol(proto: dict[str, Any]) -> None:
    validate_published_schema(proto, "protocol.schema.json", "protocol")
    proto = _object(proto, "protocol")
    _closed(proto, {"protocol_id", "schema_version", "title", "release_status", "version", "domain_pack", "class", "hypothesis", "intervention", "timing", "duration", "measurement_plan", "expected_effect", "stop_conditions", "contraindications", "claim_ids", "evidence_floor", "jurisdiction_flags", "safety", "review_gate", "fork_of", "authors", "last_reviewed"}, "protocol")
    require(proto, ["protocol_id", "schema_version", "title", "release_status", "domain_pack", "class", "hypothesis", "intervention", "timing", "duration", "measurement_plan", "stop_conditions", "contraindications", "claim_ids", "evidence_floor", "jurisdiction_flags", "safety", "review_gate"], "protocol")
    _version(proto, "protocol")
    _identifier(proto["protocol_id"], "proto_", "protocol.protocol_id")
    _text(proto["title"], "protocol.title", minimum=3, maximum=160)
    release_status = _enum(proto["release_status"], PROTOCOL_RELEASE_STATUSES, "protocol.release_status")
    _enum(proto["domain_pack"], PROTOCOL_DOMAINS, "protocol.domain_pack")
    _enum(proto["class"], PROTOCOL_CLASSES, "protocol.class")
    _text(proto["hypothesis"], "protocol.hypothesis", minimum=10, maximum=2000)
    intervention = _object(proto["intervention"], "protocol.intervention")
    _closed(intervention, {"summary", "steps", "dose_descriptor", "materials"}, "protocol.intervention")
    require(intervention, ["summary", "steps"], "protocol.intervention")
    _text(intervention["summary"], "protocol.intervention.summary", minimum=5, maximum=500)
    _strings(intervention["steps"], "protocol.intervention.steps", nonempty=True)
    if "dose_descriptor" in intervention:
        _text(intervention["dose_descriptor"], "protocol.intervention.dose_descriptor")
    if "materials" in intervention:
        _strings(intervention["materials"], "protocol.intervention.materials")
    timing = _object(proto["timing"], "protocol.timing")
    _closed(timing, {"anchor", "clock_local", "phase_note", "frequency"}, "protocol.timing")
    require(timing, ["anchor"], "protocol.timing")
    _enum(timing["anchor"], {"upon_waking", "morning", "midday", "afternoon", "evening", "pre_sleep", "with_meals", "circadian_phase", "as_needed_non_urgent", "fixed_clock"}, "protocol.timing.anchor")
    for field in ("clock_local", "phase_note", "frequency"):
        if field in timing:
            _text(timing[field], f"protocol.timing.{field}")
    duration = _object(proto["duration"], "protocol.duration")
    _closed(duration, {"days", "washout_days", "min_adherence"}, "protocol.duration")
    require(duration, ["days"], "protocol.duration")
    if not isinstance(duration["days"], int) or isinstance(duration["days"], bool) or not 1 <= duration["days"] <= 366:
        raise ValidationError("protocol.duration.days must be an integer from 1 to 366")
    if "washout_days" in duration and (not isinstance(duration["washout_days"], int) or isinstance(duration["washout_days"], bool) or not 0 <= duration["washout_days"] <= 90):
        raise ValidationError("protocol.duration.washout_days must be an integer from 0 to 90")
    if "min_adherence" in duration and (not isinstance(duration["min_adherence"], (int, float)) or isinstance(duration["min_adherence"], bool) or not 0 <= duration["min_adherence"] <= 1):
        raise ValidationError("protocol.duration.min_adherence must be a number from 0 to 1")
    for index, raw in enumerate(_array(proto["measurement_plan"], "protocol.measurement_plan", nonempty=True)):
        row = _object(raw, f"protocol.measurement_plan[{index}]")
        _closed(row, {"metric", "method", "cadence", "notes"}, f"protocol.measurement_plan[{index}]")
        require(row, ["metric", "method", "cadence"], f"protocol.measurement_plan[{index}]")
        _text(row["metric"], f"protocol.measurement_plan[{index}].metric")
        _enum(row["method"], {"self_report", "photo", "wearable_rollup", "timer", "journal", "scale_1_10"}, f"protocol.measurement_plan[{index}].method")
        _text(row["cadence"], f"protocol.measurement_plan[{index}].cadence")
    _strings(proto["stop_conditions"], "protocol.stop_conditions", nonempty=True)
    contraindication_ids: set[str] = set()
    for index, raw in enumerate(_array(proto["contraindications"], "protocol.contraindications", nonempty=True)):
        label = f"protocol.contraindications[{index}]"
        row = _object(raw, label)
        _closed(row, {"condition_id", "label", "severity", "action", "match_terms"}, label)
        require(row, ["condition_id", "label", "severity", "action", "match_terms"], label)
        condition_id = _identifier(row["condition_id"], "contra_", f"{label}.condition_id")
        if condition_id in contraindication_ids:
            raise ValidationError(f"protocol.contraindications has duplicate condition_id {condition_id}")
        contraindication_ids.add(condition_id)
        _text(row["label"], f"{label}.label", minimum=3, maximum=300)
        severity = _enum(row["severity"], CONTRAINDICATION_SEVERITIES, f"{label}.severity")
        action = _enum(row["action"], CONTRAINDICATION_ACTIONS, f"{label}.action")
        _strings(row["match_terms"], f"{label}.match_terms", nonempty=True)
        if severity in {"high", "critical"} and action == "block_pending_human_review":
            raise ValidationError(f"{label} high/critical severity requires signed-clearance or permanent block action")
    for claim_id in _strings(proto["claim_ids"], "protocol.claim_ids", nonempty=True):
        _identifier(claim_id, "claim_", "protocol.claim_ids[]")
    _enum(proto["evidence_floor"], EVIDENCE_TIERS, "protocol.evidence_floor")
    _strings(proto["jurisdiction_flags"], "protocol.jurisdiction_flags", allowed={"none", "culinary_only", "supplement_label_varies", "controlled_substance_check", "clinician_required", "age_restricted"})
    safety = _object(proto["safety"], "protocol.safety")
    _closed(safety, {"not_diagnosis", "not_prescription", "emergency_route", "requires_clinician_clearance", "medical_functionality_disabled", "clearance_handling"}, "protocol.safety")
    require(safety, ["not_diagnosis", "not_prescription", "emergency_route", "medical_functionality_disabled", "clearance_handling"], "protocol.safety")
    if safety["not_diagnosis"] is not True or safety["not_prescription"] is not True:
        raise ValidationError("protocol.safety must set not_diagnosis and not_prescription true")
    _text(safety["emergency_route"], "protocol.safety.emergency_route", minimum=10)
    if safety["medical_functionality_disabled"] is not True:
        raise ValidationError("protocol.safety.medical_functionality_disabled must be true")
    if safety["clearance_handling"] != "external_verifier_unavailable_fail_closed":
        raise ValidationError("protocol.safety.clearance_handling must fail closed")
    if "requires_clinician_clearance" in safety and not isinstance(safety["requires_clinician_clearance"], bool):
        raise ValidationError("protocol.safety.requires_clinician_clearance must be boolean")
    if "last_reviewed" in proto:
        _iso_date(proto["last_reviewed"], "protocol.last_reviewed")
        _not_future_date(proto["last_reviewed"], "protocol.last_reviewed")
    review_gate = _object(proto["review_gate"], "protocol.review_gate")
    _closed(review_gate, {"evidence_reviewed", "safety_reviewed", "clinical_legal_reviewed"}, "protocol.review_gate")
    require(review_gate, ["evidence_reviewed", "safety_reviewed", "clinical_legal_reviewed"], "protocol.review_gate")
    if any(not isinstance(review_gate[field], bool) for field in review_gate):
        raise ValidationError("protocol.review_gate values must be boolean")
    gate_complete = all(review_gate.values())
    if release_status == "reviewed" and not gate_complete:
        raise ValidationError("reviewed protocol requires every review gate")
    if release_status == "draft_synthetic" and gate_complete:
        raise ValidationError("draft_synthetic protocol cannot claim completed review gates")


def validate_claim(claim: dict[str, Any]) -> None:
    validate_published_schema(claim, "claim.schema.json", "claim")
    claim = _object(claim, "claim")
    _closed(claim, {"claim_id", "schema_version", "statement", "evidence_tier", "certainty", "pico", "harms", "directness", "funding_coi", "integrity", "rights", "sources", "domain_pack", "population", "applicability", "limitations", "last_reviewed", "status", "admission", "conflicts", "conflict_flag", "conflicts_with", "not_a_personal_prescription"}, "claim")
    require(claim, ["claim_id", "schema_version", "statement", "evidence_tier", "certainty", "pico", "harms", "directness", "funding_coi", "integrity", "rights", "sources", "domain_pack", "population", "applicability", "limitations", "last_reviewed", "status", "admission", "conflicts", "not_a_personal_prescription"], "claim")
    if claim.get("schema_version") != CLAIM_SCHEMA_VERSION:
        raise ValidationError(f"claim.schema_version must be {CLAIM_SCHEMA_VERSION}")
    _identifier(claim["claim_id"], "claim_", "claim.claim_id")
    _text(claim["statement"], "claim.statement", minimum=10, maximum=1000)
    evidence_tier = _enum(claim["evidence_tier"], EVIDENCE_TIERS, "claim.evidence_tier")
    certainty = _enum(claim["certainty"], CERTAINTY_LEVELS, "claim.certainty")
    pico = _object(claim["pico"], "claim.pico")
    _closed(pico, {"population", "intervention", "comparator", "outcome", "timeframe"}, "claim.pico")
    require(pico, ["population", "intervention", "comparator", "outcome", "timeframe"], "claim.pico")
    for field in ("population", "intervention", "comparator", "outcome", "timeframe"):
        _text(pico[field], f"claim.pico.{field}", minimum=3, maximum=500)
    harms = _object(claim["harms"], "claim.harms")
    _closed(harms, {"summary", "certainty"}, "claim.harms")
    require(harms, ["summary", "certainty"], "claim.harms")
    _text(harms["summary"], "claim.harms.summary", minimum=3, maximum=1000)
    harms_certainty = _enum(harms["certainty"], CERTAINTY_LEVELS, "claim.harms.certainty")
    directness = _enum(claim["directness"], {"direct", "partially_direct", "indirect", "unclear"}, "claim.directness")
    funding_coi = _object(claim["funding_coi"], "claim.funding_coi")
    _closed(funding_coi, {"funding", "coi_status", "notes"}, "claim.funding_coi")
    require(funding_coi, ["funding", "coi_status"], "claim.funding_coi")
    _text(funding_coi["funding"], "claim.funding_coi.funding", minimum=3, maximum=500)
    funding_coi_status = _enum(funding_coi["coi_status"], {"none_declared", "declared", "unknown"}, "claim.funding_coi.coi_status")
    if "notes" in funding_coi:
        _text(funding_coi["notes"], "claim.funding_coi.notes", maximum=1000)
    integrity = _object(claim["integrity"], "claim.integrity")
    _closed(integrity, {"status", "correction_status", "supersession_status", "reviewed_on", "correction_checked_on", "next_review_due", "supersedes_claim_id", "superseded_by_claim_id"}, "claim.integrity")
    require(integrity, ["status", "correction_status", "supersession_status", "reviewed_on", "next_review_due"], "claim.integrity")
    integrity_status = _enum(integrity["status"], {"clear", "corrected", "unverified", "retracted", "expression_of_concern", "rights_violation"}, "claim.integrity.status")
    integrity_correction = _enum(integrity["correction_status"], CORRECTION_STATUSES, "claim.integrity.correction_status")
    supersession_status = _enum(integrity["supersession_status"], {"not_checked", "current", "superseded"}, "claim.integrity.supersession_status")
    for field in ("reviewed_on", "next_review_due"):
        _iso_date(integrity[field], f"claim.integrity.{field}")
    _not_future_date(integrity["reviewed_on"], "claim.integrity.reviewed_on")
    if integrity_correction != "not_checked":
        if "correction_checked_on" not in integrity:
            raise ValidationError("claim.integrity.correction_checked_on is required after a correction check")
        _iso_date(integrity["correction_checked_on"], "claim.integrity.correction_checked_on")
        _not_future_date(integrity["correction_checked_on"], "claim.integrity.correction_checked_on")
    for field in ("supersedes_claim_id", "superseded_by_claim_id"):
        if field in integrity:
            _identifier(integrity[field], "claim_", f"claim.integrity.{field}")
    if supersession_status == "superseded" and "superseded_by_claim_id" not in integrity:
        raise ValidationError("superseded claim integrity requires superseded_by_claim_id")
    rights = _object(claim["rights"], "claim.rights")
    _closed(rights, {"ingestion_mode", "license_review_status", "notes"}, "claim.rights")
    require(rights, ["ingestion_mode", "license_review_status"], "claim.rights")
    ingestion_mode = _enum(rights["ingestion_mode"], SOURCE_USE_PERMISSIONS, "claim.rights.ingestion_mode")
    license_review_status = _enum(rights["license_review_status"], {"pending", "approved", "rejected"}, "claim.rights.license_review_status")
    if "notes" in rights:
        _text(rights["notes"], "claim.rights.notes", maximum=1000)
    _text(claim["domain_pack"], "claim.domain_pack")
    _text(claim["population"], "claim.population", minimum=5, maximum=500)
    _text(claim["applicability"], "claim.applicability", minimum=5, maximum=1000)
    _strings(claim["limitations"], "claim.limitations", nonempty=True)
    _iso_date(claim["last_reviewed"], "claim.last_reviewed")
    _not_future_date(claim["last_reviewed"], "claim.last_reviewed")
    status = _enum(claim["status"], CLAIM_STATUSES, "claim.status")
    if claim["not_a_personal_prescription"] is not True:
        raise ValidationError("claim.not_a_personal_prescription must be true")
    conflicts = _object(claim["conflicts"], "claim.conflicts")
    _closed(conflicts, {"status", "notes"}, "claim.conflicts")
    require(conflicts, ["status"], "claim.conflicts")
    _enum(conflicts["status"], CONFLICT_STATUSES, "claim.conflicts.status")
    if "notes" in conflicts:
        _text(conflicts["notes"], "claim.conflicts.notes")
    admission = _object(claim["admission"], "claim.admission")
    admission_fields = {
        "user_facing_allowed", "evidence_review_complete", "license_review_complete",
        "correction_check_complete", "harms_review_complete",
        "funding_coi_review_complete", "integrity_review_complete",
        "directness_review_complete",
    }
    _closed(admission, admission_fields, "claim.admission")
    require(admission, sorted(admission_fields), "claim.admission")
    if any(not isinstance(admission[field], bool) for field in admission):
        raise ValidationError("claim.admission values must be boolean")
    if status != "active" and admission["user_facing_allowed"] is True:
        raise ValidationError("only an active claim may be admitted for user-facing use")
    if status == "active" and not all(admission.values()):
        raise ValidationError("active claim requires every evidence admission gate")

    seen: set[str] = set()
    corrections: list[str] = []
    source_kinds: set[str] = set()
    for index, raw in enumerate(_array(claim["sources"], "claim.sources", nonempty=True)):
        label = f"claim.sources[{index}]"
        source = _object(raw, label)
        _closed(source, {"source_id", "title", "kind", "publisher_or_authority", "url", "year", "doi", "pmid", "registration_id", "risk_of_bias", "license", "use_permission", "retrieved_on", "reviewed_on", "correction_status", "correction_checked_on", "notes"}, label)
        require(source, ["source_id", "title", "kind", "publisher_or_authority", "license", "use_permission", "retrieved_on", "reviewed_on", "correction_status"], label)
        source_id = _identifier(source["source_id"], "src_", f"{label}.source_id")
        if source_id in seen:
            raise ValidationError(f"claim.sources has duplicate source_id {source_id}")
        seen.add(source_id)
        _text(source["title"], f"{label}.title")
        source_kind = _enum(source["kind"], SOURCE_KINDS, f"{label}.kind")
        source_kinds.add(source_kind)
        _text(source["publisher_or_authority"], f"{label}.publisher_or_authority")
        if not any(source.get(key) for key in ("doi", "pmid", "url")):
            raise ValidationError(f"{label} requires a DOI, PMID, or authority URL")
        if "url" in source:
            _https(source["url"], f"{label}.url")
        if "doi" in source:
            doi = _text(source["doi"], f"{label}.doi").removeprefix("https://doi.org/")
            if not doi.startswith("10.") or "/" not in doi:
                raise ValidationError(f"{label}.doi must be a DOI")
        if "pmid" in source and not re.fullmatch(r"[0-9]{1,12}", _text(source["pmid"], f"{label}.pmid")):
            raise ValidationError(f"{label}.pmid must contain digits only")
        if "registration_id" in source:
            _text(source["registration_id"], f"{label}.registration_id", minimum=3, maximum=120)
        if "risk_of_bias" in source:
            _enum(source["risk_of_bias"], {"low", "some_concerns", "high", "not_assessed"}, f"{label}.risk_of_bias")
        if source_kind == "registered_rct" and (
            not source.get("registration_id") or source.get("risk_of_bias") != "low"
        ):
            raise ValidationError(f"{label} registered_rct requires a registration_id and low risk_of_bias")
        if "year" in source and (not isinstance(source["year"], int) or isinstance(source["year"], bool) or not 1800 <= source["year"] <= 2100):
            raise ValidationError(f"{label}.year must be an integer from 1800 to 2100")
        source_license = _enum(source["license"], SOURCE_LICENSES, f"{label}.license")
        use_permission = _enum(source["use_permission"], SOURCE_USE_PERMISSIONS, f"{label}.use_permission")
        if use_permission in {"open_access_full_text", "public_domain_full_text"} and source_license not in {"cc0", "cc_by_4_0", "cc_by_nc_4_0", "public_domain"}:
            raise ValidationError(f"{label} full-text permission is incompatible with its license")
        if use_permission == "licensed_excerpt" and source_license == "unknown":
            raise ValidationError(f"{label} cannot license an excerpt with an unknown license")
        _iso_date(source["retrieved_on"], f"{label}.retrieved_on")
        _iso_date(source["reviewed_on"], f"{label}.reviewed_on")
        _not_future_date(source["retrieved_on"], f"{label}.retrieved_on")
        _not_future_date(source["reviewed_on"], f"{label}.reviewed_on")
        if date.fromisoformat(source["reviewed_on"]) < date.fromisoformat(source["retrieved_on"]):
            raise ValidationError(f"{label}.reviewed_on cannot precede retrieved_on")
        correction = _enum(source["correction_status"], CORRECTION_STATUSES, f"{label}.correction_status")
        if correction != "not_checked":
            if "correction_checked_on" not in source:
                raise ValidationError(f"{label}.correction_checked_on is required after a correction check")
            _iso_date(source["correction_checked_on"], f"{label}.correction_checked_on")
            _not_future_date(source["correction_checked_on"], f"{label}.correction_checked_on")
        if "notes" in source:
            notes = _text(source["notes"], f"{label}.notes", maximum=500)
            if "\n" in notes or "\r" in notes:
                raise ValidationError(f"{label}.notes must remain one-line bibliographic metadata")
        corrections.append(correction)
    if status == "active":
        if evidence_tier in {"E", "Q"}:
            raise ValidationError("Tier E discovery and Tier Q quarantine claims cannot be active")
        if certainty in {"uncertain", "very_low"}:
            raise ValidationError("active claim certainty is too low for user-facing admission")
        if harms_certainty in {"uncertain", "very_low"}:
            raise ValidationError("active claim harms certainty is too low for user-facing admission")
        if directness == "unclear":
            raise ValidationError("active claim requires a completed directness assessment")
        if funding_coi_status == "unknown":
            raise ValidationError("active claim requires completed funding and conflict review")
        if integrity_status not in {"clear", "corrected"} or integrity_correction in {"not_checked", "retracted", "expression_of_concern"}:
            raise ValidationError("active claim integrity and correction status are not admissible")
        if supersession_status != "current":
            raise ValidationError("active claim requires a current supersession check")
        if license_review_status != "approved":
            raise ValidationError("active claim requires approved rights and license review")
        if conflicts["status"] == "unknown":
            raise ValidationError("active claim requires a completed conflict review")
        if not source_kinds.intersection(TIER_SOURCE_KINDS[evidence_tier]):
            raise ValidationError(f"active Tier {evidence_tier} claim lacks a matching source design")
        discovery_sources = sorted(source_kinds.intersection(DISCOVERY_ONLY_SOURCE_KINDS))
        if discovery_sources:
            raise ValidationError(
                "active claim cannot include discovery-only source kinds: "
                + ", ".join(discovery_sources)
            )
        if any(value in {"not_checked", "retracted", "expression_of_concern"} for value in corrections):
            raise ValidationError("active claim requires completed correction checks with no retraction concern")
        today = datetime.now(timezone.utc).date()
        if today - date.fromisoformat(claim["last_reviewed"]) > timedelta(days=365):
            raise ValidationError("active claim evidence review is stale")
        for raw in claim["sources"]:
            checked = raw.get("correction_checked_on")
            if not checked or today - date.fromisoformat(checked) > timedelta(days=180):
                raise ValidationError("active claim correction check is stale")
        if date.fromisoformat(integrity["next_review_due"]) < today:
            raise ValidationError("active claim next review is overdue")
        if not integrity.get("correction_checked_on") or today - date.fromisoformat(integrity["correction_checked_on"]) > timedelta(days=180):
            raise ValidationError("active claim integrity correction check is stale")
        if ingestion_mode != "metadata_only" and not any(
            source["use_permission"] == ingestion_mode for source in claim["sources"]
        ):
            raise ValidationError("claim ingestion mode is not supported by a source rights receipt")


def validate_household(hh: dict[str, Any]) -> None:
    validate_published_schema(hh, "household.schema.json", "household")
    hh = _object(hh, "household")
    _closed(hh, {"household_id", "schema_version", "vault_mode", "display_name", "subjects", "stewards", "created_at", "notes"}, "household")
    require(hh, ["household_id", "schema_version", "vault_mode", "display_name", "subjects", "stewards", "created_at"], "household")
    _version(hh, "household")
    if hh["vault_mode"] != "synthetic_plaintext_prototype":
        raise ValidationError("reference vault is synthetic_plaintext_prototype only")
    _identifier(hh["household_id"], "hh_", "household.household_id")
    _text(hh["display_name"], "household.display_name", maximum=120)
    _iso_datetime(hh["created_at"], "household.created_at")
    subject_ids: set[str] = set()
    for index, raw in enumerate(_array(hh["subjects"], "household.subjects", nonempty=True)):
        label = f"household.subjects[{index}]"
        subject = _object(raw, label)
        _closed(subject, {"subject_id", "display_name", "role", "can_read_own", "timezone", "locale"}, label)
        require(subject, ["subject_id", "display_name", "role", "can_read_own"], label)
        subject_id = _identifier(subject["subject_id"], "sub_", f"{label}.subject_id")
        if subject_id in subject_ids:
            raise ValidationError(f"duplicate subject_id {subject_id}")
        subject_ids.add(subject_id)
        _text(subject["display_name"], f"{label}.display_name")
        _enum(subject["role"], {"self", "partner", "child", "parent", "grandparent", "dependent", "other"}, f"{label}.role")
        if subject["can_read_own"] is not True:
            raise ValidationError(f"{label}.can_read_own must be true")
        for field in ("timezone", "locale"):
            if field in subject:
                _text(subject[field], f"{label}.{field}")
    steward_ids: set[str] = set()
    for index, raw in enumerate(_array(hh["stewards"], "household.stewards", nonempty=True)):
        label = f"household.stewards[{index}]"
        steward = _object(raw, label)
        _closed(steward, {"operator_id", "display_name", "subject_scope", "permissions"}, label)
        require(steward, ["operator_id", "display_name", "subject_scope"], label)
        operator_id = _identifier(steward["operator_id"], "op_", f"{label}.operator_id")
        if operator_id in steward_ids:
            raise ValidationError(f"duplicate operator_id {operator_id}")
        steward_ids.add(operator_id)
        _text(steward["display_name"], f"{label}.display_name")
        if not set(_strings(steward["subject_scope"], f"{label}.subject_scope", nonempty=True)).issubset(subject_ids):
            raise ValidationError(f"{label}.subject_scope references an unknown subject")
        if "permissions" in steward:
            _strings(steward["permissions"], f"{label}.permissions", allowed={"read", "write_observe", "start_protocol", "export_handoff", "manage_consent", "admin"})


def validate_consent(consent: dict[str, Any]) -> None:
    validate_published_schema(consent, "consent.schema.json", "consent")
    consent = _object(consent, "consent")
    _closed(consent, {"consent_id", "schema_version", "household_id", "subject_id", "authorized_by_id", "authority_basis", "purposes", "data_classes", "recipients", "processors", "actions", "field_allowlist", "record_scope", "revision", "supersedes_consent_id", "granted_at", "expires_at", "withdrawn_at", "status", "dignity_clause", "notice_version"}, "consent")
    require(consent, ["consent_id", "schema_version", "household_id", "subject_id", "authorized_by_id", "authority_basis", "purposes", "data_classes", "recipients", "processors", "actions", "record_scope", "revision", "granted_at", "status", "dignity_clause"], "consent")
    _version(consent, "consent")
    _identifier(consent["consent_id"], "consent_", "consent.consent_id")
    _identifier(consent["household_id"], "hh_", "consent.household_id")
    _identifier(consent["subject_id"], "sub_", "consent.subject_id")
    _text(consent["authorized_by_id"], "consent.authorized_by_id")
    _enum(consent["authority_basis"], {"self", "parental_responsibility", "legal_guardian", "authorized_representative", "steward_delegated"}, "consent.authority_basis")
    _strings(consent["purposes"], "consent.purposes", nonempty=True, allowed=CONSENT_PURPOSES)
    _strings(consent["data_classes"], "consent.data_classes", nonempty=True, allowed=CONSENT_DATA_CLASSES)
    _strings(consent["actions"], "consent.actions", nonempty=True, allowed=CONSENT_ACTIONS)
    recipient_pairs: set[tuple[str, str]] = set()
    for index, raw in enumerate(_array(consent["recipients"], "consent.recipients", nonempty=True)):
        recipient = _object(raw, f"consent.recipients[{index}]")
        _closed(recipient, {"recipient_id", "kind"}, f"consent.recipients[{index}]")
        require(recipient, ["recipient_id", "kind"], f"consent.recipients[{index}]")
        recipient_id = _text(recipient["recipient_id"], f"consent.recipients[{index}].recipient_id")
        recipient_kind = _enum(recipient["kind"], RECIPIENT_KINDS, f"consent.recipients[{index}].kind")
        pair = (recipient_id, recipient_kind)
        if pair in recipient_pairs:
            raise ValidationError("consent.recipients must contain unique id/kind pairs")
        recipient_pairs.add(pair)
    processor_pairs: set[tuple[str, str]] = set()
    for index, raw in enumerate(_array(consent["processors"], "consent.processors", nonempty=True)):
        label = f"consent.processors[{index}]"
        processor = _object(raw, label)
        _closed(processor, {"processor_id", "kind", "allowed_tiers"}, label)
        require(processor, ["processor_id", "kind", "allowed_tiers"], label)
        processor_id = _text(processor["processor_id"], f"{label}.processor_id")
        processor_kind = _enum(processor["kind"], PROCESSOR_KINDS, f"{label}.kind")
        _strings(processor["allowed_tiers"], f"{label}.allowed_tiers", nonempty=True, allowed=MODEL_TIERS - {"none"})
        pair = (processor_id, processor_kind)
        if pair in processor_pairs:
            raise ValidationError("consent.processors must contain unique id/kind pairs")
        processor_pairs.add(pair)
    scope = _object(consent["record_scope"], "consent.record_scope")
    _closed(scope, {"event_ids", "protocol_run_ids"}, "consent.record_scope")
    require(scope, ["event_ids", "protocol_run_ids"], "consent.record_scope")
    for event_id in _strings(scope["event_ids"], "consent.record_scope.event_ids"):
        _identifier(event_id, "evt_", "consent.record_scope.event_ids[]")
    for run_id in _strings(scope["protocol_run_ids"], "consent.record_scope.protocol_run_ids"):
        _identifier(run_id, "run_", "consent.record_scope.protocol_run_ids[]")
    if not isinstance(consent["revision"], int) or isinstance(consent["revision"], bool) or consent["revision"] < 1:
        raise ValidationError("consent.revision must be a positive integer")
    if "supersedes_consent_id" in consent:
        supersedes = _identifier(consent["supersedes_consent_id"], "consent_", "consent.supersedes_consent_id")
        if supersedes == consent["consent_id"]:
            raise ValidationError("consent cannot supersede itself")
    _iso_datetime(consent["granted_at"], "consent.granted_at")
    _not_future_datetime(consent["granted_at"], "consent.granted_at")
    if "expires_at" in consent:
        _iso_datetime(consent["expires_at"], "consent.expires_at")
    if "withdrawn_at" in consent:
        _iso_datetime(consent["withdrawn_at"], "consent.withdrawn_at")
        _not_future_datetime(consent["withdrawn_at"], "consent.withdrawn_at")
    if "field_allowlist" in consent:
        _strings(consent["field_allowlist"], "consent.field_allowlist")
    status = _enum(consent["status"], {"active", "expired", "withdrawn", "superseded"}, "consent.status")
    if status == "withdrawn" and "withdrawn_at" not in consent:
        raise ValidationError("withdrawn consent requires withdrawn_at")
    if status != "withdrawn" and "withdrawn_at" in consent:
        raise ValidationError("only withdrawn consent may include withdrawn_at")
    granted = _parsed_datetime(consent["granted_at"])
    if "expires_at" in consent and _parsed_datetime(consent["expires_at"]) <= granted:
        raise ValidationError("consent.expires_at must be after granted_at")
    if "withdrawn_at" in consent and _parsed_datetime(consent["withdrawn_at"]) < granted:
        raise ValidationError("consent.withdrawn_at cannot precede granted_at")
    now = datetime.now(timezone.utc)
    if status == "active" and "expires_at" in consent and _parsed_datetime(consent["expires_at"]) <= now:
        raise ValidationError("expired consent cannot remain active")
    if status == "expired" and ("expires_at" not in consent or _parsed_datetime(consent["expires_at"]) > now):
        raise ValidationError("expired consent requires a past expires_at")
    if consent["dignity_clause"] is not True:
        raise ValidationError("consent.dignity_clause must be true")


def validate_egress(policy: dict[str, Any]) -> None:
    validate_published_schema(policy, "egress.schema.json", "egress")
    policy = _object(policy, "egress")
    _closed(policy, {"policy_id", "schema_version", "household_id", "subject_id", "default_deny", "rules", "updated_at", "steward_id"}, "egress")
    require(policy, ["policy_id", "schema_version", "household_id", "subject_id", "default_deny", "rules", "updated_at"], "egress")
    _version(policy, "egress")
    _identifier(policy["policy_id"], "egress_", "egress.policy_id")
    _identifier(policy["household_id"], "hh_", "egress.household_id")
    _identifier(policy["subject_id"], "sub_", "egress.subject_id")
    if policy["default_deny"] is not True:
        raise ValidationError("egress.default_deny must be true")
    _iso_datetime(policy["updated_at"], "egress.updated_at")
    if "steward_id" in policy:
        _identifier(policy["steward_id"], "op_", "egress.steward_id")
    seen: set[str] = set()
    for index, raw in enumerate(_array(policy["rules"], "egress.rules", nonempty=True)):
        label = f"egress.rules[{index}]"
        rule = _object(raw, label)
        _closed(rule, {"sensitivity_class", "allowed_tiers", "redaction_profile", "notes"}, label)
        require(rule, ["sensitivity_class", "allowed_tiers", "redaction_profile"], label)
        sensitivity = _enum(rule["sensitivity_class"], SENSITIVITY_CLASSES, f"{label}.sensitivity_class")
        if sensitivity in seen:
            raise ValidationError(f"duplicate egress rule for {sensitivity}")
        seen.add(sensitivity)
        tiers = _strings(rule["allowed_tiers"], f"{label}.allowed_tiers", nonempty=True, allowed=MODEL_TIERS)
        profile = _enum(rule["redaction_profile"], REDACTION_PROFILES, f"{label}.redaction_profile")
        if "none" in tiers and (len(tiers) != 1 or profile != "block"):
            raise ValidationError(f"{label} must use only tier none with block redaction")
        if "notes" in rule:
            _text(rule["notes"], f"{label}.notes")
    if seen != SENSITIVITY_CLASSES:
        raise ValidationError(f"egress must define every sensitivity class; missing={sorted(SENSITIVITY_CLASSES - seen)}")


def validate_pack_meta(meta: dict[str, Any]) -> None:
    meta = _object(meta, "pack")
    _closed(meta, {"pack_id", "title", "version", "description", "class", "release_status", "last_reviewed"}, "pack")
    require(meta, ["pack_id", "title", "version", "description", "class", "release_status", "last_reviewed"], "pack")
    _text(meta["pack_id"], "pack.pack_id")
    _text(meta["title"], "pack.title")
    _text(meta["version"], "pack.version")
    _text(meta["description"], "pack.description", minimum=10)
    _enum(meta["class"], PROTOCOL_CLASSES, "pack.class")
    _enum(meta["release_status"], PROTOCOL_RELEASE_STATUSES, "pack.release_status")
    _iso_date(meta["last_reviewed"], "pack.last_reviewed")
    _not_future_date(meta["last_reviewed"], "pack.last_reviewed")


def validate_active_run(run: dict[str, Any]) -> None:
    run = _object(run, "protocol_run")
    _closed(run, {"run_id", "protocol_id", "pack_id", "started_at", "status", "protocol_snapshot", "gate_flags"}, "protocol_run")
    require(run, ["run_id", "protocol_id", "pack_id", "started_at", "status", "protocol_snapshot", "gate_flags"], "protocol_run")
    _identifier(run["run_id"], "run_", "protocol_run.run_id")
    _identifier(run["protocol_id"], "proto_", "protocol_run.protocol_id")
    _text(run["pack_id"], "protocol_run.pack_id")
    _enum(run["status"], {"active"}, "protocol_run.status")
    _iso_datetime(run["started_at"], "protocol_run.started_at")
    _strings(run["gate_flags"], "protocol_run.gate_flags")
    snapshot = _object(run["protocol_snapshot"], "protocol_run.protocol_snapshot")
    validate_protocol(snapshot)
    if snapshot["release_status"] != "reviewed":
        raise ValidationError("active run cannot contain a draft protocol snapshot")


def validate_phenotype(phenotype: dict[str, Any]) -> None:
    validate_published_schema(phenotype, "phenotype.schema.json", "phenotype")
    phenotype = _object(phenotype, "phenotype")
    _closed(phenotype, {"phenotype_id", "schema_version", "household_id", "subject_id", "built_at", "ledger_event_count", "chronotype_lite", "baselines", "constraints", "allergies_self_report", "active_protocols", "current_stack", "recent_tags", "rebuild_command"}, "phenotype")
    require(phenotype, ["phenotype_id", "schema_version", "household_id", "subject_id", "built_at", "ledger_event_count", "baselines", "constraints", "active_protocols", "current_stack"], "phenotype")
    _version(phenotype, "phenotype")
    _identifier(phenotype["phenotype_id"], "pheno_", "phenotype.phenotype_id")
    _identifier(phenotype["household_id"], "hh_", "phenotype.household_id")
    _identifier(phenotype["subject_id"], "sub_", "phenotype.subject_id")
    _iso_datetime(phenotype["built_at"], "phenotype.built_at")
    if not isinstance(phenotype["ledger_event_count"], int) or isinstance(phenotype["ledger_event_count"], bool) or phenotype["ledger_event_count"] < 0:
        raise ValidationError("phenotype.ledger_event_count must be a non-negative integer")
    _object(phenotype["baselines"], "phenotype.baselines")
    for field in ("constraints", "active_protocols", "current_stack"):
        _array(phenotype[field], f"phenotype.{field}")
    if phenotype.get("rebuild_command") not in (None, "bios_substrate phenotype rebuild"):
        raise ValidationError("phenotype.rebuild_command is not recognized")


def validate_agent_manifest(manifest: dict[str, Any]) -> None:
    validate_published_schema(manifest, "agent-manifest.schema.json", "agent_manifest")
    manifest = _object(manifest, "agent_manifest")
    _closed(manifest, {"agent_id", "schema_version", "title", "reads", "writes", "evidence_tiers_may_cite", "escalation_triggers", "tools_required", "must_not"}, "agent_manifest")
    require(manifest, ["agent_id", "schema_version", "title", "reads", "writes", "evidence_tiers_may_cite", "escalation_triggers", "tools_required"], "agent_manifest")
    _version(manifest, "agent_manifest")
    _identifier(manifest["agent_id"], "agent_", "agent_manifest.agent_id")
    _text(manifest["title"], "agent_manifest.title")
    _strings(manifest["reads"], "agent_manifest.reads", allowed=SENSITIVITY_CLASSES)
    _strings(manifest["writes"], "agent_manifest.writes", allowed={"none", "observe", "protocol_run", "export", "consent"})
    _strings(manifest["evidence_tiers_may_cite"], "agent_manifest.evidence_tiers_may_cite", allowed=CITABLE_EVIDENCE_TIERS)
    _strings(manifest["escalation_triggers"], "agent_manifest.escalation_triggers", nonempty=True)
    _strings(manifest["tools_required"], "agent_manifest.tools_required")
    if "must_not" in manifest:
        _strings(manifest["must_not"], "agent_manifest.must_not")


REGISTRY_DOMAINS = {"health_stewardship", "movement_training", "martial_arts_movement", "culinary_botanicals", "complementary_practice_education"}
REGISTRY_PROHIBITIONS = {
    "diagnose", "treat_or_prescribe", "interpret_clinical_results",
    "recommend_medication_or_supplement_changes", "provide_controlled_substance_dosing_or_sourcing",
    "claim_unproven_energy_mechanisms_as_fact", "replace_qualified_professional",
}


def validate_domain_agent_registry(registry: dict[str, Any]) -> None:
    validate_published_schema(registry, "domain-agent-registry.schema.json", "domain_agent_registry")
    registry = _object(registry, "domain_agent_registry")
    _closed(registry, {"registry_id", "schema_version", "last_reviewed", "advice_mode", "reserved_name_denylist", "prohibited_actions", "agents"}, "domain_agent_registry")
    require(registry, ["registry_id", "schema_version", "last_reviewed", "advice_mode", "reserved_name_denylist", "prohibited_actions", "agents"], "domain_agent_registry")
    _version(registry, "domain_agent_registry")
    _identifier(registry["registry_id"], "registry_", "domain_agent_registry.registry_id")
    _iso_date(registry["last_reviewed"], "domain_agent_registry.last_reviewed")
    if registry["advice_mode"] != "education_and_organization_only":
        raise ValidationError("domain_agent_registry.advice_mode must be education_and_organization_only")
    denylist = {value.lower() for value in _strings(registry["reserved_name_denylist"], "domain_agent_registry.reserved_name_denylist", nonempty=True)}
    if denylist != RESERVED_PUBLIC_NAMES:
        raise ValidationError("domain_agent_registry must deny the exact reserved public names")
    prohibited = set(_strings(registry["prohibited_actions"], "domain_agent_registry.prohibited_actions", nonempty=True))
    if not REGISTRY_PROHIBITIONS.issubset(prohibited):
        raise ValidationError(f"domain_agent_registry missing mandatory prohibitions: {sorted(REGISTRY_PROHIBITIONS - prohibited)}")
    seen_ids: set[str] = set()
    seen_domains: set[str] = set()
    for index, raw in enumerate(_array(registry["agents"], "domain_agent_registry.agents", nonempty=True)):
        label = f"domain_agent_registry.agents[{index}]"
        agent = _object(raw, label)
        _closed(agent, {"agent_id", "pack_id", "canonical_label", "brand_status", "domain", "purpose", "allowed_actions", "must_not", "data_classes_read", "evidence_tiers_may_cite", "implementation_status"}, label)
        require(agent, ["agent_id", "pack_id", "canonical_label", "brand_status", "domain", "purpose", "allowed_actions", "must_not", "data_classes_read", "evidence_tiers_may_cite", "implementation_status"], label)
        agent_id = _identifier(agent["agent_id"], "agent_", f"{label}.agent_id")
        domain = _enum(agent["domain"], REGISTRY_DOMAINS, f"{label}.domain")
        if agent_id in seen_ids or domain in seen_domains:
            raise ValidationError(f"domain_agent_registry duplicate identity at {label}")
        seen_ids.add(agent_id)
        seen_domains.add(domain)
        if agent["brand_status"] != "generic_public":
            raise ValidationError(f"{label}.brand_status must be generic_public")
        _text(agent["pack_id"], f"{label}.pack_id")
        _text(agent["canonical_label"], f"{label}.canonical_label")
        public_identity = " ".join(
            str(agent[field]).lower()
            for field in ("agent_id", "pack_id", "canonical_label", "purpose")
        )
        if any(re.search(rf"\b{re.escape(name)}\b", public_identity) for name in denylist):
            raise ValidationError(f"{label} uses a reserved public name")
        _text(agent["purpose"], f"{label}.purpose", minimum=20)
        _strings(agent["allowed_actions"], f"{label}.allowed_actions", nonempty=True)
        must_not = set(_strings(agent["must_not"], f"{label}.must_not", nonempty=True))
        if not REGISTRY_PROHIBITIONS.issubset(must_not):
            raise ValidationError(f"{label}.must_not is missing mandatory prohibitions")
        _strings(agent["data_classes_read"], f"{label}.data_classes_read", allowed=CONSENT_DATA_CLASSES)
        _strings(agent["evidence_tiers_may_cite"], f"{label}.evidence_tiers_may_cite", nonempty=True, allowed=CITABLE_EVIDENCE_TIERS)
        if agent["implementation_status"] != "registry_only":
            raise ValidationError(f"{label}.implementation_status must remain registry_only in prerelease")
    if seen_domains != REGISTRY_DOMAINS:
        raise ValidationError(f"domain_agent_registry must contain the bounded domain set; missing={sorted(REGISTRY_DOMAINS - seen_domains)}")


def validate_idea_source(source: dict[str, Any]) -> None:
    validate_published_schema(source, "idea-source.schema.json", "idea_source")
    source = _object(source, "idea_source")
    _closed(source, {"idea_source_id", "schema_version", "title", "creators", "kind", "publisher", "publication_year", "isbn", "authority_url", "discovery_tier", "content_policy", "claim_admission_rule", "notes", "retrieved_on"}, "idea_source")
    require(source, ["idea_source_id", "schema_version", "title", "creators", "kind", "publisher", "publication_year", "authority_url", "discovery_tier", "content_policy", "claim_admission_rule", "retrieved_on"], "idea_source")
    _version(source, "idea_source")
    _identifier(source["idea_source_id"], "idea_", "idea_source.idea_source_id")
    _text(source["title"], "idea_source.title")
    _strings(source["creators"], "idea_source.creators", nonempty=True)
    _enum(source["kind"], {"book", "podcast", "video", "newsletter", "popular_article"}, "idea_source.kind")
    _text(source["publisher"], "idea_source.publisher")
    if not isinstance(source["publication_year"], int) or not 1800 <= source["publication_year"] <= 2100:
        raise ValidationError("idea_source.publication_year must be an integer from 1800 to 2100")
    _https(source["authority_url"], "idea_source.authority_url")
    if source["discovery_tier"] != "idea_source_only":
        raise ValidationError("idea_source.discovery_tier must be idea_source_only")
    if source["content_policy"] != "bibliographic_metadata_only_no_copyrighted_full_text":
        raise ValidationError("idea_source.content_policy must prohibit copyrighted full-text ingestion")
    if source["claim_admission_rule"] != "resolve_to_primary_systematic_review_or_guideline_before_user_facing_advice":
        raise ValidationError("idea_source.claim_admission_rule must require independent evidence resolution")
    _iso_date(source["retrieved_on"], "idea_source.retrieved_on")
    if "notes" in source:
        notes = _text(source["notes"], "idea_source.notes", maximum=500)
        if "\n" in notes or "\r" in notes:
            raise ValidationError("idea_source.notes must remain one-line bibliographic metadata")


def validate_handoff_receipt(receipt: dict[str, Any]) -> None:
    validate_published_schema(receipt, "handoff-receipt.schema.json", "handoff_receipt")
