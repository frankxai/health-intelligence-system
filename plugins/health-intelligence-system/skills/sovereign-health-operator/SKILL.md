---
name: sovereign-health-operator
description: Set up and operate a sovereign personal health system with local-first private vaults, wearable/smartwatch/smart-ring data ingestion, nutrition/fitness/energy review loops, ChatGPT/Claude/local-LLM prompt packs, clinician-safe possibility mapping, and doctor-visit handoff workflows. Use when a user asks to build or run a private health operating system, install health agent skills into Codex/Claude Code/OpenCode, aggregate wearable data, optimize general wellness routines, prepare clinician questions, or protect sensitive health data while using agents. Never diagnose, prescribe, interpret tests, choose treatment, or provide emergency triage.
---

# Sovereign Health Operator

## Overview

Use this skill to help a person become a better health operator and patient advocate, not their own doctor. Build local-first systems for records, nutrition, fitness, sleep, energy, wearables, doctor visits, and source-backed questions while preserving clinical and privacy boundaries.

## Hard Boundary

Do not:

- diagnose or rule conditions in/out;
- interpret labs, imaging, pathology, genomics, wearable signals, or clinician notes;
- recommend treatment, medication changes, supplement doses, fasting, rehab, or disease protocols;
- decide whether symptoms are urgent;
- imply local LLMs are medically reliable because they are private;
- place raw health records in public Git.

Allowed outputs:

- private vault setup;
- source-backed wellness and education summaries;
- wearable-data inventory and trend summaries with caveats;
- ordinary nutrition, movement, recovery, and energy tracking loops;
- possibility maps that say "could be worth asking about", not "you have this";
- clinician questions, record checklists, and handoff exports.

## Workflow

1. Pick privacy mode before handling data: public/sanitized, consumer AI, health AI, regulated workspace, local-first, or private infrastructure.
2. Create or inspect the private vault using `templates/private-vault-manifest.md`.
3. Add records, wearable exports, medication/supplement inventory, and weekly loops.
4. Choose AI mode: coding agent, ChatGPT/Claude project, local LLM, or no model.
5. For wellness optimization, summarize patterns and propose low-risk experiments framed as self-tracking.
6. For symptoms, diseases, abnormal data, or concerns, create a possibility map and clinician questions.
7. Before any cloud AI use, create an `ai-sanitized-context-export.md` and run privacy preflight.
8. Before any visit, generate doctor visit prep and clinician handoff export.

## When To Load References

- Read `references/operator-workflows.md` when building the full health operating loop.
- Read `references/privacy-modes.md` when deciding between ChatGPT, local LLM, private infrastructure, and manual redaction.
- Read `references/wearable-ingestion.md` when aggregating Apple Health, Health Connect, Oura, WHOOP, Garmin, phone, or ring data.
- Read `references/possibility-mapping.md` when the user asks what could be going on, what patterns might matter, or what to ask a doctor.

## Default Commands

- `/private-health-instance-setup`
- `/wearable-data-ingestion`
- `/health-optimization-weekly-review`
- `/health-possibility-map`
- `/privacy-preflight-redaction`
- `/doctor-visit-prep`
- `/clinician-handoff-export`

## Model Guidance

Use deterministic filtering first for privacy. A tiny local model such as a Qwen 0.5B/0.8B-class model can help classify or redact obvious identifiers, but it is not required for most users and must not be trusted as the only privacy barrier. Use small local models for:

- identifying names, dates, addresses, phone numbers, emails, IDs, and clinician names;
- converting messy notes into neutral summaries;
- checking whether a cloud prompt contains private details.

Do not use small local models for medical reasoning, lab interpretation, symptom triage, or treatment advice.

## Data Rule

Raw health records stay local by default. Cloud projects may receive only deliberate, reviewed, minimal context. Public repos receive only templates, fictional examples, or sanitized artifacts.

**Built on SIP** - Sovereign Health Operator skill
