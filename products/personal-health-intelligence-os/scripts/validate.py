#!/usr/bin/env python3
"""Validate schema, referential integrity, temporal order and synthetic boundaries."""
import argparse
from datetime import datetime, date
import json
import math
from pathlib import Path
import re
import sys
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from jsonschema import Draft202012Validator, FormatChecker

ROOT=Path(__file__).resolve().parents[1]
FORMAT_CHECKER=FormatChecker()

@FORMAT_CHECKER.checks("date-time")
def explicit_offset_timestamp(value):
    if not isinstance(value,str):return True
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})",value):return False
    try:return datetime.fromisoformat(value.replace("Z","+00:00")).utcoffset() is not None
    except ValueError:return False

RELATIONS = {
 "ingredient":{"product_id":"product"},"intake":{"product_id":"product"},
 "product":{"label_document_id":"clinical_document"},"symptom":{"document_id":"clinical_document"},
 "biomarker":{"document_id":"clinical_document"},"appointment":{"document_id":"clinical_document"},
 "purchase":{"product_id":"product"},
}

def validate_dataset(dataset, schema, require_synthetic=False):
    errors=[]
    def finite_numbers(value, path=()):
        # Python's JSON decoder accepts non-standard NaN/Infinity tokens.
        # JSON Schema bounds do not consistently reject those float values.
        if isinstance(value, float) and not math.isfinite(value):
            errors.append('/'.join(map(str, path))+': non-finite number is not a measurement')
        elif isinstance(value, dict):
            for key, child in value.items(): finite_numbers(child, path+(key,))
        elif isinstance(value, list):
            for index, child in enumerate(value): finite_numbers(child, path+(index,))
    finite_numbers(dataset)
    if errors:
        return errors
    Draft202012Validator.check_schema(schema)
    validator=Draft202012Validator(schema,format_checker=FORMAT_CHECKER)
    for err in sorted(validator.iter_errors(dataset),key=lambda e:str(list(e.path))):
        errors.append("/".join(map(str,err.path))+": "+err.message)
    if errors:
        return errors
    entities=dataset["entities"]
    all_ids=set()
    indexes={key:{r["id"] for r in records} for key,records in entities.items()}
    owners={r["id"]:r["owner_id"] for records in entities.values() for r in records}
    daily_keys=set()
    for entity,records in entities.items():
        for r in records:
            at=f"{entity}/{r['id']}"
            if r["id"] in all_ids: errors.append(at+": duplicate global record ID")
            all_ids.add(r["id"])
            if r["owner_id"] not in indexes["profile"]: errors.append(at+": missing owner profile")
            try: ZoneInfo(r["timezone"])
            except (ZoneInfoNotFoundError,ValueError): errors.append(at+": invalid IANA timezone")
            if datetime.fromisoformat(r["updated_at"].replace("Z","+00:00")) < datetime.fromisoformat(r["created_at"].replace("Z","+00:00")):
                errors.append(at+": updated_at precedes created_at")
            for field,target in RELATIONS.get(entity,{}).items():
                if field in r:
                    if r[field] not in indexes[target]: errors.append(at+": dangling "+field)
                    elif owners[r[field]]!=r["owner_id"]: errors.append(at+": cross-owner "+field)
            for source_id in r['provenance'].get('derived_from', []):
                if source_id not in owners: errors.append(at+': dangling provenance.derived_from')
                elif owners[source_id]!=r['owner_id']: errors.append(at+': cross-owner provenance.derived_from')
            if entity=='audit_event':
                target=r['entity_type']; source_id=r['record_id']
                if target not in indexes or source_id not in indexes[target]:
                    errors.append(at+': audit record_id does not identify the declared entity_type')
                elif owners[source_id]!=r['owner_id']:
                    errors.append(at+': cross-owner audit record_id')
            if entity=="daily_observation":
                key=(r["owner_id"],r["local_date"])
                if key in daily_keys: errors.append(at+": duplicate owner/local_date; resolve source conflict")
                daily_keys.add(key)
            if entity=="recipe":
                for item in r["ingredients"]:
                    if item["food_id"] not in indexes["food"]: errors.append(at+": dangling food_id")
                    elif owners[item["food_id"]]!=r["owner_id"]: errors.append(at+": cross-owner food_id")
            if entity=="meal_plan":
                for item in r["items"]:
                    if item["recipe_id"] not in indexes["recipe"]: errors.append(at+": dangling recipe_id")
                    elif owners[item["recipe_id"]]!=r["owner_id"]: errors.append(at+": cross-owner recipe_id")
            if entity=="sleep":
                start=datetime.fromisoformat(r["start_at"].replace("Z","+00:00"))
                end=datetime.fromisoformat(r["end_at"].replace("Z","+00:00"))
                if end<=start: errors.append(at+": sleep end must follow start")
                elif abs((end-start).total_seconds()/3600-r["duration_h"])>0.02:
                    errors.append(at+": duration_h disagrees with timestamp interval")
            if entity in ("review","experiment"):
                start=r.get("period_start",r.get("start_date")); end=r.get("period_end",r.get("end_date"))
                if date.fromisoformat(start)>date.fromisoformat(end): errors.append(at+": reversed period")
            if entity=="biomarker" and "reference_low" in r and "reference_high" in r and r["reference_low"]>r["reference_high"]:
                errors.append(at+": reference interval reversed")
            if require_synthetic and r["provenance"]["kind"]!="synthetic": errors.append(at+": commercial example must be synthetic")
    if require_synthetic and not dataset["synthetic"]: errors.append("Dataset synthetic flag is false")
    if require_synthetic:
        raw=json.dumps(dataset)
        if re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}",raw): errors.append("Synthetic package contains an email address")
        if re.search(r"(?:sk-[A-Za-z0-9]{16,}|gh[pousr]_[A-Za-z0-9]{20,})",raw): errors.append("Possible secret in synthetic dataset")
    return errors

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("dataset",nargs="?",default=str(ROOT/"synthetic/demo.json"))
    parser.add_argument("--require-synthetic",action="store_true")
    args=parser.parse_args()
    schema=json.loads((ROOT/"canonical/schema.json").read_text())
    dataset=json.loads(Path(args.dataset).read_text())
    errors=validate_dataset(dataset,schema,args.require_synthetic)
    if errors:
        print("\n".join(errors)); return 1
    print(json.dumps({"status":"pass","schema_version":dataset["schema_version"],"synthetic":dataset["synthetic"],"entity_types":len(dataset["entities"]),"records":sum(map(len,dataset["entities"].values()))}))
    return 0

if __name__=="__main__": sys.exit(main())
