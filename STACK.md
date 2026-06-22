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

## Installable Agent Stack

| Surface | Path | Use |
| --- | --- | --- |
| Codex plugin | `plugins/health-intelligence-system/` | Install the repo-local health operator skill and references. |
| Codex skill | `plugins/health-intelligence-system/skills/sovereign-health-operator/` | Run private setup, wearable ingestion, clinician handoff, and safety checks. |
| Prompt pack | `prompts/` | Configure ChatGPT Projects, Custom GPTs, Claude Projects, and local redaction assistants. |
| Command pack | `commands/` | Import slash-command style workflows into coding agents or local automation. |
| Private vault templates | `templates/` | Copy into Obsidian, local folders, or an encrypted workspace. |

Tiny local models are optional privacy reviewers, not medical reasoning engines. Use deterministic/manual redaction first; small local models may help flag names, IDs, dates, and obvious private fragments before any hosted AI call.

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
- Wearable and API docs: recheck Apple, Android Health Connect, Oura, WHOOP, and Health.md references before publishing connector guidance.
- Agent installation docs: recheck Codex, Claude, OpenCode, ChatGPT, Ollama, LM Studio, and Open WebUI instructions before publishing operational setup guidance.

**Built on SIP** - Health Intelligence System STACK.md v0.1
