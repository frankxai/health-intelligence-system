# Independent quality review

Personal Health Intelligence OS 0.1.0. Reviewed 12 November 2026. This is an implementation review, not clinical validation or proof of customer demand.

## Verified locally

- **36 Python regression tests passed.** This includes the original 24 tests and twelve independently added tests covering deleted product/intake records, nested cross-owner food/recipe references, ownership immutability, local-day behavior at the UTC date boundary, specification-to-adapter tab consistency, non-finite measurements, audit references and provenance lineage.
- **18 offline demo logic checks passed.** Independent execution of `design/verify-demo-core.mjs` checked summary arithmetic, exact source points, exposure reconciliation, label/unit/deletion boundaries, unknown values versus zero, stable IDs and revisions, empty states, reset, and absence of network or persistent browser storage.
- **Canonical synthetic dataset passed** JSON Schema and referential/temporal validation: 22 entity types and 39 linked fictional records. The blank dataset also passed with zero records.
- The final local workbook build receipt demonstrated a seven-day mean sleep duration of 7.357142857142857 hours, a 3.5 mg fictional exposure total, a live input perturbation, **14 boundary/restoration checks**, and zero matches in its formula error scan. The boundary checks include blank versus zero, duplicate dates, daily/intake tombstones, both label-verification states, unsupported units, missing label amounts, duplicate product IDs, and mass conversion. That receipt establishes those specific local checks only.

## Defects corrected during review

1. The canonical specification named combined Care and Recipes tabs while the adapter built separate Documents, Appointments and Meal Plans tabs. The generator, generated specification and dictionary now name the actual tabs.
2. The specification claimed snake_case workbook headers and nested child CSV exports. Native headers actually use readable labels, supplied CSVs use canonical field names, and nested values remain JSON text cells. The contract now describes that implementation and does not claim a platform exporter.
3. The canonical exposure helper could count an intake against a tombstoned product record. It now rejects that incomplete source state explicitly.
4. Nested recipe and meal-plan references did not check owner equality. The validator now rejects cross-owner food and recipe references.
5. An optimistic update could change a record's owner. The reference conflict helper now rejects ownership transfer even when the expected revision matches.
6. The first-entry contract implied optional health measurements were required. Only a date is structurally required for a daily payload; the suggested first entry remains date, known sleep, energy and a note.
7. Timestamp semantics are explicit: canonical interchange preserves an offset or Z and an IANA zone. The Google template displays timestamp cells in UTC; its Exposure day selector is a UTC day. Canonical local-day analysis is a different, explicitly named view.
8. Python's permissive JSON decoder could admit NaN and Infinity through numeric schema checks. The validator now recursively rejects non-finite values before schema and integrity validation.
9. Audit references and derived-record lineage could contain dangling or cross-owner references. The validator now checks referenced identity, declared audit entity type and owner equality.

The design owner also corrected the demo caffeine limit to the schema maximum and hardened exposure handling for unverified, missing, deleted and unsupported source contributions. The 18 logic checks include those boundaries.

## Native acceptance and release limits

Native Google import required a repair because date-valued cells and chart series did not survive the initial conversion. The lead implementation agent reported readback of 25 tabs, 22 native tables, two chart series and the expected numerical results after repair. Final native perturbation, chart rendering and export receipts must be kept with the released revision; the independent local tests do not substitute for them.

Notion database rows, relations and views need native readback and duplication evidence. A successful database create is not evidence that customer duplication remaps relations correctly. The lead agent owns those receipts.

The workbook source now blocks unsupported units and missing label amounts, checks product and ingredient labels, handles tombstones, and prevents duplicate daily rows from inflating coverage or silently selecting a measurement. The local boundary checks passed. A further source review confirmed that an active intake referencing a deleted product/ingredient requires source review, and that selected ingredients beyond the first 20 calculator lines produce an explicit extension message. Final native readback after these changes remains part of the lead agent's acceptance receipt.

The Chromium verification script is present, but this environment blocked browser launch with a socket permission error. No rendered web screenshot or responsive browser check is claimed from that failed run. VM tests check application logic and selected markup invariants; they do not establish rendered layout, screen-reader behavior, chart clipping or browser compatibility.

Fresh customer-account installation, an accepted checkout-to-delivery transaction, a customer export/reopen test, assistant permission/revocation testing, and final consumer/commercial terms remain release gates. The ten-minute first check-in target is unmeasured. Background synchronization, wearable imports and FHIR export are not implemented.

## Release posture

The pack is suitable for a controlled synthetic installation review. General commercial readiness requires the open acceptance receipts above. No health outcome, diagnosis, dosing decision, customer installation, partner delivery capacity or live payment path is established by source-code tests.
