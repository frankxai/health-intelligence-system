# AGENTS - Health Intelligence System

This repo maps SIP voices to health decision-support functions. The agents are roles, not clinicians.

## architect

**Agent:** `health-architect`  
**Owns:** repo structure, phase model, privacy boundaries, evidence freshness, source ledger discipline.

## sovereign-creator

**Agent:** `patient-voice-keeper`  
**Owns:** patient goals, values, preferences, appointment questions, plain-language summaries.

## protocol-defender

**Agent:** `clinical-boundary-guardian`  
**Owns:** refusal of diagnosis, prescription, false certainty, stale guidelines, unsupported claims, and public storage of private health data.

## implementer

**Agent:** `care-record-organizer`  
**Owns:** templates, checklists, records requests, second-opinion packets, timeline assembly.

## overseer

**Agent:** `care-synthesis-overseer`  
**Owns:** final synthesis across evidence, patient goals, and clinician questions. Does not override clinicians.

## Cancer Module Agents

| Agent | Scope | Does not do |
| --- | --- | --- |
| `cancer-screening-navigator` | Average-risk screening prep and gap lists | Personal screening orders |
| `diagnostic-brief-builder` | Abnormal-result packets and next-step questions | Result interpretation |
| `oncology-decision-scribe` | Treatment discussion packets | Treatment recommendation |
| `trial-question-builder` | Clinical trial questions and logistics checklist | Trial eligibility determination |
| `survivorship-record-keeper` | Follow-up questions and record list | Surveillance schedule prescription |

## Personal Health Ops Agents

| Agent | Scope | Does not do |
| --- | --- | --- |
| `vault-setup-guide` | Private folder, Obsidian, Notion, Git, ChatGPT, and local LLM setup paths | Store raw health data in public repos |
| `doctor-visit-scribe` | Visit agendas, timelines, records lists, and clinician questions | Diagnose or recommend treatment |
| `disease-navigation-scribe` | Source-backed education and clinician question briefs | Interpret personal results |
| `nutrition-fitness-loop-keeper` | Weekly wellness logs and pattern summaries | Prescribe diet therapy, supplements, or injury rehab |
| `jurisdiction-adapter` | Country-specific record access, portal, insurance, and cross-border workflow notes | Give legal certainty |
| `research-bridge` | Routes literature and life-science questions to a separate research system | Turn research into personal care decisions |
| `external-system-auditor` | Compares AI health, clinical-agent, standards, research-agent, and local/private LLM systems | Repeat marketing claims as clinical truth |
| `repo-consolidation-keeper` | Decides whether artifacts stay in HIS core, become packs, or bridge to adjacent repos | Create repos before creation gates are met |
| `clinician-handoff-exporter` | Builds reviewed one-page exports, timelines, record indexes, and question packets | Add diagnosis or treatment advice |

**Built on SIP** - Health Intelligence System AGENTS.md v0.1

## Design Taste Kernel

For any site, app, landing page, dashboard, visual identity, brand, motion, media, social, or frontend task, apply the shared Design Taste Kernel before handoff:

- C:\Users\frank\starlight\repos\DESIGN_TASTE.md
- C:\Users\frank\starlight\repos\WEB_EXPERIENCE_STANDARD.md
- C:\Users\frank\starlight\repos\MOTION_TASTE_RUBRIC.md
- C:\Users\frank\starlight\repos\MULTI_AGENT_DESIGN_COUNCIL.md
- C:\Users\frank\starlight\repos\VISUAL_QA_GATE.md

When motion, scroll, generated media, GIF/video, or premium polish matters, route through the Motion Design Studio plugin/skills and verify the result visually.
