# Public Core, Public Reference Apps, Private Health Runtime

**Decision date:** 2026-08-24
**Safety boundary:** architecture and privacy guidance, not medical, legal, security, or compliance advice.

## Decision

Keep reusable code and safety contracts public; keep every real person's health data in a private, encrypted instance they control.

| Layer | Default visibility | Holds real health data? | Role |
| --- | --- | --- | --- |
| `health-intelligence-system` | Public | **No** | BIOS schemas, validators, evidence contracts, safe domain-agent registry, fictional fixtures, templates |
| `agentic-life-os` reference code | Public | **No** | General life application shell that may consume released HIS contracts |
| Personal encrypted runtime | Private/local | **Yes, when the person chooses** | Vault, consent grants, raw records, wearable files, local indexes, reviewed exports |
| Optional personal repo such as `frankx-life-os` | Private only | Only encrypted or deliberately minimized data | Frank-specific configuration and orchestration; not a public product dependency |

Making application code public does **not** make a deployed health workspace public. Git history, GitHub issues, CI logs, Vercel previews, analytics, error trackers, and public AI chats are not personal-health vaults.

## Runtime Rules

- A public demo uses fictional synthetic records only.
- Raw PDFs, images, portal exports, wearable streams, identifiers, and private memory stay outside public Git.
- The local vault is the source of truth. Cloud backup is optional, encrypted before upload, and tested with a restore drill.
- Vercel or another public web host may serve the documentation/demo shell; it must not receive personal health payloads by default.
- Any AI egress compiles through active consent plus the subject's default-deny sensitivity policy.
- The v0.1 reference exporter refuses grants with a non-empty field allowlist until field-level compilation is implemented; it never treats an unsupported narrow grant as broad consent.
- A clinician handoff is created locally, shows an omission/redaction receipt, and is reviewed by the person before a separate sharing action.
- A public reference app must remain useful without Frank's private instance or unavailable private packages.

## Repository Gate

Do not create `vitalis-*`, `velora-*`, or a new private health repository merely to reserve a name. First require a distinct maintainer, five substantial artifacts, a different safety boundary, a public/private data policy, executable validation, and a useful first release. Until then:

- HIS owns the public health protocol and BIOS runtime contract.
- Agentic Life OS may own the public multi-domain reference application.
- A private encrypted vault or `frankx-life-os`-style instance owns one person's live data and configuration.

## Name Independence

Machine contracts use stable neutral IDs. Candidate experience names can change without migrating health data or breaking integrations:

- `agent_bios_steward` is the stable public general-health steward identity. Vitalis may
  remain a private memorial codename only; it is not a public alias.
- `agent_training_foundations_educator` is the neutral public training identity. Velora
  remains reserved for Arcanea's established Executor persona; it is not a fitness alias.
- Martial-arts movement, culinary botanicals, and complementary-practice education use neutral public labels.

Neither Vitalis nor Velora is a public health/fitness product candidate in this release.
Do not make trademark, domain, store-handle, medical-device, or market-availability
claims from these files. A future exception requires a new qualified legal clearance
decision, not merely a repository edit.

## Non-Negotiable Boundary

Public code can help people own their health information. It cannot turn a public repository into a medical record, a public model into an undisclosed data processor, an educational agent into a clinician, or an evidence lead into personal treatment advice.
