# Research Audit: AI Health Agents And Personal Health Systems

**Evidence checked:** 2026-06-22  
**Scope:** AI labs, open-source repositories, health-data standards, local/private LLM stacks, and patient-facing workflows relevant to a person-owned Health Intelligence System.  
**Safety boundary:** This audit informs system design. It is not medical, legal, privacy, or compliance advice.

## Executive Finding

The strongest external work falls into four separate categories:

1. clinical AI research systems;
2. open-source health-agent frameworks and medical RAG toolkits;
3. interoperability and electronic health record standards;
4. local/private LLM tooling.

What is still missing is a practical, person-owned operating system that combines local markdown files, doctor-visit preparation, jurisdiction-aware record handling, nutrition and fitness loops, optional ChatGPT-style workflows, optional fully local agents, and strict clinical boundaries.

That gap is the opportunity for Health Intelligence System.

## Evidence-Grade Decision Matrix

Use [external-systems-comparison.md](external-systems-comparison.md) as the durable comparison table. The compressed decision view is:

| Category | Systems audited | HIS decision |
| --- | --- | --- |
| Personal health OS / PHR | OpenHealth, Health.md, Google PH-LLM, PHIA, Second Brain OS | Reference and selectively integrate ingestion patterns; keep HIS markdown-first and clinician-handoff oriented |
| Clinical agents and benchmarks | openCHA, MedRAG, AgentClinic, MedAgentBench, EHRAgent, FHIR MCP | Reference for architecture/evaluation; do not claim clinical-agent competence |
| Healthcare standards | FHIR, IPA, SMART on FHIR, Open Health Stack, openEHR, OpenMRS | Use as boundary formats and future app/connector guidance |
| Frontier health AI products | ChatGPT Health, ChatGPT for Healthcare, AMIE, medical model families | Support as optional modes; do not tie HIS to one vendor or diagnostic claims |
| Research agents | DeepMind Science Skills, Co-Scientist, Claude for Life Sciences, GPT-Rosalind, ToolUniverse | Route to a separate research companion, not the personal health vault |
| Local/private AI | Ollama, LM Studio, Open WebUI, Codex/OpenCode/Hermes-style agents | Support as privacy modes with explicit local security caveats |

## Open-Source Personal Health Systems

| Source | What it contributes | HIS classification | Boundary |
| --- | --- | --- | --- |
| OpenHealth | AI health assistant powered by personal data, parser layer, local and commercial LLM options | `reference` | Useful architecture reference; HIS should stay protocol-first and avoid personal medical authority claims |
| Health.md | Apple Health export to Markdown/JSON/CSV/Obsidian-style workflows | `integrate later` | Good wearable-data ingestion bridge; not a clinical interpretation layer |
| Second Brain OS | Two-vault privacy separation and coding-agent-native markdown workflows | `reference` | Absorb the privacy architecture pattern, not raw personal content |
| Google PH-LLM / PHIA | Research direction for personal health and wearable-data insights | `watchlist` | Research evidence does not make HIS clinically validated |

## AI Labs And Frontier Systems

| Source | What it contributes | What HIS should learn | Boundary |
| --- | --- | --- | --- |
| OpenAI ChatGPT Health | Dedicated health space, optional connected medical records and wellness apps, separated Health chats/memories/files, privacy controls | A dedicated health context is valuable; health should be compartmentalized from ordinary chat | Proprietary product; not a public file standard |
| OpenAI ChatGPT for Healthcare | Enterprise controls for regulated healthcare use, including governance and HIPAA-supporting features | Regulated care teams need workspace-level controls, not consumer chat habits | Different from personal consumer use |
| Google AMIE | Diagnostic dialogue and disease-management research; models optimized for clinical conversation | Pre-visit history, structured summaries, and clinician review are high-value workflows | Research system; not a DIY diagnosis engine |
| Google DeepMind Science Skills | Agent skills for genomics, structural biology, cheminformatics, literature search, and scientific workflows | A separate life-science research lane should use tool-specific skills and database grounding | Research workflow, not personal care advice |
| Anthropic Claude for Life Sciences | Life-sciences support with scientific connectors, skills, literature review, hypothesis generation, and research workflows | Validates the need for a research-specific companion system | Research/commercial workflow; not personal diagnosis |
| OpenAI GPT-Rosalind | Life-sciences model line for biology, drug discovery, translational medicine, chemistry, protein engineering, and genomics | Confirms a split between personal health ops and life-science research intelligence | Specialized model access; not a personal medical authority |

## Open-Source Health And Medical Agent Work

