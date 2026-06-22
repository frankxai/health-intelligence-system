# Companion Research Systems

**Evidence checked:** 2026-06-22  
**Scope:** how personal Health Intelligence System should relate to life-science, healthcare, neuroscience, and biomedical research intelligence systems. Not medical advice.

## Separation Rule

Personal health operations and life-science research should be separate systems.

Personal health operations ask:

- What happened to me?
- What records do I have?
- What should I ask my clinician?
- What routines am I tracking?
- What needs follow-up?

Life-science research intelligence asks:

- What does the literature say?
- What mechanisms are proposed?
- What trials exist?
- What evidence is high quality?
- What hypotheses or research questions are emerging?

These must not collapse into one system. The research system can inform questions, but it does not decide personal care.

## Proposed Companion Repo

Current private package name:

```text
Life Sciences Researcher IS
```

Purpose:

```text
Source-backed research intelligence for healthcare, life sciences, neuroscience, genomics, clinical evidence, disease landscapes, trials, and biomedical literature. No personal health records.
```

Current implementation home:

```text
frankxai/agentic-life-os/packages/life-sciences-researcher
```

Future standalone repo name, if creation gates are met:

```text
life-sciences-researcher-is
```

## Suggested File Contract

```text
life-sciences-researcher-is/
|-- README.md
|-- SAFETY.md
|-- PRIVACY.md
|-- STACK.md
|-- AGENTS.md
|-- SUB-SYSTEMS.md
|-- docs/
|   |-- literature-review-protocol.md
|   |-- evidence-grading.md
|   |-- preprint-policy.md
|   |-- trial-search-protocol.md
|   `-- disease-landscape-brief.md
|-- templates/
|   |-- evidence-dossier.md
|   |-- disease-research-brief.md
|   |-- trial-landscape.md
|   |-- mechanism-map.md
|   `-- source-ledger.md
`-- commands/
    |-- literature-review.md
    |-- disease-landscape.md
    |-- trial-map.md
    |-- mechanism-map.md
    `-- evidence-check.md
```

## Research Agent Roles

| Agent | Job | Boundary |
| --- | --- | --- |
| `biomedical-literature-scout` | Searches PubMed, preprints, clinical guidelines, and reputable sources | Flags preprints and weak evidence |
| `evidence-grader` | Separates guideline, RCT, observational, preclinical, review, and opinion evidence | Does not turn evidence into personal advice |
| `trial-landscape-mapper` | Summarizes trial search results and eligibility questions | Does not determine eligibility |
| `mechanism-cartographer` | Maps pathways, mechanisms, hypotheses, and uncertainty | Does not claim certainty |
| `research-claims-guardian` | Blocks overclaims, hype, and unsupported clinical translation | Routes personal implications to clinicians |

## Tooling To Watch

- Google DeepMind Science Skills for agentic scientific workflows.
- OpenAI GPT-Rosalind for life-sciences reasoning.
- Anthropic Claude for Life Sciences for research connectors and skills.
- ToolUniverse / biomedical agent skills for structured scientific workflows.
- MedRAG-style retrieval for medical evidence synthesis.
- AgentClinic-style evaluation to test clinical-agent claims in simulation.

## Bridge To Personal HIS

The bridge should be one-way and safety-gated:

```text
research system
  -> public evidence brief
  -> patient-friendly glossary
  -> clinician questions
  -> personal HIS
```

Do not send raw personal records into the research repo.

## Repo Creation Decision

Do not create the companion repo until the creation gates in [repo-consolidation-map.md](repo-consolidation-map.md) are met. For now, run the companion inside private Agentic Life OS as `packages/life-sciences-researcher`, then bridge to `life-sciences`, `research-intelligence-os`, and specialized neuroscience or psychology research packs after those repos are inspected.

## First Product Artifacts

1. `disease-research-brief.md` - source-backed overview of a condition.
2. `clinical-guideline-comparison.md` - compares public guideline sources by jurisdiction.
3. `trial-landscape.md` - maps trials and eligibility questions.
4. `mechanism-map.md` - separates established biology from hypotheses.
5. `patient-question-translation.md` - turns research findings into questions for clinicians.

## Source Ledger

- Google DeepMind Science Skills: https://github.com/google-deepmind/science-skills
- Google DeepMind Co-Scientist: https://deepmind.google/blog/co-scientist-a-multi-agent-ai-partner-to-accelerate-research/
- Anthropic Claude for Life Sciences: https://www.anthropic.com/news/claude-for-life-sciences
- OpenAI GPT-Rosalind: https://openai.com/index/introducing-gpt-rosalind/
- ToolUniverse skills: https://zitniklab.hms.harvard.edu/ToolUniverse/guide/skills_showcase.html
- MedRAG: https://github.com/teddy-xionggz/medrag
- AgentClinic: https://agentclinic.github.io/

**Built on SIP** - Health Intelligence System companion research systems
