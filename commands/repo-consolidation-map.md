# /repo-consolidation-map

Map whether a Health Intelligence System feature belongs in the core repo, a future pack, a research companion, or an adjacent FrankX/Starlight repo.

## Input

- Feature or artifact name.
- Intended audience.
- Data sensitivity.
- Safety boundary.
- Existing candidate repos.
- Source of evidence: local-read, GitHub-read, inventory-only, or proposed.

## Output

Use `templates/repo-disposition-matrix.md` and update `docs/repo-consolidation-map.md` when the decision is durable.

Disposition options:

- `core`;
- `absorb pattern`;
- `bridge`;
- `pack later`;
- `specialized pack`;
- `watch`;
- `leave alone`;
- `do not create`.

## Rules

- Keep `health-intelligence-system` as the public personal health core.
- Do not create a new repo until the creation gates in `docs/repo-consolidation-map.md` are met.
- Keep raw personal health records out of every public repo.
- Keep research workflows separate from personal health records.
- Mark evidence level clearly.

**Built on SIP** - Health Intelligence System command
