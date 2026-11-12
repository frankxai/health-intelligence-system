# Install your Personal Health Intelligence OS

Version 0.1.0. Native templates are private release candidates. A ten-minute first check-in is a target, not yet a measured customer result.

## Choose one home for records

| Edition | Structured records | Files | Decisions |
|---|---|---|---|
| Google | Google Sheets | Your private Drive | Reviews tab / supplied review document |
| Notion | Notion databases | Your own private file space | Reviews database |
| Complete, Stage 2 | Google Sheets | Your private Drive | Notion narrative reviews |

Use one person's records per installation. Do not enter personal data into a product master. Check current native asset URLs in the installation manifest supplied with the release. Public template duplication and checkout are not enabled in this release candidate.

## Google edition

1. Open the native Google master and use File → Make a copy into your own private folder. Copy the supplied protocol documents. Keep the new IDs in your installation receipt.
2. Confirm sharing is restricted to you. Create folders for source documents, imports, exports and backups. The seller and delivery partner do not need ongoing access.
3. Practice once with synthetic rows. Change one Daily sleep value and confirm Cockpit updates. Select the sample UTC day in Exposure and confirm 3.5 mg is the fictional ingredient total. Restore the practice change.
4. In your copy, clear sample data rows on all 22 record tabs. Preserve headers, formulas on Cockpit/Exposure, tables and validation. Do not delete columns. Set the review date to your current local calendar day.
5. Add a Daily row with date, sleep hours, energy and a note. Leave unknowns blank. The steward adds stable IDs and provenance before a validated canonical export or merge. Make this identity assignment part of partner handoff when no AI is connected.
6. Use detailed event tabs only when useful. Daily contains a chosen summary and is not added to event totals. Date-time columns and the native Exposure day use UTC. The original IANA zone remains in Timezone. An assistant can produce local-day exposure using the canonical rules separately.
7. Download your own workbook as XLSX and record tabs as CSV. Canonical CSV source files in the package use machine field names. Native exported CSVs use human labels; map them with adapters/mappings.json. Nested goals, recipe ingredients, meal items and strength sets use JSON cells in this version. Validate before using a parsed canonical dataset.

Cockpit formulas cover rows 6–505. Exposure displays the first 20 ingredient lines. Extend formula ranges before exceeding those limits. Mass conversions in native Exposure support g, mg and mcg; other units require review and suppress the selected total. It is label arithmetic, not a dose recommendation.

## Notion edition

1. Duplicate the whole Notion Edition page, including child databases and views, into your own private workspace. Customer cross-account duplication has not yet been verified. Stop and contact the installer when a view still points outside your copy.
2. Confirm every view and product relation targets the new copy. A filtered view is not a permission boundary. Keep only your account on the real working copy.
3. Practice adding a Daily entry through the inline table. The entry should appear in the dated timeline and energy chart. Remove synthetic rows from your private copy before using it for your own records.
4. Enter date, sleep, energy and a note. Avoid filling every property just because it exists. New native page UUIDs can become stable canonical IDs when Record ID is empty. Retain existing IDs during migration.
5. Use library cards, experiment boards and weekly reviews. Relations connect products, ingredient lines, intakes and source documents. Recipe ingredients and training sets remain JSON-backed fields in this version; human-readable instructions are in the page body.
6. Export Markdown and CSV with subpages. Preserve attachments separately. Validate all relations, IDs, unknown values and timezone conversions before relying on a canonical reconstruction. The automated live exporter is not installed.

## Optional AI assistant

Install the portable role instructions from agents/README.md in your chosen assistant. Discover current read/write capabilities before promising an action. Grant the smallest available workspace scope. Where selected-page or folder scope is unavailable, prefer selected exports over broad access. Prove one synthetic read, one proposed write and one readback. Record the destination, purpose and revocation path in Consent. Consent fields document intent; they do not enforce provider authorization.

No assistant, automation or synchronization service is started by these templates. Platform permissions and approval prompts still apply. An export-based daily and weekly workflow remains available without live write tools.

## Upgrades and recovery

Export and back up your current copy first. Install new structure alongside it, never over customer records. Compare schema versions. Validate a mapped import and preview duplicate/conflict decisions by stable ID and expected revision. Retain a conflict queue and the original export. Apply only reviewed changes, keep an audit receipt and verify counts, units, dates and relations. Roll back to the original copy when checks fail.

Revoking an app stops future access but does not delete past exports or provider-held copies. Delete copies and exports separately according to the customer's retention choices and each provider's controls. Leave real health values out of seller support tickets, receipts and analytics.

## Partner acceptance

The installer must demonstrate a first entry, native recalculation, private sharing, export, restore and revocation, then provide a receipt with version, object IDs, scopes and pass/fail checks. No health measurements belong in that receipt. See PARTNER_DELIVERY.md for the fixed service scope and escalation rules.