| Source | What it contributes | What HIS should learn | Boundary |
| --- | --- | --- | --- |
| openCHA / Conversational Health Agents | Open-source LLM-powered framework with interface, orchestrator, and external source integrations | HIS should define modular agents, tool contracts, and data-source boundaries | Framework for builders; needs safety/evaluation for real users |
| MedRAG / medical RAG toolkits | Medical retrieval-augmented generation patterns and evaluation around medical QA | Evidence grounding belongs in a separate source ledger/RAG layer | RAG can still be wrong and should not become personal diagnosis |
| AgentClinic | Multimodal benchmark for clinical agents in simulated environments | Any agent claiming clinical competence needs evaluation, simulated cases, and failure analysis | Benchmark only; not a user-facing health product |
| MedAgentBench | Realistic virtual EHR environment for benchmarking medical LLM agents | EHR-agent claims need realistic workflow evaluation | Research benchmark, not a personal health product |
| EHRAgent | Code-assisted tabular EHR reasoning research | Useful reminder that EHR reasoning is specialized and high risk | Not for personal record interpretation |
| FHIR MCP Server | MCP-style connector for FHIR data | Possible future app-layer connector | Do not connect to real records without security and compliance review |
| Medical Graph RAG and related repositories | Knowledge-graph retrieval for medical QA and disease relationships | Useful for research briefs and evidence maps | Risky if used to infer personal disease status |
| Awesome AI Agents for Healthcare lists | Map of agentic healthcare papers and repositories | Useful watchlist for continued audit | Curated lists vary in quality and freshness |

## Health Data Standards And Infrastructure

| Source | What it contributes | What HIS should learn | Boundary |
| --- | --- | --- | --- |
| HL7 FHIR / International Patient Access | Minimal global access patterns for patient records and cross-border patient access | HIS should treat FHIR as the future export/import language | Markdown remains the human-first working layer |
| SMART on FHIR | Authorization pattern for patient apps accessing records | Future app integrations should use standards rather than scraping portals | Requires provider/payer support |
| Google Open Health Stack | Open-source FHIR-native components for healthcare apps | Useful for a future mobile/app layer | Not necessary for v0.2 markdown-first system |
| openEHR | Vendor-neutral clinical data models and open specifications | Useful reference for serious structured health data | Too heavy for a personal first-week setup |
| OpenMRS | Mature open-source EMR for providers and resource-constrained settings | Shows how serious clinical systems handle records | Provider EMR, not personal second brain |

## Patient-Facing Workflow References

| Source | What it contributes | HIS adaptation |
| --- | --- | --- |
| AHRQ Question Builder | Prepare questions for medical visits and maximize visit time | HIS doctor-visit prep should create agendas, top questions, and follow-up confirmations |
| HHS HIPAA patient access guidance | US patients can request access to health records | HIS should include records-request and correction workflows |
| EU EHDS / MyHealth@EU | EU direction toward patient access, downloadable copies, access logs, restrictions, and cross-border patient summaries | HIS should support jurisdiction adapters rather than one global workflow |
| National portals and apps | Netherlands PGO, Germany ePA, Spain regional/national services, Croatia Portal zdravlja and CEZIH | HIS should teach users how to gather records from local systems without pretending every country works the same |

## Local And Private LLM Tooling

| Source | What it contributes | HIS adaptation |
| --- | --- | --- |
| Ollama | Local model runner that can connect to coding agents and local tools | Good private-mode foundation for technical users |
| LM Studio | Desktop local LLM app and local API | Good private-mode foundation for non-infrastructure users |
| Open WebUI | Self-hosted chat UI that can run offline with Ollama and OpenAI-compatible APIs | Good private ChatGPT-style interface when configured safely |
| Codex / OpenCode / Hermes-style local agents | Agentic file operations, markdown organization, private vault automation | Best fit for setup, folder scaffolding, template filling, and record indexing |

Local does not automatically mean safe. Users must keep local LLM services bound to trusted interfaces, avoid exposing servers publicly, encrypt backups, and understand where chat histories and model logs are stored.

## Gap Analysis

Current ecosystem strengths:

- frontier labs are improving medical dialogue, disease-management reasoning, and research workflows;
- open-source projects are exploring health-agent orchestration and medical RAG;
- standards bodies provide serious interoperability foundations;
- patient portals increasingly allow access to records;
- local LLM tooling can run private workflows.

Current ecosystem gaps:

- no widely adopted markdown-first personal health OS;
- little guidance for using ChatGPT Projects, Custom GPTs, local LLMs, Obsidian, Notion, and coding agents together;
- weak separation between personal health organization, clinical decision-making, and biomedical research;
- little jurisdiction-aware setup guidance for people living across multiple countries;
- few systems explain how to prepare better clinician summaries without turning the AI into a doctor;
- most open-source health-agent frameworks are builder-centric, not patient-operator-centric.

