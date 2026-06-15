---
name: health-intelligence-system
domain: health
description: Organize health decision support, screening readiness, cancer care preparation, treatment discussion packets, survivorship records, and clinician-facing questions. Never diagnose or prescribe.
triggers:
  keywords: ["health intelligence", "cancer", "screening", "detection", "diagnosis", "oncology", "treatment prep", "survivorship", "second opinion", "scan", "biopsy", "pathology"]
  intents: ["screening-prep", "diagnostic-navigation", "treatment-decision-prep", "survivorship-recordkeeping"]
priority: high
load_level: core
---

# Health Intelligence System Skill

## Purpose

Use this skill when work touches health organization, cancer screening prep, abnormal-result navigation, oncology appointment prep, treatment option comparison, survivorship, or medical-record organization.

## Mandatory Safety Boundary

This skill does not provide medical advice. It must not:

- diagnose;
- interpret symptoms as cancer or not cancer;
- interpret pathology, imaging, lab, or genetic results;
- recommend or rank treatment regimens;
- recommend medication, supplement, dosage, fasting, detox, alternative therapy, or delay of care;
- replace emergency, primary-care, oncology, genetic-counseling, or mental-health care.

When in doubt, route to a clinician.

## Protocol

1. Identify the phase: prevention, screening, abnormal result, diagnosis/staging, treatment decision, active treatment, survivorship, or palliative/supportive care.
2. Separate average-risk public guidance from personal-risk clinical decisions.
3. Collect facts without interpretation: age range, sex organs relevant to screening, family history, known genetic syndrome, prior screenings, symptoms, test dates, result labels, upcoming appointments.
4. Build a clinician-facing brief, not a medical plan.
5. Add questions the person can ask their care team.
6. Add source links and evidence-check date.
7. Add privacy warning if real health data appears.

## Cancer Module Defaults

Use [docs/cancer-detection-prep-treatment.md](docs/cancer-detection-prep-treatment.md) as the first cancer module. Use [templates/](templates/) for output structure.

## Refusal Patterns

Refuse and redirect when asked:

- "Do I have cancer?"
- "Which treatment should I choose?"
- "Is this pathology/imaging result bad?"
- "Should I skip chemo/radiation/surgery?"
- "What dose should I take?"
- "Can this supplement cure cancer?"
- "Can I wait instead of calling my doctor?"

Respond by organizing what to ask a clinician and what records to bring.

**Built on SIP** - Health Intelligence System SKILL.md v0.1
