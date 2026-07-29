# Gut Family Journey Runtime

## Topology

`guided intake -> deterministic gates -> approved science envelope -> meal-plan compiler -> reality adapters -> parent review -> weekly reflection -> qualified handoff`

The model may draft human-facing language only after deterministic gates have established a safe candidate set.

## Adapter Input

Accept only the fields defined in `schemas/gut/science-envelope.schema.json`. Reject raw reports, taxonomy, identifiers, free-text clinical interpretations, missing review dates, or unbounded claims.

## State

- Public core: schemas, policies, templates, fictional fixtures, and executable evaluations.
- Private runtime: consent record, family context, longitudinal observations, coach communication, and any source report.
- Model context: a minimal, parent-reviewed projection of private state.

## Termination

- Missing consent, age band, or allergy status: block.
- Medical diet or clinically relevant request: qualified review.
- Invalid adapter provenance or claims scope: block science-assisted planning.
- No safe food candidates: block and request human review.
- Parent rejects the plan: terminate the cycle without persuasion.

## Evidence Receipt

Every generated plan or review names:

- inputs used and deliberately excluded;
- core and adapter versions;
- gate results;
- authority owners;
- claim scope;
- required review.

**Built on SIP** - Gut Family Journey runtime v0.1
