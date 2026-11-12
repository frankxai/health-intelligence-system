# Architecture decisions

Status: accepted for 0.1.0 template architecture. External deployment and commerce readiness require their own release evidence.

## ADR-001: One specification, native editions

`canonical/spec.json` owns product behavior and edition ownership. `canonical/schema.json` owns the interchange model. Google and Notion adapters produce human-oriented views of that model. Stable IDs, units, record meaning and intended use remain consistent even when native formatting differs.

Use the existing health product repository and workspace assets. Do not create a parallel registry, database service, agent runtime or subscription to ship a template.

## ADR-002: Entity ownership prevents synchronization loops

In Google Edition, Sheets owns structured records and reviews. Drive owns files. In Notion Edition, Notion owns structured records and reviews, with private document locations stored as links. In Complete Edition, Sheets owns all structured records except reviews, which Notion owns. Drive owns documents. Notion may show one-way projections from Sheets.

Stage 1 ships the ownership contract, export model and conflict logic. It does not ship a background synchronization service. Customer data must never be edited in two independently canonical places. A projection must carry source ID, revision and sync timestamp and must expose its read-only status.

## ADR-003: Identity survives native platform changes

An owner-created record uses a UUID v4. An imported record uses UUID v5 of customer source namespace, entity type and upstream record ID. A manual Notion row without a Record ID uses its native page UUID as the canonical fallback during export. Once written, that identifier persists through edits and imports; a new duplicated customer installation receives its own owner identity.

Platform page IDs, sheet row numbers and view IDs are adapter metadata. Row numbers never identify a health record. A duplicate source identity with different values is a conflict; a changed row order is not a new event.

## ADR-004: Explicit provenance and missingness

Record provenance distinguishes observed, reported, hypothesis, evidence and synthetic. Confidence qualifies reliability of the source. Evidence strength is separate. Timestamp metadata uses ISO 8601 offsets and an IANA timezone. Local day grouping uses the owner's timezone, including daylight-saving transitions.

Unknown optional fields are omitted. Numeric zero means a recorded zero. A plan does not become a consumption or measurement event. Daily manual summaries and detailed events are never added together. An event-derived aggregate records its input IDs and replaces the selected metric's projection only after explicit mode selection.

## ADR-005: Ingredient exposure is arithmetic

Keep product, ingredient label and taken event separate. Each ingredient records amount per labelled serving and source unit. Exposure equals verified label amount multiplied by taken servings, grouped by normalized ingredient and local date. Planned and skipped events do not contribute.

Only explicit supported unit conversions are performed. Mass conversion can use g, mg and mcg. IU cannot be converted to mass without an ingredient-specific validated factor. Expose unknown labels and unsupported units. The output is descriptive exposure arithmetic; it does not determine an individual's safe dose or propose changes.

## ADR-006: Customer-controlled access

Default data classification is restricted-health and AI permission is false. Consent identifies principal, provider, purpose, scope, grant time and revocation. A filtered Notion view is not an access-control boundary. Shared data must reside behind actual access controls. Partner installers use synthetic records, temporary access when necessary and a handover receipt. Seller analytics must not receive health values or record identifiers.

Avoid retaining customer health records for support. Prefer a customer-created synthetic reproduction. If scoped support access is necessary, document the customer instruction, expiry, access path, deletion and revocation. Commercial-template sharing and private customer-workspace sharing are separate operations.

## ADR-007: Versioned writes, explicit conflict resolution

Each record has an integer revision. A changed incoming record must identify the revision it expects to replace. Identical content is idempotent. A stale expected revision becomes a conflict and preserves both candidates. No last-write-wins behavior is permitted. Deletion uses a tombstone; a stale projection cannot resurrect a deleted record.

The offline helpers are reference logic and tests. They do not establish an immutable or clinically certified audit system. Native history plus explicit receipts is the Stage 1 audit boundary.

## ADR-008: FHIR is a mapping boundary

Keep FHIR R4 candidate mappings for Observation, MedicationStatement, DocumentReference, Appointment, Consent and AuditEvent where relevant. Preserve source units and optional source-provided clinical codes. Do not infer LOINC or diagnosis codes. A symptom is not a confirmed Condition. A medication intake is not a prescription.

The release makes no FHIR interoperability claim and ships no validated FHIR export. A future adapter must declare an implementation guide, resource profiles, terminology bindings and validator results before making that promise.

## ADR-009: Additive upgrades and reversibility

Before upgrade, export a snapshot with schema version and preserve files. Run a dry-run migration and show the field/unit changes. Prefer additive properties. Never replace a buyer's database with a fresh demo copy. Preserve record IDs and ownership. Stop for a unit ambiguity or destructive mapping. Verify record counts, foreign keys and representative values, then retain a rollback path controlled by the customer.

## ADR-010: General wellness and recordkeeping purpose

The product supports tracking, education and descriptive reasoning. Agents do not diagnose, interpret personal laboratory results, recommend medication or supplement dose changes, prescribe therapeutic diets, or deliver rehabilitation. Product-page claims, demos and partner delivery scripts must maintain the same intended purpose. Regulatory classification depends on actual functionality and claims, not a disclaimer alone.
