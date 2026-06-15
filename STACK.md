# STACK - Health Intelligence System

## Inherited

- **Protocol:** Starlight Intelligence Protocol.
- **File contract:** README, SKILL, SOUL, AGENTS, MEMORY, STACK, CANON, SUB-SYSTEMS.
- **Evidence ledger:** Markdown source register with evidence-check dates.
- **Private data rule:** Real health data belongs in private local storage, not in this repo.

## Suggested Private Instance Layout

```text
private/
|-- records/
|   |-- labs/
|   |-- imaging/
|   |-- pathology/
|   `-- visit-notes/
|-- cancer/
|   |-- screening/
|   |-- diagnostic/
|   |-- treatment/
|   `-- survivorship/
`-- exports/
```

`private/` is intentionally gitignored.

## Source Priority

1. Current clinician guidance from the treating team.
2. Specialty society or guideline bodies relevant to the cancer type.
3. USPSTF/CDC for population screening.
4. NCI for cancer education, treatment-type overview, clinical trial, and survivorship questions.
5. Peer-reviewed papers only when the document needs a research note and the evidence is not already covered by guidelines.

## Freshness Rule

- Screening summaries: check sources before publishing.
- Treatment content: never present regimen-level guidance as current unless tied to a clinician-verified plan.
- Clinical trial content: always verify against the live trial record and care team.

**Built on SIP** - Health Intelligence System STACK.md v0.1
