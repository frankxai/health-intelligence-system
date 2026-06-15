# /cancer-second-opinion-packet

Prepare a records checklist and summary for a second opinion after a confirmed or suspected cancer diagnosis.

## Input

- Diagnosis and stage as currently documented, if known.
- Treating facility and clinicians.
- Pathology report status.
- Imaging report and image-file status.
- Biomarker/genomic test status.
- Current treatment proposal, if any.

## Output

Use `templates/treatment-decision-brief.md`, with emphasis on the records section and unanswered questions.

## Rules

- Do not imply the first opinion is wrong.
- Do not choose between clinicians.
- Do not interpret pathology, imaging, or biomarkers.
- Flag missing records clearly.
- Ask whether timing allows a second opinion before treatment begins.

**Built on SIP** - Health Intelligence System command
