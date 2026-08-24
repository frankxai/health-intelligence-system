# Health Intelligence Agent Pack

**Version:** legacy v0.2.1 surface<br>
**Release state:** installation, packaging, and promotion hold<br>
**Audience:** security, privacy, clinical-boundary, and migration reviewers only.

> Do not install or run this legacy pack as a health assistant. It predates the 2026-08-24 BIOS
> evidence, consent, and release gates and is retained only so reviewers can inspect and migrate its
> public materials. No agent-pack artifact is admitted by the current research-preview release.

The agent pack is the smallest practical download for running the system. It does not include the full documentation archive. It includes the operator surfaces that an agent or human can actually install, copy, and run.

## Included

| Surface | Path | Use |
| --- | --- | --- |
| Codex plugin | `plugins/health-intelligence-system/` | Installable plugin shell with skill metadata |
| Sovereign Health Operator skill | `plugins/health-intelligence-system/skills/sovereign-health-operator/` | Core agent behavior, privacy modes, wearable ingestion, possibility mapping, and operator workflows |
| Gut Family Journey skill | `plugins/health-intelligence-system/skills/gut-family-journey/` | Guided intake, ordinary family meal planning, practical adaptations, weekly review, and qualified coach handoff |
| Gut vertical contract | `verticals/gut-intelligence-system/`, `schemas/gut/`, `fixtures/gut/` | Open-core boundary, task envelope, machine-readable contracts, and fictional safety fixtures |
| Prompt pack | `prompts/` | ChatGPT Project, Custom GPT, Claude Project, and local redaction prompts |
| Command pack | `commands/` | Slash-command style workflows for setup, visit prep, handoff, wearable ingestion, redaction, and weekly review |
| Private vault templates | `templates/` | Copy into Obsidian, local folders, encrypted storage, or a private product runtime |
| Safety docs | `SAFETY.md`, `PRIVACY.md`, `VALIDATION.md` | Boundaries every consuming agent must preserve |

## Historical install flow — disabled

The previous download-and-install flow is intentionally disabled. A future replacement must package
exact blobs from one reviewed clean commit, pass integrity and privacy verification, and complete a
prompt-by-prompt safety review before these instructions become executable again.

## Boundary

This pack helps a person become a better health operator and patient advocate. It does not diagnose, interpret tests, prescribe, choose treatment, change medication, dose supplements, triage emergencies, or replace clinicians.

Raw health records stay local by default. Hosted AI receives only deliberate, reviewed, minimal, sanitized context.

**Built on SIP** - Health Intelligence Agent Pack
