# Portable health memory

Use these logical collections in the selected private system. One folder and an index may suffice.

| Collection | Minimum contract | Update rule |
|---|---|---|
| Context | Stated goal, time, equipment, preferences, exclusions, timezone, source/date | Reconfirm stale constraints when consequential |
| Observations | ID, source reference, observed time/day, unit, value, method, received time | Corrections supersede originals |
| Sources | Provider/file, window, timezone convention, import receipt, quality limits | Connection state and freshness are separate |
| Knowledge | Claim, URL, publication/review date, population, evidence level, limits | Citation is not personal applicability |
| Decisions | User-chosen action, reason, observation IDs, time/cost burden | Separate suggestion from adoption |
| Experiments | One reversible change, start/end, measure, stop rule, confounders | Before/after is not proof of causation |
| Care preparation | Reported timeline, exact medicine inventory, questions, reviewed export | Preserve provider instructions |

Portable exports carry schema version, units, timezone rules, provenance and correction/deletion semantics. Pseudonymization is not anonymization. Reference raw files instead of reproducing them across tools.

Keep one private system of record and deliberate minimum working copies. Exclude health data from public repositories/dashboards, error logs, traces, URLs, broad indexes and creator/business memory. Encryption and restoration must be implemented at storage level, not declared in a prompt.

Revocation stops future reads; it does not delete imported records or summaries. Handle deletion separately, respecting existing authorization and showing the affected scope before irreversible action. This skill does not supply a live authority backend.
