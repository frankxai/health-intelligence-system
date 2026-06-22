# /wearable-data-ingestion

Create a private ingestion plan for smartwatch, smart ring, phone, WHOOP, Oura, Apple Health, Android Health Connect, Garmin, Fitbit, or manual health data.

## Input

- Devices and apps.
- Export/API access available.
- Date range.
- Private vault location.
- Whether cloud AI may see sanitized summaries.
- Timezone and units.
- User notes for travel, illness, stress, soreness, alcohol, medication changes, or device changes.

## Output

Use `templates/wearable-data-ingestion-manifest.md`.

Include:

- source inventory;
- export method;
- raw file location;
- normalized fields;
- aggregation plan;
- privacy status;
- questions for clinician or qualified professional.

## Rules

- Keep raw exports local by default.
- Do not upload raw wearable exports to public repos.
- Do not interpret wearable data medically.
- Do not diagnose sleep, heart, endocrine, psychiatric, or recovery conditions.
- Convert concerning patterns into clinician questions.

**Built on SIP** - Health Intelligence System command
