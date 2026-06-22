# Coding Agent Installation Guide

**Evidence checked:** 2026-06-22  
**Scope:** install and use Health Intelligence System as a Codex, Claude Code, OpenCode, or comparable coding-agent pack.  
**Safety boundary:** This guide helps set up private health operations. It does not make the agent a clinician.

## What This Installs

The repo now ships a local plugin-style pack:

```text
plugins/
`-- health-intelligence-system/
    |-- .codex-plugin/plugin.json
    `-- skills/
        `-- sovereign-health-operator/
```

The skill helps an agent scaffold and operate:

- private health vault;
- wearable-data ingestion;
- nutrition, fitness, sleep, recovery, and energy review loops;
- possibility maps for clinician discussion;
- doctor visit prep and clinician handoff exports;
- privacy preflight before any cloud AI use.

## Codex Local Plugin

Use the repo-local plugin path:

```text
<repo>/plugins/health-intelligence-system
```

Recommended flow:

1. Install or load the plugin from the local path using the Codex app/plugin workflow available in your environment.
2. Start a new Codex thread in the private health vault folder, not the public repo, when handling private data.
3. Invoke the skill as `$sovereign-health-operator`.
4. Ask it to create or update only local private-vault files.
5. Run `/privacy-preflight-redaction` before moving any summary into ChatGPT, Claude, Notion, email, or a portal.

## Claude Code / OpenCode / Other Coding Agents

If a plugin mechanism is not available, copy the skill instruction into the agent's project instructions:

```text
Use the Health Intelligence System repo as source. Load the sovereign-health-operator skill from:
plugins/health-intelligence-system/skills/sovereign-health-operator/SKILL.md

Follow its privacy, safety, wearable-ingestion, possibility-mapping, and clinician-handoff rules.
```

Then point the agent at the private vault folder, not this public repo, when private records are involved.

## ChatGPT / Claude Project Prompt Pack

Use:

- `prompts/chatgpt-project-system-prompt.md`
- `prompts/custom-gpt-instructions.md`
- `prompts/claude-project-prompt.md`
- `prompts/local-llm-redaction-prompt.md`

Cloud project prompts should receive sanitized context by default. They should not be the raw private health database.

## Default Agent Permissions

| Capability | Public repo | Private vault |
| --- | --- | --- |
| Read docs/templates | Yes | Yes, with user intent |
| Create templates | Yes | Yes |
| Read raw records | No | Only in explicit private session |
| Upload records to cloud AI | No | Only after user review and consent |
| Diagnose or prescribe | No | No |
| Create clinician questions | Yes | Yes |

## First Task To Run

```text
Use $sovereign-health-operator to set up my private health vault. Start with privacy mode, folder layout, templates to copy, wearable sources to inventory, and first weekly review.
```

**Built on SIP** - Health Intelligence System installation guide
