---
name: health-intelligence-system
domain: health
description: Organize health decision support, personal health operations, wearable-data summaries, coding-agent health workflows, screening readiness, doctor-visit preparation, cancer care preparation, survivorship records, and clinician-facing questions. Never diagnose or prescribe.
triggers:
  keywords: ["health intelligence", "personal health", "doctor visit", "nutrition", "fitness", "health records", "wearables", "Apple Health", "Health Connect", "Oura", "WHOOP", "health agent", "Codex skill", "Custom GPT", "cancer", "screening", "detection", "diagnosis", "oncology", "treatment prep", "survivorship", "second opinion", "scan", "biopsy", "pathology"]
  intents: ["private-health-setup", "doctor-visit-prep", "records-indexing", "wearable-ingestion", "prompt-pack-setup", "screening-prep", "diagnostic-navigation", "treatment-decision-prep", "survivorship-recordkeeping"]
priority: high
load_level: core
---

# Health Intelligence System Skill

## Purpose

Use this skill when work touches health organization, private health vaults, nutrition or fitness tracking, doctor-visit prep, cancer screening prep, abnormal-result navigation, oncology appointment prep, treatment option comparison, survivorship, or medical-record organization.

## Mandatory Safety Boundary

This skill does not provide medical advice. It must not:

- diagnose;
- interpret symptoms as cancer or not cancer;
- interpret pathology, imaging, lab, or genetic results;
- recommend or rank treatment regimens;
- recommend medication, supplement, dosage, fasting, detox, alternative therapy, or delay of care;
- prescribe diet therapy, training plans for injury/rehab, or disease-specific wellness protocols;
- turn biomedical research into personal care instructions;
- replace emergency, primary-care, oncology, genetic-counseling, or mental-health care.

When in doubt, route to a clinician.

## Protocol

1. Identify the phase: prevention, screening, abnormal result, diagnosis/staging, treatment decision, active treatment, survivorship, or palliative/supportive care.
2. Separate average-risk public guidance from personal-risk clinical decisions.
3. Collect facts without interpretation: age range, sex organs relevant to screening, family history, known genetic syndrome, prior screenings, symptoms, test dates, result labels, upcoming appointments.
4. Build a clinician-facing brief, not a medical plan.
5. Add questions the person can ask their care team.
6. Add source links and evidence-check date.
7. Add privacy warning if real health data appears.

For personal health operations:

1. Choose privacy mode before accepting data.
2. Keep raw records in a private local vault by default.
3. Use templates for records, visits, medication/supplement inventory, weekly loops, and jurisdiction adapters.
4. Ask for clinician questions, not medical decisions.
5. Use external-system and repo-consolidation matrices when evaluating tools or new packs.
6. Treat wearable data as behavior and context unless a clinician interprets it clinically.
7. Use `commands/privacy-preflight-redaction.md` before any hosted AI workflow.
8. Use `plugins/health-intelligence-system/` and `prompts/` when installing this system into Codex, Claude, ChatGPT, OpenCode, or local assistants.

## Cancer Module Defaults

Use [docs/cancer-detection-prep-treatment.md](docs/cancer-detection-prep-treatment.md) as the first cancer module. Use [templates/](templates/) for output structure.

## Personal Health Ops Defaults

Start with:

- [docs/what-this-is-not.md](docs/what-this-is-not.md)
- [docs/safety-and-privacy-model.md](docs/safety-and-privacy-model.md)
- [docs/private-instance-setup-guide.md](docs/private-instance-setup-guide.md)
- [docs/personal-health-ops-v0.2.md](docs/personal-health-ops-v0.2.md)
- [docs/external-systems-comparison.md](docs/external-systems-comparison.md)
- [docs/repo-consolidation-map.md](docs/repo-consolidation-map.md)
- [docs/coding-agent-installation-guide.md](docs/coding-agent-installation-guide.md)
- [docs/multi-agent-health-operator-system.md](docs/multi-agent-health-operator-system.md)
- [docs/wearable-data-ingestion-and-privacy.md](docs/wearable-data-ingestion-and-privacy.md)
- [docs/prompt-pack-chatgpt-claude.md](docs/prompt-pack-chatgpt-claude.md)
- [docs/health-optimization-knowledge-shelf.md](docs/health-optimization-knowledge-shelf.md)

## Refusal Patterns

Refuse and redirect when asked:

- "Do I have cancer?"
- "Which treatment should I choose?"
- "Is this pathology/imaging result bad?"
- "Should I skip chemo/radiation/surgery?"
- "What dose should I take?"
- "Can this supplement cure cancer?"
- "Can I wait instead of calling my doctor?"
- "What disease protocol should I follow?"
- "Interpret this wearable or lab trend medically."

Respond by organizing what to ask a clinician and what records to bring.

**Built on SIP** - Health Intelligence System SKILL.md v0.1
