# Health Intelligence Agent Pack

**Version:** v0.2.1  
**Release state:** preclinical public prerelease  
**Audience:** people installing the Health Intelligence System operator surface into Codex, Claude, ChatGPT, OpenCode, local assistants, or a private vault workflow.

The agent pack is the smallest practical download for running the system. It does not include the full documentation archive. It includes the operator surfaces that an agent or human can actually install, copy, and run.

## Included

| Surface | Path | Use |
| --- | --- | --- |
| Codex plugin | `plugins/health-intelligence-system/` | Installable plugin shell with skill metadata |
| Sovereign Health Operator skill | `plugins/health-intelligence-system/skills/sovereign-health-operator/` | Core agent behavior, privacy modes, wearable ingestion, possibility mapping, and operator workflows |
| Prompt pack | `prompts/` | ChatGPT Project, Custom GPT, Claude Project, and local redaction prompts |
| Command pack | `commands/` | Slash-command style workflows for setup, visit prep, handoff, wearable ingestion, redaction, and weekly review |
| Private vault templates | `templates/` | Copy into Obsidian, local folders, encrypted storage, or a private product runtime |
| Safety docs | `SAFETY.md`, `PRIVACY.md`, `VALIDATION.md` | Boundaries every consuming agent must preserve |

## Install Flow

1. Download `health-intelligence-agent-pack-v0.2.1.zip` from the GitHub Release.
2. Verify `agent-pack-manifest.json` or run:

```powershell
npm run verify:agent-pack -- -Version 0.2.1 -Download
```

3. Copy `templates/` into a private vault, not a public repository.
4. Install or adapt the surface you need:
   - Codex: use `plugins/health-intelligence-system/`.
   - ChatGPT Project: use `prompts/chatgpt-project-system-prompt.md`.
   - Custom GPT: use `prompts/custom-gpt-instructions.md`.
   - Claude Project: use `prompts/claude-project-prompt.md`.
   - Local assistant/redaction: use `prompts/local-llm-redaction-prompt.md`.
5. Start with `/private-health-instance-setup`, then `/doctor-visit-prep` or `/health-optimization-weekly-review`.

## Boundary

This pack helps a person become a better health operator and patient advocate. It does not diagnose, interpret tests, prescribe, choose treatment, change medication, dose supplements, triage emergencies, or replace clinicians.

Raw health records stay local by default. Hosted AI receives only deliberate, reviewed, minimal, sanitized context.

**Built on SIP** - Health Intelligence Agent Pack
