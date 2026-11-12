# Data dictionary

Canonical schema version 0.1.0. Generated from `canonical/schema.json`; field names and types are authoritative there.

## Shared record envelope

Every entity carries the following fields. These are explicit export fields; native adapters may show only the fields needed for daily use. Metadata defaults must come from the known owner, native creation/edit timestamps and explicit source context, never inferred measurements.

| Field | Type | Required | Validation and meaning |
| --- | --- | --- | --- |
| `id` | string | yes | Stable UUID independent of platform row or page IDs; Format: uuid |
| `schema_version` | string | yes | Fixed: 0.1.0 |
| `owner_id` | string | yes | Pseudonymous owner UUID; not email or full name; Format: uuid |
| `created_at` | string | yes | Format: date-time |
| `updated_at` | string | yes | Format: date-time |
| `timezone` | string | yes | IANA timezone identifier, e.g. Europe/Amsterdam |
| `revision` | integer | yes | Minimum: 1 |
| `provenance` | object | yes | Members: kind, source, confidence, source_record_id, source_hash, derived_from, method |
| `access` | object | yes | Members: classification, readers, writers, ai_allowed |
| `deleted_at` | string | no | Format: date-time |

Provenance fields: `kind` (observed/reported/hypothesis/evidence/synthetic), `source`, `confidence` (low/moderate/high) are required. `source_record_id`, `source_hash`, `derived_from` and `method` are optional. Access requires `classification=restricted-health`, `readers`, `writers` and `ai_allowed` (default false in blank installation).

Numeric schema bounds are data-entry plausibility checks, not safe-intake limits, targets or clinical reference ranges. Unknown optional values are absent, not null or zero. Arrays default to empty only when emptiness is known. Do not infer an absence of symptoms from an empty note.

## profile

Google tab and Notion database: **Profile**. One canonical source per edition is specified in `spec.json`.

| Canonical field | Type | Required | Unit / validation / meaning |
| --- | --- | --- | --- |
| `display_name` | string | yes | Optional pseudonym. Legal name is unnecessary. |
| `goals` | array | yes | Item members: name, metric, target, unit, review_date |
| `priorities` | array | no | Items: string |
| `birth_year` | integer | no | Minimum: 1900; Maximum: 2100 |
| `height_cm` | number | no | Unit: cm; Minimum: 30; Maximum: 260 |
| `notes` | string | no | Source-preserving value |

## daily_observation

Google tab and Notion database: **Daily**. One canonical source per edition is specified in `spec.json`.

| Canonical field | Type | Required | Unit / validation / meaning |
| --- | --- | --- | --- |
| `local_date` | string | yes | Format: date |
| `sleep_hours` | number | no | Unit: h; Minimum: 0; Maximum: 24 |
| `energy_0_10` | number | no | Unit: 0 to 10 subjective scale; Minimum: 0; Maximum: 10 |
| `focus_0_10` | number | no | Unit: 0 to 10 subjective scale; Minimum: 0; Maximum: 10 |
| `mood_0_10` | number | no | Unit: 0 to 10 subjective scale; Minimum: 0; Maximum: 10 |
| `stress_0_10` | number | no | Unit: 0 to 10 subjective scale; Minimum: 0; Maximum: 10 |
| `fluid_ml` | number | no | Unit: mL; Minimum: 0; Maximum: 20000 |
| `caffeine_mg` | number | no | Unit: mg; Minimum: 0; Maximum: 3000 |
| `protein_g` | number | no | Unit: g; Minimum: 0; Maximum: 1000 |
| `fiber_g` | number | no | Unit: g; Minimum: 0; Maximum: 200 |
| `sodium_mg` | number | no | Unit: mg; Minimum: 0; Maximum: 30000 |
| `calcium_mg` | number | no | Unit: mg; Minimum: 0; Maximum: 10000 |
| `training_minutes` | number | no | Unit: min; Minimum: 0; Maximum: 1440 |
| `pain_0_10` | number | no | Unit: 0 to 10 subjective scale; Minimum: 0; Maximum: 10 |
| `pain_location` | string | no | Source-preserving value |
| `bristol_1_7` | integer | no | Minimum: 1; Maximum: 7 |
| `summary_mode` | string | no | Allowed: manual_summary, event_projection |
| `notes` | string | no | Source-preserving value |

## product

Google tab and Notion database: **Supplements**. One canonical source per edition is specified in `spec.json`.

