# External Systems Comparison

**Evidence checked:** 2026-06-22  
**Scope:** comparison of external AI health, personal health record, clinical-agent, interoperability, research-agent, and local/private LLM systems that Health Intelligence System should reference, integrate with, or explicitly avoid emulating.  
**Safety boundary:** This is product and system design research. It is not medical, legal, privacy, security, or compliance advice.

## Classification Legend

| Classification | Meaning | HIS action |
| --- | --- | --- |
| `reference` | Strong pattern to learn from, cite, or adapt conceptually | Include in design notes and source ledgers |
| `integrate later` | Useful future technical connection, but not required for the markdown-first v0.2 protocol | Track as a later pack, connector, or app layer |
| `watchlist` | Relevant but immature, fast-changing, or too broad to depend on now | Recheck before adopting |
| `do not emulate` | Interesting but unsafe, overclaimed, too clinical, or misaligned with person-owned records | Mention boundary and avoid copying the pattern |

## Executive Read

The external ecosystem is strong, but fragmented.

- Open-source personal health assistants focus on data consolidation and chat.
- Clinical-agent research focuses on benchmarks, EHR reasoning, simulated encounters, and tool use.
- Healthcare standards focus on interoperable record access.
- Life-science agent systems focus on research, not personal care.
- Local LLM tooling provides privacy options but does not create a health workflow by itself.

Health Intelligence System should occupy the missing protocol layer: a person-owned, local-first, markdown-native, clinician-handoff-oriented system that can use these tools without turning the model into a doctor.

## Personal Health And Local-First Systems

| System | Category | Useful pattern | HIS classification | HIS decision |
| --- | --- | --- | --- | --- |
| OpenHealth | Open-source AI personal health assistant | Consolidates health data, parser layer, local and commercial models, local Ollama path | `reference` | Learn from its data ingestion and local execution posture; keep HIS lighter and file-native |
| Health.md | Apple Health export to Markdown/JSON/CSV/Obsidian | Turns wearable/Apple Health data into portable files | `integrate later` | Use as an optional ingestion bridge for wearable and Apple Health data |
| Google PH-LLM | Research model for personal health signal interpretation | Shows LLM value around sleep, fitness, and wearable-derived context | `reference` | Cite as evidence that personal health insight is an active research frontier |
| Google PHIA | Agentic wearable-data personal insight research | Shows agent workflows over wearable data | `watchlist` | Track for insight-agent patterns; do not claim equivalent clinical validity |
| Second Brain OS | Local two-vault Obsidian and coding-agent memory pattern | Hard privacy boundary between public/agent-readable and private vaults | `reference` | Absorb the two-vault pattern into HIS private vault guidance |

## Clinical Agents, Medical RAG, And Benchmarks

| System | Category | Useful pattern | HIS classification | HIS decision |
| --- | --- | --- | --- | --- |
| openCHA / CHA | Conversational health agent framework | Modular health agents, orchestrator, external tools | `reference` | Learn interface/orchestrator/tool separation; avoid implying HIS is a clinical agent framework |
| MedRAG | Medical retrieval-augmented generation toolkit | Retrieval and source grounding for medical QA | `integrate later` | Use only in research companion or evidence-dossier workflows, not personal diagnosis |
| AgentClinic | Clinical-agent benchmark | Simulated clinical encounters reveal weaknesses in static QA claims | `reference` | Use as a credibility reminder that clinical AI needs evaluation before claims |
| MedAgentBench | Virtual EHR benchmark for medical LLM agents | Evaluates agents in realistic EHR workflows | `watchlist` | Track for future evaluation language; do not make EHR-agent claims in HIS |
| EHRAgent | Tabular EHR reasoning research | Code-augmented EHR reasoning over complex health records | `watchlist` | Reference as research; not a v0.2 user workflow |
| FHIR MCP Server | MCP interface to FHIR data | Possible standards-aware future connector | `integrate later` | Keep as app-layer option after the markdown protocol matures |
| Awesome healthcare MCP lists | Curated MCP server landscape | Discovery of connectors and patterns | `watchlist` | Use for periodic audits, not as authority |

