# Agentic Life OS Integration

**Evidence checked:** 2026-06-22  
**Scope:** how private Agentic Life OS should consume the public Health Intelligence System release. Not medical advice.

## Integration Contract

Agentic Life OS should treat Health Intelligence System as an upstream protocol package, not as a place to store user data.

The private product runtime should consume:

- templates from `templates/`;
- commands from `commands/`;
- safety and privacy language from `SAFETY.md`, `PRIVACY.md`, `VALIDATION.md`, and `REVIEW-GATE.md`;
- architecture docs from `docs/architecture.md`, `docs/product-boundary.md`, and `docs/safety-and-privacy-model.md`;
- plugin skill material from `plugins/health-intelligence-system/`.

The private product runtime should not copy:

- real health records into this repo;
- private vault files into release assets;
- clinician notes into public examples;
- raw wearable exports into public issues, commits, or artifacts.

## Module Mapping

| Agentic Life OS module | HIS source material | Runtime behavior |
| --- | --- | --- |
| Agentic Health OS | `templates/general-health-command-center.md`, `templates/nutrition-fitness-weekly-loop.md`, `commands/doctor-visit-prep.md` | Personal planning, routine tracking, private vault organization |
| Clinician handoff | `templates/clinician-handoff-export.md`, `commands/clinician-handoff-export.md` | User-reviewed export for appointments |
| Cancer prep | `docs/cancer-detection-prep-treatment.md`, cancer command surfaces | Screening prep, abnormal-result organization, treatment discussion questions |
| Jurisdiction adapter | `docs/jurisdiction-and-record-access-model.md`, `templates/jurisdiction-adapter.md` | Record access and care-navigation notes with legal uncertainty preserved |
| Life Sciences Researcher IS | `docs/companion-research-systems.md`, `docs/repo-consolidation-map.md` | Research-only evidence briefs and clinician-question translation |

## Runtime Rules

Agentic Health OS must:

- classify each request before answering;
- refuse diagnosis, test interpretation, treatment selection, dosing, urgent triage, or clinician replacement;
- route urgent or potentially serious symptoms to qualified care;
- keep raw records local by default;
- produce source-dated, user-reviewable outputs;
- export clinician-facing packets separately from private notes.

Life Sciences Researcher IS must:

- mark outputs as research-only;
- preserve source, retrieval date, evidence type, and limitations;
- separate established evidence from hypothesis;
- translate research into clinician questions, not personal directives;
- avoid storing or requesting personal records.

## Release Consumption Flow

```text
GitHub Release ZIP
  -> verify ZIP and manifest
  -> import templates/commands/docs into private ALOS build
  -> wire Agentic Health OS intent router
  -> run safety/refusal tests
  -> run private UX walkthrough with fictional data
  -> publish website download links to GitHub Release
```

## Validation Checklist

- `npm run package:release` succeeds in HIS.
- `npm run verify:release` succeeds in HIS.
- Agentic Life OS health tests pass.
- Agentic Life OS orchestrator tests pass.
- No public artifact contains real health data, private memory, API keys, tokens, or personal identifiers.
- UI copy says "clinician questions" or "care preparation" instead of "medical answer" or "treatment recommendation".

**Built on SIP** - Health Intelligence System Agentic Life OS integration