| Canonical field | Type | Required | Unit / validation / meaning |
| --- | --- | --- | --- |
| `name` | string | yes | Source-preserving value |
| `category` | string | yes | Allowed: supplement, medication |
| `brand` | string | no | Source-preserving value |
| `serving_label` | string | no | Label serving description; not a recommendation |
| `label_verified` | boolean | yes | Source-preserving value |
| `label_document_id` | string | no | Foreign key to clinical_document.id; Format: uuid |
| `status` | string | no | Allowed: inventory, active, paused, archived |
| `prescriber_notes` | string | no | Reported prescription instructions; agents cannot change them |
| `notes` | string | no | Source-preserving value |

## ingredient

Google tab and Notion database: **Ingredients**. One canonical source per edition is specified in `spec.json`.

| Canonical field | Type | Required | Unit / validation / meaning |
| --- | --- | --- | --- |
| `product_id` | string | yes | Foreign key to product.id; Format: uuid |
| `ingredient_name` | string | yes | Normalized ingredient name |
| `amount_per_serving` | number | yes | Unit: specified by unit; Minimum: 0 |
| `unit` | string | yes | Exact source unit. Prefer UCUM where unambiguous. Arithmetic adapters whitelist supported conversions; unfamiliar units remain unchanged. |
| `form` | string | no | Chemical form from product label |
| `label_basis` | string | no | Exact serving on label |
| `label_verified` | boolean | no | Source-preserving value |
| `notes` | string | no | Source-preserving value |

## intake

Google tab and Notion database: **Intakes**. One canonical source per edition is specified in `spec.json`.

| Canonical field | Type | Required | Unit / validation / meaning |
| --- | --- | --- | --- |
| `product_id` | string | yes | Foreign key to product.id; Format: uuid |
| `taken_at` | string | yes | Format: date-time |
| `servings` | number | yes | Unit: label servings; Minimum: 0; Maximum: 100 |
| `event_status` | string | no | Allowed: taken, planned, skipped |
| `adverse_event` | string | no | Source-preserving value |
| `notes` | string | no | Source-preserving value |

## food

Google tab and Notion database: **Foods**. One canonical source per edition is specified in `spec.json`.

| Canonical field | Type | Required | Unit / validation / meaning |
| --- | --- | --- | --- |
| `name` | string | yes | Source-preserving value |
| `basis_g` | number | yes | Unit: g; Minimum: 0.001; Maximum: 10000 |
| `energy_kcal` | number | no | Unit: kcal; Minimum: 0 |
| `protein_g` | number | no | Unit: g; Minimum: 0 |
| `fiber_g` | number | no | Unit: g; Minimum: 0 |
| `sodium_mg` | number | no | Unit: mg; Minimum: 0 |
| `calcium_mg` | number | no | Unit: mg; Minimum: 0 |
| `allergens` | array | no | Items: string |
| `source_url` | string | no | Source-preserving value |
| `notes` | string | no | Source-preserving value |

## recipe

Google tab and Notion database: **Recipes**. One canonical source per edition is specified in `spec.json`.

| Canonical field | Type | Required | Unit / validation / meaning |
| --- | --- | --- | --- |
| `name` | string | yes | Source-preserving value |
| `servings` | number | yes | Unit: servings; Minimum: 0.01; Maximum: 1000 |
| `ingredients` | array | yes | Item members: food_id, quantity_g |
| `instructions` | string | no | Source-preserving value |
| `notes` | string | no | Source-preserving value |

## meal_plan

Google tab and Notion database: **Meal Plans**. One canonical source per edition is specified in `spec.json`.

| Canonical field | Type | Required | Unit / validation / meaning |
| --- | --- | --- | --- |
| `name` | string | yes | Source-preserving value |
| `local_date` | string | yes | Format: date |
| `items` | array | yes | Item members: recipe_id, meal, servings |
| `notes` | string | no | Source-preserving value |

## hydration

Google tab and Notion database: **Hydration**. One canonical source per edition is specified in `spec.json`.

| Canonical field | Type | Required | Unit / validation / meaning |
| --- | --- | --- | --- |
| `observed_at` | string | yes | Format: date-time |
| `volume_ml` | number | yes | Unit: mL; Minimum: 0; Maximum: 10000 |
| `drink` | string | yes | Source-preserving value |
| `sodium_mg` | number | no | Unit: mg; Minimum: 0 |
| `potassium_mg` | number | no | Unit: mg; Minimum: 0 |
| `measurement_type` | string | no | Allowed: measured, estimated |
| `notes` | string | no | Source-preserving value |

