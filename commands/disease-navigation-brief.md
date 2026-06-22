# /disease-navigation-brief

Prepare a source-backed disease navigation brief for clinician discussion.

## Input

- Diagnosis or condition name as written by clinician, if available.
- Country or care jurisdiction.
- Current clinician-stated plan, if any.
- Records available.
- Questions, symptoms, constraints, and goals in the user's own words.
- Source preferences or required guideline bodies.

## Output

Use `templates/disease-navigation-brief.md`.

## Rules

- Do not diagnose.
- Do not interpret labs, imaging, pathology, or genetic results.
- Do not recommend treatment, medication, supplements, diet therapy, fasting, or delay.
- Separate public education from personal care.
- Include evidence-check date and source links.
- Convert uncertainty into clinician questions.

**Built on SIP** - Health Intelligence System command
