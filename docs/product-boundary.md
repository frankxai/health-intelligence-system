# Product Boundary

**Evidence checked:** 2026-06-22  
**Scope:** product and repository architecture for Health Intelligence System, Agentic Life OS, Agentic Health OS, and Life Sciences Researcher IS. Not medical, legal, privacy, or compliance advice.

## Decision

Use this repo as the public Health Intelligence System protocol and release package. Use the private `frankxai/agentic-life-os` repo as the product monorepo. Inside that private product, Agentic Health OS is the personal-health runtime and Life Sciences Researcher IS is a research-only companion module.

Do not create another private health repo yet. The current split is strong enough:

| Layer | Repo or package | Audience | Holds private health data? | Job |
| --- | --- | --- | --- | --- |
| Health Intelligence System | `frankxai/health-intelligence-system` | Public users, agents, reviewers | No | Protocol, templates, plugin, release package, validation, safety contract |
| Agentic Life OS | `frankxai/agentic-life-os` | Private product runtime | Only in user-controlled private instances | Coordinates life modules and product UX |
| Agentic Health OS | `agentic-life-os/packages/health` | Personal health operators | Only in private vault integrations | Nutrition, training, sleep, routines, doctor prep, clinician handoff, personal health organization |
| Life Sciences Researcher IS | `agentic-life-os/packages/life-sciences-researcher` | Research operators | No | Literature, trials, mechanisms, biomedical data envelopes, research-only briefs |
| Future research repo | Deferred | Public research users | No | Split only if research workflows outgrow ALOS and HIS |

## Why This Split

Health has two very different risk surfaces:

- Personal health operations need privacy, continuity, empathy, and clinician handoff.
- Life-science research needs evidence grading, source provenance, literature discipline, and explicit non-clinical boundaries.

Combining them into one module would tempt the system to turn research into personal advice. Splitting them lets the product be useful without crossing that line.

## Naming

Use these names consistently:

- `Health Intelligence System`: public protocol and distributable package.
- `Agentic Life OS`: umbrella product for health, creator, business, family, memory, investor, and adjacent life modules.
- `Agentic Health OS`: personal health module inside Agentic Life OS.
- `Life Sciences Researcher IS`: research-only biomedical intelligence module.

Avoid using "Health Intelligence System" for the private runtime. HIS is the public safety contract that the runtime consumes.

## Bridges

Allowed bridges:

- HIS release package -> Agentic Health OS templates and commands.
- HIS safety contract -> Agentic Health OS refusal and routing logic.
- Life Sciences Researcher IS -> public research brief -> patient-friendly glossary -> clinician questions -> Agentic Health OS.
- Agentic Health OS -> clinician handoff export reviewed by the user.

Blocked bridges:

- Raw personal records -> public HIS repo.
- Raw personal records -> research repo.
- Research-only findings -> personal diagnosis, prognosis, treatment choice, medication changes, supplement dosing, or emergency triage.
- Wearable trends -> medical interpretation without clinician review.

## Repo Creation Gates

Create a separate public or private repo only when all are true:

- The module has a distinct maintainer or operating lane.
- It has at least five substantial files that make the current repo noisier.
- It has a different safety boundary from the current owner repo.
- It has a clear public/private data policy.
- It has a validation checklist.
- The first release is useful without private health data.

Current decision: keep the research companion inside private Agentic Life OS for now and publish the public safety/protocol layer through Health Intelligence System v0.2.0.

**Built on SIP** - Health Intelligence System product boundary
