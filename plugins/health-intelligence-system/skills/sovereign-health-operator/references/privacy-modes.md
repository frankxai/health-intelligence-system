# Privacy Modes

## Decision

Use the least data exposure that still gets the job done.

| Mode | Use when | Rule |
| --- | --- | --- |
| Manual/local | Maximum privacy | No model sees raw records |
| Local coding agent | User accepts local file access | Agent reads private files only in explicit session |
| Tiny local LLM | Redaction/classification helper | Never sole privacy barrier |
| ChatGPT/Claude project | Convenience matters | Use reviewed sanitized summaries |
| Health-specific cloud | User accepts dedicated health product | Keep health separate from general chat |
| Regulated workspace | Care team or organization | Follow compliance policy |

## Small Local Model Rule

Small models are optional. Use them for privacy preflight and rough classification, not health reasoning. Prefer deterministic redaction plus human review before model review.

## Cloud Prompt Rule

Before cloud use, create:

- what the model needs to know;
- what was removed;
- remaining sensitivity;
- user consent note;
- expiration/delete note if supported.

**Built on SIP** - Sovereign Health Operator reference
