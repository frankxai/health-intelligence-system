"""Household vault filesystem layout."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .validate import validate_household


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def slug(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_-]+", "-", text.strip().lower()).strip("-")
    return s or "x"


def subject_dir(vault: Path, subject_id: str) -> Path:
    return vault / "subjects" / subject_id


def init_household_vault(
    path: Path,
    *,
    household_name: str,
    subject_label: str = "self",
    steward_label: str = "steward",
    timezone_name: str = "UTC",
) -> dict[str, Any]:
    path = path.resolve()
    path.mkdir(parents=True, exist_ok=True)

    hh_id = f"hh_{slug(household_name)}"
    sub_id = f"sub_{slug(subject_label)}"
    op_id = f"op_{slug(steward_label)}"
    created = utc_now()

    household = {
        "household_id": hh_id,
        "schema_version": "0.1.0",
        "display_name": household_name,
        "subjects": [
            {
                "subject_id": sub_id,
                "display_name": subject_label,
                "role": "self",
                "can_read_own": True,
                "timezone": timezone_name,
            }
        ],
        "stewards": [
            {
                "operator_id": op_id,
                "display_name": steward_label,
                "subject_scope": [sub_id],
                "permissions": [
                    "read",
                    "write_observe",
                    "start_protocol",
                    "export_handoff",
                    "manage_consent",
                    "admin",
                ],
            }
        ],
        "created_at": created,
        "notes": "BIOS household vault. Subject may always read everything written about them.",
    }
    validate_household(household)

    (path / "household.json").write_text(json.dumps(household, indent=2) + "\n", encoding="utf-8")
    (path / "README.md").write_text(
        f"""# BIOS household vault

Household: **{household_name}** (`{hh_id}`)

- Canonical unit: household (steward model: subject ≠ operator allowed)
- Ledger is append-only JSONL under each subject
- Never put raw clinical PDFs in a public git remote
- High-frequency wearable streams → local Parquet outside git; commit rollups only

## Layout

```text
household.json
subjects/<subject_id>/
  ledger.jsonl
  phenotype.json          # derived
  consent/
  egress.json
  protocols/active/
  protocols/completed/
  exports/
  media/                  # optional local photos (gitignored recommended)
```

