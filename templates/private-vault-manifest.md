# Private Vault Manifest

**Person/private slug:** `<private>`  
**Created:** `<YYYY-MM-DD>`  
**Updated:** `<YYYY-MM-DD>`  
**Privacy mode:** `<local-only / hybrid / health cloud / regulated team / private infrastructure>`  
**Storage location:** `<local path or private storage note>`  
**Medical disclaimer:** This vault organizes personal health records and questions. It is not medical advice.

## Folder Map

| Folder | Purpose | Contains raw health data? | Backup rule |
| --- | --- | --- | --- |
| `00-command-center/` | Dashboard, open questions, record index | No, unless user adds private notes | Encrypted backup |
| `10-records/` | Labs, imaging, visit notes, PDFs, portal exports | Yes | Encrypted backup only |
| `20-doctor-visits/` | Visit prep, completed notes, referrals | Yes | Encrypted backup only |
| `30-daily-loops/` | Nutrition, fitness, sleep, symptoms, energy | Potentially | Encrypted backup only |
| `40-evidence/` | Public source ledger and education notes | Usually no | Can be synced if sanitized |
| `50-jurisdiction/` | Record access, portals, insurance, care routing | Potentially | Encrypted backup only |
| `90-exports/` | Clinician handoffs and sanitized AI context | Review each file | Share deliberately |

## Tooling

| Tool | Purpose | Data allowed | Notes |
| --- | --- | --- | --- |
| Obsidian | Local markdown vault | Private if local | Strong default |
| Notion | Dashboard/task layer | Lower-sensitivity or accepted cloud data | Avoid raw records by default |
| ChatGPT Project | AI organization | Sanitized or deliberate context | Avoid general memory drift |
| ChatGPT Health | Dedicated health AI | User-accepted connected data | Use where available and appropriate |
| Local LLM | Private summaries | Raw data if local setup is trusted | Check logs and network exposure |
| Git | Templates and sanitized docs | No raw records by default | Use encrypted archives only if needed |

## Red Lines

- [ ] No raw records in public Git.
- [ ] No private identifiers in public examples.
- [ ] No uncontrolled cloud sync for raw records unless deliberately accepted.
- [ ] No clinical decisions delegated to AI.
- [ ] No source-backed artifact without an evidence-check date.

**Built on SIP** - Health Intelligence System template
