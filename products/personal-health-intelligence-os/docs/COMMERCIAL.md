# Commercial release brief

Personal Health Intelligence OS · 0.1.0 · proposed offer, 12 November 2026

## Positioning decision

Sell an owned health record workspace with clear data lineage and a short daily capture flow. The buyer purchases curation, editable interfaces, installation materials, quality assurance and optional setup. Do not sell medical outcomes, clinical interpretation or autonomous supplement advice.

Start with founders, creators and AI power users already using Google or Notion. Their first job is to replace scattered notes with a useful check-in and a consistent weekly review. Fitness/PKM users are adjacent. Coaches/practitioners and teams require additional consent, isolation and professional-role design; they are not the first release's default deployment.

## Offer and release scope

| Offer | Price hypothesis | Purchase model | Release boundary |
| --- | ---: | --- | --- |
| Google Workspace | €29 | One-time editable template package | Native Sheets, docs, guide, synthetic examples and portable instructions |
| Notion | €39 | One-time editable template package | Dashboard, databases, views, synthetic examples and portable instructions |
| Complete Connected | €79 | One-time bundle hypothesis | Bundle/integration specification only until Stage 2 sync and clean-customer installation pass. Do not market automatic sync as shipped |
| Partner Setup | €249 | Separately contracted one-time service | Configure one selected edition; synthetic acceptance; handoff and revocation. Price does not include unlimited import or clinical personalization |

These prices are hypotheses, not validated willingness to pay. Establish consumer-facing tax-inclusive display, final fees, support scope and delivery rights in the selected checkout before publishing. No recurring software fee is justified at Stage 1. Customer workspace/assistant subscriptions are separate.

## Alternatives and defendable value

