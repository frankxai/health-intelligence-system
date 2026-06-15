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

**Built on SIP** - Health Intelligence System AGENTS.md v0.1
