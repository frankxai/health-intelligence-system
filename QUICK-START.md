# Quick Start

**Evidence checked:** 2026-06-22<br>
**Status:** preclinical public prerelease until clinical/legal review is logged.

## 1. Read the Boundary First

Health Intelligence System is a decision-preparation and recordkeeping system. It does not diagnose, interpret results, recommend treatment, prescribe medication, or replace care.

If symptoms, abnormal results, suspected cancer, confirmed cancer, or severe side effects are involved, use this system to prepare for qualified clinical care.

## 2. Pick the Right Cancer Workflow

| Situation | Start here |
| --- | --- |
| You are well and want to organize screening | `commands/cancer-screening-plan.md` |
| You have an abnormal result or symptom-based referral | `commands/cancer-diagnostic-brief.md` |
| You have a confirmed diagnosis and oncology options | `commands/cancer-treatment-board-prep.md` |
| You want another oncologist to review records | `commands/cancer-second-opinion-packet.md` |
| You are after treatment or between treatment phases | `commands/cancer-follow-up-plan.md` |

## 2b. Or Start A Private General Health Workflow

For nutrition, fitness, routine health organization, and doctor-visit preparation, start with:

- `docs/what-this-is-not.md`
- `docs/safety-and-privacy-model.md`
- `docs/architecture.md`
- `docs/research-audit-ai-health-agents-2026.md`
- `docs/external-systems-comparison.md`
- `docs/built-on-inspired-by.md`
- `docs/sovereign-health-ecosystem-blueprint.md`
- `docs/private-instance-setup-guide.md`
- `docs/jurisdiction-and-record-access-model.md`
- `docs/companion-research-systems.md`
- `docs/repo-consolidation-map.md`
- `docs/personal-health-ops-v0.2.md`
- `templates/private-vault-manifest.md`
- `templates/general-health-command-center.md`
- `templates/health-record-index.md`
- `templates/medication-supplement-inventory.md`
- `templates/doctor-visit-prep.md`
- `templates/nutrition-fitness-weekly-loop.md`
- `templates/disease-navigation-brief.md`
- `templates/jurisdiction-adapter.md`
- `templates/insurance-and-care-access-index.md`
- `templates/clinician-handoff-export.md`

Keep these in a private workspace. Use them to track facts, routines, records, questions, and visit prep, not to diagnose or choose treatment.

Useful v0.2 commands:

- `commands/private-health-instance-setup.md`
- `commands/doctor-visit-prep.md`
- `commands/disease-navigation-brief.md`
- `commands/jurisdiction-adapter.md`
- `commands/clinician-handoff-export.md`
- `commands/external-system-audit.md`
- `commands/repo-consolidation-map.md`

## 3. Use Templates

Copy the relevant file from `templates/` into your private workspace, not this public repo:

- `cancer-screening-plan.md`
- `diagnostic-appointment-brief.md`
- `treatment-decision-brief.md`
- `clinician-summary.md`
- `clinician-handoff-export.md`
- `evidence-ledger.md`
- `follow-up-plan.md`
- `side-effect-log.md`
- `private-vault-manifest.md`
- `general-health-command-center.md`
- `health-record-index.md`
- `medication-supplement-inventory.md`
- `doctor-visit-prep.md`
- `nutrition-fitness-weekly-loop.md`
- `disease-navigation-brief.md`
- `jurisdiction-adapter.md`
- `insurance-and-care-access-index.md`

## 4. Keep Private Data Private

Create a private folder outside public git history:

```text
private/
|-- records/
|-- cancer/
`-- exports/
```

Do not commit names, dates of birth, medical record numbers, pathology reports, imaging files, lab values, treatment dates, medications, clinician names tied to a private case, insurance data, or appointment notes.

## 5. Validate Before Sharing

Run through [VALIDATION.md](VALIDATION.md) before sharing any artifact. Public artifacts must have:

- medical disclaimer;
- evidence-check date;
- source links;
- no private health data;
- no diagnosis or treatment recommendation;
- clear clinician handoff.

**Built on SIP** - Health Intelligence System quick start v0.1
