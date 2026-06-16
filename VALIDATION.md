# Validation Checklist

Run this before publishing, packaging, or sharing an artifact.

## SIP Contract

- [ ] README, SKILL, SOUL, AGENTS, MEMORY, STACK, CANON, and SUB-SYSTEMS exist.
- [ ] Artifact includes "Built on SIP" where it composes SIP structure.
- [ ] Source repo and release version are named.

## Health Safety

- [ ] Artifact says it is not medical advice.
- [ ] It does not diagnose, stage, interpret results, or recommend treatment.
- [ ] It separates screening, diagnosis, treatment, and survivorship.
- [ ] It routes symptoms, abnormal tests, and severe side effects to clinicians.
- [ ] It does not recommend supplements, alternative protocols, medication changes, or delayed care.

## Evidence

- [ ] Evidence-check date is present.
- [ ] Source links are present and current.
- [ ] Public screening guidance is described as average-risk baseline, not personal instruction.
- [ ] Treatment content is education and question preparation only.

## Privacy

- [ ] No real names, dates of birth, identifiers, or contact details.
- [ ] No real pathology, imaging, lab, genomic, medication, or treatment records.
- [ ] No private family history.
- [ ] No private files from `private/` are included.

## Release Package

- [ ] `npm run package:release` completes.
- [ ] ZIP exists in `dist/`.
- [ ] GitHub Release includes `release-manifest.json` with checksums.
- [ ] `npm run verify:release` passes for the local ZIP and manifest.
- [ ] Downloaded GitHub Release assets pass `scripts/verify-release.ps1 -Version <version> -Download`.
- [ ] GitHub Release is marked prerelease until clinical/legal review is logged.

**Built on SIP** - Health Intelligence System validation checklist v0.1
