# Architecture

**Evidence checked:** 2026-06-22  
**Scope:** Health Intelligence System v0.2 architecture for public docs, private vaults, AI modes, clinician handoffs, jurisdiction adapters, and research companions.  
**Safety boundary:** This is system architecture. It does not provide medical advice, diagnosis, treatment, medication, supplement, emergency, legal, or compliance guidance.

## System Shape

```text
public HIS repo
  -> docs, commands, templates, safety gates

private health vault
  -> records, logs, visits, questions, exports

AI assistance layer
  -> ChatGPT / Custom GPT / ChatGPT Health / local LLM / private model / coding agent

clinician handoff
  -> one-page summary, timeline, record index, top questions

research companion
  -> public evidence brief, glossary, clinician questions
```

The public repo contains reusable structure. The private vault contains real health context. The AI layer is optional and privacy-tiered. The clinician handoff is always reviewed by the person before sharing.

## Data Tiers

| Tier | Examples | Default location | AI use |
| --- | --- | --- | --- |
| Public | Templates, fictional examples, safety docs | Public repo | Safe for public models |
| Sanitized | De-identified summaries, general goals, non-identifying patterns | Private vault export folder | Can be used with cloud AI if user accepts |
| Private | Records, portal exports, medication lists, appointment notes, identifiers | Local encrypted vault | Local-only or deliberate user-controlled sharing |
| Clinical source | Physician notes, labs, imaging reports, pathology, prescriptions | Original portal plus private copy | Organize and summarize facts; do not interpret |
| Research | Papers, guidelines, trials, disease education | Research companion or source ledger | Public research workflow only |

## Privacy Modes

| Mode | Name | Default tools | Raw record rule |
| --- | --- | --- | --- |
| 0 | Public/sanitized | GitHub, public docs | Never include real records |
| 1 | Consumer AI convenience | ChatGPT, Custom GPT, Projects | Share only deliberately accepted context |
| 2 | Compartmentalized health AI | ChatGPT Health or comparable health space | Keep health data separated from ordinary chats |
| 3 | Regulated workspace | Healthcare/enterprise workspace | Follow organization policy and review |
| 4 | Local-first private | Obsidian, encrypted disk, Codex/OpenCode/Hermes, Ollama/LM Studio | Raw records stay local |
| 5 | Private infrastructure | Private APIs, model gateway, encrypted storage, audit logs | Treat as security engineering project |

## Core Workflows

| Workflow | Input | Output | Safety gate |
| --- | --- | --- | --- |
| Private setup | Privacy mode, country, preferred tools | Vault manifest and folder layout | No raw data in public Git |
| Data ingestion | Wearables, portal downloads, PDFs, visit notes | Record index and missing-record list | Do not interpret results |
| Doctor visit prep | Appointment purpose, timeline, records, questions | One-page visit brief | Clinician owns decisions |
| Disease navigation | Clinician-stated condition and public sources | Education brief and clinician questions | No AI diagnosis or treatment ranking |
| Nutrition/fitness loop | Weekly wellness logs | Pattern summary and professional questions | No diet therapy, supplement, or rehab prescription |
| Jurisdiction adapter | Country/region, portals, insurance context | Record-access and care-access checklist | Not legal certainty |
| Clinician handoff | Reviewed private notes and records index | Export packet | Person reviews before sharing |
| Research bridge | Literature question | Evidence brief, glossary, questions | No personal care decision |

## Agent Roles

| Agent | Job | Must not do |
| --- | --- | --- |
| `health-architect` | Maintains architecture, scope, and public/private boundaries | Store real records in public files |
| `vault-setup-guide` | Creates private vault structure and setup checklist | Recommend raw records in ordinary Git |
| `record-indexer` | Organizes file metadata and missing records | Interpret labs or imaging |
| `doctor-visit-scribe` | Builds visit agenda, timeline, and questions | Diagnose or select treatment |
| `nutrition-fitness-loop-keeper` | Summarizes wellness patterns | Prescribe diet therapy, supplements, or rehab |
| `jurisdiction-adapter` | Localizes record access and care logistics | Give legal certainty |
| `privacy-boundary-guardian` | Blocks private-data leakage | Relax rules for convenience |
| `clinical-boundary-guardian` | Blocks diagnosis/treatment/medication drift | Provide clinical judgment |
| `research-bridge` | Converts research into questions and glossary | Apply research directly to personal care |

## Interop Boundary

Markdown is the working layer. Standards belong at the boundary:

- FHIR/IPA for future structured patient-record imports and exports.
- CSV/JSON for wearable and Apple Health derived data.
- PDF for clinician-facing summaries when needed.
- Plain text for copy/paste into portals or appointment notes.
- Notion/Obsidian views for dashboards, never as the only source of truth.

## Release Gates

Before a public release expands beyond preclinical prerelease:

- source audit is current;
- safety scan passes;
- privacy leak scan passes;
- private-data fixture stays private;
- workflow dry runs pass;
- clinical/legal/UX review gate is updated.

**Built on SIP** - Health Intelligence System architecture