| Alternative | Already good at | Product's proposed reason to buy |
| --- | --- | --- |
| [Notion health and fitness templates](https://www.notion.com/templates/category/health-fitness) | Editable trackers and personal dashboards, including free choices | Versioned schema, tested install path, provenance, unknown-data handling and complete export instructions |
| [Bearable](https://bearable.app/support/common-questions/bearable-free-vs-premium-features/) | Free symptom/mood/sleep/medication/nutrition tracking and CSV export; premium adds correlation reports and expanded history | Sell workspace customization and source-linked libraries only where buyers want them. Do not claim competitors lack exports or AI-compatible data |
| [Exist](https://exist.io/) | Manual tracking plus service syncing, correlations and weekly summaries; individual plan publicly lists $6.99/month or $62.90/year | Own-workspace schemas and editable workflows are the differentiator hypothesis. Exist already supports [PDF/CSV/JSON export](https://kb.exist.io/article/14-how-do-i-export-my-data) |
| Native spreadsheets | Flexible owned tables and calculations | Curated workflow, working visual hierarchy, synthetic training data and reproducible validation |
| Apple Health / wearable apps | Device-led measurement capture. [Apple documents XML export](https://support.apple.com/en-euro/guide/iphone/iph5ede58c3d/ios) | Add documents, user reports, source-linked reviews and portable records across chosen tools. Automatic Apple/wearable import is not shipped |
| [Android Health Connect](https://support.google.com/android/answer/13770320?hl=en) | On-device health/fitness/medical data exchange between permitted apps; [granular read/write permissions](https://support.google.com/android/answer/12201230) | Treat as a future customer-controlled data source, not a replacement target. This package has no tested Health Connect adapter |
| Generic AI conversation | Convenient discussion | Persistent user-owned records, explicit change proposals and a reproducible record of what was actually entered |

These are positioning hypotheses, not evidence of competitive superiority. A template can be copied; the defensible investment is clean-install reliability, maintained adapters, transparent evidence and an effective partner delivery network.

**Product implication:** do not rebuild mature mobile symptom capture or correlation pipelines in Stage 1. Keep the editable workspace as the decision/document layer. Validate whether a small import from an existing tracker delivers more value than another custom input form. An import must preserve source IDs, times, missingness and provenance and pass fixture tests before being offered.

## Commerce decision

Prefer a hosted digital-download checkout. Provisional choice: Polar Starter for digital editions, subject to product acceptance, seller onboarding and account readiness. This reduces tax administration and avoids a custom checkout build. Reuse an existing approved merchant-of-record account when it is already operational. Seller-account activation and the checkout-to-download test remain required; neither occurred in this research work.

Existing infrastructure identified by the parent repository audit: `frankxai/frankx.ai-vercel-website` contains `app/api/webhooks/stripe/route.ts` at commit `5aa442cc01399f3d2e14a37e7a1fec6e6ddb1511`, with `stripe` dependency `^22.6.2`. This is evidence of code reuse potential, not an active merchant account, configured health-product SKU, accepted MoR enrollment or working delivery workflow. Read the route and existing conventions before implementing a product entitlement. No new custom checkout has been built for this pack.

| Provider | Verified public position | Material tradeoff |
| --- | --- | --- |
| [Polar](https://polar.sh/resources/pricing) | New org Starter 5% + $0.50; +1.5% non-US cards. Earlier orgs can retain a distinct Early Member rate. Merchant of record | Payout/FX/dispute fees may apply; seller approval and digital-product fit required |
| [Lemon Squeezy](https://www.lemonsqueezy.com/pricing) | 5% + $0.50 baseline, no ecommerce monthly charge; merchant of record | [Extra fees](https://docs.lemonsqueezy.com/help/getting-started/fees) include non-US, PayPal, subscription and payout cases |
| [Gumroad](https://gumroad.com/pricing) | Hosted digital products; merchant of record; 10% + $0.50 direct, 30% Discover | [Fee help](https://gumroad.com/help/article/66-gumroads-fees) also lists card processing 2.9% + $0.30 for direct sales. Confirm actual transaction fees |
| [Stripe](https://docs.stripe.com/payments/managed-payments/how-it-works) | Standard Stripe is payment processing; Managed Payments is a separate merchant-of-record flow for eligible digital sales | [Managed Payments adds 3.5%](https://support.stripe.com/questions/managed-payments-pricing?locale=en-GB) to processing; country/product eligibility and coverage apply. Ordinary Stripe service invoicing leaves seller tax responsibility |

Rates checked 12 November 2026. Fixed fees are quoted in provider currency, not converted to euros. Do not rank using a headline rate alone; compare the same buyer country, tax-inclusive amount, card type, currency and payout schedule.

**Separate setup-service billing:** [Polar's current AUP](https://polar.sh/legal/acceptable-use-policy) is oriented to digital deliverables and says businesses primarily offering human services should not use it. Do not create a €249 consulting/setup Polar SKU without explicit provider acceptance. Contract and invoice eligible partner setup separately through the established seller/partner service process; verify VAT and consumer terms for that service.

## Distribution and validation plan

Prepare one synthetic before/after demo, one concise product page and one useful free check-in preview. Use FrankX's own editorial channel first, then a small invite-only pilot from existing interested people. Nothing in this package authorizes outreach, publication or automatic messaging.

Run five independent customer installs before treating Stage 1 as generally ready. Proposed gates: at least four reach the first useful check-in within 10 minutes; every installation preserves private access and exports a known record; no customer needs founder intervention after receiving the partner handoff; at least three continue weekly review into week two. Record time and failures, not health measurements. These are proposed targets, not achieved results.

Test the €29/€39 offers at actual checkout with truthful scope. Complete Edition can be a clearly labeled waitlist until connected acceptance exists; do not collect payment for an unstated future sync promise. A paid pilot needs complete delivery/refund terms. A free preview must not require health data.

## Publication checklist

- Digital package license preserves the existing MIT core and required notices. Do not claim exclusive rights or impose contradictory redistribution restrictions on MIT-derived source. Sell service, maintenance and curation honestly; obtain review before introducing separately licensed original assets.
- Final screenshot/demo uses the exact released revision and synthetic labels. Claims match verified features.
- Seller identity, support contact, compatibility, tax-inclusive final price, delivery, statutory rights, refund policy and support/update period are set.
- For immediate digital access, implement applicable express-consent/acknowledgement and durable confirmation requirements. Do not claim a blanket no-refund policy. [EU consumer guidance](https://europa.eu/youreurope/business/selling-in-eu/selling-goods-services/ecommerce-distance-selling/index_en.htm).
- One live low-value test purchase/refund and private delivery/duplicate test passes. Store a receipt without customer health information.
- Commerce events contain SKU/order/license metadata only. No health data enters webhooks, audience targeting, analytics or affiliate URLs.

## Release economics and next decision

Do not add paid SaaS subscriptions before demand. Initial budget: existing workspace tools, existing hosting and transaction fees only. Measure support minutes, first-check-in time, delivery failures, refunds and week-two continuation. Reconsider a recurring plan only when customers repeatedly pay for a specific ongoing service and its operating cost is understood.
