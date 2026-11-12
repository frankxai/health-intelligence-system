# Personal Health Intelligence OS

Version 0.1.0. Stage 1 release candidate. The product specification and schema are canonical; this document describes the buyer outcome and acceptance boundaries.

## Product decision

A customer buys an editable health workspace, keeps the records in their own Google or Notion account, and brings the AI assistant they already use. The product earns its value through consistent records, ingredient reconciliation, useful descriptive reviews, and portable context. It must work without a seller-operated database or a new AI subscription.

The first release serves AI power users who want one durable record of sleep, daily wellbeing, nutrition, training, symptoms, supplements, documents and experiments. A partner can install and personalize the workspace using synthetic examples, then hand control to the customer before real records are entered.

## Intended use

Personal record keeping, general wellness education, descriptive trends, source reconciliation and preparation for informed health conversations. Agents may aggregate product-label exposures and compare observations with customer-entered goals. Agents must not diagnose, interpret personal laboratory results, recommend medication or supplement dose changes, prescribe diet therapy, or deliver injury rehabilitation. A reference range copied from a laboratory remains a source field, never an automated judgement.

## Editions

| Edition | Structured records | Documents | Reviews | Release promise |
| --- | --- | --- | --- | --- |
| Google Workspace | Google Sheets | Google Drive | Sheets | Editable workbook, descriptive dashboard, structured libraries, protocols and portable instructions |
| Notion | Native Notion databases | Private attachment or owner storage URI | Notion | Daily cockpit, relational libraries, filtered views and reusable reviews |
| Complete Connected | Sheets | Drive | Notion | Both editions and explicit ownership map; automated projections belong to Stage 2 |

Stage 1 must not market automatic synchronization, continuously running agents, tested ten-minute installation, clinical interoperability, or all-platform write support before evidence exists.

## Core journeys

1. **Start:** choose edition, duplicate into a private owner workspace, select timezone and two priorities, leave unrelated modules unused, complete one daily record.
2. **Record:** enter known observations in a small daily surface. Leave unknown values blank. Capture a product label and ingredients separately from an intake event. A plan is never counted as a consumed item.
3. **Understand:** see a bounded date window, record coverage and descriptive averages. Inspect source rows behind every number. No composite health score or false precision.
4. **Review:** compare a declared outcome with baseline, surface missingness and confounders, choose one bounded observation or capture improvement. Preserve the distinction between an observed change and an intervention effect.
5. **Own:** export records with stable IDs, documents and provenance. Revoke assistant access without losing the workspace. Upgrade template structure without replacing customer rows.

## Information architecture

Daily Health Cockpit is the primary entry point. Supplement Intelligence Library, Food Intelligence Library, Sleep and Recovery Studio, Training and Performance Dashboard, Biomarker Explorer, Experiment Laboratory, Weekly Intelligence Review and Personal Health Timeline are views of shared entities. They must not create independent copies of the same observations.

The canonical schema covers 22 entities: profile, daily observations, products, label ingredients, intakes, foods, recipes, meal plans, hydration, sleep, training, recovery, symptoms/conditions, biomarkers, clinical documents, appointments, experiments, evidence, purchases, reviews, consent and audit events. Products distinguish supplements from medications. Conditions distinguish a user's report from a documented clinical record.

## Required Stage 1 behavior

| Requirement | Acceptance evidence |
| --- | --- |
| Daily check-in has an obvious entry surface | Fresh private install, enter a record, inspect saved row and dashboard dependency |
| Unknown differs from zero | Blank sleep is excluded from its average; reported zero training remains a valid observation |
| Ingredient arithmetic is explainable | Two fictional products provide 2 mg + 1.5 mg B6; two taken events yield 3.5 mg; planned/skipped events do not count |
| Provenance travels with exports | Every record includes source kind, source locator, confidence and owner identifier |
| No duplicate events after import | Reimport the same source dataset and confirm unchanged record count |
| Stale changes preserve customer data | Conflicting revisions enter a conflict receipt; existing values remain intact |
| Privacy is the default | No public real-data links, default AI permission false, no seller telemetry containing health data |
| Notion duplication preserves relation ownership | Duplicate into a separate customer workspace, inspect every relation target, confirm no seller source remains |
| Upgrades preserve data | Snapshot, dry-run migration, compare counts/IDs, apply additive change, verify rollback path |
| Partner delivery is concrete | Installation receipt identifies edition, version, owner, evidence, remaining limitations and revoked installer access |

## AI operation contract

Read the exact authorized records and provenance. Separate observed data, user reports, hypotheses and research findings. Propose a precise change or output with the reason and source. Apply only within the customer's explicit authorized scope, after reading the current revision. Return an audit receipt. Never silently alter an observation, invent a measurement, or treat a user statement as a verified label.

Assistant capabilities are adapter-specific. A connector being available is not evidence of a successful read/write workflow in a customer account. Portable manual instructions are the universal fallback. Customer OAuth and API credentials remain in the provider's connection system or the customer's local runtime.

## Release stages and measurement

| Stage | Actual scope | Exit evidence | Next highest-return action |
| --- | --- | --- | --- |
| 1: Sellable Template MVP | Native workspaces, synthetic demo, instructions, schema, offline validation, partner delivery | Fresh install, real native recalculation, relation remap, export, checkout/delivery rehearsal | One partner-delivered customer pilot with timed onboarding |
| 2: Connected Intelligence | Verified assistant adapters, import pathways, optional one-way projections | Platform-specific read/propose/apply receipts, consent revocation, stale-write and deletion tests | Automate the repeatedly observed installation bottleneck |
| 3: Premium Product Platform | Hosted/mobile experience and recurring service only after demand | Repeat usage, paid retention, support cost and privacy design validated | Build only the capability customers repeatedly pay to retain |

Initial success criteria: first useful check-in within ten minutes as a target to test; seven days of voluntary capture; weekly review completed; successful export; no unexpected sharing; partner handover without founder intervention. Track completion metadata only with consent. Avoid health outcomes as product success claims.

## Commercial boundary

€29 Google, €39 Notion, €79 Complete and €149–€299 installation are price hypotheses. A template purchase is one-time access to the stated version and maintenance policy. Managed recurring support requires a distinct contract, scoped access and consent; it must not imply clinical care. No automatic renewal or service promise follows from a template purchase.

## Current limitations

Local schema validation and synthetic arithmetic can prove deterministic logic. They do not prove native account installation, Notion relation remapping, actual assistant permissions, legal positioning, checkout delivery, or ongoing service execution. Release receipts must identify which of these were actually observed.
