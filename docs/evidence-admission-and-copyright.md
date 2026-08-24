# Evidence Admission, Discovery Sources, and Copyright

**Reviewed:** 2026-08-24
**Scope:** public knowledge curation for BIOS. Not medical or legal advice.

## Small, Curated, Claim-Level by Default

BIOS does not build a giant undifferentiated health RAG corpus. It keeps a small claim ledger whose entries declare:

- DOI, PMID, or an HTTPS authority/publisher URL;
- evidence tier and explicit certainty;
- population, applicability, and limitations;
- source license and permitted content use;
- retrieval and review dates;
- correction/retraction status;
- conflict status; and
- the non-prescription boundary.

Malformed, unknown-field, non-active, or retracted-source contracts fail closed in the reference runtime.

The strengthened claim contract is schema `0.1.1`. This explicit prerelease revision prevents older, underspecified `0.1.0` claim objects from being silently treated as fully reviewed evidence.

## Discovery Is Not Evidence

Popular books, podcasts, newsletters, creator videos, and interviews—including material by Tony Robbins, Peter Diamandis, Andrew Huberman, or any other public educator—are **idea sources only**. They can suggest a question or a paper to locate. Their claims cannot reach a user-facing protocol or advice surface until independently resolved to an appropriate primary study, systematic review, or current authority guideline and admitted through the claim contract.

The public example at [`bios/knowledge/idea-sources/life-force.json`](../bios/knowledge/idea-sources/life-force.json) stores bibliographic metadata for *Life Force* only. It was identified from a user-supplied photograph. No photographed page, excerpt, scan, OCR, or copyrighted full text is included.

## Content-Use Rule

- Bibliographic metadata and links may be recorded with provenance.
- Copyrighted full text is not copied into Git, embeddings, fixtures, releases, or model context merely because a user owns a book or supplied a photograph.
- Full text may enter a local/private research workflow only when the license, public-domain status, open-access terms, or explicit permission allows that exact use.
- Even permitted full text does not automatically make every statement reliable.
- Public notes paraphrase minimally necessary insights and cite the independently admitted evidence, not the influencer as authority.
- Machine-readable bibliographic `notes` are one line and at most 500 characters. This size gate is
  only a backstop; every candidate package still requires a manual copyrighted-content scan.

## Admission Flow

```text
book / podcast / video / newsletter
  -> idea-source metadata
  -> extract candidate question (not advice)
  -> find DOI / PMID / authority guideline
  -> check population, limitations, conflicts, corrections, license
  -> claim contract review
  -> active claim or rejected/withdrawn claim
  -> only then may an educational protocol cite it
```

Correction or retraction status marked `not_checked` is an explicit unresolved risk, not proof that no notice exists. A release-quality evidence review should perform and date the check before upgrading certainty.
