# Partner-led setup and handoff

Personal Health Intelligence OS · 0.1.0 · operating kit

The founder should own product quality and the release decision. A delivery partner owns installation, account compatibility checks, the synthetic acceptance test and customer handoff. A partner is not permitted to provide clinical advice through this product.

No partner has been recruited, contacted or booked by this release. No delivery capacity, certification or response-time commitment is represented as live.

## Sellable service scope

**Proposed price: €249 per customer**, separately contracted and invoiced. Final tax-inclusive consumer price and VAT treatment must be set by the service seller. One selected Google or Notion edition, one workspace owner, one preferred assistant connection, one setup session and one correction pass within seven days. Budget 90 minutes of partner labor plus a 15-minute correction reserve. Price includes no paid workspace/assistant subscription, large migration, automated sync development, medical interpretation or ongoing health coaching.

Suggested internal partner labor ceiling: €100, subject to actual agreement and tax treatment. This is a planning allocation, not a promised margin or signed compensation. Route overscope work to a written quote before taking it on. The founder handles exceptions only when a release defect or unresolved platform limitation blocks the documented path.

## Responsibilities

| Owner | Responsibility | Acceptance evidence |
| --- | --- | --- |
| Product maintainer | Versioned source, package rights, known limits, defect fixes | Release manifest and accurate compatibility ledger |
| Delivery partner | Install from approved release, verify chosen account, document friction, handoff | Synthetic test receipt with target/version and pass/fail results |
| Customer | Own accounts, perform login, select access, enter real data, approve writes | Workspace ownership confirmed; revocation performed |
| Commerce/service seller | Contract, payment, invoices, consumer rights and support routing | Order/service record with no health content |

## Runbook

### Before the session

Send only the synthetic preview, installation guide and account prerequisites. Ask which edition/account/assistant is selected and whether the customer wants manual mode or a connection. Do not collect health history. Verify the product version and known limits. Keep customer/order ID separate from workspace data.

### During the session

1. Customer creates/duplicates the template into their own private workspace. Partner operates on the synthetic layer only; customer performs every OAuth/login step.
2. Verify edition, owner, timezone, schema version, blank-start instructions, record IDs, relations and source labels. Record manual actions and elapsed time.
3. Run one synthetic daily check-in with one missing value and one valid zero. Confirm only the reported values are stored, and the dashboard updates.
4. Run assistant read/propose/write/readback only with customer-selected access and consent. If writing is unsupported, demonstrate the documented manual workflow and mark the adapter unsupported; never advertise the connection as fully working.
5. Export the known synthetic record and inspect its ID, unit, date, provenance and relation mapping. Demonstrate correction without overwriting another record.
6. Customer removes synthetic demo records from the personal copy using the documented demo-only filter/list, or creates a blank-start copy; verify the dashboard empty state. Never clear an existing customer database to get a clean screen.
7. Remove temporary partner collaboration, revoke the connection, and verify it stops working. Customer can reconnect afterward. Confirm no public links or unexpected guests.

### Handoff

Customer runs their first real check-in privately. Partner sees only completion confirmation, not values. Deliver a receipt and a concise next-action note. Provide self-service export/deletion and support routes. Delete partner-held transient material; no recordings or screenshots containing health information.

## Receipt template

```json
{
  "receipt_version": "0.1.0",
  "install_id": "customer-generated-uuid",
  "product_version": "0.1.0",
  "edition": "google-or-notion",
  "workspace_owned_by_customer": true,
  "assistant": "customer-selected-or-manual",
  "synthetic_only_during_setup": true,
  "first_checkin_elapsed_minutes": null,
  "checks": {
    "private_access": "not_run",
    "relations_remapped": "not_run",
    "blank_and_zero": "not_run",
    "dashboard_recalculates": "not_run",
    "assistant_read": "not_run",
    "assistant_write_or_manual": "not_run",
    "export_reopens": "not_run",
    "access_revoked": "not_run"
  },
  "temporary_partner_access_removed": false,
  "health_values_collected_by_partner": false,
  "known_limits": [],
  "customer_accepted_at": null
}
```

Replace the install ID with a real UUID. Allowed checks: pass, fail, not_run, unsupported. Do not treat not_run as pass. This receipt intentionally excludes account emails, medical values, document titles, tokens and clinical content. Keep identifiers required for service support in the separate order record.

## Partner qualification

Before accepting customers, a candidate must install both editions from a clean account, demonstrate relation remapping and export, reproduce a missing-data case, and revoke its own access. Review the actual receipt. Credentials in a shared chat, a multi-client health dashboard, copied clinical files or unsupported medical advice are disqualifying practices. A public certification badge requires a real evaluated program; none exists in v0.1.0.

## Operational queue

Use the existing business operations tracker. Fields: install ID, edition, release, partner, booked time, elapsed setup, acceptance state, blocking defect, correction due and access-removed state. No symptoms, names of medications, labels, laboratory data or health goals in this queue. Do not create a second health CRM.

## Scale trigger

Document the five pilot installs before delegating broad sales. Convert recurring failures into product fixes, then shorten the runbook. After ten accepted installs, calculate true labor, refund and support costs before changing partner compensation or adding recurring managed services. No automatic messages or partner outreach are configured by this package.