## Healthcare Standards And Infrastructure

| System | Category | Useful pattern | HIS classification | HIS decision |
| --- | --- | --- | --- | --- |
| HL7 FHIR | Health-data interoperability standard | Common data exchange model | `reference` | Treat as boundary format for future imports/exports |
| International Patient Access | FHIR implementation guide for patient record access | Patient-facing access pattern, SMART on FHIR relationship | `reference` | Use to shape future patient-record import/export language |
| SMART on FHIR | Authorization pattern for health apps | Standard health app access to records | `integrate later` | Use only in future app or connector layer |
| Google Open Health Stack | FHIR-native app building blocks | Secure, offline-capable healthcare app components | `integrate later` | Consider if HIS becomes a mobile/app product |
| openEHR | Vendor-neutral EHR platform specifications and clinical models | Rigorous structured clinical data modeling | `reference` | Learn from clinical modeling discipline; too heavy for v0.2 vaults |
| OpenMRS | Mature open-source EMR | Provider-side clinical record system | `reference` | Reference as provider EMR, not personal second brain |

## Frontier AI And Health Products

| System | Category | Useful pattern | HIS classification | HIS decision |
| --- | --- | --- | --- | --- |
| ChatGPT Health | Dedicated health space in ChatGPT | Compartmentalized health chats, files, memories, and connected records | `reference` | Recommend as an optional compartmentalized mode where available and user-accepted |
| ChatGPT for Healthcare | Regulated healthcare workspace pattern | Enterprise governance and healthcare controls | `reference` | Separate consumer personal use from regulated care-team use |
| OpenAI HealthBench / health model work | Health response evaluation | Physician-informed evaluation and escalation focus | `reference` | Keep HIS release gated until clinical/legal review |
| Google AMIE | Diagnostic medical reasoning research | Clinical dialogue and diagnostic conversation research | `do not emulate` for v0.2 | Cite as clinical research; HIS must not market diagnostic capability |
| Google MedLM / medical model families | Medical AI model family pattern | Specialized medical models for healthcare settings | `watchlist` | Do not depend on model brand; keep model-agnostic |

## Life-Science Research Agents

| System | Category | Useful pattern | HIS classification | HIS decision |
| --- | --- | --- | --- | --- |
| Google DeepMind Science Skills | Agent skills for scientific workflows | Domain-specific tool skills for genomics, literature, and scientific databases | `reference` | Route research workflows to companion system |
| Google DeepMind Co-Scientist | Multi-agent scientific research partner | Multi-agent research hypothesis and evidence workflows | `reference` | Use as inspiration for research companion, not personal care |
| Anthropic Claude for Life Sciences | Life-science connectors and research workflows | Commercial research assistant layer | `reference` | Treat as validation of separate research lane |
| OpenAI GPT-Rosalind | Life-sciences model line | Specialized life-science reasoning direction | `watchlist` | Reference as frontier model direction; do not require it |
| ToolUniverse | Biomedical tool universe and scientific skills | Structured scientific tool use | `integrate later` | Candidate for life-science research companion |

## Local And Private AI Stack

| System | Category | Useful pattern | HIS classification | HIS decision |
| --- | --- | --- | --- | --- |
| Ollama | Local model runner | Local model execution and OpenAI-compatible usage patterns | `reference` | Private-mode baseline for technical users |
| LM Studio | Desktop local LLM app | Accessible local chat and local API | `reference` | Private-mode baseline for less infrastructure-heavy users |
| Open WebUI | Self-hosted chat UI | ChatGPT-style local or private interface | `integrate later` | Optional private UI, with network-exposure warning |
| Codex / OpenCode / Hermes-style agents | Coding agents for local files | Folder scaffolding, markdown organization, search, summarization | `reference` | Best fit for private-vault setup and records indexing |
| Private API gateways | Model routing and governance | Central model policy and logging | `integrate later` | Only for organizations or highly technical users |

## Do Not Emulate Patterns