## sleep

Google tab and Notion database: **Sleep**. One canonical source per edition is specified in `spec.json`.

| Canonical field | Type | Required | Unit / validation / meaning |
| --- | --- | --- | --- |
| `start_at` | string | yes | Format: date-time |
| `end_at` | string | yes | Format: date-time |
| `duration_h` | number | yes | Unit: h; Minimum: 0; Maximum: 24 |
| `source_type` | string | yes | Allowed: self_report, wearable |
| `quality_0_10` | number | no | Unit: 0 to 10 subjective scale; Minimum: 0; Maximum: 10 |
| `is_nap` | boolean | no | Source-preserving value |
| `notes` | string | no | Source-preserving value |

## training

Google tab and Notion database: **Training**. One canonical source per edition is specified in `spec.json`.

| Canonical field | Type | Required | Unit / validation / meaning |
| --- | --- | --- | --- |
| `start_at` | string | yes | Format: date-time |
| `activity` | string | yes | Allowed: strength, cardio, walking, mobility, other |
| `duration_min` | number | yes | Unit: min; Minimum: 0; Maximum: 1440 |
| `rpe_1_10` | number | no | Unit: rating of perceived exertion; Minimum: 1; Maximum: 10 |
| `distance_km` | number | no | Unit: km; Minimum: 0 |
| `sets` | array | no | Item members: exercise, reps, load_kg |
| `notes` | string | no | Source-preserving value |

## recovery

Google tab and Notion database: **Recovery**. One canonical source per edition is specified in `spec.json`.

| Canonical field | Type | Required | Unit / validation / meaning |
| --- | --- | --- | --- |
| `observed_at` | string | yes | Format: date-time |
| `kind` | string | yes | Allowed: stress, wellbeing, recovery_practice |
| `score_0_10` | number | no | Unit: 0 to 10 subjective scale; Minimum: 0; Maximum: 10 |
| `practice` | string | no | Source-preserving value |
| `duration_min` | number | no | Unit: min; Minimum: 0; Maximum: 1440 |
| `notes` | string | no | Source-preserving value |

## symptom

Google tab and Notion database: **Symptoms**. One canonical source per edition is specified in `spec.json`.

| Canonical field | Type | Required | Unit / validation / meaning |
| --- | --- | --- | --- |
| `name` | string | yes | Source-preserving value |
| `onset_at` | string | yes | Format: date-time |
| `resolved_at` | string | no | Format: date-time |
| `body_zone` | string | yes | Source-preserving value |
| `severity_0_10` | number | no | Unit: 0 to 10 subjective scale; Minimum: 0; Maximum: 10 |
| `status` | string | yes | Allowed: reported_symptom, reported_condition, clinician_documented_condition |
| `trigger_hypothesis` | string | no | Source-preserving value |
| `what_helped_report` | string | no | Source-preserving value |
| `red_flags_reported` | array | no | Items: string |
| `document_id` | string | no | Foreign key to clinical_document.id; Format: uuid |
| `notes` | string | no | Source-preserving value |

## biomarker

Google tab and Notion database: **Biomarkers**. One canonical source per edition is specified in `spec.json`.

| Canonical field | Type | Required | Unit / validation / meaning |
| --- | --- | --- | --- |
| `name` | string | yes | Source-preserving value |
| `sample_at` | string | yes | Format: date-time |
| `value` | number | yes | Unit: specified by unit |
| `unit` | string | yes | Exact source unit. Prefer UCUM where unambiguous. Arithmetic adapters whitelist supported conversions; unfamiliar units remain unchanged. |
| `reference_low` | number | no | Unit: same unit as value |
| `reference_high` | number | no | Unit: same unit as value |
| `laboratory` | string | no | Optional pseudonymous laboratory identifier |
| `loinc_code` | string | no | Source-preserving value |
| `document_id` | string | no | Foreign key to clinical_document.id; Format: uuid |
| `notes` | string | no | Source-preserving value |

## clinical_document

Google tab and Notion database: **Documents**. One canonical source per edition is specified in `spec.json`.

