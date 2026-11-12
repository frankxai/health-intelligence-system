#!/usr/bin/env python3
"""Build the canonical, synthetic-only product specification and schemas."""
import json
import uuid
from pathlib import Path
from datetime import date, timedelta

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.1.0"
NS = uuid.UUID("6c9126f3-fce4-57bb-ae82-9d38ac63e112")

def uid(name):
    return str(uuid.uuid5(NS, name))

def text(description="", enum=None):
    value = {"type": "string"}
    if description: value["description"] = description
    if enum: value["enum"] = enum
    return value

def number(unit, minimum=None, maximum=None):
    value = {"type": "number", "description": "Unit: " + unit}
    if minimum is not None: value["minimum"] = minimum
    if maximum is not None: value["maximum"] = maximum
    return value

def ref(entity, description=""):
    return {"type": "string", "format": "uuid", "description": description or f"Foreign key to {entity}.id"}

def obj(properties, required=()):
    return {"type":"object", "properties":properties, "required":list(required), "additionalProperties":False}

def arr(items): return {"type":"array", "items":items}
DATE = {"type":"string", "format":"date"}
TIME = {"type":"string", "format":"date-time"}
BOOL = {"type":"boolean"}
UNIT = {"type":"string","minLength":1,"maxLength":64,"description":"Exact source unit. Prefer UCUM where unambiguous. Arithmetic adapters whitelist supported conversions; unfamiliar units remain unchanged."}
provenance = obj({
    "kind": text(enum=["observed", "reported", "hypothesis", "evidence", "synthetic"]),
    "source": text("Source URI, filename, device or explicit user report; never a credential"),
    "confidence":text(enum=["low", "moderate", "high"]),
    "source_record_id":text("Stable upstream record identifier when known"),
    "source_hash":text("SHA-256 of source bytes when available"),
    "derived_from":arr(ref("any entity")),
    "method":text("Transformation or collection method"),
}, ["kind", "source", "confidence"])
access = obj({
    "classification":text(enum=["restricted-health"]),
    "readers":arr(text("Owner-controlled principal identifier")),
    "writers":arr(text("Owner-controlled principal identifier")),
    "ai_allowed":BOOL,
}, ["classification", "readers", "writers", "ai_allowed"])
COMMON = {
    "id":ref("this record", "Stable UUID independent of platform row or page IDs"),
    "schema_version":{"const":VERSION},
    "owner_id":ref("profile", "Pseudonymous owner UUID; not email or full name"),
    "created_at":TIME, "updated_at":TIME,
    "timezone":text("IANA timezone identifier, e.g. Europe/Amsterdam"),
    "revision":{"type":"integer", "minimum":1},
    "provenance":provenance, "access":access,
    "deleted_at":TIME,
}
COMMON_REQUIRED = [k for k in COMMON if k != "deleted_at"]

