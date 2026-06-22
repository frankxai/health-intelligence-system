# Wearable Data Ingestion And Privacy

**Evidence checked:** 2026-06-22  
**Scope:** aggregate smartwatch, smart ring, phone, WHOOP, Oura, Apple Health, Android Health Connect, and similar data into a private Health Intelligence System vault.  
**Safety boundary:** Wearable data is useful context. It is not diagnosis, emergency triage, or treatment guidance.

## Principle

Raw exports stay private. HIS works from summaries, source metadata, and reviewed trend notes.

## Source Map

| Source | Access path | HIS use | Boundary |
| --- | --- | --- | --- |
| Apple Health / Apple Watch | Apple Health export or HealthKit | Steps, workouts, sleep, heart rate, health samples | Do not upload raw XML to public or cloud AI by default |
| Android phone / wearables | Health Connect | Shared Android health and fitness data types | Respect app permissions and units |
| Oura Ring | Oura API v2 or app exports | Sleep, readiness, activity, HRV-style signals | Vendor scores are context, not diagnosis |
| WHOOP | WHOOP Developer API where available | Sleep, strain, recovery, activity | Access may require developer app or partner terms |
| Garmin / Fitbit / other | Official export/API where available | Workouts, sleep, HR, activity | Prefer official exports; note gaps |
| Manual logs | CSV or markdown | Meals, energy, symptoms, stress, soreness | User-entered context is still private |

## Normalization Contract

For every import, record:

- source;
- device;
- date range;
- timezone;
- export method;
- raw file location;
- units;
- missing fields;
- known device/app changes;
- whether the data can be shared with cloud AI.

## Privacy Preprocessing

Default order:

1. Keep raw export local.
2. Generate aggregate summary locally.
3. Remove identifiers, exact locations, filenames, and medical-record references.
4. Human review.
5. Optional tiny local model review for obvious identifiers.
6. Only then send minimal context to cloud AI if desired.

Do not rely on a small local model as the only privacy barrier. Use it as an extra reviewer, not a lock on the door.

## What To Summarize

| Domain | Useful summary | Avoid |
| --- | --- | --- |
| Sleep | Duration, consistency, wake time, subjective quality | Diagnosing sleep disorder |
| Recovery | Resting HR, HRV-style trends, soreness, illness notes | Medical interpretation |
| Activity | Steps, training sessions, zone minutes, strength sessions | Injury rehab advice |
| Nutrition | Meal timing, protein-containing meals, hydration, alcohol | Diet therapy |
| Energy | User-rated energy, mood/stress, travel, workload | Psychiatric or endocrine diagnosis |

## Source Ledger

- Apple Health export support: https://support.apple.com/guide/iphone/share-your-health-data-iph5ede58c3d/ios
- Apple HealthKit: https://developer.apple.com/documentation/healthkit
- Android Health Connect: https://developer.android.com/health-and-fitness/health-connect
- Oura API v2: https://cloud.ouraring.com/v2/docs
- WHOOP Developer Platform: https://developer.whoop.com/docs/introduction/
- Health.md: https://github.com/CodyBontecou/health-md

**Built on SIP** - Health Intelligence System wearable ingestion
