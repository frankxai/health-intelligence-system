# Safety

**Evidence checked:** 2026-06-22<br>
**Release status:** preclinical public prerelease.

## Hard Boundary

This system does not provide medical advice. It may organize questions, records, timelines, and clinician-facing summaries. It must not:

- diagnose cancer or rule it out;
- interpret symptoms, labs, pathology, imaging, genetic results, or biomarkers;
- recommend a cancer treatment, regimen, medication, supplement, dose, or delay;
- advise stopping, changing, or refusing clinician-directed care;
- promise prevention, cure, survival, or recurrence outcomes.

For personal health operations, it must also not:

- interpret labs, imaging, pathology, genetic results, wearable signals, or clinician notes;
- prescribe diet therapy, training, rehabilitation, fasting, supplements, or medication changes;
- decide whether symptoms are urgent;
- turn biomedical research into personal care instructions.

## Urgent Care Routing

For emergency symptoms, call emergency services or local urgent care. During active cancer treatment, follow the care team's urgent-contact instructions. Promptly contact the oncology team for severe or rapidly worsening side effects, including fever during chemotherapy, uncontrolled pain, breathing problems, chest pain, confusion, severe dehydration, uncontrolled vomiting, heavy bleeding, or any severe symptom the care team flagged.

## Public Content Rules

Every public health artifact must include:

- evidence-check date;
- source list;
- medical disclaimer;
- statement that personal care may differ;
- clinician handoff;
- no private case details.

## Clinical/Legal Gate

`v0.1.1` may be published as a prerelease for transparency and testing. It must not be promoted as production-ready until a qualified clinical/legal review is recorded in [REVIEW-GATE.md](REVIEW-GATE.md).

## v0.2 Safety Gates

Before publishing any personal health operations artifact, run:

- clinical boundary gate;
- source gate;
- privacy gate;
- model-mode gate;
- research bridge gate;
- jurisdiction gate;
- release gate.

See [docs/safety-and-privacy-model.md](docs/safety-and-privacy-model.md).

## BIOS v0.1 gates

- Every pack protocol cites `claim_ids` with evidence tier + sources.
- Contraindication gate runs before `bios protocol start`.
- `safety.not_diagnosis` and `safety.not_prescription` must be true.
- Ordinary wellness / habit tracking only in public packs; no controlled-substance or non-culinary plant-medicine protocols.
- Jurisdiction flags are routing fields, not automated legal advice.
- Red-flag symptoms → emergency services; agents stop.
- Household dignity clause: subjects may read everything written about them.
- Never commit real health records to this public repository (`_local/` is gitignored).

**Built on SIP** - Health Intelligence System safety gate v0.1
