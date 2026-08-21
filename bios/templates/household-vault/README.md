# Household vault skeleton (reference)

Copy mentally via `python -m bios_substrate init` — do not store real records in the public HIS repo.

```text
household.json                 # household + subjects + stewards
.gitignore                     # media, parquet, duckdb, env
README.md
subjects/
  sub_<name>/
    ledger.jsonl               # append-only truth
    phenotype.json             # derived
    egress.json                # sensitivity → model tier
    consent/
      self-tracking.json
    protocols/
      active/
      completed/
    exports/                   # clinician handoffs
    media/                     # local photos (ignored)
```

## Household vs subject

- **Household** is the ownership and backup unit (chosen BIOS default).
- **Subject** is the person the data is about.
- **Steward/operator** may differ from subject (parents, adult children).
- Dignity clause: subject can read all records about themselves.

## Connect your knowledge bases

| Layer | Role |
| --- | --- |
| Personal vault (this tree) | System of record |
| Shared BIOS packs (repo `bios/packs`) | Curated protocols + claims |
| Your markdown second brain | Non-health projects; link out, don't merge raw PHI |
| ChatGPT/Claude project | Interface only — paste sanitized context |
| Optional private git remote | Encrypted or metadata-only; never default for raw clinical PDFs |
| DuckDB/SQLite index | Rebuildable projection from ledger (future `bios index`) |

## Research / commons (later)

Contribution rail emits **protocol outcomes** (intervention → measured delta → context vector), never raw records. Not enabled in v0.1.
