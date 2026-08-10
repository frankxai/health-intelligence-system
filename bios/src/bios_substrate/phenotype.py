"""Phenotype projection rebuild from ledger."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from . import ledger as ledger_mod
from .protocol_ops import list_active_runs
from .vault import load_household, resolve_subject_id, subject_dir, utc_now


def rebuild_phenotype(vault: Path, subject: str) -> dict[str, Any]:
    household = load_household(vault)
    subject_id = resolve_subject_id(household, subject)
    events = ledger_mod.read_events(vault, subject_id)
    runs = list_active_runs(vault, subject_id)

    tag_counter: Counter[str] = Counter()
    stack: list[dict[str, Any]] = []
    constraints: list[dict[str, Any]] = []
    for e in events:
        for t in e.get("tags") or []:
            tag_counter[t] += 1
        kind = e.get("kind")
        note = (e.get("note") or "").strip()
        if kind == "tea" and note:
            stack.append(
                {
                    "name": note[:80],
                    "kind": "tea",
                    "timing_note": ",".join(e.get("tags") or []),
                    "source_event_id": e["event_id"],
                }
            )
        if kind == "supplement_intake" and note:
            stack.append(
                {
                    "name": note[:80],
                    "kind": "supplement",
                    "timing_note": ",".join(e.get("tags") or []),
                    "source_event_id": e["event_id"],
                }
            )
        if kind == "breath_session":
            stack.append(
                {
                    "name": note[:80] if note else "breath practice",
                    "kind": "practice",
                    "timing_note": "breath",
                    "source_event_id": e["event_id"],
                }
            )
        if kind == "note" and "allerg" in note.lower():
            constraints.append({"label": note[:120], "source": "self_report"})

    # keep last unique stack items by name
    seen: set[str] = set()
    stack_unique: list[dict[str, Any]] = []
    for item in reversed(stack):
        key = item["name"].lower()
        if key in seen:
            continue
        seen.add(key)
        stack_unique.append(item)
    stack_unique.reverse()

    phenotype = {
        "phenotype_id": f"pheno_{subject_id}",
        "schema_version": "0.1.0",
        "household_id": household["household_id"],
        "subject_id": subject_id,
        "built_at": utc_now(),
        "ledger_event_count": len(events),
        "chronotype_lite": {"preference": "unknown", "notes": "Infer only from sufficient sleep events later"},
        "baselines": {
            "event_kinds": dict(Counter(e.get("kind") for e in events)),
        },
        "constraints": constraints,
        "allergies_self_report": [],
        "active_protocols": [
            {
                "protocol_id": r["protocol_id"],
                "run_id": r["run_id"],
                "started_at": r["started_at"],
                "pack": r.get("pack_id"),
            }
            for r in runs
        ],
        "current_stack": stack_unique[-20:],
        "recent_tags": [t for t, _ in tag_counter.most_common(20)],
        "rebuild_command": "bios_substrate phenotype rebuild",
    }
    out = subject_dir(vault, subject_id) / "phenotype.json"
    out.write_text(json.dumps(phenotype, indent=2) + "\n", encoding="utf-8")
    return phenotype