DOMAINS = {
 "profile": {
  "sheet":"Profile", "required":["display_name", "goals"],
  "fields":{
   "display_name":text("Optional pseudonym. Legal name is unnecessary."),
   "goals":arr(obj({"name":text(),"metric":text(),"target":number("metric-dependent"),"unit":UNIT,"review_date":DATE},["name"])),
   "priorities":arr(text()), "birth_year":{"type":"integer","minimum":1900,"maximum":2100},
   "height_cm":number("cm",30,260), "notes":text(),
  }},
 "daily_observation": {
  "sheet":"Daily", "required":["local_date"],
  "fields":{
   "local_date":DATE, "sleep_hours":number("h",0,24),
   "energy_0_10":number("0 to 10 subjective scale",0,10),"focus_0_10":number("0 to 10 subjective scale",0,10),
   "mood_0_10":number("0 to 10 subjective scale",0,10),"stress_0_10":number("0 to 10 subjective scale",0,10),
   "fluid_ml":number("mL",0,20000),"caffeine_mg":number("mg",0,3000),
   "protein_g":number("g",0,1000),"fiber_g":number("g",0,200),
   "sodium_mg":number("mg",0,30000),"calcium_mg":number("mg",0,10000),
   "training_minutes":number("min",0,1440),"pain_0_10":number("0 to 10 subjective scale",0,10),
   "pain_location":text(), "bristol_1_7":{"type":"integer","minimum":1,"maximum":7},
   "summary_mode":text(enum=["manual_summary","event_projection"]),"notes":text(),
  }},
 "product": {
  "sheet":"Supplements", "required":["name","category","label_verified"],
  "fields":{
   "name":text(), "category":text(enum=["supplement","medication"]), "brand":text(),
   "serving_label":text("Label serving description; not a recommendation"),
   "label_verified":BOOL, "label_document_id":ref("clinical_document"),
   "status":text(enum=["inventory","active","paused","archived"]),
   "prescriber_notes":text("Reported prescription instructions; agents cannot change them"),
   "notes":text(),
  }},
 "ingredient": {
  "sheet":"Ingredients", "required":["product_id","ingredient_name","amount_per_serving","unit"],
  "fields":{
   "product_id":ref("product"), "ingredient_name":text("Normalized ingredient name"),
   "amount_per_serving":number("specified by unit",0), "unit":UNIT,
   "form":text("Chemical form from product label"), "label_basis":text("Exact serving on label"),
   "label_verified":BOOL, "notes":text(),
  }},
 "intake": {
  "sheet":"Intakes", "required":["product_id","taken_at","servings"],
  "fields":{
   "product_id":ref("product"), "taken_at":TIME, "servings":number("label servings",0,100),
   "event_status":text(enum=["taken","planned","skipped"]),
   "adverse_event":text(), "notes":text(),
  }},
 "food": {
  "sheet":"Foods", "required":["name","basis_g"],
  "fields":{
   "name":text(), "basis_g":number("g",0.001,10000), "energy_kcal":number("kcal",0),
   "protein_g":number("g",0), "fiber_g":number("g",0),"sodium_mg":number("mg",0),
   "calcium_mg":number("mg",0), "allergens":arr(text()), "source_url":text(),"notes":text(),
  }},
 "recipe": {
  "sheet":"Recipes", "required":["name","servings","ingredients"],
  "fields":{
   "name":text(),"servings":number("servings",0.01,1000),
   "ingredients":arr(obj({"food_id":ref("food"),"quantity_g":number("g",0.001)},["food_id","quantity_g"])),
   "instructions":text(),"notes":text(),
  }},
 "meal_plan": {
  "sheet":"Meal Plans", "required":["name","local_date","items"],
  "fields":{
   "name":text(),"local_date":DATE,
   "items":arr(obj({"recipe_id":ref("recipe"),"meal":text(enum=["breakfast","lunch","dinner","snack"]),"servings":number("servings",0.01)},["recipe_id","meal","servings"])),
   "notes":text(),
  }},
 "hydration": {
  "sheet":"Hydration", "required":["observed_at","volume_ml","drink"],
  "fields":{
   "observed_at":TIME,"volume_ml":number("mL",0,10000),"drink":text(),
   "sodium_mg":number("mg",0),"potassium_mg":number("mg",0),
   "measurement_type":text(enum=["measured","estimated"]), "notes":text(),
  }},
 "sleep": {
  "sheet":"Sleep", "required":["start_at","end_at","duration_h","source_type"],
  "fields":{
   "start_at":TIME,"end_at":TIME,"duration_h":number("h",0,24),
   "source_type":text(enum=["self_report","wearable"]),"quality_0_10":number("0 to 10 subjective scale",0,10),
   "is_nap":BOOL,"notes":text(),
  }},
 "training": {
  "sheet":"Training", "required":["start_at","activity","duration_min"],
  "fields":{
   "start_at":TIME,"activity":text(enum=["strength","cardio","walking","mobility","other"]),
   "duration_min":number("min",0,1440), "rpe_1_10":number("rating of perceived exertion",1,10),
   "distance_km":number("km",0),
   "sets":arr(obj({"exercise":text(),"reps":{"type":"integer","minimum":0},"load_kg":number("kg",0)},["exercise","reps"])),
   "notes":text(),
  }},
 "recovery": {
  "sheet":"Recovery", "required":["observed_at","kind"],
  "fields":{
   "observed_at":TIME,"kind":text(enum=["stress","wellbeing","recovery_practice"]),
   "score_0_10":number("0 to 10 subjective scale",0,10),"practice":text(),
   "duration_min":number("min",0,1440),"notes":text(),
  }},
 "symptom": {
  "sheet":"Symptoms", "required":["name","onset_at","body_zone","status"],
  "fields":{
   "name":text(),"onset_at":TIME,"resolved_at":TIME,"body_zone":text(),
   "severity_0_10":number("0 to 10 subjective scale",0,10),
   "status":text(enum=["reported_symptom","reported_condition","clinician_documented_condition"]),
   "trigger_hypothesis":text(),"what_helped_report":text(),"red_flags_reported":arr(text()),
   "document_id":ref("clinical_document"),"notes":text(),
  }},
 "biomarker": {
  "sheet":"Biomarkers", "required":["name","sample_at","value","unit"],
  "fields":{
   "name":text(),"sample_at":TIME,"value":number("specified by unit"),"unit":UNIT,
   "reference_low":number("same unit as value"),"reference_high":number("same unit as value"),
   "laboratory":text("Optional pseudonymous laboratory identifier"),"loinc_code":text(),
   "document_id":ref("clinical_document"),"notes":text(),
  }},
 "clinical_document": {
  "sheet":"Documents", "required":["name","document_type","document_date","storage_uri"],
  "fields":{
   "name":text(),"document_type":text(enum=["lab_report","clinical_note","prescription","product_label","other"]),
   "document_date":DATE,"storage_uri":text("Owner-controlled private URI; never a public health-data URL"),
   "sha256":{"type":"string","pattern":"^[a-f0-9]{64}$"},"notes":text(),
  }},
 "appointment": {
  "sheet":"Appointments", "required":["name","starts_at","status"],
  "fields":{
   "name":text(),"starts_at":TIME,"status":text(enum=["planned","completed","cancelled"]),
   "preparation":text(),"document_id":ref("clinical_document"),"notes":text(),
  }},
 "experiment": {
  "sheet":"Experiments", "required":["name","hypothesis","start_date","end_date","primary_outcome","stop_rule","status"],
  "fields":{
   "name":text(),"hypothesis":text(),"start_date":DATE,"end_date":DATE,
   "baseline_start":DATE,"baseline_end":DATE,"primary_outcome":text(),
   "intervention":text(),"confounders":arr(text()),"stop_rule":text(),
   "status":text(enum=["planned","baseline","active","stopped","reviewed"]),
   "result_summary":text(),"causal_claim_allowed":{"const":False},"notes":text(),
  }},
 "evidence": {
  "sheet":"Evidence", "required":["title","url","accessed_date","evidence_type","claim"],
  "fields":{
   "title":text(),"url":{"type":"string","format":"uri"},"accessed_date":DATE,
   "evidence_type":text(enum=["guideline","systematic_review","trial","observational","mechanistic","product_label","platform_documentation","other"]),
   "claim":text(),"population":text(),"limitations":text(),"strength":text(enum=["ungraded","low","moderate","high"]),
   "doi":text(),"notes":text(),
  }},
 "purchase": {
  "sheet":"Purchases", "required":["name","purchased_date","quantity","cost","currency"],
  "fields":{
   "name":text(),"product_id":ref("product"),"purchased_date":DATE,"quantity":number("items",0),
   "cost":number("currency units",0),"currency":text(enum=["EUR","USD","GBP"]),
   "servings_remaining":number("label servings",0),"expiry_date":DATE,"notes":text(),
  }},
 "review": {
  "sheet":"Reviews", "required":["name","cadence","period_start","period_end","summary","next_action"],
  "fields":{
   "name":text(),"cadence":text(enum=["weekly","monthly","quarterly"]),"period_start":DATE,"period_end":DATE,
   "summary":text(),"missingness_notes":text(),"confounders":arr(text()),
   "next_action":text(),"decision_owner":text(),"notes":text(),
  }},
 "consent": {
  "sheet":"Consent", "required":["name","principal","scope","status","granted_at"],
  "fields":{
   "name":text(),"principal":text(),"scope":arr(text()),"status":text(enum=["granted","revoked","expired"]),
   "granted_at":TIME,"expires_at":TIME,"revoked_at":TIME,
   "provider":text(),"purpose":text(),"notes":text(),
  }},
 "audit_event": {
  "sheet":"Audit", "required":["occurred_at","actor","operation","entity_type","record_id","outcome"],
  "fields":{
   "occurred_at":TIME,"actor":text(),"operation":text(enum=["create","update","delete","import","export","grant","revoke","sync_propose","sync_apply"]),
   "entity_type":text(),"record_id":ref("any entity"),"outcome":text(enum=["applied","proposed","rejected","conflict"]),
   "expected_revision":{"type":"integer","minimum":0},"result_revision":{"type":"integer","minimum":1},
   "before_hash":text(),"after_hash":text(),"receipt":text(),"notes":text(),
  }},
}

