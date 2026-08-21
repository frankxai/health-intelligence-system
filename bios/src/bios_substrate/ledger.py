"""Append-only ledger operations."""

from __future__ import annotations

import json
import secrets
from pathlib import Path
from typing import Any

from .validate import validate_ledger_event
from .vault import load_household, resolve_subject_id, subject_dir, utc_now


def new_event_id() -> str:
    return f"evt_{secrets.token_hex(8)}"


def append_event(
    vault: Path,
    *,
    subject: str,
    kind: str,
    note: str | None = None,
    tags: list[str] | None = None,
    metrics: dict[str, Any] | None = None,
    sensitivity_class: str = "personal",
    channel: str = "human",
    protocol_id: str | None = None,
    protocol_run_id: str | None = None,
    operator_id: str | None = None,
) -> dict[str, Any]:
    household = load_household(vault)
    subject_id = resolve_subject_id(household, subject)
    event: dict[str, Any] = {
        "event_id": new_event_id(),
        "schema_version": "0.1.0",
        "household_id": household["household_id"],
        "subject_id": subject_id,
        "recorded_at": utc_now(),
        "occurred_at": utc_now(),
        "kind": kind,
        "sensitivity_class": sensitivity_class,
        "source": {"channel": channel},
    }
    if operator_id:
        event["operator_id"] = operator_id
    if note:
        event["note"] = note
    if tags:
        event["tags"] = sorted(set(tags))
    if metrics:
        event["metrics"] = metrics
    if protocol_id:
        event["protocol_id"] = protocol_id
    if protocol_run_id:
        event["protocol_run_id"] = protocol_run_id

    validate_ledger_event(event)
    path = subject_dir(vault, subject_id) / "ledger.jsonl"
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")
    return event


def read_events(vault: Path, subject: str) -> list[dict[str, Any]]:
    household = load_household(vault)
    subject_id = resolve_subject_id(household, subject)
    path = subject_dir(vault, subject_id) / "ledger.jsonl"
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        events.append(json.loads(line))
    return events
