# Open-Core Boundary

## Decision

Keep the reusable family journey public. Keep partner science, personal health data, and commercial service operations private.

This is a product architecture contract, not medical advice. The public core does not diagnose, interpret raw microbiome reports, or prescribe care.

| Capability | Public core | Licensed / private adapter |
| --- | --- | --- |
| Family-context schema | Yes | May extend privately |
| Consent, age, allergy, scope, and claims gates | Yes | Cannot weaken |
| Meal-planning workflow and ordinary recipes | Yes | Branded library may extend |
| Weekly review and coach handoff | Yes | Coach protocols and service playbooks |
| Evidence receipt format | Yes | Proprietary evidence library |
| Microbiome interpretation | No | Qualified partner only |
| Taxa-to-food or score-to-action mappings | No | Qualified partner only |
| Proprietary claims and thresholds | No | Qualified partner only |
| Personal profiles, reports, and longitudinal history | No | Private family runtime |
| Brand, product UI, payments, coach console | No | Commercial product |

## Science Adapter Contract

The public core accepts a deliberately narrow envelope:

```json
{
  "adapter_id": "qualified-partner-adapter",
  "adapter_version": "1.0.0",
  "reviewed_at": "2026-07-01",
  "evidence_grade": "partner-reviewed",
  "goals": ["increase_food_variety"],
  "approved_food_categories": ["legumes", "whole_grains"],
  "excluded_claims": ["treats_condition"],
  "human_review_required": false
}
```

The adapter must not send raw sequencing files, taxonomic tables, clinical notes, identifiers, or unrestricted free text to the public planning core.

## Commercial Pattern

A partner can sell a branded family journey, coach-supported program, or outcomes subscription on top of this core. The defensible layer is the qualified interpretation model, evidence governance, service design, longitudinal data rights, and human support—not a closed copy of the generic workflow.

## Non-Degradation Rule

Private adapters may add stricter controls. They must not remove public-core allergy, consent, scope, evidence, or handoff gates.

**Built on SIP** - Gut Intelligence System open-core boundary v0.1
