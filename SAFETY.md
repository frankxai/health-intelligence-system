# Safety

**Safety policy reviewed:** 2026-08-24<br>
**Evidence admission:** none; all shipped claims remain draft.<br>
**Release status:** non-medical synthetic prerelease; production and promotion hold.

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

This system cannot determine urgency. If a situation may be an emergency, contact local emergency
services now. For non-emergency urgent concerns, contact a qualified clinician or the locally
appropriate urgent-care service. During active cancer treatment, follow the care team's own urgent
contact instructions.

## Public Content Rules

Every future user-facing health artifact must include:

- claim-level review, correction, supersession, and freshness dates;
- source list;
- medical disclaimer;
- statement that personal care may differ;
- clinician handoff;
- no private case details.

## Clinical/Legal Gate

No current package or agent may be published, installed, or promoted as a supported health tool.
Public source review may use fictional data only. Reopening a synthetic prerelease requires every
applicable gate in [REVIEW-GATE.md](REVIEW-GATE.md), a clean verified candidate, independent review,
and an explicit human release decision.

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

## BIOS v0.1 synthetic-foundation gates

- Every shipped claim is `draft` with `user_facing_allowed: false`.
- Every shipped pack/protocol is `draft_synthetic`; protocol start is blocked with no override flag.
- Contraindications are structured severity/action contracts. High/critical cases require a verified
  external signed-clearance path or permanent block; because no verifier ships, they fail closed.
- `safety.not_diagnosis` and `safety.not_prescription` must be true.
- `safety.medical_functionality_disabled` must be true.
- Complementary-practice education may record subjective experience and cultural tradition, but must not present an unproven energy field, mechanism, or healing claim as established fact or treatment efficacy.
- Martial-arts content is movement education and journaling only; no live-combat direction, injury rehabilitation, or substitute for a qualified instructor or clinician.
- Jurisdiction flags are routing fields, not automated legal advice.
- Red-flag symptoms → emergency services; agents stop.
- The reference vault is an unencrypted `synthetic_plaintext_prototype`; ignored paths are not a
  privacy control. Never enter or commit real health records.
- The browser preview has no input, identity, persistence, start, handoff, upload, or export surface.

**Built on SIP** - Health Intelligence System safety gate v0.1
