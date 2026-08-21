import type { HouseholdState, LedgerEvent, ProtocolDef, Subject } from "./types";
import { PROTOCOLS } from "./packs";

const KEY = "bios.steward.household.v1";

function id(prefix: string) {
  return `${prefix}_${Math.random().toString(16).slice(2, 10)}${Date.now().toString(16).slice(-4)}`;
}

function now() {
  return new Date().toISOString();
}

export function defaultHousehold(): HouseholdState {
  const self: Subject = {
    subject_id: "sub_self",
    display_name: "You",
    role: "self",
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC",
  };
  const grandma: Subject = {
    subject_id: "sub_grandma",
    display_name: "Grandma",
    role: "grandparent",
    timezone: self.timezone,
  };
  return {
    version: 1,
    household_id: "hh_demo_family",
    display_name: "Demo household",
    subjects: [self, grandma],
    active_subject_id: self.subject_id,
    events: [
      {
        event_id: id("evt"),
        recorded_at: new Date(Date.now() - 3600_000).toISOString(),
        kind: "breath_session",
        note: "Box breathing — demo seed",
        tags: ["breath", "demo"],
        sensitivity_class: "personal",
        subject_id: self.subject_id,
        channel: "human",
      },
    ],
    active_runs: [],
  };
}

export function loadHousehold(): HouseholdState {
  if (typeof window === "undefined") return defaultHousehold();
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) {
      const d = defaultHousehold();
      localStorage.setItem(KEY, JSON.stringify(d));
      return d;
    }
    return JSON.parse(raw) as HouseholdState;
  } catch {
    return defaultHousehold();
  }
}

export function saveHousehold(state: HouseholdState) {
  if (typeof window === "undefined") return;
  localStorage.setItem(KEY, JSON.stringify(state));
}

export function resetHousehold(): HouseholdState {
  const d = defaultHousehold();
  saveHousehold(d);
  return d;
}

export function appendEvent(
  state: HouseholdState,
  partial: {
    kind: LedgerEvent["kind"];
    note: string;
    tags?: string[];
    sensitivity_class?: LedgerEvent["sensitivity_class"];
    channel?: LedgerEvent["channel"];
    subject_id?: string;
    protocol_id?: string;
    protocol_run_id?: string;
  },
): HouseholdState {
  const event: LedgerEvent = {
    event_id: id("evt"),
    recorded_at: now(),
    subject_id: partial.subject_id || state.active_subject_id,
    sensitivity_class: partial.sensitivity_class || "personal",
    channel: partial.channel || "human",
    kind: partial.kind,
    note: partial.note,
    tags: partial.tags || [],
    protocol_id: partial.protocol_id,
    protocol_run_id: partial.protocol_run_id,
  };
  return {
    ...state,
    events: [...state.events, event],
  };
}

export function startProtocol(state: HouseholdState, protocol: ProtocolDef): HouseholdState {
  if (state.active_runs.some((r) => r.protocol_id === protocol.id)) {
    return state;
  }
  const run_id = id("run");
  let next: HouseholdState = {
    ...state,
    active_runs: [
      ...state.active_runs,
      {
        run_id,
        protocol_id: protocol.id,
        title: protocol.title,
        pack: protocol.pack,
        started_at: now(),
      },
    ],
  };
  next = appendEvent(next, {
    kind: "protocol_start",
    note: `Started ${protocol.title}`,
    tags: [protocol.pack, "protocol"],
    protocol_id: protocol.id,
    protocol_run_id: run_id,
    channel: "agent",
  });
  return next;
}

export function eventsForSubject(state: HouseholdState, subjectId?: string) {
  const sid = subjectId || state.active_subject_id;
  return state.events
    .filter((e) => e.subject_id === sid)
    .slice()
    .sort((a, b) => (a.recorded_at < b.recorded_at ? 1 : -1));
}

export function activeSubject(state: HouseholdState) {
  return state.subjects.find((s) => s.subject_id === state.active_subject_id) || state.subjects[0];
}

export function buildHandoff(state: HouseholdState): string {
  const subject = activeSubject(state);
  const events = eventsForSubject(state).slice(0, 15);
  const runs = state.active_runs;
  const stack = events
    .filter((e) => ["breath_session", "tea", "meal", "meal_photo"].includes(e.kind))
    .slice(0, 8);

  const lines = [
    `# Clinician handoff — ${subject.display_name}`,
    "",
    `_Generated: ${now()} · BIOS Steward · household \`${state.household_id}\`_`,
    "",
    "> Patient-organized summary for clinical conversation. Not a diagnosis, not a prescription, not lab interpretation. Licensed clinician owns medical decisions.",
    "",
    "## Identity (minimum)",
    "",
    `- Subject: ${subject.display_name}`,
    `- Local id: \`${subject.subject_id}\``,
    `- Timezone: ${subject.timezone}`,
    `- Role in household: ${subject.role}`,
    "",
    "## Why we are here",
    "",
    "_Replace with appointment purpose in the patient's own words._",
    "",
    "## Ordinary-wellness stack (self-reported)",
    "",
  ];

  if (stack.length) {
    for (const e of stack) {
      lines.push(`- ${e.kind}: ${e.note}`);
    }
  } else {
    lines.push("- (none logged yet)");
  }

  lines.push("", "## Active n-of-1 protocols", "");
  if (runs.length) {
    for (const r of runs) {
      lines.push(`- ${r.title} — started ${r.started_at} — \`${r.run_id}\``);
    }
  } else {
    lines.push("- (none)");
  }

  lines.push("", "## Recent observations (facts only)", "");
  if (events.length) {
    for (const e of events) {
      lines.push(`- ${e.recorded_at} · \`${e.kind}\` · ${e.note}`);
    }
  } else {
    lines.push("- (none)");
  }

  lines.push(
    "",
    "## Three questions for the clinician",
    "",
    "1. _…_",
    "2. _…_",
    "3. _…_",
    "",
    "## Data request template",
    "",
    "- Problem list and visit notes (12 months)",
    "- Current medication and allergy list",
    "- Relevant labs/imaging reports",
    "- Written follow-up plan",
    "",
    "## Red flags",
    "",
    "Emergency symptoms → local emergency services. Do not wait on this document or any AI.",
    "",
    "---",
    "",
    `_Events shown: ${events.length}. Protocol catalog: ${PROTOCOLS.length}._`,
    "",
  );

  return lines.join("\n");
}
