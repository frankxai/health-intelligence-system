# BIOS — Sovereign Health Intelligence Substrate
### Angle analysis, primitive stack, repo topology, and the recommended build

> Historical design exploration, superseded for runtime behavior by the 2026-08-24 synthetic
> foundation. References to protocol execution or personal vault use are not current instructions.

Date: 2026-08-10 · Author of record: Frank / Starlight Intelligence · Status: decision document, v0.1 executed  
Implementation home: [`../bios/`](../bios/) inside `frankxai/health-intelligence-system` (branch `agent/hermes/bios-v01`)

---

## 0. Source correction and the actual thesis

The paper framing is Meta's *personal biologist / personalized therapies* trajectory (Zuckerberg public note, Aug 2026), not a Mehta paper. Two ideas matter:

- people's involvement unlocks personalized therapies and long-tail conditions;
- new roles appear — personal biologists using superintelligence with n-of-1 data.

Model layer is being commoditized (frontier labs + Biohub-class open models). **Do not build foundation bio models here.**

Javorsky-style critique still holds: without interoperable, consented longitudinal data rails, "superintelligence cures X" fails on systems and incentives, not IQ.

**Thesis:** the scarce asset is *structured, consented, longitudinal n-of-1 phenotype + outcome data, owned at the edge, aggregatable without surveillance.* BIOS claims the format.

**Positioning:** not a health app — the contribution rail + protocol format for personal biologists and families.

---

## 1. GitHub landscape (summary)

| Layer | State | Action |
| --- | --- | --- |
| Research agents (Biomni, bio MCP, skills) | Mature | Absorb / wrap later |
| Wearable / PHR connectors | Commodity | Fork MCP glue later |
| Consumer longevity OS | Shallow (e.g. longevity-os ~low stars) | Territory open |
| **Middle: n-of-1 protocol + consent + claims + steward + commons** | **Empty** | **Build** |

Existing frankxai surface:

| Repo | Disposition |
| --- | --- |
| `health-intelligence-system` | **Core** — BIOS lands here first |
| `agentic-life-os` | Private runtime consumer |
| `family-intelligence-systems` | Pattern source (consent, household) |
| `second-brain-os` | Two-vault privacy pattern |
| mind / psych / neuroscience IS repos | Future **domain packs**, not interconnected systems |
| `human-mind-intelligence-system` etc. | Collapse into packs when curated |

Do **not** wire N repos together. One ledger · one phenotype · one protocol format · packs.

---

## 2. Five angles (compose, don't pick one)

| | Angle | Verdict |
|---|---|---|
| A | Personal Health OS / vault + agents | Wedge — reference client of B |
| B | Protocol + Commons format | Spine |
| C | Skill/agent registry | Growth loop later |
| D | Evidence / claims engine | Moat |
| E | Embodiment (breath → cohort → retreat) | Cash + initiation (Arcanea/FrankX) |

Order: **B defines format → A proves it → D makes A valuable → E monetizes → C scales supply.**

---

## 3. Ten primitives (implemented as schemas)

See `bios/schemas/*`. Keystone = **Protocol**. Ownership unit = **household** (steward model).

Trust gates: contraindication before start; no diagnosis; jurisdiction flags; red-flag route to emergency services.

---

## 4. Storage decision

Canonical = **Markdown/JSON + JSONL under local (optionally private-git) filesystem**.  
DuckDB/SQLite = derived index later.  
Notion = view only.  
High-frequency streams = Parquet outside git.

---

## 5. Sovereignty tiers

T0 Whisper (ChatGPT pack) · T1 Steward · T2 local LLM · T3 builder node.  
Differentiator: **subject ≠ operator** with dignity clause.

---

## 6. Repo topology

Stay inside HIS until creation gates fire (`docs/repo-consolidation-map.md`). Planned split names: `bios-protocol`, `bios`, `bios-packs`, `bios-connectors`, `bios-commons`.

---

## 7. Monetization posture

Open substrate. Charge curation packs, steward hosting, embodiment. Never sell the individual record. Protocol packs (teas, breath, circadian) = premium later under FrankX/Arcanea branding; schema stays neutral **BIOS**.

---

## 8. What shipped in this execution (Days 1–14 kickoff)

- [x] Schemas for ledger, protocol, claim, consent, egress, household, phenotype, agent manifest  
- [x] Reference CLI scaffolding exists; all shipped protocol starts are now blocked synthetic tests
- [x] Packs: circadian, breath, nutrition, tea (claim-tiered, ordinary wellness only)  
- [x] T0 ChatGPT project pack + household vault template docs  
- [x] Steward second-subject path  
- [x] Unit tests  

**Explicit non-goals in v0.1:** food-logger product, wearable ingest pipelines, DP commons, plant-medicine dosing, diagnosis agents, interconnecting mind/psych repos.

### Next 100 days (still the plan)

| Window | Outcome |
| --- | --- |
| Days 15–30 | Steward phone capture path; second/third family subjects real |
| Days 31–60 | Contraindication UX polish; more claims; real clinician appointment export test |
| Days 61–100 | Subject-zero protocol outcomes essay + optional commons RFC |

### Gating decision locked

**Vault unit = household** (not lone subject). Schema carries the extra dimension once.

---

## 9. Safety boundary (non-negotiable)

BIOS organizes ordinary wellness experiments and clinician conversation prep.  
It does **not** diagnose, prescribe, interpret labs, or provide controlled-substance / non-culinary plant-medicine guidance. Jurisdiction flags route those topics to humans and local law — never to automated protocols in v0.1.

---

## 10. How to run

```bash
cd health-intelligence-system
PYTHONPATH=bios/src python -m bios_substrate --help
PYTHONPATH=bios/src python -m unittest discover -s bios/tests -v
```
