# Private Instance Setup Guide

**Evidence checked:** 2026-06-22  
**Scope:** how to create a private Health Intelligence System instance with local folders, Obsidian, optional Notion, optional ChatGPT, optional local LLMs, and optional Git. Not medical advice.

## Step 1: Choose Privacy Mode

Pick one before storing data.

| Mode | Choose this if | Tools |
| --- | --- | --- |
| Local-only | You do not want raw health data in cloud AI tools | local folders, Obsidian, encrypted disk, Codex/OpenCode/Hermes, Ollama/LM Studio |
| Hybrid | You want local records but cloud AI for sanitized summaries | local vault plus ChatGPT/Custom GPT/Project with sanitized context |
| Health cloud | You accept a dedicated health AI product for connected records | ChatGPT Health or comparable health-specific workspace |
| Regulated team | A clinic, company, or care team is involved | regulated workspace, audit logs, compliance review |

## Step 2: Create Private Folder

Create this outside public repositories:

```text
HealthVault/
|-- 00-command-center/
|-- 10-records/
|-- 20-doctor-visits/
|-- 30-daily-loops/
|-- 40-evidence/
|-- 50-jurisdiction/
`-- 90-exports/
```

Recommended first files:

- `00-command-center/private-vault-manifest.md`
- `00-command-center/general-health-command-center.md`
- `00-command-center/health-record-index.md`
- `00-command-center/medication-supplement-inventory.md`
- `20-doctor-visits/YYYY-MM-DD_doctor-visit-prep.md`
- `30-daily-loops/YYYY-WW_nutrition-fitness-weekly-loop.md`
- `40-evidence/source-ledger.md`
- `50-jurisdiction/jurisdiction-adapter.md`

## Step 3: Copy Templates

Copy from the public repo into the private vault:

- `templates/general-health-command-center.md`
- `templates/private-vault-manifest.md`
- `templates/health-record-index.md`
- `templates/doctor-visit-prep.md`
- `templates/nutrition-fitness-weekly-loop.md`
- `templates/disease-navigation-brief.md`
- `templates/medication-supplement-inventory.md`
- `templates/insurance-and-care-access-index.md`
- `templates/jurisdiction-adapter.md`
- `templates/evidence-ledger.md`
- `templates/clinician-summary.md`
- `templates/clinician-handoff-export.md`

## Step 4: Decide Whether To Use Git

Use Git for:

- templates;
- system docs;
- sanitized examples;
- encrypted backups;
- private configuration that contains no raw health data.

Do not use ordinary Git for:

- raw medical records;
- portal exports;
- images, scans, PDFs, lab reports, pathology reports;
- names, dates of birth, identifiers, insurance numbers;
- private family history.

If a user insists on Git for raw records, require encryption before commit and verify that generated files, previews, thumbnails, logs, and temporary files are excluded. This still needs a human privacy decision.

## Step 5: Obsidian Setup

Recommended:

- open `HealthVault/` as an Obsidian vault;
- keep attachments under `10-records/`;
- link each appointment to relevant records;
- use tags like `#appointment`, `#question`, `#record-request`, `#nutrition`, `#fitness`, `#follow-up`;
- keep dashboards simple.

## Step 6: Notion Setup

Use Notion for lower-sensitivity dashboards if desired:

- appointment tracker;
- habit dashboard;
- high-level record inventory;
- task list;
- non-sensitive source notes.

Avoid raw records and detailed private medical timelines unless the user knowingly accepts cloud storage and account-security risk.

## Step 7: ChatGPT Setup

If using ChatGPT:

1. Use ChatGPT Health when available for health-specific data.
2. Otherwise create a dedicated Project called `Health Intelligence`.
3. Turn on project-only memory if available and appropriate.
4. Turn memory off or use Temporary Chat for sensitive one-off questions.
5. Upload only sanitized summaries unless the user intentionally chooses otherwise.
6. Use prompts that ask for clinician questions, timelines, and source-backed education, not diagnosis.

Starter instruction:

```text
You are my Health Intelligence organizer. Help me organize records, timelines, doctor-visit questions, nutrition/fitness logs, and source-backed education. Do not diagnose, interpret test results, prescribe, recommend supplements, or choose treatment. When care decisions are involved, help me prepare questions for qualified clinicians.
```

## Step 8: Custom GPT Setup

Use a Custom GPT for reusable behavior, not as the source of truth.

Suggested knowledge files:

- public HIS safety docs;
- public HIS templates;
- fictional examples;
- no raw personal records unless the user intentionally accepts that storage model.

Suggested tools:

- web browsing for current public sources;
- file analysis for user-provided summaries;
- no autonomous external sharing.

## Step 9: Local LLM Setup

For local-first users:

- install Ollama or LM Studio;
- optionally install Open WebUI for a local chat interface;
- keep services bound to localhost or a trusted private network only;
- store model logs and chat histories in known locations;
- do not expose the local LLM server to the public internet;
- use Codex/OpenCode/Hermes for markdown and folder operations.

Local models are useful for:

- summarizing a private weekly log;
- converting messy notes into a doctor-visit draft;
- generating record-index entries from filenames;
- checking whether a document accidentally contains identifiers.

Local models are not automatically medically reliable. Use them for organization, not clinical judgment.

## Step 10: First Operating Loop

Day 1:

- create vault;
- copy templates;
- make command center;
- create private vault manifest;
- index existing records at a high level.

Before next appointment:

- create doctor-visit prep;
- update medication and supplement inventory as taken;
- gather records;
- list top three questions;
- create clinician summary export.

Weekly:

- fill nutrition/fitness loop;
- summarize patterns;
- save clinician/professional questions;
- update record index.

Monthly:

- audit missing records;
- check backups;
- check source freshness;
- review privacy mode.

**Built on SIP** - Health Intelligence System setup guide
