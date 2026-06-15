# /cancer-screening-plan

Build a clinician-facing cancer screening preparation plan.

## Input

- Age and jurisdiction.
- Relevant anatomy for screening.
- Prior screenings and dates.
- Family history and known genetic risks.
- Tobacco pack-years if relevant.
- Prior abnormal results.

## Output

Use `templates/cancer-screening-plan.md`.

## Rules

- Do not order tests.
- Do not diagnose.
- Do not override clinician advice.
- Mark average-risk vs high-risk unknown if risk is unclear.
- Include evidence-check date and source links.

**Built on SIP** - Health Intelligence System command
