"""Protocol pack loading and run lifecycle."""

from __future__ import annotations

import json
import secrets
from pathlib import Path
from typing import Any

from .paths import PACKS
from .validate import ValidationError, validate_claim, validate_protocol
from .vault import load_household, resolve_subject_id, subject_dir, utc_now
from . import ledger as ledger_mod


def list_packs() -> list[str]:
    if not PACKS.exists():
        return []
    return sorted(p.name for p in PACKS.iterdir() if p.is_dir() and (p / "pack.json").exists())


def load_pack(pack_id: str) -> dict[str, Any]:
    root = PACKS / pack_id
    meta_path = root / "pack.json"
    if not meta_path.exists():
        raise FileNotFoundError(f"unknown pack: {pack_id}")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    claims: dict[str, dict[str, Any]] = {}
    claims_dir = root / "claims"
    if claims_dir.exists():
        for fp in claims_dir.glob("*.json"):
            claim = json.loads(fp.read_text(encoding="utf-8"))
            validate_claim(claim)
            claims[claim["claim_id"]] = claim
    protocols: dict[str, dict[str, Any]] = {}
    proto_dir = root / "protocols"
    if proto_dir.exists():
        for fp in proto_dir.glob("*.json"):
            proto = json.loads(fp.read_text(encoding="utf-8"))
            validate_protocol(proto)
            missing = [c for c in proto["claim_ids"] if c not in claims]
            if missing:
                raise ValidationError(f"{fp.name} cites missing claims: {missing}")
            protocols[proto["protocol_id"]] = proto
            # also index short ids without prefix for CLI convenience
            short = proto["protocol_id"].removeprefix("proto_")
            protocols.setdefault(short, proto)
            protocols.setdefault(fp.stem, proto)
    return {"meta": meta, "claims": claims, "protocols": protocols, "root": root}


def _contraindication_gate(proto: dict[str, Any], events: list[dict[str, Any]]) -> list[str]:
    """Soft gate: flag if ledger notes mention contraindication keywords."""
    flags: list[str] = []
    blob = " ".join(
        (e.get("note") or "") + " " + " ".join(e.get("tags") or []) for e in events
    ).lower()
    for item in proto.get("contraindications") or []:
        # extract simple tokens longer than 4 chars
        tokens = [t for t in item.lower().replace("/", " ").split() if len(t) > 4]
        for t in tokens:
            if t in {"should", "before", "after", "while", "under", "without", "clinician"}:
                continue
            if t in blob:
                flags.append(f"possible match on contraindication note: {item}")
                break
    if proto.get("class") in {"clinician_supervised_only", "jurisdiction_restricted"}:
        flags.append(f"protocol class is {proto['class']} — do not start without qualified human clearance")
    if "controlled_substance_check" in (proto.get("jurisdiction_flags") or []):
        flags.append("jurisdiction_flag controlled_substance_check — blocked in reference CLI")
    return flags


def start_protocol(
    vault: Path,
    *,
    subject: str,
    pack_id: str,
    protocol_key: str,
    force: bool = False,
) -> dict[str, Any]:
    pack = load_pack(pack_id)
    proto = pack["protocols"].get(protocol_key) or pack["protocols"].get(f"proto_{protocol_key}")
    if not proto:
        known = sorted({p["protocol_id"] for p in pack["protocols"].values() if "protocol_id" in p})
        raise KeyError(f"protocol {protocol_key!r} not in pack {pack_id}; known={known}")

    household = load_household(vault)
    subject_id = resolve_subject_id(household, subject)
    events = ledger_mod.read_events(vault, subject_id)
    flags = _contraindication_gate(proto, events)
    hard = [f for f in flags if "blocked" in f or "do not start" in f]
    if hard and not force:
        raise ValidationError("contraindication gate blocked start:\n- " + "\n- ".join(hard))
    if flags and not force:
        # soft flags still block unless --force for safety-first default
        raise ValidationError(
            "contraindication gate requires review (re-run with --force only after human review):\n- "
            + "\n- ".join(flags)
        )

    run_id = f"run_{secrets.token_hex(6)}"
    sdir = subject_dir(vault, subject_id)
    active_path = sdir / "protocols" / "active" / f"{run_id}.json"
    record = {
        "run_id": run_id,
        "protocol_id": proto["protocol_id"],
        "pack_id": pack_id,
        "started_at": utc_now(),
        "status": "active",
        "protocol_snapshot": proto,
        "gate_flags": flags,
        "forced": force,
    }
    active_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    ledger_mod.append_event(
        vault,
        subject=subject_id,
        kind="protocol_start",
        note=f"Started {proto['title']}",
        tags=[pack_id, "protocol"],
        protocol_id=proto["protocol_id"],
        protocol_run_id=run_id,
        sensitivity_class="personal",
        channel="agent",
    )
    return record


def list_active_runs(vault: Path, subject: str) -> list[dict[str, Any]]:
    household = load_household(vault)
    subject_id = resolve_subject_id(household, subject)
    active = subject_dir(vault, subject_id) / "protocols" / "active"
    if not active.exists():
        return []
    runs = []
    for fp in sorted(active.glob("*.json")):
        runs.append(json.loads(fp.read_text(encoding="utf-8")))
    return runs
