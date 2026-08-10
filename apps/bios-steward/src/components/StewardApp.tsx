"use client";

import { useEffect, useMemo, useState } from "react";
import { CircadianRing } from "@/components/CircadianRing";
import { PHASES, PROTOCOLS } from "@/lib/packs";
import {
  activeSubject,
  appendEvent,
  buildHandoff,
  eventsForSubject,
  loadHousehold,
  resetHousehold,
  saveHousehold,
  startProtocol,
} from "@/lib/store";
import type { CaptureMode, HouseholdState, ProtocolDef } from "@/lib/types";

const CAPTURES: { mode: CaptureMode; label: string; hint: string; placeholder: string }[] = [
  { mode: "breath_session", label: "Breath", hint: "5 min practice", placeholder: "Box breathing 5m · calm" },
  { mode: "meal_photo", label: "Meal", hint: "Photo + note", placeholder: "Lunch · protein yes · hunger 6" },
  { mode: "tea", label: "Tea", hint: "Culinary only", placeholder: "Mint tea · wind-down" },
  { mode: "note", label: "Note", hint: "Facts only", placeholder: "Slept 7h · sore knee noted" },
];

function formatTime(iso: string) {
  try {
    return new Intl.DateTimeFormat(undefined, {
      hour: "2-digit",
      minute: "2-digit",
      month: "short",
      day: "numeric",
    }).format(new Date(iso));
  } catch {
    return iso.slice(0, 16);
  }
}

function hourNowLabel() {
  return new Intl.DateTimeFormat(undefined, {
    hour: "numeric",
    minute: "2-digit",
  }).format(new Date());
}

