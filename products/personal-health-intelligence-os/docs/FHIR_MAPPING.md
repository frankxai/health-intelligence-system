# Interoperability scope

Personal Health Intelligence OS · 0.1.0

Keep day-to-day capture readable. Use the canonical JSON/CSV model for ordinary workspace operation, with optional FHIR mappings at an export boundary. No FHIR server, certified interface, EHR connection or validated clinical exchange is shipped.

FHIR R4 4.0.1 is a pinned mapping target for possible future export, not a claim that R4 is the newest release. HL7's R4 pages explicitly identify newer published versions. Preserve original source code/unit/value and only attach a clinical code after verification; do not invent LOINC, SNOMED or medication identifiers.

| Canonical entity | Candidate FHIR R4 resource | Required mapping decision |
| --- | --- | --- |
| Profile | Patient | Only export identity the customer explicitly selects; stable local ID remains distinct from clinical identifier |
| User goals | Goal | Preserve author, status and recorded target; no clinical endorsement implied |
| Daily/sleep/hydration/training measurements | Observation or QuestionnaireResponse | Verified code, source method, effective time, subject and units; subjective scales remain explicitly self-reported |
| Symptom report | Observation | A reported symptom is not a diagnosis; only source-confirmed clinical conditions map to Condition |
| Reported medication use | MedicationStatement | Distinguish reported use from a prescription, administration or recommendation |
| Laboratory value | Observation with DiagnosticReport reference where appropriate | Preserve laboratory-reported unit, reference range, specimen/time and source; no diagnostic interpretation |
| Clinical document | DocumentReference | Document MIME type, source location, owner and checksum; reference metadata has its own provenance |
| Visit | Appointment / Encounter | Planned booking and completed clinical encounter are distinct states |
| Source lineage | Provenance | Actor, activity, target version and original source; preserve record's native metadata first |
| Access history | AuditEvent | Distinguish use/access events from content provenance |
| Consent | Consent | Match actual purpose/actor/scope; exporting a Consent resource does not establish legal consent by itself |
| Foods/recipes/inventory/experiments/reviews | Keep canonical extension model | Do not force recipes into medical nutrition orders or imply clinical research enrollment |

Primary mapping references: [Observation](https://hl7.org/fhir/R4/observation.html), [MedicationStatement](https://hl7.org/fhir/R4/medicationstatement.html), [DocumentReference](https://hl7.org/fhir/R4/documentreference.html), [Provenance](https://hl7.org/fhir/R4/provenance.html).

A future adapter must validate the selected resource/profile version, coding systems, UCUM conversions, required fields, subject references, absent-data reasons and timezone offsets against a FHIR validator. Lossy or unresolved fields go into an export report for human review. No customer installation depends on implementing clinical terminology.
