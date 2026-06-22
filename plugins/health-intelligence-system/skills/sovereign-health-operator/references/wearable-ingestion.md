# Wearable Ingestion

## Sources

Use official exports and APIs when available:

- Apple Health export or HealthKit.
- Android Health Connect.
- Oura API v2.
- WHOOP Developer API where user has access.
- Garmin/Fitbit/phone exports where available.
- Manual CSV when APIs are unavailable.

## Normalized Fields

Track source, date range, timezone, device, export method, and units. Keep raw exports private.

Preferred summaries:

- sleep duration and regularity;
- resting heart rate;
- HRV where available;
- steps and activity minutes;
- workouts and training load;
- recovery/readiness scores as vendor-specific signals;
- user notes for illness, alcohol, travel, stress, soreness, and unusual days.

## Boundary

Wearable data is context, not diagnosis. Do not interpret abnormal patterns medically. Turn concerning trends into clinician questions.

**Built on SIP** - Sovereign Health Operator reference
