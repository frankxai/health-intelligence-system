# Gut Family Onboarding

## Purpose

Create the minimum safe context for an ordinary-wellness family meal journey. Do not collect a raw microbiome report, medical record, identifiable child profile, or free-form symptom history.

## Inputs

- Parent confirmation and data-scope choice.
- Child alias and age band.
- Allergy status, known allergens, clinician exclusions, and whether a medical diet applies.
- Up to three family goals.
- Accepted foods, learning foods, avoid foods, preparation time, budget band, and school days.
- Optional approved science envelope from a qualified adapter.

## Workflow

1. Explain the scope: family meal organization and coach questions, not medical advice.
2. Ask the parent to choose the minimum data scope.
3. Capture the context using `templates/gut-family-context.md`.
4. Validate it against `schemas/gut/family-context.schema.json`.
5. Stop if consent, age band, or allergy status is missing.
6. Route to a qualified professional if a medical diet, symptom, abnormal result, growth concern, eating disorder, or treatment question appears.
7. If a science envelope exists, validate provenance and allowed claim scope. Never request raw results.
8. Produce a short context summary for parent review before planning.

## Output

- Parent-reviewed family context.
- Gate result: `ready`, `blocked`, or `qualified_review_required`.
- Missing information list.
- Explicit list of information not collected.

**Built on SIP** - Gut family onboarding v0.1
