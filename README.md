# Health Intelligence System

> SIP-aligned health intelligence layer for prevention, detection readiness, diagnosis navigation, treatment decision prep, and survivorship recordkeeping.

**Tier:** sovereign domain sub-stack under SIS  
**Status:** `v0.2.0 preclinical-prerelease`<br>
**First module:** Personal Health Operations, with Cancer Intelligence as the first clinical-prep module<br>
**Evidence check:** 2026-06-22<br>
**Release gate:** preclinical public prerelease until clinical/legal review is logged  
**License:** MIT for repo scaffold and protocols; private health records never belong in this public repo.

## What This Is

Health Intelligence System is the organizational layer for health decisions. It helps a person keep evidence, questions, appointments, test results, family history, screening history, treatment options, side effects, and follow-up plans in one coherent system.

It is designed to compose with SIS and the private Agentic Life OS product line without pretending to be a doctor:

- It prepares appointments, questions, and decision briefs.
- It tracks source provenance and date of guideline checks.
- It separates average-risk screening guidance from personal risk.
- It keeps diagnosis, treatment selection, medication dosing, and emergency decisions with licensed clinicians.

Product boundary:

- `health-intelligence-system` is the public protocol, templates, release package, prompt pack, Codex plugin, and safety contract.
- `agentic-life-os` is the private product monorepo where the usable Agentic Health OS runtime should live.
- Agentic Health OS handles personal health organization, nutrition/training/wellness loops, clinician-prep workflows, and private vault orchestration.
- Life Sciences Researcher IS is research-only. It may produce evidence briefs and clinician questions, but it does not interpret personal records or choose care.

Core positioning:

- Help people become better health operators and patient advocates, not their own doctors.
- Aggregate records, wearable exports, routines, questions, and clinician instructions into a private working system.
- Use AI for summarization, organization, redaction, checklist generation, and question preparation.
- Keep diagnosis, lab interpretation, medication changes, supplement dosing, treatment selection, injury rehab, and emergency triage with licensed clinicians.

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

## Personal Health Operations v0.2 Draft

The next layer extends the same safety model into a private personal-health command center for nutrition, fitness, doctor-visit prep, health-record indexing, and LLM-assisted summaries.

Start with:

- [docs/research-audit-ai-health-agents-2026.md](docs/research-audit-ai-health-agents-2026.md) - source-backed audit of AI health-agent, health-data, local-LLM, and research-intelligence references.
- [docs/external-systems-comparison.md](docs/external-systems-comparison.md) - evidence-grade comparison matrix for systems to reference, integrate later, watch, or avoid emulating.
- [docs/built-on-inspired-by.md](docs/built-on-inspired-by.md) - public positioning and attribution posture.
- [docs/architecture.md](docs/architecture.md) - public repo, private vault, AI layer, clinician handoff, and research companion architecture.
- [docs/safety-and-privacy-model.md](docs/safety-and-privacy-model.md) - safety, privacy, source, model-mode, research, jurisdiction, and release gates.
- [docs/what-this-is-not.md](docs/what-this-is-not.md) - plain-language boundary page.
- [docs/sovereign-health-ecosystem-blueprint.md](docs/sovereign-health-ecosystem-blueprint.md) - open ecosystem blueprint for local folders, Obsidian, Notion, ChatGPT, Custom GPTs, local LLMs, and coding agents.
- [docs/private-instance-setup-guide.md](docs/private-instance-setup-guide.md) - setup path for a private personal health vault.
- [docs/jurisdiction-and-record-access-model.md](docs/jurisdiction-and-record-access-model.md) - adapter model for the Netherlands, Germany, Spain, Croatia, the US, China, and other jurisdictions.
- [docs/companion-research-systems.md](docs/companion-research-systems.md) - proposed separation between personal health operations and life-science research intelligence.
- [docs/repo-consolidation-map.md](docs/repo-consolidation-map.md) - decision map for HIS core, future packs, research companions, and adjacent FrankX/Starlight repos.
- [docs/product-boundary.md](docs/product-boundary.md) - exact split between public HIS, private Agentic Life OS, Agentic Health OS, and Life Sciences Researcher.
- [docs/agentic-life-os-integration.md](docs/agentic-life-os-integration.md) - how the private product runtime should consume this public release.
- [docs/personal-health-ops-v0.2.md](docs/personal-health-ops-v0.2.md) - private-instance architecture draft.
- [docs/coding-agent-installation-guide.md](docs/coding-agent-installation-guide.md) - how to install the repo into Codex, Claude Code, OpenCode, and similar coding agents.
- [docs/multi-agent-health-operator-system.md](docs/multi-agent-health-operator-system.md) - role map for vault, wearable, doctor-visit, optimization, disease-navigation, research, and safety agents.
- [docs/wearable-data-ingestion-and-privacy.md](docs/wearable-data-ingestion-and-privacy.md) - Apple Health, Health Connect, Oura, WHOOP, and Health.md-style export model.
- [docs/prompt-pack-chatgpt-claude.md](docs/prompt-pack-chatgpt-claude.md) - ChatGPT Project, Custom GPT, Claude Project, and local redaction prompts.
- [docs/health-optimization-knowledge-shelf.md](docs/health-optimization-knowledge-shelf.md) - evidence-aware shelf for fitness, nutrition, sleep, mobility, and patient-advocacy references.

