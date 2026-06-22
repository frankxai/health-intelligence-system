# Prompt Pack For ChatGPT, Claude, And Local LLMs

**Evidence checked:** 2026-06-22  
**Scope:** system and project prompts for using HIS with ChatGPT, Claude, Custom GPTs, local LLMs, and coding agents.  
**Safety boundary:** Prompts must keep the model in organizer, educator, and clinician-question mode.

## Files

- `prompts/chatgpt-project-system-prompt.md`
- `prompts/custom-gpt-instructions.md`
- `prompts/claude-project-prompt.md`
- `prompts/local-llm-redaction-prompt.md`

## Prompt Rules

Every prompt should say:

- organize records, timelines, routines, and questions;
- do not diagnose, prescribe, interpret tests, choose treatment, or triage emergencies;
- distinguish public education from personal advice;
- ask for evidence-check dates;
- use clinician handoff;
- minimize private data;
- refuse unsafe requests by converting them into clinician questions.

## Context Tiers

| Context | Cloud prompt? | Notes |
| --- | --- | --- |
| Public docs and templates | Yes | Safe |
| Sanitized weekly summary | Maybe | Review first |
| Wearable aggregate trends | Maybe | Remove identifiers and raw files |
| Raw records | No by default | Local-only unless deliberate |
| Disease research brief | Yes if public | No personal records |
| Clinician handoff export | Maybe | User reviews first |

**Built on SIP** - Health Intelligence System prompt pack
