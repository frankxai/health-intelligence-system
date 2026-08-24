"""Adversarial tests for the non-medical BIOS prerelease foundation."""

from __future__ import annotations

import copy
import inspect
import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from bios_substrate import __main__ as cli  # noqa: E402
from bios_substrate.audit import verify_handoff_receipt  # noqa: E402
from bios_substrate.handoff import build_handoff  # noqa: E402
from bios_substrate.ledger import append_event, read_events  # noqa: E402
from bios_substrate.privacy import compile_export_events, load_consents, load_egress_policy  # noqa: E402
from bios_substrate.protocol_ops import (  # noqa: E402
    list_packs,
    load_pack,
    start_protocol,
    validate_protocol_evidence_parity,
)
from bios_substrate.registry import load_agent_manifest, load_domain_agent_registry, load_idea_sources  # noqa: E402
from bios_substrate.validate import (  # noqa: E402
    ValidationError,
    strict_json_loads,
    validate_claim,
    validate_consent,
    validate_domain_agent_registry,
    validate_idea_source,
    validate_published_schema,
)
from bios_substrate.vault import add_subject, init_household_vault  # noqa: E402


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _consent_path(vault: Path) -> Path:
    return vault / "subjects" / "sub_self" / "consent" / "self-tracking.json"


def _scope_events(vault: Path, *events: dict, run_ids: list[str] | None = None) -> None:
    path = _consent_path(vault)
    consent = _read(path)
    consent["record_scope"] = {
        "event_ids": [event["event_id"] for event in events],
        "protocol_run_ids": run_ids or [],
    }
    _write(path, consent)


class PublishedContractTests(unittest.TestCase):
    def test_all_schemas_are_valid_draft_2020_12_closed_objects(self):
        paths = sorted((ROOT / "schemas").glob("*.schema.json"))
        self.assertGreaterEqual(len(paths), 11)
        for path in paths:
            schema = strict_json_loads(path.read_text(encoding="utf-8"), path.name)
            Draft202012Validator.check_schema(schema)
            self.assertEqual(schema.get("type"), "object", path.name)
            self.assertFalse(schema.get("additionalProperties"), path.name)
            self.assertTrue(schema.get("required"), path.name)

    def test_runtime_uses_schema_format_checker(self):
        event = {
            "event_id": "evt_demo",
            "schema_version": "0.1.0",
            "household_id": "hh_demo",
            "subject_id": "sub_demo",
            "recorded_at": "not-a-date",
            "kind": "note",
            "sensitivity_class": "public",
            "source": {"channel": "human"},
        }
        with self.assertRaisesRegex(ValidationError, "date-time"):
            validate_published_schema(event, "ledger-event.schema.json", "event")

    def test_duplicate_json_keys_are_rejected(self):
        with self.assertRaisesRegex(ValidationError, "duplicate key 'status'"):
            strict_json_loads('{"status":"draft","status":"active"}', "claim")


