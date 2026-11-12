"""Pure, offline record operations. No network, credentials or workspace writes."""
from copy import deepcopy
from datetime import datetime
from decimal import Decimal
import hashlib
import json
import uuid
from zoneinfo import ZoneInfo

VOLATILE = {"updated_at", "revision"}

class ConflictError(ValueError):
    pass

def content_hash(record):
    """Hash the logical record; revision/update time do not alter its identity."""
    logical = {k:v for k,v in record.items() if k not in VOLATILE}
    return hashlib.sha256(json.dumps(logical, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

def imported_id(source_namespace, entity_type, source_record_id):
    """Stable ID from a customer namespace and an upstream identity, never value order."""
    namespace = uuid.UUID(source_namespace)
    return str(uuid.uuid5(namespace, entity_type + "\0" + str(source_record_id)))

def notion_record_id(record_id, native_page_id):
    """Manual Notion entry can use the already stable native page UUID on export."""
    return str(uuid.UUID(record_id if record_id else native_page_id))

def sync_decision(current, incoming, expected_revision):
    """Optimistic, one-direction projection decision. No last-write-wins shortcut."""
    if current is None:
        if expected_revision not in (0, None):
            raise ConflictError("Creation expected an existing revision")
        return "create"
    if current["id"] != incoming["id"]:
        raise ConflictError("Record identities differ")
    if current["owner_id"] != incoming["owner_id"]:
        raise ConflictError("Record ownership cannot change during projection or import")
    if content_hash(current) == content_hash(incoming):
        return "unchanged"
    if current.get("deleted_at") and not incoming.get("deleted_at"):
        raise ConflictError("A stale projection cannot resurrect a tombstone")
    if expected_revision != current["revision"]:
        raise ConflictError("Stale revision: keep current and incoming for human resolution")
    return "tombstone" if incoming.get("deleted_at") else "update"

def merge_import(dataset, incoming, expected_revisions=None):
    """Dry-run merge returning a new dataset and receipts; conflicts never overwrite."""
    result = deepcopy(dataset)
    receipts = []
    expected_revisions = expected_revisions or {}
    for entity, records in incoming["entities"].items():
        target = result["entities"][entity]
        by_id = {r["id"]:(i,r) for i,r in enumerate(target)}
        for record in records:
            pair = by_id.get(record["id"])
            current = pair[1] if pair else None
            try:
                decision = sync_decision(current, record, expected_revisions.get(record["id"], 0))
            except ConflictError as exc:
                receipts.append({"entity":entity,"id":record["id"],"outcome":"conflict","reason":str(exc),"current":current,"incoming":record})
                continue
            new = deepcopy(record)
            if decision in ("update","tombstone"):
                new["revision"] = current["revision"] + 1
                target[pair[0]] = new
                by_id[new["id"]] = (pair[0], new)
            elif decision == "create":
                target.append(new)
                by_id[new["id"]] = (len(target)-1,new)
            receipts.append({"entity":entity,"id":record["id"],"outcome":decision,"before_hash":content_hash(current) if current else None,"after_hash":content_hash(new)})
    return result, receipts

def supplement_exposures(dataset, local_date):
    """Aggregate taken, label-based exposure; no safety or clinical recommendation."""
    entities = dataset["entities"]
    products = {r["id"]:r for r in entities["product"]}
    factors = {"mg":Decimal("1"),"g":Decimal("1000"),"mcg":Decimal("0.001")}
    totals = {}
    for intake in entities["intake"]:
        if intake.get("event_status") != "taken" or intake.get("deleted_at"):
            continue
        day = datetime.fromisoformat(intake["taken_at"].replace("Z","+00:00")).astimezone(ZoneInfo(intake["timezone"])).date().isoformat()
        if day != local_date:
            continue
        product = products[intake["product_id"]]
        if product.get("deleted_at"):
            raise ValueError("Cannot report exposure for a deleted product record")
        if not product["label_verified"]:
            raise ValueError("Cannot report verified exposure from an unverified product label")
        for ingredient in entities["ingredient"]:
            if ingredient["product_id"] != product["id"] or ingredient.get("deleted_at"):
                continue
            if ingredient.get("label_verified") is not True:
                raise ValueError("Ingredient label basis is unverified")
            unit = ingredient["unit"]
            if unit not in factors:
                raise ValueError("Unsupported arithmetic unit: retain source unit and review manually")
            key = ingredient["ingredient_name"]
            totals[key] = totals.get(key,Decimal(0)) + Decimal(str(ingredient["amount_per_serving"])) * Decimal(str(intake["servings"])) * factors[unit]
    return {name:{"value":float(value),"unit":"mg","interpretation":"arithmetic only"} for name,value in sorted(totals.items())}
