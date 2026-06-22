# /health-possibility-map

Create a clinician-safe map of possible categories to discuss when the user has symptoms, concerns, abnormal data, or a known disease topic.

## Input

- Concern in the user's own words.
- Timeline.
- Relevant records or data available.
- Wearable or log patterns, if any.
- Known diagnosis or clinician-stated facts, if applicable.
- Country/jurisdiction.
- Urgency signals as described by user.

## Output

Use `templates/health-possibility-map.md`.

Include:

- facts provided;
- uncertainties;
- possible categories to ask about;
- missing records or data;
- clinician questions;
- safety routing.

## Rules

- Do not diagnose.
- Do not say what the user likely has.
- Do not interpret labs, imaging, pathology, genomics, or wearable data.
- Do not reassure that something is safe to wait on.
- Do not recommend treatment, medication, supplements, fasting, diet therapy, or delay.
- Severe, urgent, or rapidly worsening concerns route to qualified care.

**Built on SIP** - Health Intelligence System command
