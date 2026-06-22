# Safety And Privacy Model

**Evidence checked:** 2026-06-22  
**Scope:** safety, privacy, source, and release controls for personal health operations with LLMs and agents.  
**Safety boundary:** This page is not medical, legal, security, privacy, or compliance advice. It defines product rules for this repo.

## Non-Negotiable Boundary

Health Intelligence System organizes records, routines, questions, source ledgers, and clinician-facing summaries.

It does not:

- diagnose;
- rule conditions in or out;
- interpret labs, imaging, pathology, biomarkers, genetics, or clinician notes;
- recommend treatment;
- recommend medication changes;
- recommend supplements, doses, fasting, or disease protocols;
- design injury rehabilitation;
- provide emergency triage;
- replace clinicians, emergency services, pharmacists, dietitians, therapists, or other licensed professionals.

## Safety Gates

| Gate | What it checks | Required result |
| --- | --- | --- |
| Clinical boundary gate | Diagnosis, treatment, medication, supplement, emergency, lab interpretation language | Block or rewrite as clinician questions |
| Source gate | External factual claims, guideline references, product claims | Source URL plus evidence-check date |
| Privacy gate | Identifiers, private records, portal exports, family history, hidden metadata mentions | Keep out of public repo |
| Model-mode gate | Whether cloud, local, regulated, or private infrastructure is being used | State the data rule before use |
| Research bridge gate | Whether research is being applied to the person | Convert into education, glossary, and clinician questions |
| Jurisdiction gate | Country-specific record/legal/process claims | Mark as orientation and source it |
| Release gate | Review status and package contents | Keep prerelease until review passes |

## Private Data Rules

Never commit:

- names, birth dates, contact details, identifiers;
- appointment notes tied to a real person;
- portal exports, PDFs, images, scans, screenshots;
- lab values, pathology, imaging, genomics, medication records;
- insurance IDs or payer correspondence;
- family history that identifies relatives;
- chat logs containing private health details.

Use public examples only when they are fictional and labeled as fictional.

## Recommended Private Vault Pattern

```text
HealthVault/
|-- 00-command-center/
|-- 10-records/
|-- 20-doctor-visits/
|-- 30-daily-loops/
|-- 40-evidence/
|-- 50-jurisdiction/
`-- 90-exports/
```

Raw records belong under the private vault, not in this public repo.

## AI Mode Decision Table

| User posture | Recommended mode | Reason |
| --- | --- | --- |
| Maximum privacy | Local-first private | Raw records stay local and encrypted |
| Convenience with some cloud acceptance | Hybrid | Use sanitized context with cloud AI |
| Dedicated health AI access | Compartmentalized health AI | Health files/chats are separated from ordinary chat |
| Care team or company | Regulated workspace | Governance, audit, compliance review needed |
| Technical private stack | Private infrastructure | Requires security and ops discipline |

## Safe Prompting Rules

Use prompts that ask for:

- timeline cleanup;
- missing-record checklists;
- top questions for clinician;
- source-backed education;
- glossary;
- concise summaries;
- privacy risk review.

Avoid prompts that ask:

- "What do I have?"
- "Which treatment should I choose?"
- "Is this lab result bad?"
- "Should I stop or start this medication?"
- "What supplement dose treats this?"
- "Is this emergency serious?"

## Output Label

Every clinician-facing output should include:

```text
Patient-prepared summary for clinical discussion. Not medical advice.
Prepared on: <YYYY-MM-DD>
Source of facts: patient notes and records listed below.
```

## Review Standard

A public artifact is ready only if:

- a clinician can tell it is preparation, not advice;
- a privacy-conscious user can tell what stays local;
- a health-tech operator can see standards awareness;
- a researcher can see that personal records and research are separate;
- a first-time user can tell what to do next without exposing private data.

**Built on SIP** - Health Intelligence System safety and privacy model
