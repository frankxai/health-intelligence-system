# /bios — Sovereign Health Intelligence Substrate

Initialize or operate a BIOS household vault, ordinary-wellness protocols, and clinician handoff.

Not medical advice. No diagnosis or prescribing.

## Steps

1. Read `bios/README.md` and `SAFETY.md`.
2. Init vault outside the public repo (e.g. private path or `_local/`).
3. Prefer claim-tiered packs under `bios/packs/` over inventing interventions.
4. Run contraindication gate; never `--force` without human review.
5. Export clinician handoff before visits; human reviews before share.

```bash
PYTHONPATH=bios/src python -m bios_substrate init --household "Family" --subject self --path "$HOME/bios-vaults/family"
PYTHONPATH=bios/src python -m bios_substrate observe --vault "$HOME/bios-vaults/family" --kind breath_session --note "box 5m" --tags breath
PYTHONPATH=bios/src python -m bios_substrate protocol start --vault "$HOME/bios-vaults/family" --pack breath --id box-breath-5m
PYTHONPATH=bios/src python -m bios_substrate handoff --vault "$HOME/bios-vaults/family"
```
