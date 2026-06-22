# SUB-SYSTEMS - Health Intelligence System

## Functional Decomposition

Health Intelligence System is organized by care phase, not body system. That keeps it useful when real care crosses specialties.

| Sub-system | Function | Primary outputs |
| --- | --- | --- |
| Prevention & Risk | Capture risk factors and clinician questions | risk inventory, family-history map |
| Screening & Detection | Prepare age/risk-based screening conversations | screening plan, screening gap list |
| Diagnostic Navigation | Organize abnormal results and next appointments | diagnostic brief, result timeline |
| Treatment Planning | Prepare oncology conversations and second opinions | treatment decision brief, second-opinion packet |
| Supportive Care & Survivorship | Track side effects, late effects, and follow-up questions | side-effect log, follow-up plan |
| Evidence & Clinician Interface | Maintain source freshness and clinician-ready summaries | evidence ledger, clinician summary |
| Private Personal Health Ops | Track records, nutrition, fitness, visits, insurance, and weekly patterns | command center, record index, weekly loop |
| Jurisdiction Adapter | Localize record access, portal, insurance, and cross-border workflows | country pack, care-access index |
| Research Bridge | Route literature and life-science questions to a separate research system | research brief, evidence dossier |
| External Systems Audit | Compare AI health systems, standards, agents, and local/private LLM stacks | comparison matrix, source ledger |
| Repo Consolidation | Decide whether new artifacts stay in core, become packs, or bridge to adjacent repos | disposition matrix, creation gate |
| Clinician Handoff Spec | Produce reviewed one-page exports, timelines, record lists, and question packets | clinician handoff export |
| Wearable Data Ingestion | Index phone, watch, ring, WHOOP, Oura, Apple Health, Health Connect, and Health.md-style exports | ingestion manifest, metric dictionary, sanitized summary |
| AI Prompt & Skill Pack | Install reusable agent workflows for Codex, Claude, OpenCode, ChatGPT, and local assistants | plugin, skill, project prompts, command pack |
| Health Optimization Loop | Review sleep, training, nutrition, energy, symptoms, adherence, and routine constraints | weekly review, experiments-to-discuss, clinician questions |
| Possibility Mapping | Organize concerns and possible categories without concluding diagnosis | possibility map, uncertainty list, care-team questions |

## Cancer Intelligence v0.1

The first module is cancer detection prep and treatment decision support:

- screening is not diagnosis;
- abnormal screening requires clinician-directed follow-up;
- diagnosis usually requires tissue/pathology confirmation and staging;
- treatment selection depends on cancer type, stage, biomarkers, patient health, goals, and clinician judgment;
- clinical trials require a separate eligibility and logistics conversation;
- survivorship needs a follow-up plan and treatment record.

## Composition Rules

- Screening & Detection may reference USPSTF and CDC.
- Treatment Planning may reference NCI education pages, but does not recommend regimens.
- Evidence & Clinician Interface must stamp every artifact with `Evidence checked: YYYY-MM-DD`.
- Any symptom, abnormal result, or diagnosis routes to clinician confirmation.
- Private Personal Health Ops stores real records only in private workspaces.
- Research Bridge may create education and clinician questions, but not personal diagnosis or treatment advice.
- External Systems Audit must classify systems as `reference`, `integrate later`, `watchlist`, or `do not emulate`.
- Repo Consolidation must prefer core-plus-packs over premature repo sprawl.
- Clinician Handoff Spec must label exports as patient-prepared and reviewed before sharing.
- Wearable Data Ingestion may summarize exported metrics and provenance, but does not interpret trends as disease signals.
- AI Prompt & Skill Pack must inherit the repo safety boundary and keep private data local unless the user deliberately prepares a sanitized export.
- Health Optimization Loop may support routines and reflection, but never prescribes medical nutrition therapy, supplements, medication changes, injury rehab, or disease protocols.
- Possibility Mapping may identify categories to ask a clinician about, but never states or ranks a diagnosis.

**Built on SIP** - Health Intelligence System SUB-SYSTEMS.md v0.1