| Canonical field | Type | Required | Unit / validation / meaning |
| --- | --- | --- | --- |
| `name` | string | yes | Source-preserving value |
| `document_type` | string | yes | Allowed: lab_report, clinical_note, prescription, product_label, other |
| `document_date` | string | yes | Format: date |
| `storage_uri` | string | yes | Owner-controlled private URI; never a public health-data URL |
| `sha256` | string | no | Pattern: `^[a-f0-9]{64}$` |
| `notes` | string | no | Source-preserving value |

## appointment

Google tab and Notion database: **Appointments**. One canonical source per edition is specified in `spec.json`.

| Canonical field | Type | Required | Unit / validation / meaning |
| --- | --- | --- | --- |
| `name` | string | yes | Source-preserving value |
| `starts_at` | string | yes | Format: date-time |
| `status` | string | yes | Allowed: planned, completed, cancelled |
| `preparation` | string | no | Source-preserving value |
| `document_id` | string | no | Foreign key to clinical_document.id; Format: uuid |
| `notes` | string | no | Source-preserving value |

## experiment

Google tab and Notion database: **Experiments**. One canonical source per edition is specified in `spec.json`.

| Canonical field | Type | Required | Unit / validation / meaning |
| --- | --- | --- | --- |
| `name` | string | yes | Source-preserving value |
| `hypothesis` | string | yes | Source-preserving value |
| `start_date` | string | yes | Format: date |
| `end_date` | string | yes | Format: date |
| `baseline_start` | string | no | Format: date |
| `baseline_end` | string | no | Format: date |
| `primary_outcome` | string | yes | Source-preserving value |
| `intervention` | string | no | Source-preserving value |
| `confounders` | array | no | Items: string |
| `stop_rule` | string | yes | Source-preserving value |
| `status` | string | yes | Allowed: planned, baseline, active, stopped, reviewed |
| `result_summary` | string | no | Source-preserving value |
| `causal_claim_allowed` | boolean | no | Fixed: False |
| `notes` | string | no | Source-preserving value |

## evidence

Google tab and Notion database: **Evidence**. One canonical source per edition is specified in `spec.json`.

| Canonical field | Type | Required | Unit / validation / meaning |
| --- | --- | --- | --- |
| `title` | string | yes | Source-preserving value |
| `url` | string | yes | Format: uri |
| `accessed_date` | string | yes | Format: date |
| `evidence_type` | string | yes | Allowed: guideline, systematic_review, trial, observational, mechanistic, product_label, platform_documentation, other |
| `claim` | string | yes | Source-preserving value |
| `population` | string | no | Source-preserving value |
| `limitations` | string | no | Source-preserving value |
| `strength` | string | no | Allowed: ungraded, low, moderate, high |
| `doi` | string | no | Source-preserving value |
| `notes` | string | no | Source-preserving value |

## purchase

Google tab and Notion database: **Purchases**. One canonical source per edition is specified in `spec.json`.

| Canonical field | Type | Required | Unit / validation / meaning |
| --- | --- | --- | --- |
| `name` | string | yes | Source-preserving value |
| `product_id` | string | no | Foreign key to product.id; Format: uuid |
| `purchased_date` | string | yes | Format: date |
| `quantity` | number | yes | Unit: items; Minimum: 0 |
| `cost` | number | yes | Unit: currency units; Minimum: 0 |
| `currency` | string | yes | Allowed: EUR, USD, GBP |
| `servings_remaining` | number | no | Unit: label servings; Minimum: 0 |
| `expiry_date` | string | no | Format: date |
| `notes` | string | no | Source-preserving value |

## review

Google tab and Notion database: **Reviews**. One canonical source per edition is specified in `spec.json`.

| Canonical field | Type | Required | Unit / validation / meaning |
| --- | --- | --- | --- |
| `name` | string | yes | Source-preserving value |
| `cadence` | string | yes | Allowed: weekly, monthly, quarterly |
| `period_start` | string | yes | Format: date |
| `period_end` | string | yes | Format: date |
| `summary` | string | yes | Source-preserving value |
| `missingness_notes` | string | no | Source-preserving value |
| `confounders` | array | no | Items: string |
| `next_action` | string | yes | Source-preserving value |
| `decision_owner` | string | no | Source-preserving value |
| `notes` | string | no | Source-preserving value |

## consent

Google tab and Notion database: **Consent**. One canonical source per edition is specified in `spec.json`.

