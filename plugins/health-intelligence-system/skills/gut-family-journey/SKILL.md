---
name: gut-family-journey
description: Build a safe, practical family meal journey from parent-owned preferences, routines, allergy constraints, and an optional approved science-adapter envelope. Use for guided family intake, ordinary meal planning, picky-eater adaptations, school and travel planning, weekly reviews, and coach handoffs. Never diagnose, interpret raw microbiome or medical tests, prescribe diet therapy or supplements, or store identifiable child health data in public systems.
---

# Gut Family Journey

## Outcome

Help a parent turn an approved family context into one manageable week of ordinary meals, observe what worked, and prepare useful questions for a qualified coach or clinician.

## Required Gates

Before planning, verify:

1. Parent consent and chosen data scope.
2. Child age band.
3. Confirmed allergy status and exclusions.
4. No medical diet, symptom assessment, abnormal-result interpretation, growth concern, eating-disorder request, treatment question, or supplement request.
5. If science is used: adapter identity, version, review date, evidence grade, permitted food categories, excluded claims, and human-review flag.

Missing or failed gates stop planning. Route the family to qualified review where appropriate.

## Workflow

1. Run `commands/gut-family-onboarding.md`.
2. Summarize the minimum context and ask the parent to review it.
3. Run `commands/gut-first-week-plan.md`.
4. Anchor every meal in an accepted food, add at most one optional learning food, and provide a familiar fallback.
5. Fit preparation, budget, school, travel, and food-acceptance constraints.
6. Generate `templates/gut-evidence-receipt.md`.
7. After the week, run `commands/gut-weekly-review.md`.
8. Export parent-approved observations with `commands/gut-coach-handoff.md`.

## Authority

- The parent owns goals, consent, preferences, and use of the plan.
- A qualified clinician or dietitian owns medical assessment and medical nutrition therapy.
- A licensed science adapter owns microbiome interpretation and science-to-action mappings.
- The public core owns workflow structure, deterministic gates, evidence receipts, and handoff formatting.

## Data Rule

Use aliases and the minimum necessary context. Do not request or retain names, birth dates, contact details, raw reports, taxonomic tables, medical records, medication lists, or identifiable coach messages. Completed family artifacts belong in a private workspace.

## Claims Rule

Use language such as "try", "observe", "ordinary meal", and "question for your qualified professional." Never say a food repairs, balances, heals, treats, prevents, or guarantees a microbiome or health outcome.

## References

Read `references/journey-runtime.md` for the system topology, adapter contract, state model, and termination rules.

**Built on SIP** - Gut Family Journey skill v0.1
