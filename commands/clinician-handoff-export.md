# /clinician-handoff-export

Create a reviewed clinician-facing export packet from private HIS files.

## Input

- Doctor visit prep file.
- Health record index entries relevant to the visit.
- Medication and supplement inventory as taken.
- Disease navigation brief if applicable.
- User-approved timeline and top questions.
- Preferred export format: markdown, PDF, print, portal message, or email draft.

## Output

Use `templates/clinician-handoff-export.md`.

The export should include:

- patient-prepared label;
- purpose and date;
- one-page summary;
- top questions;
- timeline;
- records attached or available;
- medication/supplement inventory;
- follow-up checklist;
- privacy review checklist.

## Rules

- Do not add new medical conclusions.
- Do not interpret records.
- Do not recommend treatment, medication, supplements, or delay.
- Do not include raw records unless the user explicitly chooses to attach them.
- Remove unnecessary identifiers before sharing through non-clinical channels.
- The person must review before sharing.

**Built on SIP** - Health Intelligence System command
