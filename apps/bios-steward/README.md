# BIOS Steward synthetic preview

This source tree is a **read-only, synthetic design preview**, not a health app. It is excluded from
the public release package and must not be deployed as a personal-data surface.

Hard-disabled by design:

- personal, household, wearable, clinical, genomic, image, or identifying data entry;
- browser persistence, including `localStorage`, IndexedDB, cookies, and accounts;
- protocol start, medical advice, symptom evaluation, clinician handoff generation, export, upload,
  clipboard sharing, or network submission.

The cards are synthetic evidence-contract labels. All shipped BIOS claims and protocols remain
`draft` / `draft_synthetic` and the governed Python runtime refuses to start them.

## Local engineering checks

```bash
pnpm install --frozen-lockfile
pnpm lint
pnpm typecheck
pnpm build
```

Running the page locally is a visual engineering check only. Do not enter real data because there is
no approved private storage architecture in this prototype.
