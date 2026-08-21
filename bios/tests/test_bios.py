"""BIOS reference tests — stdlib unittest."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from bios_substrate.protocol_ops import list_packs, load_pack, start_protocol  # noqa: E402
from bios_substrate.validate import ValidationError, validate_protocol  # noqa: E402
from bios_substrate.vault import add_subject, init_household_vault  # noqa: E402
from bios_substrate.ledger import append_event, read_events  # noqa: E402
from bios_substrate.phenotype import rebuild_phenotype  # noqa: E402
from bios_substrate.handoff import build_handoff  # noqa: E402
from bios_substrate import __main__ as cli  # noqa: E402


class PackTests(unittest.TestCase):
    def test_all_packs_load(self):
        packs = list_packs()
        self.assertGreaterEqual(len(packs), 4)
        for p in packs:
            loaded = load_pack(p)
            self.assertTrue(loaded["protocols"])
            self.assertTrue(loaded["claims"])


class VaultFlowTests(unittest.TestCase):
    def test_init_observe_protocol_handoff(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "hh"
            init_household_vault(vault, household_name="Demo House", subject_label="self")
            append_event(vault, subject="self", kind="breath_session", note="box breathing", tags=["breath"])
            append_event(vault, subject="self", kind="tea", note="mint culinary tea", tags=["tea", "evening"])
            # morning light should start clean
            run = start_protocol(vault, subject="self", pack_id="circadian", protocol_key="morning-light-10m")
            self.assertEqual(run["status"], "active")
            ph = rebuild_phenotype(vault, "self")
            self.assertGreaterEqual(ph["ledger_event_count"], 3)
            text = build_handoff(vault, "self")
            self.assertIn("Clinician handoff", text)
            self.assertIn("not a diagnosis", text.lower())
            events = read_events(vault, "self")
            self.assertTrue(any(e["kind"] == "protocol_start" for e in events))

    def test_steward_second_subject(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "hh"
            init_household_vault(vault, household_name="Family", subject_label="alex")
            sub = add_subject(vault, display_name="grandma", role="grandparent")
            self.assertTrue(sub.startswith("sub_"))
            append_event(vault, subject="grandma", kind="note", note="slept ok", channel="phone")
            events = read_events(vault, "grandma")
            self.assertEqual(len(events), 1)

    def test_gate_blocks_controlled_flag_protocols(self):
        # Ensure validate_protocol rejects missing safety
        bad = {
            "protocol_id": "proto_x",
            "schema_version": "0.1.0",
            "title": "Bad",
            "domain_pack": "custom",
            "class": "ordinary_wellness",
            "hypothesis": "x" * 20,
            "intervention": {"summary": "do thing", "steps": ["a"]},
            "timing": {"anchor": "morning"},
            "duration": {"days": 1},
            "measurement_plan": [{"metric": "m", "method": "self_report", "cadence": "d"}],
            "stop_conditions": ["stop"],
            "contraindications": ["none known"],
            "claim_ids": ["claim_x"],
            "evidence_floor": "anecdote_n",
            "jurisdiction_flags": ["none"],
            "safety": {"not_diagnosis": False, "not_prescription": True, "emergency_route": "call emergency"},
        }
        with self.assertRaises(ValidationError):
            validate_protocol(bad)


class CliTests(unittest.TestCase):
    def test_cli_validate(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "v"
            rc = cli.main(["init", "--household", "H", "--path", str(vault)])
            self.assertEqual(rc, 0)
            rc = cli.main(["validate", "--vault", str(vault)])
            self.assertEqual(rc, 0)
            rc = cli.main(["packs"])
            self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
