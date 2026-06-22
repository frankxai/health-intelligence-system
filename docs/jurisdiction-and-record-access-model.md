# Jurisdiction And Record Access Model

**Evidence checked:** 2026-06-22  
**Scope:** how Health Intelligence System adapts to local health systems. This is orientation, not legal advice.

## Core Idea

The core Health Intelligence System should be global and localizable. It should not pretend that record access, insurance, referrals, or digital portals work the same everywhere.

Each jurisdiction adapter should answer:

- Where does a person access records?
- What can they download?
- How do they request missing records?
- What rights do they have to access, correct, restrict, or share data?
- How do ePrescriptions and patient summaries work?
- How do insurance, referrals, and care pathways affect the practical workflow?
- What language should be used in clinician-facing exports?

## Global Baseline

Use these as common foundations:

- WHO digital health strategy for broad digital-health governance direction.
- HL7 FHIR for interoperable health-data exchange.
- International Patient Access for minimal patient-access expectations.
- AHRQ Question Builder as a practical appointment-prep model.
- Local patient-rights and health-data law for actual access.

## European Union

The European Health Data Space strengthens patient rights around health-data access, downloading copies, access logs, restrictions, opt-outs where enabled by country, rectification, and cross-border services such as ePrescription and Patient Summaries.

HIS adapter should include:

- local portal/app;
- MyHealth@EU availability;
- Patient Summary availability;
- ePrescription/eDispensation availability;
- local language export labels;
- emergency and urgent-care routing.

## Netherlands

Relevant pattern:

- patients can view medical records through a PGO or directly through doctor/healthcare institution;
- Dutch government guidance says providers must grant access requests within one month;
- patients can ask who accessed records.

HIS adapter should include:

- PGO inventory;
- GP/hospital portal list;
- request letter in Dutch and English;
- access-log question;
- insurer notes;
- cross-border travel summary.

## Germany

Relevant pattern:

- Germany uses the electronic patient record, ePA;
- access and implementation details can vary by insurer and statutory/private insurance context;
- users should check their own insurer app and current ePA settings.

HIS adapter should include:

- insurer app name;
- ePA access status;
- opt-out/access-control notes where applicable;
- medication plan and ePrescription notes;
- Hausarzt/specialist/referral workflow;
- German/English clinician summary.

## Spain

Relevant pattern:

- digital health systems are often regional;
- EU patient notices describe cross-border Patient Summary services;
- records, appointments, prescriptions, and portals can differ by autonomous community.

HIS adapter should include:

- autonomous community portal;
- tarjeta sanitaria / public-private care distinction;
- Spanish/English summary;
- specialist referral workflow;
- cross-border Patient Summary notes.

## Croatia

Relevant pattern:

- Portal zdravlja gives Croatian citizens access to part of their healthcare information from CEZIH;
- Croatian government guidance treats health data as a special category and says the chosen physician is required to make personal health data available to the patient;
- cross-border EU patient notices apply for participating services.

HIS adapter should include:

- e-Građani / Portal zdravlja access;
- CEZIH notes;
- selected physician contact;
- Croatian/English summary;
- EU cross-border Patient Summary and ePrescription notes.

## United States

Relevant pattern:

- HIPAA gives patients access rights to medical records;
- ONC information-blocking rules support access, exchange, and use of electronic health information;
- portals and third-party apps often use FHIR/SMART patterns.

HIS adapter should include:

- portal inventory;
- HIPAA records-request template;
- correction-request template;
- insurance/payer portal;
- referral/prior-authorization tracker;
- medication list and pharmacy notes.

## China

Relevant pattern:

- EHR access and apps can be regional, hospital-specific, and platform-specific;
- published research notes national policy encouragement for hospitals and medical facilities to release EHR data to citizen apps, but implementation varies.

HIS adapter should include:

- city/province/hospital portal;
- app or mini-program inventory;
- local language export;
- hospital record request process;
- local privacy and data-transfer cautions.

## Adapter Template

Each country pack should include:

```text
jurisdiction/
|-- README.md
|-- record-access.md
|-- portal-inventory.md
|-- insurance-care-access.md
|-- doctor-visit-language.md
|-- emergency-routing.md
|-- privacy-and-sharing.md
`-- source-ledger.md
```

## Source Ledger

- WHO digital health: https://www.who.int/health-topics/digital-health
- HL7 International Patient Access: https://build.fhir.org/ig/HL7/fhir-ipa/
- EU health-data rights: https://health.ec.europa.eu/ehealth-digital-health-and-care/my-rights-over-my-health-data_en
- EU electronic cross-border health services: https://health.ec.europa.eu/ehealth-digital-health-and-care/digital-health-and-care/electronic-cross-border-health-services_en
- Netherlands medical-record access: https://www.government.nl/themes/family-health-and-care/patients-rights-and-privacy/accessing-updating-or-deleting-medical-records
- Spain Patient Information Notice: https://health.ec.europa.eu/ehealth-digital-health-and-care/digital-health-and-care/electronic-cross-border-health-services/patient-information-notices-spain_en
- Croatia Health Portal: https://gov.hr/en/portal-zdravlja-health-portal-is-mobile-friendly/2340
- Croatia personal health data: https://gov.hr/en/personal-data-concerning-health/616
- HHS HIPAA right of access: https://www.hhs.gov/hipaa/for-individuals/right-to-access/index.html
- ONC information blocking: https://healthit.gov/information-blocking/

**Built on SIP** - Health Intelligence System jurisdiction model
