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

- [ ] Claim receipts carry review/correction/supersession dates; no manifest hardcodes an
  `evidence_checked` date.
- [ ] Source links are present and current.
- [ ] Public screening guidance is described as average-risk baseline, not personal instruction.
- [ ] Treatment content is education and question preparation only.
- [ ] External systems are classified as `reference`, `integrate later`, `watchlist`, or `do not emulate`.
- [ ] Repo disposition decisions mark evidence level: `local-read`, `github-read`, `inventory-only`, or `proposed`.
- [ ] Every BIOS claim has a DOI, PMID, or authority URL plus PICO/timeframe, outcome and harms certainty, directness, funding/COI, integrity/correction/supersession dates, and rights/ingestion mode.
- [ ] Evidence tiers follow A/B/C/D/E/Q semantics; E is discovery only and Q is quarantine, and neither
  can support an active claim or reviewed protocol.
- [ ] Books, podcasts, newsletters, and creator media remain `idea_source_only`; no copyrighted full text is packaged and no user-facing protocol cites an idea source directly.
- [ ] No shipped claim is active or user-facing; no shipped protocol or pack is reviewed/startable.
- [ ] Active-claim tests reject unchecked, stale, retracted, expression-of-concern, rights-incompatible,
  and discovery-only sole-source evidence.

## Privacy

- [ ] No real names, dates of birth, identifiers, or contact details.
- [ ] No real pathology, imaging, lab, genomic, medication, or treatment records.
- [ ] No private family history.
- [ ] No private files from `private/` are included.
- [ ] No raw private files from `HealthVault/` are included.
- [ ] Any AI-sanitized context was reviewed before export.
- [ ] Handoff tests prove exact subject/recipient/processor/purpose/action/data-class/tier/event/run
  consent, complete default-deny egress rules, identifier handling, and signed/hash-bound receipts.
- [ ] Recipient output reveals no denied sensitivity classes, omission counts, or raw ledger count.
- [ ] Cross-subject lines, duplicate JSON keys, unknown fields, invalid/future chronology,
  duplicate/ambiguous consent, revoked/expired consent, and malformed egress fail closed.

## Executable BIOS Gates

- [ ] `python -m unittest discover -s bios/tests -v` passes.
- [ ] `python -m bios_substrate validate --vault <synthetic-vault>` passes.
- [ ] The start API and CLI expose no `--force`; real shipped-fixture tests prove every current pack
  and protocol is non-startable.
- [ ] Runtime validation executes the published Draft 2020-12 schemas with format checking before
  stricter semantics.
- [ ] The bounded domain-agent registry contains only stewardship, movement/training, martial-arts movement, culinary botanicals, and complementary-practice education.
- [ ] Complementary-practice content separates subjective/traditional context from established evidence and never asserts an unproven energy mechanism as fact.

## Workflow Dry Runs

- [ ] Netherlands user using Obsidian plus a ChatGPT Project.
- [ ] Local-only user using Ollama, LM Studio, or Open WebUI.
- [ ] Caregiver preparing a complex doctor visit.
- [ ] US user requesting records through HIPAA/FHIR-style workflows.
- [ ] Researcher asking a disease literature question routed to the research companion.

## Release Package

- [ ] `npm run package:release` completes.
- [ ] Packaging starts only from one clean commit/tree/index, rejects untracked/ignored/forbidden
  content, and archives exact Git blobs rather than recursively copying the worktree.
- [ ] ZIP exists in `dist/`.
- [ ] GitHub Release includes `release-manifest.json` with checksums.
- [ ] `npm run verify:release` passes for the local ZIP and manifest.
- [ ] Downloaded GitHub Release assets pass `scripts/verify-release.ps1 -Version <version> -Download`.
- [ ] GitHub Release is marked prerelease until clinical/legal review is logged.

**Built on SIP** - Health Intelligence System validation checklist v0.1
