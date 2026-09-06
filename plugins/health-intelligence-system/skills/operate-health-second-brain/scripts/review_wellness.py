#!/usr/bin/env python3
"""Strict, local-only descriptive analysis of daily wellness aggregates."""
import argparse
import csv
import json
import math
import re
import sys
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

METRICS = {
    "sleep_hours": ("hours", 0, 24, False),
    "steps": ("count", 0, 200000, True),
    "movement_minutes": ("minutes", 0, 1440, False),
    "training_minutes": ("minutes", 0, 1440, False),
    "energy_rating": ("rating_1_5", 1, 5, True),
    "meal_regular_day": ("boolean", 0, 1, True),
}
HEADERS = ["date", "metric", "value", "unit", "source_id"]
MAX_BYTES = 2_000_000
MAX_ROWS = 20_000


def iso_day(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError("Date must use YYYY-MM-DD.")
    return date.fromisoformat(value)


def source_token(value):
    return isinstance(value, str) and re.fullmatch(r"[a-z][a-z0-9-]{0,31}", value) is not None


def read_rows(stream):
    reader = csv.DictReader(stream, strict=True)
    if reader.fieldnames != HEADERS:
        raise ValueError("CSV header must be date,metric,value,unit,source_id in that order.")
    rows = []
    for line, row in enumerate(reader, 2):
        if line > MAX_ROWS + 1:
            raise ValueError("Row limit exceeded.")
        try:
            if set(row) != set(HEADERS) or any(value is None for value in row.values()):
                raise ValueError()
            observed = iso_day(row["date"])
            metric = row["metric"]
            unit, lower, upper, integer = METRICS[metric]
            value = float(row["value"])
            if (row["unit"] != unit or not source_token(row["source_id"])
                    or not math.isfinite(value) or not lower <= value <= upper
                    or (integer and not value.is_integer())):
                raise ValueError()
        except (KeyError, ValueError, TypeError):
            raise ValueError(f"Invalid daily observation at CSV line {line}; no partial report produced.") from None
        rows.append((observed, metric, value, row["source_id"]))
    return rows


def review(rows, end, timezone, selections=None):
    end = iso_day(end)
    if end < date.min + timedelta(days=13):
        raise ValueError("End date does not permit a complete 14-day window.")
    try:
        ZoneInfo(timezone)
    except (ZoneInfoNotFoundError, ValueError, TypeError):
        raise ValueError("Timezone must be a valid IANA name.") from None
    selections = selections or {}
    if any(key not in METRICS or not source_token(value) for key, value in selections.items()):
        raise ValueError("Source selections must use supported metrics and source tokens.")
    first, current_start = end - timedelta(days=13), end - timedelta(days=6)
    grouped = defaultdict(set)
    duplicates = 0
    excluded = 0
    for observed, metric, value, source in rows:
        if not first <= observed <= end:
            excluded += 1
            continue
        key = (metric, source, observed)
        if value in grouped[key]:
            duplicates += 1
        grouped[key].add(value)
    output = []
    for metric, (unit, *_rest) in METRICS.items():
        sources = sorted({source for m, source, _ in grouped if m == metric})
        chosen = selections.get(metric)
        if chosen and chosen not in sources:
            raise ValueError(f"Selected source for {metric} has no observations in the review window.")
        if not chosen and len(sources) == 1:
            chosen = sources[0]
        item = {"metric": metric, "unit": unit, "available_sources": sources,
                "source_id": chosen, "status": "no_data", "conflicting_days": [],
                "previous": None, "current": None, "observed_mean_difference": None}
        if len(sources) > 1 and chosen is None:
            item["status"] = "source_selection_required"
        elif chosen:
            daily = {}
            for (m, source, observed), values in grouped.items():
                if m != metric or source != chosen:
                    continue
                if len(values) != 1:
                    item["conflicting_days"].append(observed.isoformat())
                else:
                    daily[observed] = next(iter(values))
            item["conflicting_days"].sort()
            for label, start, stop in [
                ("previous", first, current_start - timedelta(days=1)),
                ("current", current_start, end),
            ]:
                points = sorted((day, value) for day, value in daily.items() if start <= day <= stop)
                item[label] = {
                    "start": start.isoformat(), "end": stop.isoformat(),
                    "observed_days": len(points), "expected_days": 7,
                    "mean_observed": round(sum(v for _, v in points) / len(points), 3) if points else None,
                    "last_observed": points[-1][0].isoformat() if points else None,
                }
            if all(item[window]["observed_days"] >= 4 for window in ("previous", "current")):
                item["status"] = "descriptive_comparison"
                item["observed_mean_difference"] = round(
                    item["current"]["mean_observed"] - item["previous"]["mean_observed"], 3)
            else:
                item["status"] = "insufficient_coverage"
        output.append(item)
    return {
        "schema_version": "1.0.0", "report_kind": "descriptive_wellness_review",
        "sensitivity": "private_health_derived", "timezone": timezone,
        "date_semantics": "pre-normalized local daily aggregates; sleep uses wake-up day",
        "window": {"start": first.isoformat(), "end": end.isoformat()},
        "quality": {"input_rows": len(rows), "outside_window_rows": excluded,
                    "exact_duplicate_rows": duplicates,
                    "minimum_observed_days_per_window": 4},
        "metrics": output,
        "limits": ["Observed days only; missing data is not zero.",
                   "Four-day coverage is a completeness heuristic, not clinical validation.",
                   "Differences are descriptive, not causal or statistically validated.",
                   "Source authenticity and consent are not established by this report.",
                   "No diagnosis, treatment, readiness score, or medical recommendation."],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--end", required=True)
    parser.add_argument("--timezone", required=True)
    parser.add_argument("--source", action="append", default=[], metavar="METRIC=SOURCE")
    args = parser.parse_args()
    try:
        selections = {}
        for pair in args.source:
            metric, source = pair.split("=", 1)
            if metric in selections:
                raise ValueError("Each metric permits one source selection.")
            selections[metric] = source
        # Bound the actual read, including files that change after opening.
        with args.csv_path.open("rb") as source:
            raw = source.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError("CSV exceeds the two-megabyte limit.")
        import io
        rows = read_rows(io.StringIO(raw.decode("utf-8-sig"), newline=""))
        result = review(rows, args.end, args.timezone, selections)
    except (OSError, UnicodeError, csv.Error):
        print("Input could not be read as a bounded UTF-8 CSV.", file=sys.stderr)
        return 2
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