Then copy the relevant templates into a private workspace:

- `private-vault-manifest.md`
- `general-health-command-center.md`
- `health-record-index.md`
- `medication-supplement-inventory.md`
- `doctor-visit-prep.md`
- `nutrition-fitness-weekly-loop.md`
- `disease-navigation-brief.md`
- `jurisdiction-adapter.md`
- `insurance-and-care-access-index.md`
- `clinician-handoff-export.md`
- `wearable-data-ingestion-manifest.md`
- `health-operator-weekly-review.md`
- `health-possibility-map.md`
- `ai-sanitized-context-export.md`

The v0.2 command surfaces are:

1. `/private-health-instance-setup` - choose privacy mode and create the first private vault.
2. `/doctor-visit-prep` - prepare a 72-hour appointment brief.
3. `/disease-navigation-brief` - create source-backed education and clinician questions for a clinician-stated condition.
4. `/jurisdiction-adapter` - localize record access, portals, insurance, and cross-border notes.
5. `/clinician-handoff-export` - produce a reviewed clinician-facing export.
6. `/external-system-audit` - classify external systems as reference, integrate later, watchlist, or do not emulate.
7. `/repo-consolidation-map` - decide whether an artifact belongs in core, a pack, or a research companion.
8. `/wearable-data-ingestion` - turn wearable and phone exports into a private manifest and sanitized summaries.
9. `/health-optimization-weekly-review` - summarize sleep, training, nutrition, energy, symptoms, and adherence patterns without medical claims.
10. `/health-possibility-map` - organize possibilities, evidence, uncertainties, and clinician questions without diagnosis.
11. `/privacy-preflight-redaction` - prepare sanitized context before using consumer or hosted AI.

This v0.2 layer is for personal organization and clinician-facing preparation. It does not diagnose, interpret results, prescribe diets, prescribe training, recommend supplements, or replace clinicians.

Installable agent surfaces:

- `plugins/health-intelligence-system/` packages the repo as a Codex-compatible plugin with the `sovereign-health-operator` skill.
- `prompts/` contains project prompts for ChatGPT, Custom GPTs, Claude, and local redaction assistants.
- `commands/` contains slash-command style workflows that other coding agents can import or adapt.
- Local-only users can run the same workflows inside Obsidian plus a local assistant stack such as Ollama, LM Studio, Open WebUI, OpenCode, or a private API gateway.

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
|-- plugins/
|-- prompts/
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
- Verify the release ZIP with [VERIFY.md](VERIFY.md).
- Read safety boundaries in [SAFETY.md](SAFETY.md).
- Read privacy rules in [PRIVACY.md](PRIVACY.md).
- Build the release ZIP locally with `npm run package:release`.
- Check a local package with `npm run verify:release`.

The GitHub release ZIP is the canonical public download. Website download pages should link to GitHub Releases rather than storing duplicate archives.

## Evidence Sources

The first evidence ledger is [docs/evidence-sources.md](docs/evidence-sources.md). Core sources include USPSTF, CDC, and NCI. Clinical recommendations change; every public-facing health artifact must carry an evidence-check date and source links.

## Built on SIP

This repo adopts the SIP file contract, sovereignty clause, attestation pattern, and composition discipline from Starlight Intelligence System.

**Built on SIP** - Starlight Intelligence Protocol v1.1.1