Created: {created}
""",
        encoding="utf-8",
    )

    sdir = subject_dir(path, sub_id)
    for rel in [
        "consent",
        "protocols/active",
        "protocols/completed",
        "exports",
        "media",
    ]:
        (sdir / rel).mkdir(parents=True, exist_ok=True)

    (sdir / "ledger.jsonl").touch()
    egress = {
        "policy_id": f"egress_{slug(subject_label)}",
        "schema_version": "0.1.0",
        "household_id": hh_id,
        "subject_id": sub_id,
        "default_deny": True,
        "rules": [
            {
                "sensitivity_class": "public",
                "allowed_tiers": ["local", "tee_or_venice", "frontier"],
                "redaction_profile": "none",
            },
            {
                "sensitivity_class": "personal",
                "allowed_tiers": ["local", "tee_or_venice", "frontier"],
                "redaction_profile": "identifiers_only",
            },
            {
                "sensitivity_class": "clinical",
                "allowed_tiers": ["local", "tee_or_venice"],
                "redaction_profile": "clinical_strip",
            },
            {
                "sensitivity_class": "genomic",
                "allowed_tiers": ["local"],
                "redaction_profile": "block",
            },
        ],
        "updated_at": created,
        "steward_id": op_id,
    }
    (sdir / "egress.json").write_text(json.dumps(egress, indent=2) + "\n", encoding="utf-8")

    consent = {
        "consent_id": f"consent_{slug(subject_label)}_self_track",
        "schema_version": "0.1.0",
        "household_id": hh_id,
        "subject_id": sub_id,
        "authorized_by_id": op_id,
        "authority_basis": "self",
        "purposes": ["self_tracking", "agent_assist", "clinician_handoff", "backup"],
        "data_classes": ["wellness_logs", "meal_photos", "wearable_rollups", "supplement_stack"],
        "recipients": [
            {"recipient_id": sub_id, "kind": "self"},
            {"recipient_id": op_id, "kind": "steward"},
            {"recipient_id": "local_agent", "kind": "local_agent"},
        ],
        "actions": ["collect", "store", "summarize", "ai_process", "export"],
        "granted_at": created,
        "status": "active",
        "dignity_clause": True,
        "notice_version": "bios-0.1",
    }
    (sdir / "consent" / "self-tracking.json").write_text(
        json.dumps(consent, indent=2) + "\n", encoding="utf-8"
    )

    gitignore = path / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text(
            "media/\n*.parquet\n*.duckdb\n.env\nexports/*-private*\n",
            encoding="utf-8",
        )

    return household


def load_household(vault: Path) -> dict[str, Any]:
    data = json.loads((vault / "household.json").read_text(encoding="utf-8"))
    validate_household(data)
    return data


def resolve_subject_id(household: dict[str, Any], subject: str) -> str:
    subjects = household["subjects"]
    if subject.startswith("sub_"):
        for s in subjects:
            if s["subject_id"] == subject:
                return subject
        raise KeyError(f"unknown subject_id {subject}")
    # match label or bare slug
    want = slug(subject)
    for s in subjects:
        if slug(s["display_name"]) == want or s["subject_id"] == f"sub_{want}":
            return s["subject_id"]
    if len(subjects) == 1 and subject in {"self", "default", "me"}:
        return subjects[0]["subject_id"]
    raise KeyError(f"unknown subject {subject!r}; known: {[s['subject_id'] for s in subjects]}")


def add_subject(
    vault: Path,
    *,
    display_name: str,
    role: str = "dependent",
    timezone_name: str = "UTC",
) -> str:
    household = load_household(vault)
    sub_id = f"sub_{slug(display_name)}"
    if any(s["subject_id"] == sub_id for s in household["subjects"]):
        raise ValueError(f"subject already exists: {sub_id}")
    household["subjects"].append(
        {
            "subject_id": sub_id,
            "display_name": display_name,
            "role": role,
            "can_read_own": True,
            "timezone": timezone_name,
        }
    )
    # expand primary steward scope
    if household["stewards"]:
        scope = household["stewards"][0].setdefault("subject_scope", [])
        if sub_id not in scope:
            scope.append(sub_id)
    validate_household(household)
    (vault / "household.json").write_text(json.dumps(household, indent=2) + "\n", encoding="utf-8")

    sdir = subject_dir(vault, sub_id)
    for rel in ["consent", "protocols/active", "protocols/completed", "exports", "media"]:
        (sdir / rel).mkdir(parents=True, exist_ok=True)
    (sdir / "ledger.jsonl").touch()
    created = utc_now()
    egress = {
        "policy_id": f"egress_{slug(display_name)}",
        "schema_version": "0.1.0",
        "household_id": household["household_id"],
        "subject_id": sub_id,
        "default_deny": True,
        "rules": [
            {
                "sensitivity_class": "public",
                "allowed_tiers": ["local", "tee_or_venice", "frontier"],
                "redaction_profile": "none",
            },
            {
                "sensitivity_class": "personal",
                "allowed_tiers": ["local", "tee_or_venice", "frontier"],
                "redaction_profile": "identifiers_only",
            },
            {
                "sensitivity_class": "clinical",
                "allowed_tiers": ["local"],
                "redaction_profile": "clinical_strip",
            },
            {
                "sensitivity_class": "genomic",
                "allowed_tiers": ["none"],
                "redaction_profile": "block",
            },
        ],
        "updated_at": created,
        "steward_id": household["stewards"][0]["operator_id"],
    }
    (sdir / "egress.json").write_text(json.dumps(egress, indent=2) + "\n", encoding="utf-8")
    return sub_id