definitions = {}
for entity, definition in DOMAINS.items():
    definitions[entity] = obj({**COMMON, **definition["fields"]}, COMMON_REQUIRED + definition["required"])
schema = {
 "$schema":"https://json-schema.org/draft/2020-12/schema",
 "$id":"https://example.invalid/personal-health-intelligence-os/0.1.0/schema.json",
 "title":"Personal Health Intelligence OS interchange dataset",
 "description":"Owner-controlled health records. The URL is an identifier, not a network dependency.",
 "type":"object", "additionalProperties":False,
 "required":["schema_version","synthetic","entities"],
 "properties":{
  "schema_version":{"const":VERSION},"synthetic":BOOL,
  "entities":obj({entity:arr({"$ref":f"#/$defs/{entity}"}) for entity in DOMAINS}, list(DOMAINS)),
 }, "$defs":definitions,
}

spec = {
 "product":"Personal Health Intelligence OS", "version":VERSION,"stage":"1-template-release-candidate",
 "intended_use":"Personal record keeping, educational context, preparation and bounded self-observation. No diagnosis, treatment selection or automated prescribing.",
 "canonical_source":"canonical/spec.json and canonical/schema.json",
 "identity":{"record_id":"UUID v4 for user entry; UUID v5 for deterministic import using source namespace + source record ID. Native Notion page UUID is the stable fallback when a manual row has no explicit Record ID; preserve it on export and subsequent updates.","owner_id":"pseudonymous UUID, never customer email","schema_version":VERSION,"revision":"positive integer optimistic concurrency token"},
 "timestamp_policy":{"storage":"Canonical JSON uses ISO 8601 with explicit offset or Z","display":"Canonical local-day analysis uses the record IANA timezone. The Google template stores and displays timestamp cells as UTC serial values; date-only cells are local calendar dates.","day_key":"local_date in owner timezone; the Google Exposure calculator explicitly selects a UTC day, not a local-day total","dst":"never infer a repeated local clock time without offset"},
 "missingness":"Omit unknown optional fields. Numeric zero is a reported zero. Do not fill gaps, interpolate or fabricate observations.",
 "daily_projection_policy":"manual_summary and event_projection are mutually exclusive per owner/local_date/metric. Event detail wins only when the owner explicitly selects event_projection; preserve manual history and derived_from IDs. Never add a daily aggregate to its events.",
 "confidence":"Confidence qualifies source reliability, not a probability of diagnosis. Research evidence strength is separate.",
 "editions":{
  "google":{"canonical_records":"Google Sheets","documents":"Google Drive","reviews":"Google Sheets","ai":"manual portable instructions plus assistant-specific connection"},
  "notion":{"canonical_records":"Notion databases","documents":"private Notion attachment or owner storage URI","reviews":"Notion","ai":"manual portable instructions plus supported Notion connection"},
  "complete":{"canonical_records":"Google Sheets","documents":"Google Drive","reviews":"Notion","notion_projection":"read-only data projection; Notion review/decision entities are canonical there","sync_stage":"2; no background sync shipped in Stage 1"},
 },
 "complete_ownership":{entity:("Notion" if entity=="review" else "Google Sheets") for entity in DOMAINS},
 "sync":{"direction":"one canonical owner per entity to projections","identity":"id, schema_version, revision, content_hash","conflicts":"reject stale revisions; preserve both candidate and current record in conflict queue; human resolution","audit":"append receipt with before/after hash and actor; do not store provider secrets","deletion":"explicit tombstone; projections remove after confirmed owner deletion; never resurrect from stale snapshots","transport":"customer-controlled connector; no seller data transit required","idempotency":"source_namespace + source_record_id + canonical content hash","automatic_sync_implemented":False},
 "privacy":{"default":"private, no public shares, AI access false","analytics":"only opt-in installation metadata without record IDs, symptoms, measurements or document titles","support":"synthetic reproduction preferred; time-bounded consent for scoped access; revoke after handover","retention":"owner controls records; product seller holds no customer health data by default","deletion":"export, confirm scope, revoke integrations, delete owner-selected records and retained copies; disclose vendor backup schedules"},
 "upgrade":{"policy":"additive schemas by default, snapshot export first, migration dry-run, preserve IDs/rows and private data, explicit review for destructive changes","compatibility":"0.1.x patches must not silently alter required fields or units"},
 "entities":{entity:{"tab":d["sheet"],"required_payload_fields":d["required"],"fields":list(d["fields"]),"google_mapping":"Native workbook headers are human-readable labels mapped by adapters/mappings.json. Supplied CSV headers use canonical snake_case names. Nested arrays and objects remain JSON text cells; no nested child-table CSV exporter is implemented.","notion_mapping":"Human-readable properties use adapters/mappings.json. Top-level foreign keys use native relations into the duplicated local databases; nested arrays remain JSON rich-text. Platform page IDs are adapter metadata unless adopted as a missing Record ID fallback.","fhir_candidate":{
  "profile":"Patient (minimal pseudonymous mapping)","daily_observation":"Observation","product":"Medication only where medication semantics apply; no forced mapping for everyday supplement catalogs","ingredient":"Medication.ingredient only for a mapped Medication","intake":"MedicationStatement for reported medication intake; not a prescription","food":"No forced R4 mapping; retain food composition table","hydration":"Observation","sleep":"Observation","training":"Observation","recovery":"Observation","symptom":"Observation or documented Condition","biomarker":"Observation + DiagnosticReport","clinical_document":"DocumentReference","appointment":"Appointment","experiment":"No ResearchStudy mapping without a separate research workflow","evidence":"DocumentReference for source documents; no claim of an R4 Citation resource","review":"Composition only with a specified clinical document profile","consent":"Consent","audit_event":"AuditEvent"}.get(entity,"No required FHIR mapping") } for entity,d in DOMAINS.items()},
 "fhir":{"version":"R4 conceptual mappings only","status":"No FHIR exporter, validation or clinical interoperability certification claimed","units":"UCUM candidates retain source unit; no IU/mass conversion without ingredient-specific factors","codes":"optional LOINC codes must come from actual source; never infer clinical codes from everyday labels"},
 "onboarding_target":{"first_check_in_minutes":10,"measurement":"unverified target until an independent customer trial completes","minimum_fields":["local_date"],"recommended_first_entry":["local_date","sleep_hours","energy_0_10","notes"],"optional_rule":"Unknown measurements stay blank. No measurement is mandatory merely to complete setup."},
 "prices_hypotheses_eur":{"google":29,"notion":39,"complete":79,"premium_setup_min":149,"premium_setup_max":299},
 "release_gates":["fresh-account installation proof","synthetic-only template inspection","formula recalculation and readback","Notion relation remap after duplication","customer export/delete rehearsal","supported assistant read/propose/write demonstration","checkout and delivery rehearsal","merchant legal/tax/health-claims review"],
}

