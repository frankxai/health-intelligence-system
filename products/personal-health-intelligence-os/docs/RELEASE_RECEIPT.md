# Release receipt 0.1.0

As of 12 November 2026. Decision: Stage 1 release candidate for review and installer pilot. General commercial release is held. No real health history was imported into this product pack.

## What exists

| Surface | Implemented | Evidence | Remaining acceptance |
|---|---|---|---|
| Canonical source | 22 schemas, field dictionary, versioned specification, blank dataset, 39 linked synthetic records | 36 Python tests and synthetic/blank validation | Live platform round-trip exporter is not installed |
| Google edition | Native workbook, 25 tabs, 22 native record tables, 2 native charts, validated dropdowns, cockpit, ingredient exposure, 4 protocol/operation documents, 5 organized folders | Native readback, successful numeric input perturbation and restore, exported workbook has correct totals and no formula-error matches | Fresh customer-account copy, export/restore and OAuth revocation |
| Notion edition | Daily cockpit, 22 typed databases, 39 example records, product/document relations, 19 linked views including chart/board/gallery/calendar, guides and portable instructions | Full same-workspace duplicate: 22 databases/39 records, new Daily source and remapped ingredient-to-product relations | Cross-account duplication, mobile rendered review, full export/restore |
| Portable agent pack | Shared operation contract and 7 roles | Read/propose/apply receipts, source grading and privacy boundaries | Customer/provider-specific acceptance |
| Demo and product page | Offline interactive synthetic cockpit and draft product page | 18 logic checks; exported sample entries pass schema | Rendered browser and touch/keyboard screenshots unavailable in this environment |
| Partner delivery | €249 scope hypothesis, role boundaries, runbook, receipt and handoff checks | Saved in Drive and Notion | No partner recruited, assigned or contacted |
| Commerce | Official-source platform comparison, FAQ, launch drafts, existing Stripe code path identified | Pricing remains hypotheses; human service billing is separate | No checkout, payment, tax configuration, purchase or delivery test |

## Verification details

Workbook baseline: mean sleep 7.357142857 h across the chosen seven days, mean energy 6.714285714, fictional ingredient exposure 3.5 mg on the selected UTC day. Native Google edit of the last sleep value from 8 to 9 changes the mean to 7.5; the input was restored to 8. All validation changes used synthetic records.

Workbook boundary checks cover zero versus missing values, duplicate dates with a missing measurement, coverage, tombstoned daily observations, product/ingredient label verification, unsupported units, missing label amount, deleted intake, duplicate product ID, mixed mass units and restoration. Canonical tests additionally cover finite numbers, ownership and lineage references, stable identity, tombstones, consent scope and conflict handling.

Initial XLSX conversion preserved cell values and layout but dropped ISO date cells and chart series. The builder now exports numeric date serials. Native repair restored all timestamp/date cells, set timestamp interpretation to UTC, and bound both charts to actual series. Native table metadata and dropdown options were verified. This is why every installer must read back the converted native objects rather than assume successful upload proves functionality.

## Installation friction and limits

Ten minutes to the first useful entry is a target, not measured customer proof. The template asks only for date, sleep, energy and a note. Identity/provenance assignment is part of partner handoff or the optional steward workflow before validated export. Detailed libraries are optional.

Google summaries cover rows 6–505. Exposure displays the first 20 ingredient lines and requests extension when the selected ingredient has additional lines. Native exposure uses UTC days and supports g/mg/mcg mass conversion; unsupported units or unresolved sources suppress the total. Canonical assistants can calculate local-day totals separately. Nested recipes, meal plans, goals and strength sets use JSON fields in this version. This is a usability limitation, not a promised native line-item editor.

Actual workspace permissions enforce access. Schema flags and Notion filters do not. No personal health data belongs in seller analytics, checkout metadata, public issues or partner receipts. A same-workspace duplicate is useful evidence but does not establish isolation or permissions in another customer account.

## Three-stage release decision

1. Stage 1: native template release candidate implemented. Complete one independent customer installation, rendered mobile review, export/restore and provider revocation; then test purchase/download delivery and publish an eligible template listing. Keep unpassed gates visible.
2. Stage 2: portable instructions and deterministic offline conflict/unit logic exist. Live imports, authenticated synchronization, scheduled agents and unattended writes are not implemented. Complete Edition owns measurements in Sheets, files in Drive and narrative reviews in Notion; no unnecessary bidirectional sync.
3. Stage 3: no hosted health application, mobile companion, paid community or recurring subscription was launched. Require demonstrated customer demand and a maintained private data boundary before building them.

Highest-return next action: appoint one delivery partner to run a fresh customer-account pilot using the provided acceptance receipt. The founder reviews the receipt and the release decision, rather than performing each installation.