## Health Intelligence System Position

Health Intelligence System should be:

- local-first by default;
- markdown-native for long-term portability;
- privacy-tiered rather than privacy-theater;
- clinician-handoff oriented;
- jurisdiction-adaptable;
- standards-aware but not standards-burdened;
- compatible with ChatGPT, Custom GPTs, ChatGPT Health, local LLMs, Obsidian, Notion, Git, Codex, OpenCode, Hermes, and future agents;
- explicit that disease education, symptom timelines, and record summaries are not diagnosis.

## Source Ledger

- OpenAI ChatGPT Health: https://openai.com/index/introducing-chatgpt-health/
- OpenAI ChatGPT Health help: https://help.openai.com/en/articles/20001036-what-is-chatgpt-health
- OpenAI ChatGPT for Healthcare: https://help.openai.com/en/articles/20001046-chatgpt-for-healthcare
- OpenAI Data Controls: https://help.openai.com/en/articles/7730893-data-controls-faq
- OpenAI Memory FAQ: https://help.openai.com/articles/8590148-memory-faq
- OpenAI Projects in ChatGPT: https://help.openai.com/en/articles/10169521-projects-in-chatgpt
- OpenAI Health Privacy Notice: https://openai.com/policies/health-privacy-policy/
- OpenAI HealthBench: https://openai.com/index/healthbench/
- Google AMIE research blog: https://research.google/blog/amie-a-research-ai-system-for-diagnostic-medical-reasoning-and-conversations/
- Google AMIE real-world clinical study blog: https://research.google/blog/exploring-the-feasibility-of-conversational-diagnostic-ai-in-a-real-world-clinical-study/
- Google for Health AI models: https://health.google/ai-models/
- Google DeepMind Science Skills: https://github.com/google-deepmind/science-skills
- Google DeepMind Co-Scientist: https://deepmind.google/blog/co-scientist-a-multi-agent-ai-partner-to-accelerate-research/
- Anthropic Claude for Life Sciences: https://www.anthropic.com/news/claude-for-life-sciences
- OpenAI GPT-Rosalind: https://openai.com/index/introducing-gpt-rosalind/
- OpenHealth: https://github.com/OpenHealthForAll/open-health
- Health.md: https://github.com/CodyBontecou/health-md
- Google PH-LLM: https://research.google/pubs/towards-a-personal-health-large-language-model/
- Google PHIA / Nature Communications: https://www.nature.com/articles/s41467-025-67922-y
- openCHA paper: https://academic.oup.com/jamiaopen/article/8/4/ooaf067/8186991
- openCHA site: https://www.opencha.com/
- openCHA GitHub: https://github.com/Institute4FutureHealth/CHA
- MedRAG toolkit: https://github.com/teddy-xionggz/medrag
- AgentClinic: https://agentclinic.github.io/
- AgentClinic GitHub: https://github.com/samuelschmidgall/agentclinic
- MedAgentBench: https://github.com/stanfordmlgroup/medagentbench
- EHRAgent: https://github.com/wshi83/EHRAgent
- FHIR MCP Server: https://github.com/the-momentum/fhir-mcp-server
- ToolUniverse: https://github.com/mims-harvard/ToolUniverse
- HL7 International Patient Access: https://build.fhir.org/ig/HL7/fhir-ipa/
- Google Open Health Stack: https://opensource.google/projects/openhealthstack
- openEHR: https://openehr.org/
- OpenMRS: https://openmrs.org/
- AHRQ Question Builder: https://www.ahrq.gov/questions/question-builder/index.html
- HHS HIPAA access rights: https://www.hhs.gov/hipaa/for-individuals/right-to-access/index.html
- ONC Information Blocking: https://healthit.gov/information-blocking/
- WHO Digital Health: https://www.who.int/health-topics/digital-health
- EU health data rights: https://health.ec.europa.eu/ehealth-digital-health-and-care/my-rights-over-my-health-data_en
- Netherlands medical-record access: https://www.government.nl/themes/family-health-and-care/patients-rights-and-privacy/accessing-updating-or-deleting-medical-records
- Spain cross-border patient notice: https://health.ec.europa.eu/ehealth-digital-health-and-care/digital-health-and-care/electronic-cross-border-health-services/patient-information-notices-spain_en
- Croatia Health Portal: https://gov.hr/en/portal-zdravlja-health-portal-is-mobile-friendly/2340
- Croatia health-data rights: https://gov.hr/en/personal-data-concerning-health/616
- Ollama: https://ollama.com/
- LM Studio: https://lmstudio.ai/
- Open WebUI: https://docs.openwebui.com/

**Built on SIP** - Health Intelligence System research audit
