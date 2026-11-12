import copy
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from data_ops import ConflictError,content_hash,imported_id,notion_record_id,sync_decision,merge_import,supplement_exposures
from validate import validate_dataset

class RecordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.demo=json.loads((ROOT/"synthetic/demo.json").read_text())
        cls.blank=json.loads((ROOT/"synthetic/blank.json").read_text())
        cls.schema=json.loads((ROOT/"canonical/schema.json").read_text())
    def test_demo_valid_synthetic(self):
        self.assertEqual(validate_dataset(self.demo,self.schema,True),[])
    def test_blank_valid(self):
        self.assertEqual(validate_dataset(self.blank,self.schema),[])
    def test_stable_source_identity(self):
        ns=self.demo["entities"]["profile"][0]["id"]
        self.assertEqual(imported_id(ns,"daily_observation","record-1"),imported_id(ns,"daily_observation","record-1"))
        self.assertNotEqual(imported_id(ns,"daily_observation","record-1"),imported_id(ns,"symptom","record-1"))
    def test_notion_page_id_fallback(self):
        value=self.demo["entities"]["profile"][0]["id"]
        self.assertEqual(notion_record_id(None,value.replace("-","")),value)
    def test_idempotent_import(self):
        first,receipts=merge_import(self.blank,self.demo)
        self.assertEqual(sum(r["outcome"]=="create" for r in receipts),39)
        second,receipts=merge_import(first,self.demo)
        self.assertEqual(first,second)
        self.assertTrue(all(r["outcome"]=="unchanged" for r in receipts))
    def test_stale_update_preserves_current(self):
        changed=copy.deepcopy(self.demo)
        changed["entities"]["daily_observation"][0]["energy_0_10"]=1
        merged,receipts=merge_import(self.demo,changed)
        self.assertEqual(merged,self.demo)
        self.assertEqual(sum(r["outcome"]=="conflict" for r in receipts),1)
    def test_authorized_revision_update(self):
        changed=copy.deepcopy(self.demo)
        record=changed["entities"]["daily_observation"][0]
        record["energy_0_10"]=0
        merged,receipts=merge_import(self.demo,changed,{record["id"]:1})
        self.assertEqual(merged["entities"]["daily_observation"][0]["energy_0_10"],0)
        self.assertEqual(merged["entities"]["daily_observation"][0]["revision"],2)
    def test_tombstone_not_resurrected(self):
        current=copy.deepcopy(self.demo["entities"]["profile"][0]); incoming=copy.deepcopy(current)
        current["deleted_at"]="2026-10-02T10:00:00+02:00"
        with self.assertRaises(ConflictError):sync_decision(current,incoming,1)
    def test_duplicate_day_rejected(self):
        changed=copy.deepcopy(self.demo)
        changed["entities"]["daily_observation"][1]["local_date"]=changed["entities"]["daily_observation"][0]["local_date"]
        self.assertTrue(any("duplicate owner/local_date" in e for e in validate_dataset(changed,self.schema)))
    def test_dangling_reference_rejected(self):
        changed=copy.deepcopy(self.demo); changed["entities"]["product"]=[]
        self.assertTrue(any("dangling product_id" in e for e in validate_dataset(changed,self.schema)))
    def test_unknown_not_zero(self):
        changed=copy.deepcopy(self.demo)
        changed["entities"]["daily_observation"][0].pop("energy_0_10")
        self.assertEqual(validate_dataset(changed,self.schema),[])
        changed["entities"]["daily_observation"][0]["energy_0_10"]=None
        self.assertTrue(validate_dataset(changed,self.schema))
    def test_timezone_required(self):
        changed=copy.deepcopy(self.demo); changed["entities"]["profile"][0]["timezone"]="Not/AZone"
        self.assertTrue(any("invalid IANA timezone" in e for e in validate_dataset(changed,self.schema)))
    def test_exposure_arithmetic(self):
        self.assertEqual(supplement_exposures(self.demo,"2026-10-01")["vitamin_b6"]["value"],3.5)
        self.assertEqual(supplement_exposures(self.demo,"2026-10-02"),{})
    def test_mass_units_conversion(self):
        changed=copy.deepcopy(self.demo)
        changed["entities"]["ingredient"][1]["amount_per_serving"]=1500
        changed["entities"]["ingredient"][1]["unit"]="mcg"
        self.assertEqual(supplement_exposures(changed,"2026-10-01")["vitamin_b6"]["value"],3.5)
    def test_iu_not_silently_converted(self):
        changed=copy.deepcopy(self.demo); changed["entities"]["ingredient"][0]["unit"]="IU"
        with self.assertRaises(ValueError):supplement_exposures(changed,"2026-10-01")
    def test_planned_not_consumed(self):
        changed=copy.deepcopy(self.demo); changed["entities"]["intake"][0]["event_status"]="planned"
        self.assertEqual(supplement_exposures(changed,"2026-10-01")["vitamin_b6"]["value"],1.5)
    def test_label_unverified(self):
        changed=copy.deepcopy(self.demo); changed["entities"]["product"][0]["label_verified"]=False
        with self.assertRaises(ValueError):supplement_exposures(changed,"2026-10-01")
    def test_duration_mismatch(self):
        changed=copy.deepcopy(self.demo); changed["entities"]["sleep"][0]["duration_h"]=8
        self.assertTrue(any("duration_h disagrees" in e for e in validate_dataset(changed,self.schema)))
    def test_private_email_rejected_in_demo(self):
        changed=copy.deepcopy(self.demo); changed["entities"]["profile"][0]["notes"]="demo@example.invalid"
        self.assertTrue(any("email address" in e for e in validate_dataset(changed,self.schema,True)))
    def test_hash_ignores_revision_only(self):
        a=self.demo["entities"]["profile"][0];b=copy.deepcopy(a);b["revision"]=2
        self.assertEqual(content_hash(a),content_hash(b))
    def test_repeated_update_cannot_reuse_stale_revision(self):
        changed=copy.deepcopy(self.blank)
        record=copy.deepcopy(self.demo["entities"]["daily_observation"][0])
        record["energy_0_10"]=1
        second=copy.deepcopy(record);second["energy_0_10"]=2
        changed["entities"]["daily_observation"]=[record,second]
        merged,receipts=merge_import(self.demo,changed,{record["id"]:1})
        self.assertEqual([r["outcome"] for r in receipts],["update","conflict"])
        self.assertEqual(merged["entities"]["daily_observation"][0]["energy_0_10"],1)
    def test_cross_owner_reference_rejected(self):
        changed=copy.deepcopy(self.demo)
        other=copy.deepcopy(changed["entities"]["profile"][0])
        other["id"]="c1a1ce35-3e95-440e-a5f8-a20b100e286c";other["owner_id"]=other["id"]
        changed["entities"]["profile"].append(other)
        changed["entities"]["intake"][0]["owner_id"]=other["id"]
        self.assertTrue(any("cross-owner product_id" in e for e in validate_dataset(changed,self.schema)))
    def test_demo_rejects_non_synthetic_record(self):
        changed=copy.deepcopy(self.demo);changed["entities"]["profile"][0]["provenance"]["kind"]="reported"
        self.assertTrue(any("must be synthetic" in e for e in validate_dataset(changed,self.schema,True)))
    def test_invalid_timestamp_offset_rejected(self):
        changed=copy.deepcopy(self.demo);changed["entities"]["profile"][0]["created_at"]="2026-10-01T12:00:00"
        self.assertTrue(validate_dataset(changed,self.schema))

if __name__=="__main__":unittest.main()