def base(entity, name):
    return {"id":uid(entity+":"+name),"schema_version":VERSION,"owner_id":uid("profile:sample"),
      "created_at":"2026-10-01T12:00:00+02:00","updated_at":"2026-10-01T12:00:00+02:00", "timezone":"Europe/Amsterdam","revision":1,
      "provenance":{"kind":"synthetic","source":"synthetic-demo-generator","confidence":"high"},
      "access":{"classification":"restricted-health","readers":[],"writers":[],"ai_allowed":False}}

demo={"schema_version":VERSION,"synthetic":True,"entities":{entity:[] for entity in DOMAINS}}
def add(entity, key, **payload):
    r={**base(entity,key),**payload}; demo["entities"][entity].append(r); return r

profile=add("profile","sample",display_name="Sample Profile",goals=[{"name":"Observe sleep consistency","metric":"sleep_hours","review_date":"2026-10-15"}],priorities=["Sleep regularity","Consistent daily capture"],notes="SYNTHETIC DEMO. No individual health record or recommended targets.")
for i in range(14):
    d=(date(2026,10,1)+timedelta(days=i)).isoformat()
    add("daily_observation",d,local_date=d,sleep_hours=round([7.0,7.5,6.5,8,7.5,7,8.0][i%7],1),energy_0_10=[6,7,5,8,7,6,8][i%7],focus_0_10=[6,7,5,7,8,6,8][i%7],mood_0_10=7,stress_0_10=[4,3,6,2,3,5,2][i%7],fluid_ml=[1900,2100,1800,2300,2200,2000,2400][i%7],caffeine_mg=[80,80,120,0,80,80,0][i%7],protein_g=100+i%3*10,fiber_g=24+i%4*2,training_minutes=30 if i%2 else 0,summary_mode="manual_summary",notes="Synthetic scenario; fluid volume is an observation, not an intake target.")

