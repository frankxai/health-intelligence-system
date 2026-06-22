# Privacy

Health data is sensitive. This public repo is for reusable structure, not real cases.

## Never Commit

- names, birth dates, addresses, emails, phone numbers;
- medical record numbers or insurance identifiers;
- appointment notes tied to a real person;
- pathology, imaging, lab, genomic, medication, or treatment records;
- clinician names connected to a private case;
- photos, scans, PDFs, screenshots, portal exports;
- family history that identifies relatives.

## Private Workspace Pattern

Use a separate private folder outside public git history:

```text
private/
|-- records/
|-- cancer/
`-- exports/
```

The included `.gitignore` excludes `private/`, but do not rely on one safeguard. Before sharing or packaging, run the validation checklist.

For the v0.2 private health vault, prefer:

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

Private GitHub is not the default storage layer for raw health records. Use it only for templates, sanitized examples, or encrypted archives after a deliberate privacy decision.

## Sharing Rule

Public examples must use fictional data and must be labeled as fictional. Real care summaries should be shared only with the person, their caregivers if authorized, and qualified clinicians.

**Built on SIP** - Health Intelligence System privacy policy v0.1
