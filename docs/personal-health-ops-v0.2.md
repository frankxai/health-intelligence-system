# Personal Health Operations v0.2

**Evidence checked:** 2026-06-22  
**Status:** private-instance architecture draft.  
**Scope:** nutrition, fitness, doctor-visit preparation, health-record organization, and LLM-assisted health intelligence. This is wellness organization and clinician-facing preparation, not medical advice.

## Purpose

Personal Health Operations extends Health Intelligence System from cancer-specific clinical prep into a broader sovereign health command center. The system should help a person:

- keep records findable;
- prepare for doctor visits;
- track nutrition, training, sleep, recovery, symptoms, and questions;
- turn messy health context into concise clinician summaries;
- use ChatGPT or similar tools without surrendering the private record as the source of truth.

## Design Principle

The master health record stays private and person-owned. LLMs help organize, summarize, question, and compare evidence, but they do not diagnose, prescribe, interpret tests, recommend medication or supplements, or replace clinicians.

## Private Instance Layout

Use a private folder outside public git history.

```text
private/
|-- 00-command-center/
|   |-- private-vault-manifest.md
|   |-- general-health-command-center.md
|   |-- health-record-index.md
|   |-- medication-supplement-inventory.md
|   `-- open-questions.md
|-- 10-records/
|   |-- labs/
|   |-- imaging/
|   |-- visit-notes/
|   |-- medications/
|   |-- insurance/
|   `-- portal-exports/
|-- 20-doctor-visits/
|   |-- upcoming/
|   |-- completed/
|   `-- referrals/
|-- 30-daily-loops/
|   |-- nutrition/
|   |-- fitness/
|   |-- sleep-recovery/
|   `-- symptoms-and-energy/
|-- 40-evidence/
|   |-- source-ledger.md
|   `-- guideline-checks/
|-- 50-jurisdiction/
|   |-- jurisdiction-adapter.md
|   `-- insurance-and-care-access-index.md
`-- 90-exports/
    |-- clinician-summaries/
    |-- clinician-handoff-export.md
    `-- ai-sanitized-context/
```

## Operating Layers

| Layer | Purpose | LLM use | Boundary |
| --- | --- | --- | --- |
| Private health vault | Source of truth for records, logs, and visit notes | No automatic sharing | Never commit to public git |
| Record index | Find what exists without exposing every file | LLM may help structure filenames and indexes | Avoid identifiers in public examples |
| Daily health loop | Track food pattern, training, sleep, energy, symptoms, and questions | Summarize trends and suggest questions | No diagnosis or protocols |
| Doctor visit loop | Prepare agenda, timeline, records list, and top questions | Turn notes into a concise visit brief | Clinician owns medical decisions |
| Evidence ledger | Track sources, access dates, and freshness | Compare sources and flag stale claims | Use current authoritative sources |
| Export layer | Produce clinician-ready summaries | Generate short, factual drafts | Person reviews before sharing |

## Agent Roles

| Agent | Job | Must not do |
| --- | --- | --- |
| `health-architect` | Maintains folder model, evidence freshness, privacy boundaries | Store real private data in public files |
| `care-record-organizer` | Indexes labs, visit notes, imaging reports, medications, and referrals | Interpret results |
| `doctor-visit-scribe` | Builds visit agendas, timelines, and question lists | Diagnose or recommend treatment |
| `nutrition-loop-keeper` | Tracks meals, appetite, hydration, preferences, and clinician questions | Prescribe diet therapy or supplements |
| `training-loop-keeper` | Tracks training, load, soreness, recovery, and constraints | Override injury, rehab, or clinician advice |
| `evidence-freshness-checker` | Finds source dates and flags stale guidance | Present sources as personal medical instruction |
| `clinical-boundary-guardian` | Reviews outputs for diagnosis, treatment, medication, supplement, and privacy drift | Relax safety rules for convenience |

## Daily Loop

Keep this lightweight. A good daily entry is enough to help the weekly review without becoming a second job.

- Sleep and recovery: duration, quality, stress, soreness, illness notes.
- Nutrition: meal pattern, protein-containing meals, fruits/vegetables, hydration, alcohol, unusual reactions.
- Fitness: session type, duration, intensity, main lifts or movement, pain/injury notes.
- Symptoms or concerns: facts only, dates, severity in the user's words, triggers noticed.
- Questions: anything to ask a clinician, coach, therapist, dentist, or other professional.

## Weekly Review

Once per week, ask the LLM to summarize only the week of logs:

1. What patterns are visible?
2. What improved or worsened?
3. What questions should be saved for a clinician or qualified professional?
4. What records or appointments are missing?
5. What is the simplest next-week experiment that stays within ordinary wellness behavior?

Avoid medical claims. The output should be a planning brief, not a diagnosis.

## Doctor Visit Workflow

Use a 72-hour prep rhythm:

1. Gather recent symptoms, timeline, medications/supplements as taken, allergies, prior records, and appointment purpose.
2. Build a one-page visit brief with top three questions.
3. Confirm what records to bring or request.
4. After the visit, write down clinician instructions, follow-up owner, expected results, and next appointment.
5. Add new records to the index.

## ChatGPT And Similar Tools

Use LLMs as an interface, not as the health database.

- Use a dedicated ChatGPT Project or Health space if available, so health context stays separated from other work.
- Use Temporary Chat for especially sensitive one-off questions.
- Keep memory off for sensitive health details unless there is a deliberate reason to save a preference.
- Share the minimum necessary context. Prefer sanitized summaries over raw PDFs, names, birth dates, medical record numbers, insurance identifiers, or full portal exports.
- Ask for sources and evidence-check dates when discussing guidelines.
- Ask for "questions to ask my clinician" rather than "what should I do medically?"
- Review any generated summary before sending it to a clinician.

## Evidence Baseline

Use current authoritative sources first:

- AHRQ Question Builder for appointment preparation.
- HHS HIPAA patient rights pages for access to health records.
- CDC nutrition pages for general healthy eating language.
- Physical Activity Guidelines for Americans for baseline activity guidance.
- OpenAI privacy, data controls, memory, Temporary Chat, and ChatGPT Health docs for AI data-handling choices.

Personal care may differ by diagnosis, medications, injury status, age, pregnancy status, disability, eating-disorder history, metabolic disease, cardiovascular risk, clinician guidance, and local jurisdiction.

## Safety Rules

- Do not use this system to decide whether symptoms are serious.
- Do not use it to interpret labs, imaging, pathology, genetic results, or clinician notes.
- Do not use it to start, stop, change, or delay medication, treatment, supplements, fasting, diet therapy, or rehabilitation.
- Emergency or severe symptoms route to emergency services, urgent care, or the care team's urgent-contact instructions.
- Any output intended for a clinician must include date, purpose, source of facts, and a clear note that it is patient-prepared.

## First Week Setup

1. Create the private folder structure.
2. Add `private-vault-manifest.md`.
3. Add `general-health-command-center.md`.
4. Add `health-record-index.md`.
5. Add `medication-supplement-inventory.md`.
6. Add one `doctor-visit-prep.md` for the next appointment.
7. Add one `nutrition-fitness-weekly-loop.md`.
8. Add `jurisdiction-adapter.md` for the country or countries involved.
9. Run a weekly review with only the week's logs.
10. Save a clinician-facing export only after human review.

**Built on SIP** - Health Intelligence System private operations architecture v0.2 draft
