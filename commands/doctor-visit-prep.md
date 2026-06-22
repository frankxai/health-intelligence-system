# /doctor-visit-prep

Prepare a clinician-facing doctor visit brief from private notes and records.

## Input

- Appointment date, clinician, specialty, and location.
- Visit purpose in the user's own words.
- Recent timeline, symptoms, concerns, or changes.
- Medication and supplement inventory as taken.
- Allergies or prior reactions.
- Relevant records and missing records.
- Top questions, goals, constraints, and preferred language.

## Output

Use `templates/doctor-visit-prep.md` and, if sharing externally, `templates/clinician-handoff-export.md`.

The output should include:

- one-page visit purpose;
- top three questions;
- timeline since last visit;
- current medications and supplements as taken;
- records to bring or request;
- follow-up confirmations;
- privacy and boundary check.

## 72-Hour Rhythm

| Timing | Action |
| --- | --- |
| 72 hours before | Gather notes, records, medications, supplements, symptoms, and questions |
| 24 hours before | Condense to one page and select top three questions |
| During visit | Confirm follow-up owner, expected result timing, and urgent-contact criteria |
| Same day after | Record clinician instructions in private vault |
| Within one week | Add new records, referrals, and tasks to the index |

## Rules

- Do not diagnose.
- Do not interpret test results.
- Do not recommend treatment, medication, supplements, or delay.
- Do not decide emergency severity.
- Convert uncertainty into questions for the clinician.
- Keep private records in the private vault, not this public repo.

**Built on SIP** - Health Intelligence System command
