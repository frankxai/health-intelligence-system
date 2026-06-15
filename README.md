# Health Intelligence System

> SIP-aligned health intelligence layer for prevention, detection readiness, diagnosis navigation, treatment decision prep, and survivorship recordkeeping.

**Tier:** sovereign domain sub-stack under SIS  
**Status:** `v0.1.0 preclinical-prerelease`  
**First module:** Cancer Intelligence  
**Evidence check:** 2026-06-15  
**Release gate:** preclinical public prerelease until clinical/legal review is logged  
**License:** MIT for repo scaffold and protocols; private health records never belong in this public repo.

## What This Is

Health Intelligence System is the organizational layer for health decisions. It helps a person keep evidence, questions, appointments, test results, family history, screening history, treatment options, side effects, and follow-up plans in one coherent system.

It is designed to compose with SIS without pretending to be a doctor:

- It prepares appointments, questions, and decision briefs.
- It tracks source provenance and date of guideline checks.
- It separates average-risk screening guidance from personal risk.
- It keeps diagnosis, treatment selection, medication dosing, and emergency decisions with licensed clinicians.

## What This Is Not

- Not medical advice.
- Not diagnosis.
- Not treatment recommendation.
- Not medication, supplement, or protocol design.
- Not a replacement for oncology, primary care, genetic counseling, or emergency care.
- Not a place to store real private health data in public git history.

If a person has symptoms, abnormal tests, suspected cancer, confirmed cancer, severe side effects, or urgent clinical concerns, this system routes them to qualified care.

## Sub-System Map

| Sub-system | Purpose | First artifacts |
| --- | --- | --- |
| Prevention & Risk | Family history, exposure inventory, risk-factor questions | `risk-inventory.md`, `family-history-map.md` |
| Screening & Detection | Age/risk-based screening checklist and appointment prep | `screening-plan.md`, `screening-gap-list.md` |
| Diagnostic Navigation | Abnormal-result brief, specialist questions, test timeline | `diagnostic-brief.md`, `records-request.md` |
| Treatment Planning | Tumor-board prep, options comparison, second-opinion packet | `treatment-decision-brief.md` |
| Supportive Care & Survivorship | Side-effect tracking, follow-up schedule, survivorship plan | `side-effect-log.md`, `follow-up-plan.md` |
| Evidence & Clinician Interface | Source ledger, guideline freshness, clinician handoff | `evidence-sources.md`, `clinician-summary.md` |

## Daily-5

These are the five practical surfaces for v0.1:

1. `/cancer-screening-plan` - build an average-risk screening checklist and flag clinician questions.
2. `/cancer-diagnostic-brief` - organize an abnormal result, symptoms, prior tests, and next appointment questions.
3. `/cancer-treatment-board-prep` - prepare a structured treatment discussion packet.
4. `/cancer-second-opinion-packet` - gather pathology, imaging, staging, and treatment proposal records.
5. `/cancer-follow-up-plan` - track post-treatment surveillance questions and long-term effects.

## Repo Layout

```text
.
|-- AGENTS.md
|-- CANON.md
|-- MEMORY.md
|-- README.md
|-- SKILL.md
|-- SOUL.md
|-- STACK.md
|-- SUB-SYSTEMS.md
|-- commands/
|-- docs/
`-- templates/
```

## Cancer Module

Start with [docs/cancer-detection-prep-treatment.md](docs/cancer-detection-prep-treatment.md). It covers:

- screening vs diagnosis;
- cancer-screening prep;
- abnormal-result escalation;
- cancer treatment decision prep;
- clinical trial questions;
- survivorship and follow-up records;
- safety boundaries and emergency routing.

## Download and Validate

- Start with [QUICK-START.md](QUICK-START.md).
- Validate the package with [VALIDATION.md](VALIDATION.md).
- Read safety boundaries in [SAFETY.md](SAFETY.md).
- Read privacy rules in [PRIVACY.md](PRIVACY.md).
- Build the release ZIP locally with `npm run package:release`.

The GitHub release ZIP is the canonical public download. Website download pages should link to GitHub Releases rather than storing duplicate archives.

## Evidence Sources

The first evidence ledger is [docs/evidence-sources.md](docs/evidence-sources.md). Core sources include USPSTF, CDC, and NCI. Clinical recommendations change; every public-facing health artifact must carry an evidence-check date and source links.

## Built on SIP

This repo adopts the SIP file contract, sovereignty clause, attestation pattern, and composition discipline from Starlight Intelligence System.

**Built on SIP** - Starlight Intelligence Protocol v1.1.1