label=add("clinical_document","sample-label",name="Synthetic label for arithmetic demo",document_type="product_label",document_date="2026-10-01",storage_uri="demo://labels/sample-label",notes="Fictional label values. No actual product or manufacturer.")
p1=add("product","sample-a",name="Sample Product A",category="supplement",brand="Fictional Demo",serving_label="1 demonstration unit",label_verified=True,label_document_id=label["id"],status="inventory",notes="Synthetic arithmetic example. Not a dosing instruction.")
p2=add("product","sample-b",name="Sample Product B",category="supplement",brand="Fictional Demo",serving_label="1 demonstration unit",label_verified=True,label_document_id=label["id"],status="inventory",notes="Synthetic arithmetic example. Not a dosing instruction.")
add("ingredient","sample-a-b6",product_id=p1["id"],ingredient_name="vitamin_b6",amount_per_serving=2,unit="mg",label_basis="per demonstration unit",label_verified=True,notes="Fictional amount.")
add("ingredient","sample-b-b6",product_id=p2["id"],ingredient_name="vitamin_b6",amount_per_serving=1.5,unit="mg",label_basis="per demonstration unit",label_verified=True,notes="Fictional amount.")
add("intake","sample-a-day1",product_id=p1["id"],taken_at="2026-10-01T09:00:00+02:00",servings=1,event_status="taken",notes="Synthetic event. Does not recommend use.")
add("intake","sample-b-day1",product_id=p2["id"],taken_at="2026-10-01T09:30:00+02:00",servings=1,event_status="taken",notes="Combined B6 arithmetic = 3.5 mg for this fictional day. No clinical threshold judgement.")
food=add("food","sample-oats",name="Sample oats",basis_g=100,energy_kcal=380,protein_g=13,fiber_g=10,sodium_mg=5,calcium_mg=50,allergens=["Check gluten cross-contact on actual label"],notes="Illustrative composition only; replace with verified label or recognized database.")
recipe=add("recipe","sample-porridge",name="Sample porridge",servings=1,ingredients=[{"food_id":food["id"],"quantity_g":50}],instructions="Prepare following the actual food package instructions.",notes="Illustrative recipe. Water omitted from nutritional ingredients.")
add("meal_plan","sample-breakfast",name="Sample breakfast plan",local_date="2026-10-01",items=[{"recipe_id":recipe["id"],"meal":"breakfast","servings":1}],notes="An optional plan, not a record of consumption.")
add("hydration","sample-water",observed_at="2026-10-01T09:00:00+02:00",volume_ml=250,drink="Water",measurement_type="estimated",notes="Illustrative detail only; daily summary remains manual and must not be added to this event.")
add("sleep","sample-night",start_at="2026-09-30T23:00:00+02:00",end_at="2026-10-01T06:00:00+02:00",duration_h=7,source_type="self_report",quality_0_10=7,is_nap=False,notes="Synthetic detail aligned to the daily summary; not an additional sleep record to total.")
add("training","sample-walk",start_at="2026-10-02T12:00:00+02:00",activity="walking",duration_min=30,rpe_1_10=3,distance_km=2,notes="Synthetic session.")
add("recovery","sample-pause",observed_at="2026-10-01T15:00:00+02:00",kind="recovery_practice",practice="Quiet pause",duration_min=5,score_0_10=6,notes="Synthetic self-report.")
add("symptom","sample-stiffness",name="Sample shoulder stiffness",onset_at="2026-10-02T15:00:00+02:00",body_zone="shoulder",severity_0_10=2,status="reported_symptom",trigger_hypothesis="Long desk session",what_helped_report="Movement break",red_flags_reported=[],notes="Synthetic symptom; association is not diagnosis.")
lab=add("clinical_document","sample-lab",name="Synthetic laboratory report",document_type="lab_report",document_date="2026-10-01",storage_uri="demo://reports/sample-lab",notes="No real test or person.")
add("biomarker","sample-marker",name="Example marker",sample_at="2026-10-01T08:00:00+02:00",value=42,unit="ng/mL",reference_low=20,reference_high=80,document_id=lab["id"],laboratory="Fictional Demo Lab",notes="Arbitrary demonstration values. Reference range is fictional and not clinical guidance.")
add("appointment","sample-review",name="Sample records review",starts_at="2026-10-20T10:00:00+02:00",status="planned",preparation="Bring questions and owner-selected records.",notes="Synthetic appointment, not a real booking.")
add("experiment","sample-break",name="Scheduled movement break",hypothesis="A scheduled movement break may coincide with lower afternoon stiffness.",baseline_start="2026-10-01",baseline_end="2026-10-07",start_date="2026-10-08",end_date="2026-10-14",primary_outcome="Self-reported afternoon stiffness 0–10",intervention="One scheduled movement break during desk work",confounders=["Work duration","Training","Sleep"],stop_rule="Stop the experiment for worsening symptoms or unexpected effects.",status="planned",causal_claim_allowed=False,notes="Synthetic low-risk behavioral observation; no efficacy conclusion.")
add("evidence","schema-source",title="HL7 FHIR R4 Observation resource",url="https://hl7.org/fhir/R4/observation.html",accessed_date="2026-11-12",evidence_type="platform_documentation",claim="Observation is a candidate mapping for measurements; the product does not implement a validated FHIR exporter.",strength="ungraded",limitations="Mapping reference only.",notes="Source URL for interoperability design, not a medical recommendation.")
add("purchase","sample-purchase",name="Sample Product A purchase",product_id=p1["id"],purchased_date="2026-10-01",quantity=1,cost=12,currency="EUR",servings_remaining=29,expiry_date="2027-10-01",notes="Fictional price and inventory.")
add("review","sample-week",name="Sample weekly review",cadence="weekly",period_start="2026-10-01",period_end="2026-10-07",summary="Synthetic example: sleep and energy vary across the week; no causal conclusion.",missingness_notes="Daily records contain a limited subset of optional measures.",confounders=["Caffeine","Workload","Training"],next_action="Choose a consistent capture time for the next week.",decision_owner="Sample Profile",notes="A sample review, not a personalized conclusion.")
add("consent","sample-local-only",name="Sample local record access",principal="owner",scope=["read","write"],status="granted",granted_at="2026-10-01T12:00:00+02:00",provider="owner workspace",purpose="Personal record keeping",notes="AI sharing stays disabled. Example only, not actual consent.")
add("audit_event","sample-create",occurred_at="2026-10-01T12:00:00+02:00",actor="synthetic-demo-generator",operation="create",entity_type="profile",record_id=profile["id"],outcome="applied",result_revision=1,receipt="demo-receipt-001",notes="Synthetic audit example. Platform history is not an immutable clinical audit log.")