class DraftFoundationTests(unittest.TestCase):
    def test_every_shipped_claim_and_protocol_is_non_startable_draft(self):
        for pack_id in list_packs():
            pack = load_pack(pack_id)
            self.assertEqual(pack["meta"]["release_status"], "draft_synthetic")
            for claim in pack["claims"].values():
                self.assertEqual(claim["status"], "draft")
                self.assertFalse(claim["admission"]["user_facing_allowed"])
            unique_protocols = {row["protocol_id"]: row for row in pack["protocols"].values()}
            self.assertTrue(unique_protocols)
            for protocol in unique_protocols.values():
                self.assertEqual(protocol["release_status"], "draft_synthetic")
                self.assertTrue(protocol["safety"]["medical_functionality_disabled"])

    def test_real_shipped_fixtures_cannot_start(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "synthetic"
            init_household_vault(vault, household_name="Synthetic", subject_label="self")
            for pack_id in list_packs():
                pack = load_pack(pack_id)
                protocol = next(iter(pack["protocols"].values()))
                with self.assertRaisesRegex(ValidationError, "non-startable synthetic draft"):
                    start_protocol(
                        vault,
                        subject="self",
                        pack_id=pack_id,
                        protocol_key=protocol["protocol_id"],
                    )

    def test_force_override_surface_is_absent(self):
        self.assertNotIn("force", inspect.signature(start_protocol).parameters)
        parser = cli.build_parser()
        with self.assertRaises(SystemExit):
            parser.parse_args(
                [
                    "protocol",
                    "start",
                    "--vault",
                    "x",
                    "--pack",
                    "breath",
                    "--id",
                    "fixture",
                    "--force",
                ]
            )

    def test_contraindications_are_structured_hard_actions(self):
        for pack_id in list_packs():
            pack = load_pack(pack_id)
            for protocol in {row["protocol_id"]: row for row in pack["protocols"].values()}.values():
                for item in protocol["contraindications"]:
                    self.assertIn(item["severity"], {"review", "high", "critical"})
                    self.assertIn(
                        item["action"],
                        {
                            "block_pending_human_review",
                            "block_and_require_verified_signed_clearance",
                            "permanent_runtime_block",
                        },
                    )


class ConsentAndHandoffTests(unittest.TestCase):
    def test_minimum_necessary_exact_event_scope_and_no_denied_metadata_leak(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "synthetic"
            init_household_vault(vault, household_name="Synthetic", subject_label="self")
            allowed = append_event(
                vault,
                subject="self",
                kind="hydration",
                note="ALLOWED-SYNTHETIC",
                sensitivity_class="personal",
            )
            append_event(
                vault,
                subject="self",
                kind="symptom",
                note="DENIED-CLINICAL-SYNTHETIC",
                sensitivity_class="clinical",
            )
            append_event(
                vault,
                subject="self",
                kind="note",
                note="DENIED-GENOMIC-SYNTHETIC",
                sensitivity_class="genomic",
            )
            _scope_events(vault, allowed)
            text = build_handoff(vault, "self")
            self.assertIn("Included ledger events: 1", text)
            self.assertNotIn("ALLOWED-SYNTHETIC", text)
            self.assertNotIn("DENIED-CLINICAL-SYNTHETIC", text)
            self.assertNotIn("DENIED-GENOMIC-SYNTHETIC", text)
            self.assertNotIn("Omitted", text)
            self.assertNotIn("Validated local ledger event count", text)

    def test_processor_recipient_purpose_action_tier_are_exact(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "synthetic"
            init_household_vault(vault, household_name="Synthetic", subject_label="self")
            with self.assertRaisesRegex(ValidationError, "processor"):
                build_handoff(
                    vault,
                    "self",
                    processor_id="unconsented_processor",
                    processor_kind="hosted_model",
                    target_tier="frontier",
                )
            with self.assertRaisesRegex(ValidationError, "recipient"):
                build_handoff(
                    vault,
                    "self",
                    recipient_id="clinic_unconsented",
                    recipient_kind="clinician",
                )

    def test_protocol_event_requires_exact_run_id_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "synthetic"
            hh = init_household_vault(vault, household_name="Synthetic", subject_label="self")
            event = append_event(
                vault,
                subject="self",
                kind="protocol_checkin",
                note="SYNTHETIC-RUN-NOTE",
                sensitivity_class="personal",
                protocol_id="proto_synthetic",
                protocol_run_id="run_synthetic",
            )
            _scope_events(vault, event)
            grants = load_consents(vault, hh["household_id"], "sub_self")
            policy = load_egress_policy(vault, hh["household_id"], "sub_self")
            compiled = compile_export_events(
                [event],
                grants=grants,
                policy=policy,
                recipient_id="sub_self",
                recipient_kind="self",
                processor_id="bios_local_runtime",
                processor_kind="local_runtime",
                target_tier="local",
            )
            self.assertEqual(compiled["included"], [])
            self.assertEqual(set(compiled), {"included", "consent_ids"})
            _scope_events(vault, event, run_ids=["run_synthetic"])
            grants = load_consents(vault, hh["household_id"], "sub_self")
            compiled = compile_export_events(
                [event],
                grants=grants,
                policy=policy,
                recipient_id="sub_self",
                recipient_kind="self",
                processor_id="bios_local_runtime",
                processor_kind="local_runtime",
                target_tier="local",
            )
            self.assertEqual([row["event_id"] for row in compiled["included"]], [event["event_id"]])

    def test_event_kind_enforces_sensitivity_floor_at_append_and_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "synthetic"
            hh = init_household_vault(vault, household_name="Synthetic", subject_label="self")
            with self.assertRaisesRegex(ValidationError, "requires at least clinical sensitivity"):
                append_event(
                    vault,
                    subject="self",
                    kind="symptom",
                    note="SYNTHETIC",
                    sensitivity_class="public",
                )
            event = append_event(
                vault,
                subject="self",
                kind="symptom",
                note="SYNTHETIC",
                sensitivity_class="clinical",
            )
            _scope_events(vault, event)
            grants = load_consents(vault, hh["household_id"], "sub_self")
            policy = load_egress_policy(vault, hh["household_id"], "sub_self")
            event["sensitivity_class"] = "public"
            with self.assertRaisesRegex(ValidationError, "requires at least clinical sensitivity"):
                compile_export_events(
                    [event],
                    grants=grants,
                    policy=policy,
                    recipient_id="sub_self",
                    recipient_kind="self",
                    processor_id="bios_local_runtime",
                    processor_kind="local_runtime",
                    target_tier="local",
                )

    def test_duplicate_event_ids_fail_at_ledger_and_export_boundaries(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "synthetic"
            hh = init_household_vault(vault, household_name="Synthetic", subject_label="self")
            event = append_event(
                vault,
                subject="self",
                kind="note",
                note="FIRST-SYNTHETIC",
                sensitivity_class="personal",
            )
            duplicate = copy.deepcopy(event)
            duplicate["note"] = "SECOND-SYNTHETIC"
            _scope_events(vault, event)
            grants = load_consents(vault, hh["household_id"], "sub_self")
            policy = load_egress_policy(vault, hh["household_id"], "sub_self")
            with self.assertRaisesRegex(ValidationError, "duplicate event_id"):
                compile_export_events(
                    [event, duplicate],
                    grants=grants,
                    policy=policy,
                    recipient_id="sub_self",
                    recipient_kind="self",
                    processor_id="bios_local_runtime",
                    processor_kind="local_runtime",
                    target_tier="local",
                )
            ledger = vault / "subjects" / "sub_self" / "ledger.jsonl"
            with ledger.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(duplicate) + "\n")
            with self.assertRaisesRegex(ValidationError, "duplicates event_id"):
                read_events(vault, "self")

    def test_protocol_outcome_requires_exact_run_and_data_class_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "synthetic"
            hh = init_household_vault(vault, household_name="Synthetic", subject_label="self")
            with self.assertRaisesRegex(ValidationError, "protocol_run_id"):
                append_event(
                    vault,
                    subject="self",
                    kind="protocol_outcome",
                    sensitivity_class="personal",
                    protocol_id="proto_synthetic",
                )
            event = append_event(
                vault,
                subject="self",
                kind="protocol_outcome",
                sensitivity_class="personal",
                protocol_id="proto_synthetic",
                protocol_run_id="run_synthetic",
            )
            consent_path = _consent_path(vault)
            consent = _read(consent_path)
            consent["data_classes"].append("protocol_outcomes_deid")
            consent["record_scope"] = {
                "event_ids": [event["event_id"]],
                "protocol_run_ids": [],
            }
            _write(consent_path, consent)
            policy = load_egress_policy(vault, hh["household_id"], "sub_self")
            grants = load_consents(vault, hh["household_id"], "sub_self")
            compiled = compile_export_events(
                [event],
                grants=grants,
                policy=policy,
                recipient_id="sub_self",
                recipient_kind="self",
                processor_id="bios_local_runtime",
                processor_kind="local_runtime",
                target_tier="local",
            )
            self.assertEqual(compiled["included"], [])
            consent["record_scope"]["protocol_run_ids"] = ["run_synthetic"]
            _write(consent_path, consent)
            grants = load_consents(vault, hh["household_id"], "sub_self")
            compiled = compile_export_events(
                [event],
                grants=grants,
                policy=policy,
                recipient_id="sub_self",
                recipient_kind="self",
                processor_id="bios_local_runtime",
                processor_kind="local_runtime",
                target_tier="local",
            )
            self.assertEqual([row["event_id"] for row in compiled["included"]], [event["event_id"]])

    def test_future_grant_and_future_withdrawal_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "synthetic"
            init_household_vault(vault, household_name="Synthetic", subject_label="self")
            path = _consent_path(vault)
            consent = _read(path)
            consent["granted_at"] = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
            _write(path, consent)
            with self.assertRaisesRegex(ValidationError, "future"):
                build_handoff(vault, "self")

            consent["granted_at"] = datetime.now(timezone.utc).isoformat()
            consent["status"] = "withdrawn"
            consent["withdrawn_at"] = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
            _write(path, consent)
            with self.assertRaisesRegex(ValidationError, "future"):
                build_handoff(vault, "self")

    def test_duplicate_consent_id_and_revocation_precedence_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "synthetic"
            init_household_vault(vault, household_name="Synthetic", subject_label="self")
            original_path = _consent_path(vault)
            original = _read(original_path)
            duplicate_path = original_path.parent / "duplicate.json"
            _write(duplicate_path, original)
            with self.assertRaisesRegex(ValidationError, "duplicate consent_id"):
                build_handoff(vault, "self")
            duplicate_path.unlink()

            revoked = copy.deepcopy(original)
            revoked["consent_id"] = "consent_self_track_revoked"
            revoked["revision"] = 2
            revoked["supersedes_consent_id"] = original["consent_id"]
            revoked["status"] = "withdrawn"
            revoked["withdrawn_at"] = revoked["granted_at"]
            _write(original_path.parent / "revocation.json", revoked)
            with self.assertRaisesRegex(ValidationError, "no active exact-scope export consent"):
                build_handoff(vault, "self")

    def test_later_predecessor_withdrawal_invalidates_earlier_successor(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "synthetic"
            hh = init_household_vault(vault, household_name="Synthetic", subject_label="self")
            original_path = _consent_path(vault)
            original = _read(original_path)
            granted = datetime.now(timezone.utc) - timedelta(minutes=5)
            original["granted_at"] = granted.isoformat()
            successor = copy.deepcopy(original)
            successor["consent_id"] = "consent_self_track_successor"
            successor["revision"] = 2
            successor["supersedes_consent_id"] = original["consent_id"]
            successor["granted_at"] = (granted + timedelta(minutes=1)).isoformat()
            original["status"] = "withdrawn"
            original["withdrawn_at"] = (granted + timedelta(minutes=2)).isoformat()
            _write(original_path, original)
            _write(original_path.parent / "successor.json", successor)
            with self.assertRaisesRegex(ValidationError, "must postdate its predecessor withdrawal"):
                load_consents(vault, hh["household_id"], "sub_self")

    def test_signed_hash_receipt_is_persisted_and_tamper_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "synthetic"
            init_household_vault(vault, household_name="Synthetic", subject_label="self")
            text = build_handoff(vault, "self")
            self.assertIn("Local audit receipt", text)
            receipts = list((vault / "subjects" / "sub_self" / "exports" / "receipts").glob("*.json"))
            self.assertEqual(len(receipts), 1)
            receipt = _read(receipts[0])
            self.assertTrue(verify_handoff_receipt(vault, receipt))
            receipt["content_sha256"] = "0" * 64
            self.assertFalse(verify_handoff_receipt(vault, receipt))


class EvidenceAdmissionTests(unittest.TestCase):
    def _claim(self) -> dict:
        return copy.deepcopy(next(iter(load_pack("breath")["claims"].values())))

    def _activate(self, claim: dict) -> dict:
        claim["status"] = "active"
        claim["evidence_tier"] = "A"
        claim["certainty"] = "moderate"
        claim["harms"]["certainty"] = "moderate"
        claim["directness"] = "direct"
        claim["funding_coi"] = {
            "funding": "Independent synthetic test fixture",
            "coi_status": "none_declared",
        }
        claim["conflicts"] = {"status": "not_applicable", "notes": "Synthetic test"}
        claim["admission"] = {
            "user_facing_allowed": True,
            "evidence_review_complete": True,
            "license_review_complete": True,
            "correction_check_complete": True,
            "harms_review_complete": True,
            "funding_coi_review_complete": True,
            "integrity_review_complete": True,
            "directness_review_complete": True,
        }
        claim["last_reviewed"] = datetime.now(timezone.utc).date().isoformat()
        claim["integrity"] = {
            "status": "clear",
            "correction_status": "none_found",
            "supersession_status": "current",
            "reviewed_on": claim["last_reviewed"],
            "correction_checked_on": claim["last_reviewed"],
            "next_review_due": (datetime.now(timezone.utc) + timedelta(days=180)).date().isoformat(),
        }
        claim["rights"] = {
            "ingestion_mode": "metadata_only",
            "license_review_status": "approved",
        }
        for index, source in enumerate(claim["sources"]):
            source["reviewed_on"] = claim["last_reviewed"]
            source["correction_status"] = "none_found"
            source["correction_checked_on"] = claim["last_reviewed"]
            source["kind"] = "grade_guideline"
        return claim

    def test_active_claim_cannot_have_unchecked_or_retracted_source(self):
        claim = self._activate(self._claim())
        claim["sources"][0]["correction_status"] = "not_checked"
        claim["sources"][0].pop("correction_checked_on", None)
        with self.assertRaisesRegex(ValidationError, "correction checks"):
            validate_claim(claim)
        claim = self._activate(self._claim())
        claim["sources"][0]["correction_status"] = "retracted"
        with self.assertRaisesRegex(ValidationError, "retraction concern"):
            validate_claim(claim)

    def test_book_or_discovery_source_cannot_be_sole_active_support(self):
        claim = self._activate(self._claim())
        source = claim["sources"][0]
        source["kind"] = "book"
        source["license"] = "unknown"
        source["use_permission"] = "metadata_only"
        claim["sources"] = [source]
        with self.assertRaisesRegex(ValidationError, "matching source design"):
            validate_claim(claim)

    def test_discovery_source_cannot_ride_alongside_active_evidence(self):
        claim = self._activate(self._claim())
        claim["sources"][1]["kind"] = "podcast"
        claim["sources"][1]["license"] = "unknown"
        claim["sources"][1]["use_permission"] = "metadata_only"
        with self.assertRaisesRegex(ValidationError, "discovery-only source kinds"):
            validate_claim(claim)

    def test_full_text_permission_must_match_license(self):
        claim = self._claim()
        claim["sources"][0]["license"] = "unknown"
        claim["sources"][0]["use_permission"] = "open_access_full_text"
        with self.assertRaisesRegex(ValidationError, "incompatible with its license"):
            validate_claim(claim)

    def test_schema_and_semantic_admission_are_both_enforced(self):
        claim = self._claim()
        claim["population"] = "x"
        with self.assertRaisesRegex(ValidationError, "claim.schema.json"):
            validate_claim(claim)
        claim = self._claim()
        claim["admission"]["user_facing_allowed"] = True
        with self.assertRaisesRegex(ValidationError, "only an active claim"):
            validate_claim(claim)

    def test_reviewed_protocol_claim_status_and_floor_must_match(self):
        pack = load_pack("breath")
        claim = self._activate(copy.deepcopy(next(iter(pack["claims"].values()))))
        validate_claim(claim)
        protocol = copy.deepcopy(next(iter(pack["protocols"].values())))
        protocol["release_status"] = "reviewed"
        protocol["review_gate"] = {
            "evidence_reviewed": True,
            "safety_reviewed": True,
            "clinical_legal_reviewed": True,
        }
        claims = {claim["claim_id"]: claim}
        protocol["evidence_floor"] = "D"
        with self.assertRaisesRegex(ValidationError, "evidence floor does not match"):
            validate_protocol_evidence_parity(protocol, claims)
        protocol["evidence_floor"] = claim["evidence_tier"]
        claim["status"] = "withdrawn"
        with self.assertRaisesRegex(ValidationError, "non-active claims"):
            validate_protocol_evidence_parity(protocol, claims)


class RegistryAndVaultTests(unittest.TestCase):
    def test_registry_is_generic_only_and_reserved_names_are_denied(self):
        registry = load_domain_agent_registry()
        self.assertEqual(set(registry["reserved_name_denylist"]), {"vitalis", "velora"})
        self.assertTrue(all(row["implementation_status"] == "registry_only" for row in registry["agents"]))
        tampered = copy.deepcopy(registry)
        tampered["agents"][0]["canonical_label"] = "Vitalis"
        with self.assertRaisesRegex(ValidationError, "reserved public name"):
            validate_domain_agent_registry(tampered)

    def test_agent_manifest_has_no_runtime_write_surface(self):
        manifest = load_agent_manifest()
        self.assertEqual(manifest["writes"], ["none"])
        self.assertEqual(manifest["tools_required"], [])

    def test_idea_sources_are_metadata_only(self):
        for source in load_idea_sources():
            self.assertEqual(source["discovery_tier"], "idea_source_only")
            self.assertIn("no_copyrighted_full_text", source["content_policy"])
            validate_idea_source(source)
            oversized = copy.deepcopy(source)
            oversized["notes"] = "copied text " * 100
            with self.assertRaisesRegex(ValidationError, "idea-source.schema.json"):
                validate_idea_source(oversized)

    def test_vault_is_explicitly_synthetic_and_cross_subject_reads_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "synthetic"
            household = init_household_vault(vault, household_name="Synthetic", subject_label="self")
            self.assertEqual(household["vault_mode"], "synthetic_plaintext_prototype")
            self.assertIn("Never enter personal", (vault / "README.md").read_text(encoding="utf-8"))
            add_subject(vault, display_name="subject-b", role="other")
            event = append_event(vault, subject="self", kind="note", note="synthetic")
            event["subject_id"] = "sub_subject-b"
            ledger = vault / "subjects" / "sub_self" / "ledger.jsonl"
            ledger.write_text(json.dumps(event) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValidationError, "another subject"):
                read_events(vault, "self")

    def test_cli_validation_passes_synthetic_vault_and_draft_packs(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "synthetic"
            self.assertEqual(cli.main(["init", "--household", "Synthetic", "--path", str(vault)]), 0)
            self.assertEqual(cli.main(["validate", "--vault", str(vault)]), 0)


if __name__ == "__main__":
    unittest.main()
