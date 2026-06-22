# /privacy-preflight-redaction

Prepare a private health summary for possible cloud AI, Notion, email, portal, or collaborator use.

## Input

- Draft context or export.
- Destination: ChatGPT, Claude, Notion, email, portal, clinician, caregiver, or public example.
- Minimum task the destination needs to solve.
- User's accepted privacy mode.

## Output

Use `templates/ai-sanitized-context-export.md`.

Include:

- destination and purpose;
- removed data categories;
- remaining sensitivity;
- what the AI may do;
- what the AI must not do;
- human review checkbox.

## Local Model Option

A tiny local model can be used as a second-pass reviewer for obvious identifiers, but it is optional and not sufficient by itself. Use deterministic removal and human review first.

## Rules

- Remove names, dates of birth, addresses, emails, phone numbers, IDs, exact appointment details, clinician names tied to a case, file paths, insurance identifiers, portal exports, and family identifiers unless explicitly required.
- Do not send raw records to public examples.
- Do not promise anonymization.
- Label the result as sanitized, not anonymous.

**Built on SIP** - Health Intelligence System command