for path,value in [(ROOT/"canonical/schema.json",schema),(ROOT/"canonical/spec.json",spec),(ROOT/"synthetic/demo.json",demo),(ROOT/"synthetic/blank.json",{"schema_version":VERSION,"synthetic":False,"entities":{entity:[] for entity in DOMAINS}})]:
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+"\n")

dictionary=["# Data dictionary", "", f"Canonical schema version {VERSION}. Generated from `canonical/schema.json`; field names and types are authoritative there.", "", "## Shared record envelope", "", "Every entity carries the following fields. These are explicit export fields; native adapters may show only the fields needed for daily use. Metadata defaults must come from the known owner, native creation/edit timestamps and explicit source context, never inferred measurements.", "", "| Field | Type | Required | Validation and meaning |", "| --- | --- | --- | --- |"]
def describe(field):
    values=[]
    if "description" in field:values.append(field["description"])
    if "format" in field:values.append("Format: "+field["format"])
    if "enum" in field:values.append("Allowed: "+", ".join(map(str,field["enum"])))
    if "const" in field:values.append("Fixed: "+str(field["const"]))
    if "minimum" in field:values.append("Minimum: "+str(field["minimum"]))
    if "maximum" in field:values.append("Maximum: "+str(field["maximum"]))
    if "pattern" in field:values.append("Pattern: `"+field["pattern"]+"`")
    if field.get("type")=="object":values.append("Members: "+", ".join(field["properties"]))
    if field.get("type")=="array":
        item=field["items"]
        if item.get("type")=="object":values.append("Item members: "+", ".join(item["properties"]))
        else:values.append("Items: "+item.get("type","record"))
    return "; ".join(values).replace("|","\\|") or "Source-preserving value"
