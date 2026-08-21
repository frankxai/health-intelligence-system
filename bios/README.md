# BIOS — Sovereign Health Intelligence Substrate

**Version:** 0.1.0-prerelease  
**Home:** lives inside [`health-intelligence-system`](../README.md) until creation gates justify split repos  
**Status:** executable protocol + reference CLI + wellness domain packs  
**Not medical advice.** Organize, measure n-of-1 ordinary-wellness experiments, and prepare clinician handoffs. Do not diagnose, prescribe, or interpret labs.

## Thesis (one paragraph)

Frontier models are being commoditized. The scarce asset is **structured, consented, longitudinal n-of-1 phenotype + outcome data**, owned at the edge, aggregatable without surveillance. BIOS claims the missing middle: vault · ledger · phenotype · **protocol** · claims · consent · egress · steward · contribution rail · clinician handoff.

## What ships in v0.1

| Surface | Path | Purpose |
| --- | --- | --- |
| Schemas | [`schemas/`](schemas/) | Machine-readable contracts for the ten primitives |
| Reference CLI | [`src/bios/`](src/bios/) | `init`, `observe`, `protocol`, `phenotype`, `handoff`, `validate` |
| Domain packs | [`packs/`](packs/) | Circadian, breath, nutrition, tea — claim-tiered, ordinary wellness |
| Household vault skeleton | [`templates/household-vault/`](templates/household-vault/) | Subject ≠ operator steward model |
| T0 ChatGPT pack | [`templates/t0-chatgpt-project-pack.md`](templates/t0-chatgpt-project-pack.md) | Grandma / phone-first operator pack |
| Decision record | [`../docs/bios-decision-2026-08-10.md`](../docs/bios-decision-2026-08-10.md) | Angles, landscape, monetization, 100-day plan |

## Quick start (subject zero)

```bash
# from repo root
python -m bios_substrate --help
python -m bios_substrate init --household demo-house --subject self --path ./_local/bios-demo
python -m bios_substrate observe --vault ./_local/bios-demo --subject self \
  --kind breath_session --note "box breathing 5 min" --tags breath,calm
python -m bios_substrate protocol start --vault ./_local/bios-demo --subject self \
  --pack circadian --id morning-light-10m
python -m bios_substrate phenotype rebuild --vault ./_local/bios-demo --subject self
python -m bios_substrate handoff --vault ./_local/bios-demo --subject self --out ./_local/handoff.md
python -m bios_substrate validate --vault ./_local/bios-demo
```

Local `_local/` is gitignored. Never commit real health records.

## Ten primitives

1. **Vault** — plain files under version control; unit of ownership is the **household** (subjects nested inside).
2. **Ledger** — append-only JSONL observations; never mutated.
3. **Phenotype** — derived projection of the ledger (chronotype-lite, constraints, stack, baselines).
4. **Protocol** — declarative n-of-1 intervention spec (the keystone format).
5. **Claims ledger** — every assertion carries evidence tier + source + review date.
6. **Consent lattice** — per-field × recipient × purpose × revocable.
7. **Egress boundary** — sensitivity class → model tier (local / TEE / frontier) with redaction as compile step.
8. **Agent contract** — manifests declare data classes, writes, tools, evidence tiers, escalations.
9. **Contribution rail** — emit protocol outcomes, never raw records (stub in v0.1).
10. **Clinician handoff** — deterministic one-pager: timeline, stack, questions, data-request template.

## Sovereignty tiers

| Tier | Who | Runtime |
| --- | --- | --- |
| T0 Whisper | Non-technical dependent | Existing ChatGPT / Meta AI + project pack; steward vault |
| T1 Steward | Family architect | Private repo or local vault + phone captures |
| T2 Sovereign | Privacy-maximal | Local LLM + local vault only |
| T3 Node | Builders / researchers | Full swarm (Hermes, Claude Code, Codex) + commons later |

## Safety hard lines

- No diagnosis. Differentials only as *questions for a clinician*.
- No prescribing medication, disease protocols, or medical nutrition therapy.
- Ordinary wellness experiments only (breath, light, sleep hygiene, meal timing, culinary herbs/teas).
- **Plant medicine / controlled substances:** jurisdiction routing field only — never dose or source guidance.
- Red-flag symptoms → emergency services; bypass agents.
- Contraindication gate runs before any protocol `start`.
- Claims without `evidence_tier` + `source` cannot load in packs.

## Repo topology (planned, not forced)

Per consolidation gates in [`docs/repo-consolidation-map.md`](../docs/repo-consolidation-map.md):

```text
bios-protocol   (schemas only)     — split when external implementers exist
bios            (reference CLI)    — this folder today
bios-packs      (domain packs)     — packs/ today
bios-connectors (MCP glue)         — later
bios-commons    (DP outcomes)      — after real n-of-1 mass
```

Mind / psychology / neuroscience frankxai repos become **domain packs**, not interconnected systems.

## Tests

```bash
python -m unittest discover -s bios/tests -v
```

## License

MIT — same as parent Health Intelligence System. Protocol text may dual-license CC-BY for schemas on split.
