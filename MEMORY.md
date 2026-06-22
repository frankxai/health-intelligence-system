# MEMORY - Health Intelligence System

## Instance

- **Name:** Health Intelligence System
- **Slug:** `health-intelligence-system`
- **Date spawned:** 2026-06-15
- **Status:** v0.2 personal health ops draft layered on v0.1 cancer module
- **First module:** Cancer Intelligence
- **Evidence check:** 2026-06-22

## Commitments

- Build clinician-facing preparation artifacts.
- Keep real health data out of public files.
- Use source links for screening and treatment-education claims.
- Never recommend cancer treatment.
- Treat the cancer module as the first proof-of-pattern for HIS.
- Keep personal health operations separate from life-science research intelligence.
- Make privacy modes explicit: public/sanitized, consumer AI, health AI, regulated workspace, local-first, and private infrastructure.
- Keep `health-intelligence-system` as public core and use packs only when creation gates are met.
- Reference existing AI health systems honestly and classify them as reference, integrate later, watchlist, or do not emulate.
- Prefer clinician handoff, source ledgers, and private vaults over symptom-checking or treatment recommendations.
- Position the system as a way to become a better health operator and patient advocate, never as a way to become one's own doctor.
- Package the workflows as reusable agent surfaces: Codex plugin, Codex skill, prompt pack, command pack, and local vault templates.
- Treat wearable and phone data as private context and routine telemetry unless interpreted by a clinician.
- Use local small models only for optional redaction/classification review, not medical reasoning.

## Roadmap

1. v0.1 - cancer detection prep and treatment decision documentation.
2. v0.2 - private personal-health operations for nutrition, fitness, doctor-visit prep, record indexing, and LLM-assisted summaries.
3. v0.3 - private-instance export pattern, wearable manifest dry runs, and clinician handoff spec.
4. v0.4 - source freshness checker, prompt-pack evaluator, and external-system audit refresh loop.
5. v0.5 - disease-specific education packs with clinician-stated diagnosis gates.
6. v1.0 - repeatable HIS module pattern for other health domains.

## Open Questions

- Should this repo remain standalone or be mirrored under SIS `verticals/health-intelligence/`?
- Should cancer-type-specific packs live as private modules or public education-only stubs?
- Which jurisdiction should be primary beyond the current US guideline baseline?
- After repo-disposition review, should `life-science-research-intelligence-system` be a new public repo or bridged through `life-sciences` and `research-intelligence-os`?
- After workflow dry runs, should the private vault template become a GitHub template repo, downloadable ZIP, or Codex-guided local scaffold?
- Should disease-specific packs live as education-only public modules, private-instance modules, or both with a strict bridge boundary?
- Which agent-runtime adapters should be first-class beyond the Codex plugin: Claude Code, OpenCode, Open WebUI, or ChatGPT Projects?

**Built on SIP** - Health Intelligence System MEMORY.md v0.1
