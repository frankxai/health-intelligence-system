import { EVIDENCE_FIXTURES } from "@/lib/packs";

const WARNING =
  "Synthetic design preview only. Do not enter, paste, upload, or infer personal, household, wearable, clinical, genomic, image, or identifying data.";

export function StewardApp() {
  return (
    <div className="app-shell">
      <div className="safety-banner" role="alert" aria-live="polite">
        <strong>NO REAL HEALTH DATA · NO MEDICAL FUNCTIONALITY · NO EXPORT</strong>
        <br />
        {WARNING}
      </div>

      <header className="topbar">
        <div className="brand">
          <div className="brand-mark" aria-hidden />
          <div>
            <h1>BIOS Steward · synthetic preview</h1>
            <p>Read-only evidence-contract demonstration</p>
          </div>
        </div>
        <span className="tier" data-tier="uncertain">
          PRECLINICAL · NON-RUNNABLE
        </span>
      </header>

      <main>
        <section className="panel">
          <div className="panel-inner">
            <div className="kicker">
              <span className="kicker-dot" />
              Governed foundation preview
            </div>
            <h2 className="display">See the safety contract before any product loop exists.</h2>
            <p className="lede">
              This browser surface intentionally has no input, account, household identity, local
              persistence, protocol start, handoff generation, clipboard export, upload, or network
              submission path. The catalog below contains synthetic test labels only.
            </p>
            <div className="meta-row" aria-label="Disabled capabilities">
              <span className="meta-chip">Storage <strong>disabled</strong></span>
              <span className="meta-chip">Health input <strong>disabled</strong></span>
              <span className="meta-chip">Protocol execution <strong>disabled</strong></span>
              <span className="meta-chip">Export <strong>disabled</strong></span>
            </div>
          </div>
        </section>

        <div className="section-head">
          <div>
            <h2>Discovery-only evidence fixtures</h2>
            <p>Read-only test metadata · not user-facing advice</p>
          </div>
        </div>

        <section className="card-grid" aria-label="Synthetic evidence fixtures">
          {EVIDENCE_FIXTURES.map((fixture) => (
            <article key={fixture.id} className="protocol-card">
              <div className="pack">{fixture.domain}</div>
              <h3>{fixture.title}</h3>
              <p style={{ color: "var(--ink-soft)", fontSize: "0.92rem" }}>{fixture.purpose}</p>
              <div className="pill-row">
                <span className="tier">Status · draft synthetic</span>
              </div>
              <h4>Hard-disabled</h4>
              <ul style={{ color: "var(--ink-soft)", paddingLeft: 18 }}>
                {fixture.blockedActions.map((action) => (
                  <li key={action}>{action}</li>
                ))}
              </ul>
            </article>
          ))}
        </section>

        <section className="panel" style={{ marginTop: 24 }}>
          <div className="panel-inner">
            <h2>What must happen before a real product</h2>
            <ol style={{ color: "var(--ink-soft)", paddingLeft: 20 }}>
              <li>Independent evidence, correction, rights, funding, and conflict review.</li>
              <li>Clinician, privacy, security, accessibility, and jurisdiction review.</li>
              <li>Encrypted private storage and exact consent/egress enforcement.</li>
              <li>Adversarial tests proving a browser cannot bypass the governed runtime.</li>
            </ol>
          </div>
        </section>
      </main>

      <div className="safety-banner" role="note" style={{ marginTop: 24 }}>
        {WARNING} For urgent concerns, use local emergency services or an appropriate qualified
        professional; this preview does not evaluate symptoms.
      </div>
    </div>
  );
}
