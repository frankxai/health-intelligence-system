# /external-system-audit

Audit an external AI health, clinical-agent, health-data, research-agent, or local/private LLM system for possible HIS reference or integration.

## Input

- System name.
- URL or repository.
- Category: personal health, clinical agent, medical RAG, data standard, research agent, local/private AI, jurisdictional service, or other.
- Current source date.
- Claimed capabilities.
- Data handled.
- Privacy/security posture.
- Medical or clinical claims.
- License or availability if relevant.

## Output

Use `templates/external-system-comparison-matrix.md` or update `docs/external-systems-comparison.md`.

Classify the system as:

- `reference`;
- `integrate later`;
- `watchlist`;
- `do not emulate`.

## Audit Questions

- What does this system actually do?
- Is it personal-health, clinical-care, research, infrastructure, or general AI?
- Does it store or process private health data?
- Does it make diagnosis, treatment, medication, supplement, or emergency claims?
- Is it open-source, proprietary, research-only, or regulated-workspace oriented?
- What can HIS learn from it?
- What must HIS avoid copying?
- What source proves the claim?

## Rules

- Use primary sources where possible.
- Include source URL and access date.
- Do not repeat marketing claims as fact without labeling them.
- Do not imply HIS has equivalent clinical performance.
- Do not adopt a connector or paid service without a separate cost/impact gate.

**Built on SIP** - Health Intelligence System command
