# Validation Checklist

Run this before publishing, packaging, or sharing an artifact.

## SIP Contract

- [ ] README, SKILL, SOUL, AGENTS, MEMORY, STACK, CANON, and SUB-SYSTEMS exist.
- [ ] Artifact includes "Built on SIP" where it composes SIP structure.
- [ ] Source repo and release version are named.

## Health Safety

- [ ] Artifact says it is not medical advice.
- [ ] It does not diagnose, stage, interpret results, or recommend treatment.
- [ ] It does not interpret labs, imaging, pathology, genomics, wearable data, or clinician notes.
- [ ] It separates screening, diagnosis, treatment, and survivorship.
- [ ] It routes symptoms, abnormal tests, and severe side effects to clinicians.
- [ ] It does not recommend supplements, alternative protocols, medication changes, or delayed care.
- [ ] Nutrition and fitness content is ordinary wellness tracking only, not diet therapy, supplement dosing, injury rehab, or disease treatment.
- [ ] Disease navigation uses clinician-stated facts and turns uncertainty into clinician questions.
- [ ] Research outputs do not become personal care instructions.

## Evidence

- [ ] Evidence-check date is present.
- [ ] Source links are present and current.
- [ ] Public screening guidance is described as average-risk baseline, not personal instruction.
- [ ] Treatment content is education and question preparation only.
- [ ] External systems are classified as `reference`, `integrate later`, `watchlist`, or `do not emulate`.
- [ ] Repo disposition decisions mark evidence level: `local-read`, `github-read`, `inventory-only`, or `proposed`.

## Privacy

- [ ] No real names, dates of birth, identifiers, or contact details.
- [ ] No real pathology, imaging, lab, genomic, medication, or treatment records.
- [ ] No private family history.
- [ ] No private files from `private/` are included.
- [ ] No raw private files from `HealthVault/` are included.
- [ ] Any AI-sanitized context was reviewed before export.

## Workflow Dry Runs

- [ ] Netherlands user using Obsidian plus a ChatGPT Project.
- [ ] Local-only user using Ollama, LM Studio, or Open WebUI.
- [ ] Caregiver preparing a complex doctor visit.
- [ ] US user requesting records through HIPAA/FHIR-style workflows.
- [ ] Researcher asking a disease literature question routed to the research companion.

## Release Package

- [ ] `npm run package:release` completes.
- [ ] ZIP exists in `dist/`.
- [ ] GitHub Release includes `release-manifest.json` with checksums.
- [ ] `npm run verify:release` passes for the local ZIP and manifest.
- [ ] Downloaded GitHub Release assets pass `scripts/verify-release.ps1 -Version <version> -Download`.
- [ ] GitHub Release is marked prerelease until clinical/legal review is logged.

**Built on SIP** - Health Intelligence System validation checklist v0.1
