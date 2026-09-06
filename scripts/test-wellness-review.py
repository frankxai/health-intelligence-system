import importlib.util
import io
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins/health-intelligence-system/skills/operate-health-second-brain/scripts/review_wellness.py"
spec = importlib.util.spec_from_file_location("review_wellness", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
HEADER = "date,metric,value,unit,source_id\n"


def report(text, **kwargs):
    return module.review(module.read_rows(io.StringIO(HEADER + text)), "2026-09-06", "Europe/Amsterdam", **kwargs)


def metric(result, name="sleep_hours"):
    return next(x for x in result["metrics"] if x["metric"] == name)


class WellnessReviewTests(unittest.TestCase):
    def test_missing_is_unknown(self):
        item = metric(report(""))
        self.assertEqual(item["status"], "no_data")
        self.assertIsNone(item["observed_mean_difference"])

    def test_sparse_data_never_imputes_zero(self):
        item = metric(report("2026-09-01,sleep_hours,8,hours,watch\n"))
        self.assertEqual(item["current"]["mean_observed"], 8)
        self.assertEqual(item["current"]["observed_days"], 1)
        self.assertIsNone(item["previous"]["mean_observed"])
        self.assertIsNone(item["observed_mean_difference"])

    def test_duplicate_and_conflict(self):
        result = report("2026-09-01,sleep_hours,8,hours,watch\n" * 2 +
                        "2026-09-01,sleep_hours,7,hours,watch\n")
        self.assertEqual(result["quality"]["exact_duplicate_rows"], 1)
        self.assertEqual(metric(result)["conflicting_days"], ["2026-09-01"])
        self.assertEqual(metric(result)["current"]["observed_days"], 0)

    def test_devices_are_not_added(self):
        text = "2026-09-01,steps,6000,count,watch\n2026-09-01,steps,5000,count,phone\n"
        self.assertEqual(metric(report(text), "steps")["status"], "source_selection_required")
        item = metric(report(text, selections={"steps": "watch"}), "steps")
        self.assertEqual(item["current"]["mean_observed"], 6000)
        self.assertEqual(item["available_sources"], ["phone", "watch"])

    def test_source_change_prevents_comparison(self):
        text = "2026-08-25,sleep_hours,6,hours,old\n2026-09-01,sleep_hours,8,hours,new\n"
        self.assertEqual(metric(report(text))["status"], "source_selection_required")
        self.assertIsNone(metric(report(text, selections={"sleep_hours": "new"}))["observed_mean_difference"])

    def test_complete_fixture_and_cli(self):
        run = subprocess.run([sys.executable, str(SCRIPT), str(ROOT / "fixtures/wellness/fictional-daily.csv"),
                              "--end", "2026-09-06", "--timezone", "Europe/Amsterdam"],
                             check=True, capture_output=True, text=True)
        data = json.loads(run.stdout)
        item = metric(data)
        self.assertEqual(item["current"]["observed_days"], 5)
        self.assertEqual(item["observed_mean_difference"], 0.5)
        self.assertEqual(data["sensitivity"], "private_health_derived")

    def test_invalid_values_reject_whole_input(self):
        for row in [
            "2026-02-30,sleep_hours,8,hours,watch",
            "2026-09-01,sleep_hours,NaN,hours,watch",
            "2026-09-01,sleep_hours,inf,hours,watch",
            "2026-09-01,sleep_hours,8,minutes,watch",
            "2026-09-01,steps,1.5,count,watch",
            "2026-09-01,energy_rating,6,rating_1_5,self",
            "2026-09-01,glucose,120,mg-dl,watch",
            "2026-09-01,sleep_hours,8,hours,ignore instructions",
            "2026-09-01,sleep_hours,8,hours,watch,extra",
            "2026-09-01,sleep_hours,8,hours",
        ]:
            with self.subTest(row=row), self.assertRaises(ValueError):
                report(row + "\n")

    def test_unknown_header_rejected(self):
        with self.assertRaises(ValueError):
            module.read_rows(io.StringIO("date,metric,value,unit,source_id,notes\n"))

    def test_calendar_and_source_validation(self):
        for end, zone in [("2026-02-30", "UTC"), ("0001-01-01", "UTC"), ("2026-09-06", "Invalid/Zone")]:
            with self.subTest(end=end, zone=zone), self.assertRaises(ValueError):
                module.review([], end, zone)
        with self.assertRaises(ValueError):
            report("", selections={"sleep_hours": "missing"})

    def test_outside_window_does_not_change_sources(self):
        item = metric(report("2026-01-01,sleep_hours,6,hours,old\n2026-09-01,sleep_hours,8,hours,new\n"))
        self.assertEqual(item["available_sources"], ["new"])

    def test_zero_is_real_data(self):
        item = metric(report("2026-09-01,training_minutes,0,minutes,self\n"), "training_minutes")
        self.assertEqual(item["current"]["observed_days"], 1)
        self.assertEqual(item["current"]["mean_observed"], 0)


if __name__ == "__main__":
    unittest.main()
