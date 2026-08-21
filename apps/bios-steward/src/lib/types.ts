export type Sensitivity = "public" | "personal" | "clinical" | "genomic";

export type EventKind =
  | "note"
  | "breath_session"
  | "meal"
  | "meal_photo"
  | "tea"
  | "sleep"
  | "protocol_start"
  | "protocol_checkin";

export interface LedgerEvent {
  event_id: string;
  recorded_at: string;
  kind: EventKind;
  note: string;
  tags: string[];
  sensitivity_class: Sensitivity;
  subject_id: string;
  protocol_id?: string;
  protocol_run_id?: string;
  channel: "human" | "phone" | "agent";
}

export interface Subject {
  subject_id: string;
  display_name: string;
  role: string;
  timezone: string;
}

export interface ProtocolDef {
  id: string;
  short: string;
  title: string;
  pack: string;
  hypothesis: string;
  summary: string;
  steps: string[];
  evidence_tier: "expert_consensus" | "cohort" | "mechanistic" | "traditional";
  anchor: "upon_waking" | "morning" | "midday" | "evening" | "pre_sleep" | "with_meals" | "as_needed";
  duration_days: number;
  contraindications: string[];
}

export interface ActiveRun {
  run_id: string;
  protocol_id: string;
  title: string;
  pack: string;
  started_at: string;
}

export interface HouseholdState {
  household_id: string;
  display_name: string;
  subjects: Subject[];
  active_subject_id: string;
  events: LedgerEvent[];
  active_runs: ActiveRun[];
  version: 1;
}

export type CaptureMode = "breath_session" | "meal_photo" | "tea" | "note";
