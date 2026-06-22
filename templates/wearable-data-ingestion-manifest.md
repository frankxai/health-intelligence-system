# Wearable Data Ingestion Manifest

**Person/private slug:** `<private>`  
**Prepared on:** `<YYYY-MM-DD>`  
**Date range:** `<YYYY-MM-DD to YYYY-MM-DD>`  
**Privacy mode:** `<local-only / hybrid / health cloud / regulated team / private infrastructure>`  
**Medical disclaimer:** Wearable data is context for wellness tracking and clinician questions, not diagnosis.

## Source Inventory

| Source | Device/app | Export/API method | Date range | Raw file location | Share status |
| --- | --- | --- | --- | --- | --- |
| Apple Health / Apple Watch | | | | | |
| Android Health Connect | | | | | |
| Oura | | | | | |
| WHOOP | | | | | |
| Garmin/Fitbit/other | | | | | |
| Manual logs | | | | | |

## Normalized Fields

| Field | Source | Unit | Timezone | Notes |
| --- | --- | --- | --- | --- |
| Sleep duration | | | | |
| Sleep timing | | | | |
| Resting heart rate | | | | |
| HRV-style signal | | | | |
| Steps/activity minutes | | | | |
| Workouts/training | | | | |
| Recovery/readiness score | | | | |
| Energy/stress notes | | | | |

## Context Notes

- Travel:
- Illness:
- Alcohol:
- High stress:
- Soreness/injury:
- Device/app changes:
- Missing data:

## Privacy Check

- [ ] Raw exports stay local.
- [ ] Cloud AI receives only reviewed summaries, if any.
- [ ] File paths and identifiers removed from summaries.
- [ ] Vendor scores are labeled as context, not diagnosis.

**Built on SIP** - Health Intelligence System template
