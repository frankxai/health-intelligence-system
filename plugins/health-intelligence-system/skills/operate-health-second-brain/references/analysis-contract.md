# Daily wellness analysis

CSV header: `date,metric,value,unit,source_id` exactly. Each row is one daily aggregate from one source, never an event or workout set. Dates are real ISO local dates already normalized by the adapter. Sleep uses wake-up day. Normalize original timestamps before generating this CSV; timezone labels cannot fix travel-related day boundaries.

Supported metrics: sleep_hours/hours; steps/count; movement_minutes/minutes; training_minutes/minutes; energy_rating/rating_1_5; meal_regular_day/boolean. The last is a user-defined routine marker, not a food-quality judgment. It is optional and must not encourage restrictive eating. Zero means positively reported zero, never an imputed absence.

The analyzer validates exact headers, metric/unit pairs, finite numeric values, real dates, and source tokens; rejects invalid files; removes exact duplicate daily rows; excludes conflicting daily values; and requires source selection when multiple sources occur in the 14-day window. It emits every supported metric, including no-data states.

Compare adjacent seven-day windows ending on --end. Emit a difference only with at least four observed days in EACH window from the same chosen source. This is a completeness heuristic, not clinical/statistical validation. Means cover observed days only: no imputation, significance test, causal claim, recommendation, or readiness score. Report coverage beside every value. Weekday/weekend imbalance, travel, sickness and source changes confound comparisons.

Bounds are parser sanity limits, not healthy ranges. Derived output remains sensitive. source_id is a pseudonymous token, never a name, credential or record text. The analyzer cannot establish consent, source authenticity, identity, deletion, encryption, or permission to share.
