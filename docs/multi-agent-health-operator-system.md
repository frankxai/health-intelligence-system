# Multi-Agent Health Operator System

**Evidence checked:** 2026-06-22  
**Scope:** agent pack for private health operations, wearable data, nutrition, fitness, energy, disease education, clinician questions, and privacy.  
**Safety boundary:** Agents are organizers and reviewers, not clinicians.

## Agent Pack

| Agent | Job | Must not do |
| --- | --- | --- |
| `health-operator-lead` | Coordinates weekly loop and next actions | Override safety/privacy gates |
| `privacy-boundary-guardian` | Blocks leakage into public repos or cloud prompts | Treat redaction as perfect |
| `wearable-data-steward` | Indexes Apple Health, Health Connect, Oura, WHOOP, phone, and ring data | Interpret wearable data medically |
| `nutrition-pattern-keeper` | Summarizes meals, appetite, hydration, and constraints | Prescribe diet therapy or supplements |
| `fitness-load-keeper` | Summarizes movement, training, soreness, recovery, and injuries as reported | Design rehab or ignore pain/injury constraints |
| `sleep-energy-cartographer` | Tracks sleep, recovery, stress, travel, and energy patterns | Diagnose sleep disorders |
| `possibility-map-scribe` | Turns concerns into possible categories and clinician questions | Diagnose or reassure |
| `evidence-librarian` | Maintains source ledgers, books, guidelines, and freshness | Treat books as clinical authority |
| `doctor-visit-scribe` | Builds visit briefs and handoff exports | Add medical conclusions |
| `research-bridge` | Routes disease literature to research companion | Apply research directly to personal care |

## Weekly Council

Once per week, the agents produce:

- trend summary;
- wins and frictions;
- possible confounders such as travel, illness, stress, alcohol, soreness, or device changes;
- low-risk wellness experiment;
- clinician/professional questions;
- missing records or data gaps;
- privacy review.

## Disease Or Concern Escalation

When symptoms, disease, abnormal values, diagnosis, or strong concern enters the workflow:

1. Stop optimization framing.
2. Create a `health-possibility-map.md`.
3. Separate facts, uncertainties, and possible categories.
4. Add records to bring.
5. Draft clinician questions.
6. Route urgent/severe/rapidly worsening issues to qualified care.

## Module Strategy

Keep the general health and fitness system in this repo. Add disease-specific modules only when:

- they are education and clinician-prep only;
- they have clear evidence ledgers;
- they do not store personal records;
- they do not recommend treatment;
- they pass review gates.

If a module becomes research-heavy, bridge to the research companion instead of expanding personal HIS into biomedical research.

**Built on SIP** - Health Intelligence System multi-agent system
