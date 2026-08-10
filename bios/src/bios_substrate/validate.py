"""Lightweight required-field validators (stdlib). Full JSON Schema optional later."""

from __future__ import annotations

from typing import Any


class ValidationError(ValueError):
    pass


def require(obj: dict[str, Any], fields: list[str], label: str) -> None:
    missing = [f for f in fields if f not in obj or obj[f] in (None, "")]
    if missing:
        raise ValidationError(f"{label} missing required fields: {', '.join(missing)}")


def validate_ledger_event(event: dict[str, Any]) -> None:
    require(
        event,
        [
            "event_id",
            "schema_version",
            "household_id",
            "subject_id",
            "recorded_at",
            "kind",
            "sensitivity_class",
            "source",
        ],
        "ledger_event",
    )
    if event.get("schema_version") != "0.1.0":
        raise ValidationError("ledger_event.schema_version must be 0.1.0")
    if not str(event["event_id"]).startswith("evt_"):
        raise ValidationError("event_id must start with evt_")
    src = event["source"]
    if not isinstance(src, dict) or "channel" not in src:
        raise ValidationError("source.channel required")


def validate_protocol(proto: dict[str, Any]) -> None:
    require(
        proto,
        [
            "protocol_id",
            "schema_version",
            "title",
            "domain_pack",
            "class",
            "hypothesis",
            "intervention",
            "timing",
            "duration",
            "measurement_plan",
            "stop_conditions",
            "contraindications",
            "claim_ids",
            "evidence_floor",
            "jurisdiction_flags",
            "safety",
        ],
        "protocol",
    )
    if proto.get("schema_version") != "0.1.0":
        raise ValidationError("protocol.schema_version must be 0.1.0")
    safety = proto.get("safety") or {}
    if safety.get("not_diagnosis") is not True or safety.get("not_prescription") is not True:
        raise ValidationError("protocol.safety must set not_diagnosis and not_prescription true")
    if not proto.get("claim_ids"):
        raise ValidationError("protocol must cite at least one claim_id")
    if not proto.get("contraindications"):
        raise ValidationError("protocol must list contraindications")
    if proto.get("class") not in {
        "ordinary_wellness",
        "habit_tracking",
        "education",
        "clinician_supervised_only",
        "jurisdiction_restricted",
    }:
        raise ValidationError("invalid protocol.class")


def validate_claim(claim: dict[str, Any]) -> None:
    require(
        claim,
        [
            "claim_id",
            "schema_version",
            "statement",
            "evidence_tier",
            "sources",
            "domain_pack",
            "last_reviewed",
            "status",
        ],
        "claim",
    )
    if not claim.get("sources"):
        raise ValidationError("claim must include sources")
    if claim.get("not_a_personal_prescription") is False:
        raise ValidationError("claims must not be personal prescriptions")


def validate_household(hh: dict[str, Any]) -> None:
    require(
        hh,
        ["household_id", "schema_version", "display_name", "subjects", "stewards", "created_at"],
        "household",
    )
    if not hh.get("subjects") or not hh.get("stewards"):
        raise ValidationError("household needs subjects and stewards")
