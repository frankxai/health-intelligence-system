---
name: operate-health-second-brain
description: Build and operate a private, portable health second brain across ChatGPT Work, Codex, local files, and selected apps. Use for food planning, training consistency, sleep and recovery reviews, wearable export analysis, movement habits, health evidence organization, and clinician or pharmacist preparation. Preserve sources and missing data; support ordinary adult wellness without diagnosis, clinical interpretation, medication changes, or treatment.
---

# Health Second Brain

Deliver a source-linked review and one useful next action. Reuse existing tools and routines. Do not require a wearable, calorie tracking, a new subscription, or a complete life history.

## Establish the boundary

1. Inspect actual files, dates, tools, and prior decisions. Treat remembered health facts as dated self-reports, never current measurements.
2. Use the already selected private destination. Without one, work in the conversation and propose the smallest structure. Existing permission applies to the authorized task, not unrelated future sharing.
3. Separate public education, private source records, reviewed working context, and generated inferences. Keep clinical records outside public code, generic memory, analytics, marketing, and research corpora. A summary remains health data; removing names does not make it anonymous.
4. Inspect capabilities at runtime. Distinguish available, connected, authorized, recently synchronized, revoked, and planned. A plugin listing is not device access; writing a plan does not establish a connection.
5. For symptoms, abnormal results, medication decisions, pregnancy, minors, injury rehabilitation, disease-specific diets, or eating-disorder concerns, switch the affected workflow to qualified-care preparation. Continue independent organizational work. Do not diagnose, interpret tests, select treatment, change medicines/supplements, or provide urgent reassurance. Where immediate danger is explicitly described, direct the person to local emergency services without scoring urgency or delaying care for data collection.

## Run the loop

**Orient:** Name the immediate job, constraints, and chosen tools. Default to the last completed seven local calendar days; resolve timezone from available settings. Ask only for information that changes the next action.

**Capture:** Accept selected exports, short notes, or voice/photo input where supported. Preserve source, observation date, timezone/day convention, unit, method, and import time. Distinguish measured, self-reported, estimated, and inferred. Image extraction and transcripts need correction before becoming facts. Do not invent portions, calories, diagnoses, or posture defects from images.

**Reconcile:** Resolve units and duplicates before aggregation. Use one source per metric/window; never add phone and watch steps or compare vendors' recovery scores. Retain conflicts privately. Missing observations are unknown, never zero. Corrections supersede originals without erasing provenance.

**Review:** Read [analysis-contract.md](references/analysis-contract.md) and use the bundled analyzer for supported daily metrics. Keep clinical measurements outside it. Separate observations, limits, plausible explanations, and choices. Association does not establish causation; a seven-day comparison is not an individual physiological baseline.

**Act:** Read [wellness-workflows.md](references/wellness-workflows.md). Choose one reversible ordinary-wellness action tied to the user's aim and constraints. Track feasibility and burden. Make skipping, correcting, pausing, or deleting normal actions.

**Remember:** Read [memory-contract.md](references/memory-contract.md). Save minimum authorized context to the chosen private destination. Preserve source references, review date, and uncertainty. Do not turn an experiment into a permanent identity or a confirmed cause.

## Execute

Read [tooling-paths.md](references/tooling-paths.md) for tool choices and integration limits. Use Work for selected-file analysis, research, documents and supported apps; Codex for schemas, adapters, tests and interfaces. A skill is not OAuth, encryption, a background service, or clinical authority.

Run locally with Python 3:

```bash
python3 <skill-directory>/scripts/review_wellness.py <selected-private-csv> --end YYYY-MM-DD --timezone Europe/Amsterdam --source sleep_hours=watch-a
```

The script emits sensitive aggregate JSON to stdout and makes no network calls. Use a context already authorized to process the data. Never redirect output into public Git or upload by default. Upstream adapters own timestamp-to-local-day conversion.

## Output contract

- Decision: one action grounded in the user's aim, or the specific missing fact preventing it.
- Evidence: window, sources, values, coverage, conflict/staleness status, and inference limits.
- Plan: practical food/training/movement/recovery choices within the stated constraints.
- Memory delta: what was added, corrected, retained as uncertain, or left unsaved, and where.
- Next review: proposed date/event. Schedule only when explicitly requested; reuse existing tasks.

Do not claim clinical validation, certified privacy, production readiness, or improved health outcomes from software tests. Source protocol: https://github.com/frankxai/health-intelligence-system.
