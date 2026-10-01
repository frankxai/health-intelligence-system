# Health Second Brain — product and implementation direction

Decision record: 2026-09-06. Status: development increment; existing clinical/privacy review gates remain pending.

## Decision

Extend Health Intelligence System as the reusable protocol and skill source; Agentic Health OS remains the health domain within Agentic Life OS. Use one private health memory across multiple chosen surfaces. Do not create another repository, generic chatbot, device dashboard, or public personal-data plane.

User promise: **Turn scattered health information into a week you can act on.**

Health supports a person's capacity to live and work; it does not fully determine destiny or imply blame for illness. Food, movement, recovery, environment, resources, genetics and access to care all matter. The product helps users make informed choices without promising control over every outcome.

## First buyer and value

Initial buyer hypothesis: an adult knowledge worker or creator who already exercises, has fragmented notes or wearable exports, and wants a realistic routine that survives work and travel. They buy less repeated explanation, clearer choices, and useful follow-through. This is a hypothesis; repositories and software tests do not establish demand.

First valuable session: import one selected source or summarize an existing routine; produce a source-linked review, a practical next action, and a reusable private context summary in under ten minutes. No device purchase, full-history intake or calorie target required.

Business model to test: free public skill and protocol; paid self-serve activation kit with templates and guided setup; recurring payment only for demonstrated ongoing connector/review value. Test a €49 activation offer as a pricing hypothesis, not a listed product or validated price. Do not sell medical advice, sensitive-data access or unreviewed health-outcome claims. Avoid 1:1 dependency.

## Existing foundation and increment

| Component | Inspected state | Increment |
|---|---|---|
| Public HIS | v0.2.1 protocol, operator skill, templates, gut vertical and release verification | Health Second Brain skill, daily analyzer, fictional fixture, tests and integration contracts |
| Agentic Life OS | Private hardening source; strict descriptor/policy boundaries; report-only runtime | Health experience and adapter design added to that boundary |
| Health package | Static wellness briefs; non-authoritative policy simulation | Keep authority unchanged; place personalized processing in authorized private execution |
| Dashboard | Read-only synthetic architecture page | Detailed daily/weekly UX specification; visual verification pending |
| Personal instance | Separate private overlay concept | Owns actual health data, selections and credentials; no personal data copied here |

This increment adds useful local file analysis through the skill. It does not implement cloud persistence, provider OAuth, native device bridges, a deployed MCP endpoint, or public marketplace distribution.

## User jobs

| Moment | User need | Product response | Constraint |
|---|---|---|---|
| Starting | “Use what I already have.” | Goal, constraints, chosen tools, one optional import | Never require all integrations |
| Shopping or cooking | “Make good food easier this week.” | Familiar meal combinations, budget/time-aware groceries, substitutions | Respect allergy and prescribed-diet constraints; no food morality |
| Before training | “Help me keep my plan realistic.” | Existing-plan review, time/equipment options, completed-session context | Wearable scores do not clear exercise or prescribe rehabilitation |
| Desk or travel day | “Help me move comfortably.” | Optional position changes, short movement opportunities, travel fallback | No posture diagnosis or perfect-alignment claims |
| Weekly review | “What changed, and what should I adjust?” | Coverage-aware observations, one chosen action, next review | No fabricated baseline, score or causal certainty |
| Health concern | “Help me explain this clearly.” | Source-linked timeline and clinician/pharmacist questions | No medicine changes, interpretation or false reassurance |
| Changing tools | “Keep what the system learned.” | Versioned export with units, sources and corrections | Summary is still sensitive; permissions are destination-specific |

## Memory architecture

Use seven logical objects: Context, Observation, Source, EvidenceClaim, Decision, Experiment and CareBrief. Keep them in one private system of record, with explicit minimal projections into chosen tools.

Observation keys: opaque ID, metric, value/unit, observed timestamp or local day, source timezone/day convention, source reference, method (measured/self-reported/estimated), ingestion time, quality status and superseded-by reference. Provenance is retained when a record is corrected or imported twice.

A fact, an estimate and a hypothesis have separate types. Evidence level, source integrity, clinical applicability and source recency are separate attributes. A consent flag in an uploaded JSON file is not authority.

Runtime flow:
1. Authenticate the person and derive tenant/subject from the server session.
2. Check currently scoped consent for the exact data/action/destination.
3. Ingest through a source-specific adapter; normalize units and local dates.
4. Reconcile duplicates/conflicts; retain lineage and source-choice history.
5. Compute deterministic descriptive metrics.
6. Retrieve only necessary context for an optional model synthesis.
7. Present evidence, limits and the proposed action; record user adoption.
8. Export only a reviewed scope to an authorized destination; log a minimal receipt.
9. Revoke future access and handle deletion of stored/derived copies as distinct operations.

The public ALOS simulator remains report-only. These are private-adapter requirements, not a claim that a production authority store exists.

## Tool choices

