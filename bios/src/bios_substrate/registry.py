"""Public, bounded domain-agent registry loader."""

from __future__ import annotations

import json
from typing import Any

from .paths import KNOWLEDGE, PACKS, REGISTRY
from .validate import (
    ValidationError,
    strict_json_loads,
    validate_agent_manifest,
    validate_domain_agent_registry,
    validate_idea_source,
)


def load_domain_agent_registry() -> dict[str, Any]:
    path = REGISTRY / "public-domain-agents.json"
    try:
        registry = strict_json_loads(path.read_text(encoding="utf-8"), "public domain-agent registry")
    except FileNotFoundError as exc:
        raise ValidationError("public domain-agent registry is missing") from exc
    except ValidationError:
        raise
    validate_domain_agent_registry(registry)
    return registry


def load_idea_sources() -> list[dict[str, Any]]:
    root = KNOWLEDGE / "idea-sources"
    paths = sorted(root.glob("*.json"))
    if not paths:
        raise ValidationError("idea-source registry is empty")
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path in paths:
        try:
            source = strict_json_loads(path.read_text(encoding="utf-8"), f"idea source {path.name}")
        except ValidationError:
            raise
        validate_idea_source(source)
        if source["idea_source_id"] in seen:
            raise ValidationError(f"duplicate idea_source_id {source['idea_source_id']}")
        seen.add(source["idea_source_id"])
        result.append(source)
    return result


def load_agent_manifest() -> dict[str, Any]:
    path = PACKS / "agent-bios-steward.manifest.json"
    try:
        manifest = strict_json_loads(path.read_text(encoding="utf-8"), "BIOS steward agent manifest")
    except FileNotFoundError as exc:
        raise ValidationError("BIOS steward agent manifest is missing") from exc
    except ValidationError:
        raise
    validate_agent_manifest(manifest)
    return manifest
