# Privacy and trust architecture

Personal Health Intelligence OS · 0.1.0 · EU-oriented design, checked 12 November 2026

## Intended purpose

Organize a person's own records, source documents, user-set goals and self-reported observations. Provide descriptive summaries, data-quality checks and a record of decisions. The release does not diagnose, interpret laboratory findings, prescribe or change medication/supplement doses, or recommend treatment/training therapy.

Qualification follows the actual intended purpose, functionality and marketing. A disclaimer cannot undo a medical purpose. Before adding disease prediction, personalized clinical interpretation, treatment recommendations or a clinical decision workflow, reassess the product under the applicable MDR/IVDR framework using [MDCG 2019-11 rev.1](https://health.ec.europa.eu/medical-devices-sector/new-regulations/guidance-mdcg-endorsed-documents-and-other-guidance_en). No device classification, certification or regulatory exemption is claimed by this package.

## Data boundaries

| Boundary | Allowed data | Rule |
| --- | --- | --- |
| Commercial source and demos | Synthetic data, original instructions, source citations | No personal records, private source IDs, identifying examples, copied clinical files or family branches |
| Customer Google/Notion workspace | Customer records and chosen attachments | Customer owns workspace and access; initially private; no vendor access required |
| Customer's AI provider | Minimum context the customer explicitly chooses to provide | Separate customer/provider relationship; disclose connector scope and provider data settings |
| Commerce/support | Order details and operational support metadata | Never send health text, biomarkers, symptom labels, document titles or prompt transcripts to payment/analytics systems |
| Partner delivery receipt | Install version, platform, checks, completion and revocation state | Record successful checks without recording health values or screenshotting personal pages |

An account sign-in is not blanket consent to repurpose health data. [GDPR Article 9](https://eur-lex.europa.eu/legal-content/EN/TXT/?qid=1671832038722&uri=CELEX%3A32016R0679) treats health data as a special category. Business processing needs an Article 6 lawful basis and an applicable Article 9 condition; explicit consent is one possible condition. Articles 5 and 28 also require minimization and appropriate processor arrangements. The personal/household exception is not a basis for commercial partner processing. Assess actual roles and purposes before anyone accesses customer health records.

## Defaults implemented by the package

- Synthetic examples are clearly labeled and carry synthetic provenance. Blank values mean unknown; zero is a value.
- No telemetry endpoint, tracking pixel, public-agent connection, vendor database or required cloud function is bundled.
- Workspace and AI accounts belong to the customer. Credentials are never entered in template cells, agent prompts, export files or partner receipts.
- Shared dashboards contain operational install status only. Each customer receives an isolated workspace copy.
- A customer can operate manually without granting an assistant write access.
- Every proposed automated adapter is off until selected and verified. The Stage 1 package includes no automatic replication.

These are product defaults and boundaries, not a claim that Google, Notion or an AI provider offers end-to-end encryption, EU-only processing or zero retention. Customers review the chosen providers' terms, data controls, transfer terms and subprocessors. A professional customer or partner acting as a controller must determine whether a DPIA is required, particularly before larger-scale sensitive-data processing.

## Consent and access receipt

Record the customer-selected platform/account, purposes, data categories, recipient/provider, scopes, access duration, expected writes and revocation route. Keep assistant access, partner access and marketing consent separate. No preselected health-data consent. No public sharing by default.

Partner installation uses synthetic data while the customer remains present. The customer performs sign-ins. Prefer customer-operated screen share without recording; never collect passwords or recovery codes. Temporary collaborator access is exceptional, scoped and removed before acceptance. A filtered Notion view is not a privacy boundary.

## Export, deletion and retention

1. Export structured entities as CSV and versioned JSON, plus a human-readable Markdown review. Retain stable IDs, original units, observed/recorded times, timezone, provenance and explicit nulls.
2. Export attachments separately with a manifest. CSV export alone does not preserve Notion relations, files, permissions or formulas; retain the canonical relation map and test a selected record before relying on the archive.
3. Before deletion, customer may keep an offline encrypted archive. Remove selected records, attachments, mirrors and adapter queues; record the deletion receipt without retaining the deleted health contents. Disconnect assistants and revoke tokens.
4. Workspace trash, revisions, provider chats, backups and legal financial records have independent retention rules. Deleting a row or disconnecting an app does not certify deletion from every provider system. Request provider/account deletion where required and document its scope.
5. Proposed support policy: no health uploads accepted. Operational support tickets retained 90 days after resolution unless needed for an unresolved dispute or required record. Set this policy in the actual support system before launch. Accounting/order records follow the seller's applicable legal retention rules, separately from health data.

## Human permissions and change history

Users can edit their own records. Partner/admin roles are for install metadata only. Read-only reviewers get explicitly selected exports, never the master by default. Adapters append an audit receipt for every accepted mutation with actor, changed field names, prior/new revision hashes and source reference. Do not claim tamper-proof audit history in editable spreadsheets or Notion.

The vendor's v0.1.0 risk register must remain open until customer-isolation, duplicate/remap, download rights, account scope and revocation checks have passed. No GDPR compliance seal or medical safety guarantee is represented.