def field_type(field):return field.get("type","boolean" if isinstance(field.get("const"),bool) else "string")
for name,field in COMMON.items():dictionary.append(f"| `{name}` | {field_type(field)} | {'yes' if name in COMMON_REQUIRED else 'no'} | {describe(field)} |")
dictionary += ["", "Provenance fields: `kind` (observed/reported/hypothesis/evidence/synthetic), `source`, `confidence` (low/moderate/high) are required. `source_record_id`, `source_hash`, `derived_from` and `method` are optional. Access requires `classification=restricted-health`, `readers`, `writers` and `ai_allowed` (default false in blank installation).", "", "Numeric schema bounds are data-entry plausibility checks, not safe-intake limits, targets or clinical reference ranges. Unknown optional values are absent, not null or zero. Arrays default to empty only when emptiness is known. Do not infer an absence of symptoms from an empty note."]
for entity,definition in DOMAINS.items():
    dictionary += ["", "## "+entity, "", f"Google tab and Notion database: **{definition['sheet']}**. One canonical source per edition is specified in `spec.json`.", "", "| Canonical field | Type | Required | Unit / validation / meaning |", "| --- | --- | --- | --- |"]
    for name,field in definition["fields"].items():dictionary.append(f"| `{name}` | {field_type(field)} | {'yes' if name in definition['required'] else 'no'} | {describe(field)} |")