| User setup | Useful now | Engineering still required |
|---|---|---|
| ChatGPT Work | Installed skill, selected export analysis, research, documents and supported apps | App authorization and actual tool availability checked per account |
| Codex | Analyzer, validators, adapters, custom reports and reproducible fixtures | Private runtime deployment for unattended service |
| Drive / Notion | Explicitly selected context and review documents through available connectors | A single source of truth and deliberate sensitive-data scope |
| Local files / Obsidian | Markdown context and standardized daily CSV | Encryption/backup setup and source-specific imports |
| Apple Health | Deliberate export path where supported | Native HealthKit bridge and permissions |
| Android / Health Connect | Deliberate export or user-provided notes | Android companion, feature detection, permissions and revocation |
| WHOOP / Strava | Integration design grounded in provider OAuth docs | Registration, scopes, credentials, consent, rate limits and tests |
| Garmin | Developer-program evaluation | Access verification and adapter implementation |
| Oura / other providers | User-selected exports and capability discovery | Current API/access verification; no assumed scopes |
| Caliber / COROS / Tredict / other plugins | Evaluate only when installed and callable | Listed/recommended plugins are not installed connections |

## ChatGPT integration

Use skills to package reasoning workflows; an MCP server only where live state or actions justify it. Current OpenAI docs support skill-only plugins and optional MCP UI. Keep retrieval and rendering separate:
- Data tools return bounded authorized data or opaque review IDs.
- The model can inspect evidence before requesting a view.
- A render tool re-resolves the review under the active user's authorization and attaches its UI resource.
- Write tools use server validation, current consent, idempotency and explicit action scope.
- A widget does not receive credentials, raw medical files, broad context or caller-minted authority.
- A failed or revoked source appears as missing/stale, never connected or healthy.

Proposed tools: get_context_descriptor, list_source_status, prepare_wellness_review, render_wellness_review, propose_routine_change, prepare_care_brief, preview_export. Actual persistence/export stays with an authenticated private adapter. Do not advertise these tools as live.

## Quality and model allocation

Deterministic code owns parsing, units, dates, arithmetic, deduplication and schema validation. A model can help extract/structure selected notes, synthesize evidence and phrase useful questions; derived claims retain uncertainty. Use human verification for extracted allergy/medicine details and care decisions.

Evaluate on synthetic fixtures before any user data: source changes; sparse days; contradictory observations; nonfinite numbers; timezone/day errors; stale evidence; revoked permission; cross-tenant ID; prompt injection in records; false calorie certainty; medication substitution; posture diagnosis; body-image pressure; export previews; retry/idempotency; correction/deletion propagation.

No opaque overall health score. Show coverage, origin, age and uncertainty near each claim. Optimize for time to first useful decision, repeat voluntary use, burden, correction rate, and successful data portability. Health outcomes require an appropriate study, not a retention chart.

## Sequence and ownership

| Window | Owner | Deliverable | Evidence gate |
|---|---|---|---|
| Now | HIS maintainer | Skill, analyzer, contracts, synthetic test cases | Automated parsing/aggregation tests and independent skill trial |
| Next 72 hours | Product owner | Five voluntary self-serve trial sessions using existing tools | At least four produce a useful review without setup assistance; measure friction |
| Days 4–14 | Product + UX | One visually verified review flow; activation offer test | Users can distinguish source data, inference and action; record willingness to pay |
| Days 15–30 | Private runtime maintainer | One export adapter and authenticated private review path | Isolation, revocation, correction and restore tests; no raw data in telemetry |
| Days 31–90 | Integration owner | One demand-led live connector and optional ChatGPT view | Provider access secured, consent/refresh/retry/deletion behavior tested, retained use demonstrated |

Stop or simplify recurring SaaS when users do not return for the review or when integration costs exceed demonstrated willingness to pay. Keep the free skill useful. Do not build a native app merely because a bridge is technically possible.

## Source ledger

Provider capabilities checked 2026-09-06; availability still varies by account. URLs document platforms, not completed integrations.

- [OpenAI plugins](https://learn.chatgpt.com/docs/plugins): skills/connectors and supported surfaces.
- [MCP server concepts](https://developers.openai.com/plugins/concepts/mcp-server): optional server and tools.
- [MCP UI](https://developers.openai.com/plugins/build/chatgpt-ui): separate data and render tools.
- [Security and privacy](https://developers.openai.com/plugins/guides/security-privacy): input validation and data scope.
- [Health Connect](https://developer.android.com/health-and-fitness/health-connect/get-started): native feature/permission checks.
- [HealthKit](https://developer.apple.com/documentation/healthkit/authorizing-access-to-health-data): authorization entry point; rendered content was limited, so implementation specifics remain unverified.
- [WHOOP OAuth](https://developer.whoop.com/docs/developing/oauth/): app registration and scoped authorization.
- [Strava authorization](https://developers.strava.com/docs/authentication/): OAuth and token handling.
- [Garmin program](https://developer.garmin.com/gc-developer-program/overview/): program scope; account acceptance unverified.
- [WHO diet](https://www.who.int/news-room/fact-sheets/detail/healthy-diet) and [physical activity](https://www.who.int/news-room/fact-sheets/detail/physical-activity): general education foundations, not personal treatment protocols.
