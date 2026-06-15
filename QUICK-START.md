# Quick Start

**Evidence checked:** 2026-06-15  
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

## 3. Use Templates

Copy the relevant file from `templates/` into your private workspace, not this public repo:

- `cancer-screening-plan.md`
- `diagnostic-appointment-brief.md`
- `treatment-decision-brief.md`
- `clinician-summary.md`
- `evidence-ledger.md`
- `follow-up-plan.md`
- `side-effect-log.md`

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
