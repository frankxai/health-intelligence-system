"""Protocol pack loading and run lifecycle."""

from __future__ import annotations

import json
import secrets
from pathlib import Path
from typing import Any

from .paths import PACKS
from .validate import (
    ValidationError,
    validate_active_run,
    validate_claim,
    validate_pack_meta,
    validate_protocol,
    strict_json_loads,
)
from .vault import load_household, resolve_subject_id, subject_dir, utc_now
from . import ledger as ledger_mod


def list_packs() -> list[str]:
    if not PACKS.exists():
        return []
    return sorted(p.name for p in PACKS.iterdir() if p.is_dir() and (p / "pack.json").exists())


def validate_protocol_evidence_parity(
    proto: dict[str, Any], claims: dict[str, dict[str, Any]]
) -> None:
    """A reviewed protocol may use only active claims at its declared floor."""

    if proto["release_status"] != "reviewed":
        return
    if proto["evidence_floor"] in {"E", "Q"}:
        raise ValidationError("reviewed protocol cannot use discovery or quarantine evidence")
    unsafe = [claim_id for claim_id in proto["claim_ids"] if claims[claim_id]["status"] != "active"]
    if unsafe:
        raise ValidationError(f"reviewed protocol cites non-active claims: {unsafe}")
    below_floor = [
        claim_id
        for claim_id in proto["claim_ids"]
        if claims[claim_id]["evidence_tier"] != proto["evidence_floor"]
    ]
    if below_floor:
        raise ValidationError(f"reviewed protocol evidence floor does not match claims: {below_floor}")


def load_pack(pack_id: str) -> dict[str, Any]:
    root = PACKS / pack_id
    meta_path = root / "pack.json"
    if not meta_path.exists():
        raise FileNotFoundError(f"unknown pack: {pack_id}")
    try:
        meta = strict_json_loads(meta_path.read_text(encoding="utf-8"), meta_path.name)
    except ValidationError:
        raise
    validate_pack_meta(meta)
    if meta["pack_id"] != pack_id:
        raise ValidationError(f"pack directory {pack_id!r} does not match pack_id {meta['pack_id']!r}")
    claims: dict[str, dict[str, Any]] = {}
    claims_dir = root / "claims"
    if claims_dir.exists():
        for fp in sorted(claims_dir.glob("*.json")):
            try:
                claim = strict_json_loads(fp.read_text(encoding="utf-8"), fp.name)
            except ValidationError:
                raise
            validate_claim(claim)
            if claim["domain_pack"] != pack_id:
                raise ValidationError(f"{fp.name} domain_pack does not match {pack_id}")
            if claim["claim_id"] in claims:
                raise ValidationError(f"duplicate claim_id {claim['claim_id']}")
            claims[claim["claim_id"]] = claim
    protocols: dict[str, dict[str, Any]] = {}
    proto_dir = root / "protocols"
    if proto_dir.exists():
        for fp in sorted(proto_dir.glob("*.json")):
            try:
                proto = strict_json_loads(fp.read_text(encoding="utf-8"), fp.name)
            except ValidationError:
                raise
            validate_protocol(proto)
            if proto["domain_pack"] != pack_id:
                raise ValidationError(f"{fp.name} domain_pack does not match {pack_id}")
            missing = [c for c in proto["claim_ids"] if c not in claims]
            if missing:
                raise ValidationError(f"{fp.name} cites missing claims: {missing}")
            try:
                validate_protocol_evidence_parity(proto, claims)
            except ValidationError as exc:
                raise ValidationError(f"{fp.name}: {exc}") from exc
            if proto["protocol_id"] in protocols:
                raise ValidationError(f"duplicate protocol_id {proto['protocol_id']}")
            protocols[proto["protocol_id"]] = proto
            # also index short ids without prefix for CLI convenience
            short = proto["protocol_id"].removeprefix("proto_")
            protocols.setdefault(short, proto)
            protocols.setdefault(fp.stem, proto)
    if not claims or not protocols:
        raise ValidationError(f"pack {pack_id} must contain at least one claim and protocol")
    return {"meta": meta, "claims": claims, "protocols": protocols, "root": root}


def _contraindication_gate(proto: dict[str, Any], events: list[dict[str, Any]]) -> list[str]:
    """Return immutable blocks. This prerelease has no override path."""

    blocks: list[str] = []
    blob = " ".join(
        (e.get("note") or "") + " " + " ".join(e.get("tags") or []) for e in events
    ).lower()
    for item in proto.get("contraindications") or []:
        if any(term.lower() in blob for term in item["match_terms"]):
            blocks.append(
                f"{item['condition_id']} ({item['severity']}/{item['action']}): {item['label']}"
            )
    if proto.get("class") in {"clinician_supervised_only", "jurisdiction_restricted"}:
        blocks.append(f"protocol class is {proto['class']} — reference CLI cannot start it")
    if "controlled_substance_check" in (proto.get("jurisdiction_flags") or []):
        blocks.append("jurisdiction_flag controlled_substance_check — blocked in reference CLI")
    if "clinician_required" in (proto.get("jurisdiction_flags") or []):
        blocks.append("jurisdiction_flag clinician_required — blocked in reference CLI")
    if (proto.get("safety") or {}).get("requires_clinician_clearance") is True:
        blocks.append(
            "protocol requires verified external signed clearance; no verifier is shipped, so start is blocked"
        )
    return blocks


def start_protocol(
    vault: Path,
    *,
    subject: str,
    pack_id: str,
    protocol_key: str,
) -> dict[str, Any]:
    pack = load_pack(pack_id)
    proto = pack["protocols"].get(protocol_key) or pack["protocols"].get(f"proto_{protocol_key}")
    if not proto:
        known = sorted({p["protocol_id"] for p in pack["protocols"].values() if "protocol_id" in p})
        raise KeyError(f"protocol {protocol_key!r} not in pack {pack_id}; known={known}")

    if pack["meta"]["release_status"] != "reviewed":
        raise ValidationError("pack is a non-startable synthetic draft")
    if proto["release_status"] != "reviewed":
        raise ValidationError("protocol is a non-startable synthetic draft")
    if proto["safety"]["medical_functionality_disabled"] is True:
        raise ValidationError("protocol execution is disabled in this prerelease runtime")

    household = load_household(vault)
    subject_id = resolve_subject_id(household, subject)
    events = ledger_mod.read_events(vault, subject_id)
    blocks = _contraindication_gate(proto, events)
    if blocks:
        raise ValidationError("immutable safety lock blocked start:\n- " + "\n- ".join(blocks))

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
        "gate_flags": [],
    }
    validate_active_run(record)
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
        try:
            run = strict_json_loads(fp.read_text(encoding="utf-8"), fp.name)
        except ValidationError:
            raise
        validate_active_run(run)
        if run["pack_id"] != run["protocol_snapshot"]["domain_pack"]:
            raise ValidationError(f"{fp.name} pack_id does not match protocol snapshot")
        runs.append(run)
    return runs