| Canonical field | Type | Required | Unit / validation / meaning |
| --- | --- | --- | --- |
| `name` | string | yes | Source-preserving value |
| `principal` | string | yes | Source-preserving value |
| `scope` | array | yes | Items: string |
| `status` | string | yes | Allowed: granted, revoked, expired |
| `granted_at` | string | yes | Format: date-time |
| `expires_at` | string | no | Format: date-time |
| `revoked_at` | string | no | Format: date-time |
| `provider` | string | no | Source-preserving value |
| `purpose` | string | no | Source-preserving value |
| `notes` | string | no | Source-preserving value |

## audit_event

Google tab and Notion database: **Audit**. One canonical source per edition is specified in `spec.json`.

| Canonical field | Type | Required | Unit / validation / meaning |
| --- | --- | --- | --- |
| `occurred_at` | string | yes | Format: date-time |
| `actor` | string | yes | Source-preserving value |
| `operation` | string | yes | Allowed: create, update, delete, import, export, grant, revoke, sync_propose, sync_apply |
| `entity_type` | string | yes | Source-preserving value |
| `record_id` | string | yes | Foreign key to any entity.id; Format: uuid |
| `outcome` | string | yes | Allowed: applied, proposed, rejected, conflict |
| `expected_revision` | integer | no | Minimum: 0 |
| `result_revision` | integer | no | Minimum: 1 |
| `before_hash` | string | no | Source-preserving value |
| `after_hash` | string | no | Source-preserving value |
| `receipt` | string | no | Source-preserving value |
| `notes` | string | no | Source-preserving value |

## Native import and export mappings

| Canonical representation | Google Workspace | Notion | Portable export |
| --- | --- | --- | --- |
| `id` | Record ID column, never row position | Record ID property; native page UUID fallback for manual rows | Same UUID in JSON and CSV |
| `owner_id` | Profile UUID | Owner ID property containing the pseudonymous profile UUID | Pseudonymous UUID |
| `schema_version`, `revision` | Metadata columns | Metadata properties or explicit adapter defaults | Explicit fields, never omitted on interchange export |
| Numeric fields | Typed numeric columns; unit in field or adjacent unit column | Number property with unit named in property or unit property | Number plus canonical field/unit |
| Date/date-time | Typed local-calendar dates; timestamp cells explicitly displayed as UTC; original IANA zone in metadata | Date property plus explicit original timezone metadata | ISO 8601 offset timestamp and IANA timezone |
| Foreign key | UUID lookup column | Relation to local duplicated database | Referenced canonical UUID, not seller page URL |
| `provenance` | Flattened provenance.kind, provenance.source, provenance.confidence and optional source columns | Mapped flattened provenance properties | Structured object in JSON |
| `access` | Owner-controlled consent settings; spreadsheet sharing enforces access | Actual page/database sharing; views do not enforce access | Structured object plus consent records |
| Recipe ingredients | JSON text in Recipes.Ingredients | JSON rich-text in Recipes.Ingredients | Nested recipe ingredients in canonical JSON; no child CSV exporter |
| Meal-plan items | JSON text in Meal Plans.Items | JSON rich-text in Meal Plans.Items | Nested items in canonical JSON; no child CSV exporter |
| Training sets | JSON text in Training.Sets | JSON rich-text in Training.Sets | Nested sets in canonical JSON; no child CSV exporter |
| Profile goals | JSON text in Profile.Goals | JSON rich-text in Profile.Goals | Nested goals in canonical JSON; no child CSV exporter |

Native workbook headers are human-readable labels, while supplied CSVs use canonical snake_case names. adapters/mappings.json is the exact field map. Arrays and objects remain JSON text in native cells. Native CSV exports may flatten arrays, relations or files. CSV alone is not a fidelity guarantee. Restore through an explicit mapping with canonical IDs and private file inventory. JSON Schema interchange is the complete portable contract. Stage 1 reference validation does not prove that a platform-specific exporter has been implemented.

## FHIR boundary

Conceptual candidates only. The release ships no validated FHIR exporter or clinical interoperability claim. R4 includes Observation, MedicationStatement and DocumentReference. Everyday food and supplement catalogs are not forced into clinical resources. Personal symptoms must not be silently coded as diagnoses.

Primary references checked 2026-11-12: [HL7 R4 Observation](https://hl7.org/fhir/R4/observation.html), [MedicationStatement](https://hl7.org/fhir/R4/medicationstatement.html), [DocumentReference](https://hl7.org/fhir/R4/documentreference.html), [R4 resource index](https://hl7.org/fhir/R4/resourcelist.html).
