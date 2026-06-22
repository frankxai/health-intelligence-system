# Repo Consolidation Map

**Evidence checked:** 2026-06-22  
**Scope:** how Health Intelligence System should relate to adjacent FrankX/Starlight repositories and future packs.  
**Safety boundary:** This is architecture and product governance. It is not medical, legal, privacy, or compliance advice.

## Decision

Keep `health-intelligence-system` as the public core. Do not create a new repo for every idea yet. Add packs only when the core protocol has enough stable usage to justify separate ownership.

The public core should contain:

- safety, privacy, and clinical-boundary rules;
- local-first vault guidance;
- doctor-visit, record-index, jurisdiction, and clinician-handoff templates;
- external-system research audit;
- repo disposition guidance.

Separate packs should be created only when they have a clear audience, file contract, and maintenance burden.

## Evidence Levels

| Evidence level | Meaning |
| --- | --- |
| `local-read` | Repo is cloned locally and README or files were inspected |
| `github-read` | Public GitHub page or repo inventory was inspected |
| `inventory-only` | Known from `github_repos_frankxai.json` or ledger, but not fully inspected |
| `proposed` | Not created or not confirmed as a repo yet |

## Disposition Matrix

| Repo or pack | Evidence level | Proposed disposition | Rationale | Next action |
| --- | --- | --- | --- | --- |
| `health-intelligence-system` | `local-read` and `github-read` | `core` | This is the patient-operator public protocol for safety, privacy, templates, and clinician handoff | Keep as source of truth for public personal health ops |
| `personal-health-vault-template` | `proposed` | `pack later` | Useful as a private local folder starter, but can start as templates in HIS | Do not create repo until private setup workflow stabilizes |
| `health-jurisdiction-packs` | `proposed` | `pack later` | Country adapters need independent freshness reviews | Start inside HIS docs/templates; split only when NL/DE/ES/HR/US/China packs become substantial |
| `clinician-handoff-spec` | `proposed` | `pack later` | Export schema may become reusable across HIS and research systems | Start with HIS templates and command |
| `life-sciences-researcher-is` | `proposed` | `defer new repo` | Research workflows need separation, but private Agentic Life OS can host the first research-only package while public repo creation gates mature | Keep implementation inside `agentic-life-os/packages/life-sciences-researcher` for now |
| `life-sciences` | `github-read` | `bridge` | Hosts marketplace/Claude life-sciences launch material; likely better as connector/skill bridge than personal health repo | Reference in companion research systems; do not merge personal records |
| `research-intelligence-os` | `github-read` and `inventory-only` | `bridge` | General research workflow base; could host evidence grading and literature protocols | Use as research workflow substrate if cloned and matured |
| `research-intelligence-systems` | `github-read` and `inventory-only` | `watch` | Adjacent research namespace; not enough inspected detail to absorb | Audit before creating new research repos |
| `neuroscience-research-intelligence-system` | `github-read` and `inventory-only` | `specialized pack` | Domain-specific research lane; should not hold personal records | Bridge only through public evidence briefs and clinician questions |
| `psychology-research-intelligence-system` | `github-read` and `inventory-only` | `specialized pack` | Domain-specific research lane; mental-health safety needs extra care | Bridge only through education and clinician questions |
| `second-brain-os` | `local-read` and `github-read` | `absorb pattern` | Two-vault privacy model maps strongly to private health vault design | Reuse privacy architecture, not code, unless needed |
| `agentic-life-os` | `local-read` | `private product monorepo` | Best home for Agentic Health OS as a private runtime and Life Sciences Researcher IS as a research-only companion package | Consume HIS releases; keep public protocol and private runtime separate |
| `Starlight-Intelligence-System` | `local-read` | `reference substrate` | Provides SIP contract, agent discipline, and DeepMind Science Skills registry entry | Continue composing SIP; use science skills only in research companion |

## Core Plus Packs Architecture

```text
health-intelligence-system
  -> personal-health-vault-template pack
  -> health-jurisdiction-packs
  -> clinician-handoff-spec
  -> agentic-life-os private runtime
       -> Agentic Health OS
       -> Life Sciences Researcher IS
  -> future life-sciences-researcher-is public repo
       -> life-sciences
       -> research-intelligence-os
       -> neuroscience / psychology research packs
```

The arrow means "may bridge to", not "stores data in".

## Merge Rules

| If a new artifact is about... | Put it in... | Do not put it in... |
| --- | --- | --- |
| Public personal health workflow | `health-intelligence-system` | Research repos |
| Raw personal records | Private local vault outside public repos | Any public repo |
| Sanitized/fake examples | HIS or a future vault template pack | Real private vault |
| Disease literature review | Research companion or research OS | Personal HIS unless converted to questions |
| Country record-access instructions | HIS jurisdiction docs first; future jurisdiction pack later | General research OS |
| Obsidian vault mechanics | HIS if health-specific; `second-brain-os` if generic | Clinical docs |
| Model/tool benchmark | Research companion | Patient-facing workflow |

## Creation Gates For New Repos

Create a separate repo only when all are true:

- It has a distinct maintainer or operating lane.
- It has at least five files that would make the core repo noisier.
- It has a different safety boundary from HIS.
- It has a clear public/private data policy.
- It has its own validation checklist.
- The first release can be useful without private health data.

## Current Recommendation

Do not create `life-sciences-researcher-is` immediately. First, keep the implemented research-only package inside private Agentic Life OS, publish the public boundary and protocol through HIS, and inspect whether `life-sciences` plus `research-intelligence-os` can carry a future public research workflow. This prevents repo sprawl while keeping the research separation explicit.

## Source Ledger

| Source | URL or path | Date accessed | Used for |
| --- | --- | --- | --- |
| Local HIS worktree | local clone, private path omitted | 2026-06-22 | Public core status and current docs/templates |
| Local Second Brain OS worktree | local clone, private path omitted | 2026-06-22 | Two-vault privacy pattern |
| Local Agentic Life OS worktree | local clone, private path omitted | 2026-06-22 | Private product monorepo and first Health OS / Life Sciences Researcher split |
| FrankX GitHub inventory | local inventory export, private path omitted | 2026-06-22 | Repo existence and metadata |
| Starlight MCP registry | local registry export, private path omitted | 2026-06-22 | DeepMind Science Skills registry entry |
| frankxai/health-intelligence-system | https://github.com/frankxai/health-intelligence-system | 2026-06-22 | Public repo state |
| frankxai/life-sciences | https://github.com/frankxai/life-sciences | 2026-06-22 | Life-sciences bridge candidate |
| frankxai/research-intelligence-os | https://github.com/frankxai/research-intelligence-os | 2026-06-22 | Research OS candidate |
| frankxai/second-brain-os | https://github.com/frankxai/second-brain-os | 2026-06-22 | Privacy pattern reference |

**Built on SIP** - Health Intelligence System repo consolidation map
