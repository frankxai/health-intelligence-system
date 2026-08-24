# BIOS — non-medical synthetic foundation

**Version:** 0.1.0-prerelease  
**Status:** safety-contract testbed; no medical or wellness functionality is admitted
**Data boundary:** the reference vault is unencrypted and synthetic-only

BIOS currently ships machine-readable contracts and adversarial fixtures for a future sovereign
health-intelligence runtime. It does not ship a runnable intervention, personal recommendation,
encrypted health vault, or approved clinical handoff product.

## What is enforced now

- Draft 2020-12 schemas with format checking run before stricter semantic gates.
- JSON duplicate keys, unknown fields, malformed dates, future consent events, cross-subject records,
  and ambiguous consent revisions fail closed.
- Consent is exact across subject, recipient, processor, purpose, action, data class, target tier,
  event ID, and protocol-run ID.
- Revocation/supersession takes precedence; duplicate grant IDs are denied.
- Handoff compilation includes only explicitly scoped records and does not reveal denied classes or
  ledger counts. A local HMAC-SHA-256 receipt binds content, consent, processor, recipient, and policy.
- Evidence tiers are explicit: A authoritative systematic/GRADE guideline; B systematic, living, or
  umbrella review; C registered low-risk-of-bias RCT; D observational, diagnostic, implementation, or
  mechanistic evidence; E discovery only; Q quarantine. Tiers E and Q cannot support active claims.
- Claims cannot become `active` without evidence, rights, conflict, freshness, and correction gates.
- Books, podcasts, videos, newsletters, and creator media are discovery metadata only.
- Public agent identities are generic and registry-only. `vitalis` and `velora` are denied as public
  agent/product names by the registry contract.
- Every shipped claim is `draft`; every protocol and pack is `draft_synthetic`.
- `protocol start` has no override flag and refuses all shipped fixtures.

## Synthetic engineering check

```bash
# from repository root; install bios/requirements.txt in an isolated Python environment first
PYTHONPATH=bios/src python -m unittest discover -s bios/tests -v
PYTHONPATH=bios/src python -m bios_substrate init \
  --household synthetic-demo --subject synthetic --path ./_local/synthetic-demo
PYTHONPATH=bios/src python -m bios_substrate validate --vault ./_local/synthetic-demo
```

The generated directory declares `vault_mode: synthetic_plaintext_prototype` and repeats a stop
warning. Do not enter real names, household details, symptoms, routines, images, wearable exports,
clinical records, genomic data, or identifiers. `_local/` being ignored by Git is not encryption.

## Current surfaces

| Surface | Path | Current role |
| --- | --- | --- |
| Schemas | [`schemas/`](schemas/) | Published structural contracts |
| Semantic validators | [`src/bios_substrate/validate.py`](src/bios_substrate/validate.py) | Fail-closed safety and evidence admission |
| Synthetic packs | [`packs/`](packs/) | Non-runnable adversarial fixtures |
| Registry | [`registry/public-domain-agents.json`](registry/public-domain-agents.json) | Generic, education-only, registry-only roles |
| Idea-source ledger | [`knowledge/idea-sources/`](knowledge/idea-sources/) | Bibliographic metadata and locators only |
| Consent example | [`templates/clinician-handoff-consent.example.json`](templates/clinician-handoff-consent.example.json) | Synthetic exact-scope shape only |
| Browser preview | [`../apps/bios-steward/`](../apps/bios-steward/) | Read-only synthetic UI; excluded from release |

## Holds before real use

1. Independent evidence review at the outcome level, including harms, directness, population,
   intervention/comparator, timeframe, funding/conflicts, correction/supersession, and rights.
2. Qualified clinical, privacy, security, legal, accessibility, and jurisdiction review.
3. Encrypted private storage with key recovery, deletion, backup, audit, and incident response.
4. A verified external signed-clearance trust model; the reference runtime intentionally ships no
   clearance verifier and therefore blocks clearance-required cases.
5. Browser-to-governed-runtime integration with adversarial bypass testing.

Not medical advice. Do not use BIOS to diagnose, interpret records, prescribe, recommend an
intervention, change care, or decide urgency.
