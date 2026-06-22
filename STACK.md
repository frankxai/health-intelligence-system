# STACK - Health Intelligence System

## Inherited

- **Protocol:** Starlight Intelligence Protocol.
- **File contract:** README, SKILL, SOUL, AGENTS, MEMORY, STACK, CANON, SUB-SYSTEMS.
- **Evidence ledger:** Markdown source register with evidence-check dates.
- **Private data rule:** Real health data belongs in private local storage, not in this repo.

## Suggested Private Instance Layout

```text
HealthVault/
|-- 00-command-center/
|-- 10-records/
|   |-- labs/
|   |-- imaging/
|   |-- pathology/
|   |-- visit-notes/
|   `-- portal-exports/
|-- 20-doctor-visits/
|-- 30-daily-loops/
|-- 40-evidence/
|-- 50-jurisdiction/
`-- 90-exports/
```

`private/` and `HealthVault/` are private-instance concepts. Do not store real health data in this public repo.

## Optional AI Stack

| Mode | Tools | Rule |
| --- | --- | --- |
| Public/sanitized | GitHub, docs, examples | Fictional or sanitized data only |
| Consumer AI | ChatGPT, Custom GPTs, Projects | Share only deliberate context |
| Health AI | ChatGPT Health or equivalent | Keep health context separated from ordinary chat |
| Local-first | Obsidian, Codex/OpenCode/Hermes, Ollama, LM Studio, Open WebUI | Raw records stay local |
| Private infrastructure | Private APIs, model gateways, encrypted storage | Requires security and compliance review |

## Source Priority

1. Current clinician guidance from the treating team.
2. Specialty society or guideline bodies relevant to the cancer type.
3. USPSTF/CDC for population screening.
4. NCI for cancer education, treatment-type overview, clinical trial, and survivorship questions.
5. Peer-reviewed papers only when the document needs a research note and the evidence is not already covered by guidelines.
6. External AI/agent systems only as product architecture references, not as clinical authority.

## Freshness Rule

- Screening summaries: check sources before publishing.
- Treatment content: never present regimen-level guidance as current unless tied to a clinician-verified plan.
- Clinical trial content: always verify against the live trial record and care team.
- Personal health ops content: recheck AI product, privacy, local-LLM, and jurisdiction sources before publishing public instructions.

**Built on SIP** - Health Intelligence System STACK.md v0.1
