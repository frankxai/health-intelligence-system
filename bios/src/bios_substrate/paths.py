"""BIOS package path helpers."""

from __future__ import annotations

from pathlib import Path

PKG_ROOT = Path(__file__).resolve().parents[2]  # .../bios
SCHEMAS = PKG_ROOT / "schemas"
PACKS = PKG_ROOT / "packs"
TEMPLATES = PKG_ROOT / "templates"


def repo_root() -> Path:
    return PKG_ROOT.parent