| Pattern | Why not | HIS replacement |
| --- | --- | --- |
| Symptom checker framed as personal diagnosis | Encourages unsafe medical self-triage | Timeline, records, and clinician questions |
| Treatment recommender | Treatment depends on clinician assessment, records, risks, values, and jurisdiction | Options offered by clinician plus question list |
| Unbounded memory of private health details | Increases privacy and account-risk surface | Private vault, minimal summaries, explicit memory choice |
| Raw health records in ordinary Git | Git history and metadata are hard to sanitize | Local encrypted vault; optional encrypted archive only |
| Research-to-care leap | Literature may not apply to the person | Research brief -> glossary -> clinician questions |
| Jurisdiction-free record advice | Patient rights, portals, and insurance differ by country | Adapter packs with source dates |

## Source Ledger

| Source | URL | Date accessed | Used for |
| --- | --- | --- | --- |
| OpenHealth | https://github.com/OpenHealthForAll/open-health | 2026-06-22 | Personal AI health assistant and local execution reference |
| Health.md | https://github.com/CodyBontecou/health-md | 2026-06-22 | Apple Health to Markdown/JSON/CSV/Obsidian reference |
| Google PH-LLM | https://research.google/pubs/towards-a-personal-health-large-language-model/ | 2026-06-22 | Personal health LLM research reference |
| PHIA / Nature Communications | https://www.nature.com/articles/s41467-025-67922-y | 2026-06-22 | Wearable data agent research reference |
| openCHA | https://www.opencha.com/ | 2026-06-22 | Conversational health agent framework |
| CHA GitHub | https://github.com/Institute4FutureHealth/CHA | 2026-06-22 | Open-source framework implementation |
| MedRAG | https://github.com/gzxiong/MedRAG | 2026-06-22 | Medical RAG toolkit |
| AgentClinic | https://agentclinic.github.io/ | 2026-06-22 | Clinical-agent benchmark reference |
| MedAgentBench | https://github.com/stanfordmlgroup/medagentbench | 2026-06-22 | Virtual EHR benchmark reference |
| EHRAgent | https://github.com/wshi83/EHRAgent | 2026-06-22 | EHR reasoning research reference |
| FHIR MCP Server | https://github.com/the-momentum/fhir-mcp-server | 2026-06-22 | FHIR connector watchlist |
| HL7 International Patient Access | https://build.fhir.org/ig/HL7/fhir-ipa/ | 2026-06-22 | Patient record access standard reference |
| Google Open Health Stack | https://opensource.google/projects/openhealthstack | 2026-06-22 | FHIR-native healthcare app components |
| openEHR | https://openehr.org/ | 2026-06-22 | Structured clinical data modeling |
| OpenMRS | https://openmrs.org/ | 2026-06-22 | Provider EMR reference |
| ChatGPT Health | https://openai.com/index/introducing-chatgpt-health/ | 2026-06-22 | Dedicated health AI product reference |
| ChatGPT Health Help | https://help.openai.com/en/articles/20001036-what-is-chatgpt-health | 2026-06-22 | Data separation and availability reference |
| ChatGPT for Healthcare | https://help.openai.com/en/articles/20001046-chatgpt-for-healthcare | 2026-06-22 | Regulated workspace reference |
| OpenAI HealthBench | https://openai.com/index/healthbench/ | 2026-06-22 | Health response evaluation reference |
| Google health AI models | https://health.google/ai-models/ | 2026-06-22 | Medical model family reference |
| DeepMind Science Skills | https://github.com/google-deepmind/science-skills | 2026-06-22 | Scientific agent skills |
| ToolUniverse | https://github.com/mims-harvard/ToolUniverse | 2026-06-22 | Biomedical research tool skills |
| Ollama | https://ollama.com/ | 2026-06-22 | Local model runner |
| LM Studio | https://lmstudio.ai/ | 2026-06-22 | Desktop local LLM app |
| Open WebUI | https://docs.openwebui.com/ | 2026-06-22 | Local/self-hosted chat UI |

**Built on SIP** - Health Intelligence System external comparison