dictionary += ["", "## Native import and export mappings", "", "| Canonical representation | Google Workspace | Notion | Portable export |", "| --- | --- | --- | --- |", "| `id` | Record ID column, never row position | Record ID property; native page UUID fallback for manual rows | Same UUID in JSON and CSV |", "| `owner_id` | Profile UUID | Owner ID property containing the pseudonymous profile UUID | Pseudonymous UUID |", "| `schema_version`, `revision` | Metadata columns | Metadata properties or explicit adapter defaults | Explicit fields, never omitted on interchange export |", "| Numeric fields | Typed numeric columns; unit in field or adjacent unit column | Number property with unit named in property or unit property | Number plus canonical field/unit |", "| Date/date-time | Typed local-calendar dates; timestamp cells explicitly displayed as UTC; original IANA zone in metadata | Date property plus explicit original timezone metadata | ISO 8601 offset timestamp and IANA timezone |", "| Foreign key | UUID lookup column | Relation to local duplicated database | Referenced canonical UUID, not seller page URL |", "| `provenance` | Flattened provenance.kind, provenance.source, provenance.confidence and optional source columns | Mapped flattened provenance properties | Structured object in JSON |", "| `access` | Owner-controlled consent settings; spreadsheet sharing enforces access | Actual page/database sharing; views do not enforce access | Structured object plus consent records |", "| Recipe ingredients | JSON text in Recipes.Ingredients | JSON rich-text in Recipes.Ingredients | Nested recipe ingredients in canonical JSON; no child CSV exporter |", "| Meal-plan items | JSON text in Meal Plans.Items | JSON rich-text in Meal Plans.Items | Nested items in canonical JSON; no child CSV exporter |", "| Training sets | JSON text in Training.Sets | JSON rich-text in Training.Sets | Nested sets in canonical JSON; no child CSV exporter |", "| Profile goals | JSON text in Profile.Goals | JSON rich-text in Profile.Goals | Nested goals in canonical JSON; no child CSV exporter |", "", "Native workbook headers are human-readable labels, while supplied CSVs use canonical snake_case names. adapters/mappings.json is the exact field map. Arrays and objects remain JSON text in native cells. Native CSV exports may flatten arrays, relations or files. CSV alone is not a fidelity guarantee. Restore through an explicit mapping with canonical IDs and private file inventory. JSON Schema interchange is the complete portable contract. Stage 1 reference validation does not prove that a platform-specific exporter has been implemented.", "", "## FHIR boundary", "", "Conceptual candidates only. The release ships no validated FHIR exporter or clinical interoperability claim. R4 includes Observation, MedicationStatement and DocumentReference. Everyday food and supplement catalogs are not forced into clinical resources. Personal symptoms must not be silently coded as diagnoses.", "", "Primary references checked 2026-11-12: [HL7 R4 Observation](https://hl7.org/fhir/R4/observation.html), [MedicationStatement](https://hl7.org/fhir/R4/medicationstatement.html), [DocumentReference](https://hl7.org/fhir/R4/documentreference.html), [R4 resource index](https://hl7.org/fhir/R4/resourcelist.html)."]
(ROOT/"docs/DATA_DICTIONARY.md").write_text("\n".join(dictionary)+"\n")
print(f"Built {len(DOMAINS)} entity schemas and {sum(map(len,demo['entities'].values()))} synthetic records")
