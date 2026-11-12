"""Independent regressions for ownership, deleted references and platform drift."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from data_ops import ConflictError, supplement_exposures, sync_decision
from validate import validate_dataset


class IndependentBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.demo = json.loads((ROOT / 'synthetic/demo.json').read_text())
        cls.schema = json.loads((ROOT / 'canonical/schema.json').read_text())

    def other_owner(self, dataset):
        profile = copy.deepcopy(dataset['entities']['profile'][0])
        profile['id'] = 'c1a1ce35-3e95-440e-a5f8-a20b100e286c'
        profile['owner_id'] = profile['id']
        dataset['entities']['profile'].append(profile)
        return profile['id']

    def test_deleted_product_does_not_silently_contribute(self):
        changed = copy.deepcopy(self.demo)
        changed['entities']['product'][0]['deleted_at'] = '2026-10-02T12:00:00+02:00'
        with self.assertRaisesRegex(ValueError, 'deleted product'):
            supplement_exposures(changed, '2026-10-01')

    def test_deleted_intake_is_not_consumed(self):
        changed = copy.deepcopy(self.demo)
        changed['entities']['intake'][0]['deleted_at'] = '2026-10-02T12:00:00+02:00'
        self.assertEqual(supplement_exposures(changed, '2026-10-01')['vitamin_b6']['value'], 1.5)

    def test_recipe_cannot_reference_another_owner_food(self):
        changed = copy.deepcopy(self.demo)
        changed['entities']['food'][0]['owner_id'] = self.other_owner(changed)
        self.assertTrue(any('cross-owner food_id' in e for e in validate_dataset(changed, self.schema)))

    def test_meal_plan_cannot_reference_another_owner_recipe(self):
        changed = copy.deepcopy(self.demo)
        owner = self.other_owner(changed)
        changed['entities']['recipe'][0]['owner_id'] = owner
        changed['entities']['food'][0]['owner_id'] = owner
        self.assertTrue(any('cross-owner recipe_id' in e for e in validate_dataset(changed, self.schema)))

    def test_expected_revision_cannot_transfer_ownership(self):
        current = self.demo['entities']['profile'][0]
        incoming = copy.deepcopy(current)
        incoming['owner_id'] = 'c1a1ce35-3e95-440e-a5f8-a20b100e286c'
        with self.assertRaisesRegex(ConflictError, 'ownership'):
            sync_decision(current, incoming, current['revision'])

    def test_canonical_local_day_is_explicit_near_utc_midnight(self):
        changed = copy.deepcopy(self.demo)
        changed['entities']['intake'][0]['taken_at'] = '2026-10-02T00:30:00+02:00'
        # That event belongs to Oct 2 locally, despite being Oct 1 in UTC.
        self.assertEqual(supplement_exposures(changed, '2026-10-02')['vitamin_b6']['value'], 2)
        self.assertEqual(supplement_exposures(changed, '2026-10-01')['vitamin_b6']['value'], 1.5)

    def test_spec_tab_contract_matches_built_adapter(self):
        spec = json.loads((ROOT / 'canonical/spec.json').read_text())
        mapping = json.loads((ROOT / 'adapters/mappings.json').read_text())
        actual = {d['entity']: d['tab'] for d in mapping['definitions']}
        self.assertEqual({k: d['tab'] for k, d in spec['entities'].items()}, actual)

    def test_nonfinite_daily_measurement_is_rejected(self):
        changed = copy.deepcopy(self.demo)
        changed['entities']['daily_observation'][0]['energy_0_10'] = float('nan')
        self.assertTrue(validate_dataset(changed, self.schema))

    def test_nonfinite_biomarker_is_rejected(self):
        changed = copy.deepcopy(self.demo)
        changed['entities']['biomarker'][0]['value'] = float('inf')
        self.assertTrue(validate_dataset(changed, self.schema))

    def test_audit_reference_must_exist(self):
        changed = copy.deepcopy(self.demo)
        changed['entities']['audit_event'][0]['record_id'] = 'c1a1ce35-3e95-440e-a5f8-a20b100e286c'
        self.assertTrue(any('audit record_id' in e for e in validate_dataset(changed, self.schema)))

    def test_audit_reference_retains_type_and_owner(self):
        changed = copy.deepcopy(self.demo)
        changed['entities']['audit_event'][0]['entity_type'] = 'food'
        self.assertTrue(any('declared entity_type' in e for e in validate_dataset(changed, self.schema)))
        changed = copy.deepcopy(self.demo)
        owner = self.other_owner(changed)
        changed['entities']['audit_event'][0]['record_id'] = owner
        self.assertTrue(any('cross-owner audit' in e for e in validate_dataset(changed, self.schema)))

    def test_derived_lineage_must_exist_and_share_owner(self):
        changed = copy.deepcopy(self.demo)
        record = changed['entities']['daily_observation'][0]
        record['provenance']['derived_from'] = ['c1a1ce35-3e95-440e-a5f8-a20b100e286c']
        self.assertTrue(any('dangling provenance' in e for e in validate_dataset(changed, self.schema)))
        record['provenance']['derived_from'] = [self.other_owner(changed)]
        self.assertTrue(any('cross-owner provenance' in e for e in validate_dataset(changed, self.schema)))


if __name__ == '__main__':
    unittest.main()