export function StewardApp() {
  const [state, setState] = useState<HouseholdState | null>(null);
  const [mode, setMode] = useState<CaptureMode>("breath_session");
  const [note, setNote] = useState("");
  const [phase, setPhase] = useState<string | null>(null);
  const [toast, setToast] = useState<string | null>(null);
  const [tab, setTab] = useState<"operate" | "handoff" | "t0">("operate");
  const [clock, setClock] = useState(hourNowLabel());

  useEffect(() => {
    setState(loadHousehold());
    const t = setInterval(() => setClock(hourNowLabel()), 30_000);
    return () => clearInterval(t);
  }, []);

  useEffect(() => {
    if (!toast) return;
    const t = setTimeout(() => setToast(null), 2400);
    return () => clearTimeout(t);
  }, [toast]);

  const subject = state ? activeSubject(state) : null;
  const events = useMemo(() => (state ? eventsForSubject(state) : []), [state]);
  const handoff = useMemo(() => (state ? buildHandoff(state) : ""), [state]);

  function commit(next: HouseholdState, message: string) {
    saveHousehold(next);
    setState(next);
    setToast(message);
  }

  function onCapture() {
    if (!state) return;
    const text = note.trim() || CAPTURES.find((c) => c.mode === mode)?.placeholder || "logged";
    const tags = [mode.replace("_", "-")];
    if (phase) tags.push(phase);
    const next = appendEvent(state, {
      kind: mode,
      note: text,
      tags,
      channel: mode === "meal_photo" ? "phone" : "human",
    });
    setNote("");
    commit(next, "Saved to household ledger");
  }

  function onStart(p: ProtocolDef) {
    if (!state) return;
    const next = startProtocol(state, p);
    if (next === state) {
      setToast("Protocol already active");
      return;
    }
    commit(next, `Started · ${p.title}`);
  }

  function onPhaseSelect(phaseId: string, label: string) {
    setPhase(phaseId);
    const map: Record<string, CaptureMode> = {
      upon_waking: "note",
      midday: "meal_photo",
      as_needed: "breath_session",
      pre_sleep: "tea",
    };
    setMode(map[phaseId] || "note");
    setNote((n) => n || `${label} check-in`);
    setToast(`${label} armed in capture dock`);
  }

  async function copyHandoff() {
    if (!handoff) return;
    try {
      await navigator.clipboard.writeText(handoff);
      setToast("Handoff copied — review before sharing");
    } catch {
      setToast("Copy failed — select text manually");
    }
  }

  if (!state || !subject) {
    return (
      <div className="app-shell">
        <p className="empty">Loading household vault…</p>
      </div>
    );
  }

  const dayCells = PHASES.map((p) => {
    const related = events.find((e) => e.tags.includes(p.id) || e.note.toLowerCase().includes(p.label.split(" ")[0].toLowerCase()));
    return { ...p, related };
  });

  return (
    <div className="app-shell">
      {toast ? <div className="toast">{toast}</div> : null}

      <header className="topbar">
        <div className="brand">
          <div className="brand-mark" aria-hidden />
          <div>
            <h1>BIOS Steward</h1>
            <p>Household vault · ordinary wellness · clinician-ready</p>
          </div>
        </div>
        <div className="pill-row" role="tablist" aria-label="Primary views">
          {(
            [
              ["operate", "Operate"],
              ["handoff", "Handoff"],
              ["t0", "T0 pack"],
            ] as const
          ).map(([id, label]) => (
            <button
              key={id}
              type="button"
              className="pill"
              data-active={tab === id}
              onClick={() => setTab(id)}
            >
              {label}
            </button>
          ))}
        </div>
      </header>

      <div className="safety-banner" role="note">
        Not medical advice. Organize facts, run claim-tiered ordinary-wellness experiments, prepare questions.
        Emergencies → local emergency services. Culinary tea only — no plant-medicine dosing.
      </div>

      <div className="pill-row" style={{ marginBottom: 18 }} aria-label="Subjects">
        {state.subjects.map((s) => (
          <button
            key={s.subject_id}
            type="button"
            className="pill"
            data-active={state.active_subject_id === s.subject_id}
            onClick={() => commit({ ...state, active_subject_id: s.subject_id }, `Viewing ${s.display_name}`)}
          >
            {s.display_name}
            <span style={{ color: "var(--ink-mute)" }}> · {s.role}</span>
          </button>
        ))}
        <button
          type="button"
          className="pill"
          onClick={() => commit(resetHousehold(), "Demo household reset")}
        >
          Reset demo
        </button>
      </div>

      {tab === "operate" ? (
        <>
          <section className="hero-grid">
            <div className="panel">
              <div className="panel-inner">
                <div className="kicker">
                  <span className="kicker-dot" />
                  Firmware for the body
                </div>
                <h2 className="display">A living day for {subject.display_name}</h2>
                <p className="lede">
                  Capture is the product. The circadian ring is not decoration — each phase arms a real
                  protocol window. Ledger stays on this device (demo localStorage).
                </p>
                <div className="meta-row">
                  <span className="meta-chip">
                    Household <strong>{state.display_name}</strong>
                  </span>
                  <span className="meta-chip">
                    Events <strong>{events.length}</strong>
                  </span>
                  <span className="meta-chip">
                    Active protocols <strong>{state.active_runs.length}</strong>
                  </span>
                  <span className="meta-chip">
                    Zone <strong>{subject.timezone}</strong>
                  </span>
                </div>

                <div className="day-rail" aria-label="Phase status">
                  {dayCells.map((c) => (
                    <div key={c.id} className="day-cell">
                      <h4>{c.label}</h4>
                      <p>{c.related ? c.related.note.slice(0, 48) : c.hint}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="panel">
              <div className="panel-inner">
                <CircadianRing
                  activePhase={phase}
                  onSelect={onPhaseSelect}
                  hourLabel={clock}
                />
              </div>
            </div>
          </section>

          <div className="section-head">
            <div>
              <h2>Claim-tiered protocols</h2>
              <p>Ordinary wellness only · contraindications shown · start writes the ledger</p>
            </div>
          </div>

          <div className="card-grid">
            {PROTOCOLS.map((p) => {
              const active = state.active_runs.some((r) => r.protocol_id === p.id);
              return (
                <article key={p.id} className="protocol-card">
                  <div className="pack">{p.pack}</div>
                  <h3>{p.title}</h3>
                  <p style={{ color: "var(--ink-soft)", fontSize: "0.92rem" }}>{p.summary}</p>
                  <div className="pill-row">
                    <span className="tier" data-tier={p.evidence_tier}>
                      Evidence · {p.evidence_tier.replace("_", " ")}
                    </span>
                    <span className="tier">{p.duration_days} days</span>
                    <span className="tier">Anchor · {p.anchor.replace("_", " ")}</span>
                  </div>
                  <details>
                    <summary style={{ cursor: "pointer", color: "var(--ink-mute)", fontSize: "0.86rem" }}>
                      Steps & stop conditions
                    </summary>
                    <ol style={{ margin: "10px 0 0", paddingLeft: 18, color: "var(--ink-soft)", fontSize: "0.88rem" }}>
                      {p.steps.map((s) => (
                        <li key={s}>{s}</li>
                      ))}
                    </ol>
                    <p style={{ marginTop: 8, color: "var(--dawn)", fontSize: "0.8rem" }}>
                      Stop / caution: {p.contraindications.join(" · ")}
                    </p>
                  </details>
                  <div className="btn-row">
                    <button
                      type="button"
                      className="btn btn-primary"
                      disabled={active}
                      onClick={() => onStart(p)}
                    >
                      {active ? "Active" : "Start n-of-1"}
                    </button>
                    <button
                      type="button"
                      className="btn btn-ghost"
                      onClick={() => {
                        setPhase(p.anchor === "morning" ? "upon_waking" : p.anchor === "evening" ? "pre_sleep" : p.anchor);
                        setMode(
                          p.pack === "breath"
                            ? "breath_session"
                            : p.pack === "nutrition"
                              ? "meal_photo"
                              : p.pack === "tea"
                                ? "tea"
                                : "note",
                        );
                        setToast("Capture dock aligned to protocol");
                      }}
                    >
                      Align capture
                    </button>
                  </div>
                </article>
              );
            })}
          </div>

          <div className="split-2" style={{ marginTop: 22 }}>
            <div className="panel">
              <div className="panel-inner">
                <div className="section-head" style={{ marginTop: 0 }}>
                  <div>
                    <h2 style={{ fontSize: "1.25rem" }}>Ledger</h2>
                    <p>Append-only observations for {subject.display_name}</p>
                  </div>
                </div>
                <div className="ledger">
                  {events.length === 0 ? (
                    <p className="empty">No events yet — use the capture dock.</p>
                  ) : (
                    events.map((e) => (
                      <div key={e.event_id} className="ledger-item">
                        <time dateTime={e.recorded_at}>{formatTime(e.recorded_at)}</time>
                        <div>
                          <strong>{e.kind.replaceAll("_", " ")}</strong>
                          <span>{e.note}</span>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>

            <div className="panel">
              <div className="panel-inner">
                <div className="section-head" style={{ marginTop: 0 }}>
                  <div>
                    <h2 style={{ fontSize: "1.25rem" }}>Active runs</h2>
                    <p>Protocols currently on the household node</p>
                  </div>
                </div>
                {state.active_runs.length === 0 ? (
                  <p className="empty">Start a protocol card to populate this pane.</p>
                ) : (
                  <div className="ledger">
                    {state.active_runs.map((r) => (
                      <div key={r.run_id} className="ledger-item">
                        <time>{r.pack}</time>
                        <div>
                          <strong>{r.title}</strong>
                          <span>Started {formatTime(r.started_at)}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </>
      ) : null}

      {tab === "handoff" ? (
        <section className="panel">
          <div className="panel-inner">
            <div className="section-head" style={{ marginTop: 0 }}>
              <div>
                <h2>Clinician handoff</h2>
                <p>Deterministic one-pager from the ledger — human review required before share</p>
              </div>
              <button type="button" className="btn btn-dawn" onClick={copyHandoff}>
                Copy markdown
              </button>
            </div>
            <pre className="handoff">{handoff}</pre>
            <p className="notice">
              Bridges to the real care system. Does not replace clinicians. Strip identifiers if your
              egress policy requires it before any frontier model.
            </p>
          </div>
        </section>
      ) : null}

      {tab === "t0" ? (
        <section className="panel">
          <div className="panel-inner">
            <div className="kicker">
              <span className="kicker-dot" />
              Grandma tier · T0 Whisper
            </div>
            <h2 className="display" style={{ maxWidth: "18ch" }}>
              Their ChatGPT. Your vault.
            </h2>
            <p className="lede">
              Non-technical subjects keep using tools they already trust. You remain steward: copy
              redacted LOG_CANDIDATE bullets into this capture dock under their subject chip.
            </p>
            <div className="card-grid" style={{ marginTop: 18 }}>
              <article className="protocol-card">
                <h3>Project instructions</h3>
                <p style={{ color: "var(--ink-soft)", fontSize: "0.92rem" }}>
                  Paste the T0 pack from <code>bios/templates/t0-chatgpt-project-pack.md</code> into
                  their AI project. Hard rules: no diagnosis, no prescribing, emergency routing, culinary
                  tea only.
                </p>
              </article>
              <article className="protocol-card">
                <h3>Steward bridge</h3>
                <p style={{ color: "var(--ink-soft)", fontSize: "0.92rem" }}>
                  1. Switch subject to Grandma<br />
                  2. Capture meal / breath / note from their message<br />
                  3. Generate handoff before visits<br />
                  4. Dignity: they may read everything written about them
                </p>
                <div className="btn-row">
                  <button
                    type="button"
                    className="btn btn-primary"
                    onClick={() =>
                      commit(
                        { ...state, active_subject_id: "sub_grandma" },
                        "Switched to Grandma",
                      )
                    }
                  >
                    Switch to Grandma
                  </button>
                  <button type="button" className="btn btn-ghost" onClick={() => setTab("operate")}>
                    Back to operate
                  </button>
                </div>
              </article>
            </div>
          </div>
        </section>
      ) : null}

      <div className="capture-dock" role="region" aria-label="Capture dock">
        <div className="capture-grid">
          {CAPTURES.map((c) => (
            <button
              key={c.mode}
              type="button"
              className="capture-btn"
              data-active={mode === c.mode}
              onClick={() => setMode(c.mode)}
            >
              {c.label}
              <small>{c.hint}</small>
            </button>
          ))}
          <input
            className="capture-input"
            value={note}
            onChange={(e) => setNote(e.target.value)}
            placeholder={CAPTURES.find((c) => c.mode === mode)?.placeholder}
            aria-label="Observation note"
            onKeyDown={(e) => {
              if (e.key === "Enter") onCapture();
            }}
          />
          <button type="button" className="btn btn-primary" onClick={onCapture}>
            Log
          </button>
        </div>
      </div>
    </div>
  );
}
