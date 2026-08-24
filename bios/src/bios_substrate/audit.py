"""Local tamper-evident audit receipts for compiled handoffs."""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
from pathlib import Path
from typing import Any

from .validate import validate_handoff_receipt
from .vault import subject_dir, utc_now


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _audit_key(vault: Path) -> bytes:
    key_dir = vault / ".bios-private"
    key_path = key_dir / "audit-hmac.key"
    key_dir.mkdir(parents=True, exist_ok=True)
    if not key_path.exists():
        key_path.write_bytes(secrets.token_bytes(32))
        try:
            os.chmod(key_path, 0o600)
        except OSError:
            pass
    key = key_path.read_bytes()
    if len(key) != 32:
        raise ValueError("local audit key must contain exactly 32 bytes")
    return key


def build_handoff_receipt(
    vault: Path,
    *,
    household_id: str,
    subject_id: str,
    recipient_id: str,
    recipient_kind: str,
    processor_id: str,
    processor_kind: str,
    target_tier: str,
    included_event_ids: list[str],
    included_protocol_run_ids: list[str],
    consent_ids: list[str],
    egress_policy: dict[str, Any],
    content: str,
) -> dict[str, Any]:
    key = _audit_key(vault)
    generated_at = utc_now()
    receipt: dict[str, Any] = {
        "receipt_id": f"receipt_{secrets.token_hex(8)}",
        "schema_version": "0.1.0",
        "generated_at": generated_at,
        "household_id": household_id,
        "subject_id": subject_id,
        "recipient": {"recipient_id": recipient_id, "kind": recipient_kind},
        "processor": {"processor_id": processor_id, "kind": processor_kind},
        "purpose": "clinician_handoff",
        "target_tier": target_tier,
        "included_event_ids": sorted(set(included_event_ids)),
        "included_protocol_run_ids": sorted(set(included_protocol_run_ids)),
        "consent_ids": sorted(set(consent_ids)),
        "egress_policy_sha256": hashlib.sha256(_canonical(egress_policy)).hexdigest(),
        "content_sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
    }
    receipt["signature"] = {
        "algorithm": "hmac-sha256",
        "key_id": hashlib.sha256(key).hexdigest()[:16],
        "value": hmac.new(key, _canonical(receipt), hashlib.sha256).hexdigest(),
    }
    validate_handoff_receipt(receipt)
    out_dir = subject_dir(vault, subject_id) / "exports" / "receipts"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{receipt['receipt_id']}.json").write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )
    return receipt


def verify_handoff_receipt(vault: Path, receipt: dict[str, Any]) -> bool:
    validate_handoff_receipt(receipt)
    signature = receipt["signature"]
    unsigned = {key: value for key, value in receipt.items() if key != "signature"}
    key = _audit_key(vault)
    if hashlib.sha256(key).hexdigest()[:16] != signature["key_id"]:
        return False
    expected = hmac.new(key, _canonical(unsigned), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature["value"])
