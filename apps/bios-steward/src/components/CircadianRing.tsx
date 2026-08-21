"use client";

import { PHASES } from "@/lib/packs";

type PhaseId = (typeof PHASES)[number]["id"];

export function CircadianRing({
  activePhase,
  onSelect,
  hourLabel,
}: {
  activePhase?: string | null;
  onSelect: (phaseId: PhaseId, label: string) => void;
  hourLabel: string;
}) {
  const cx = 160;
  const cy = 160;
  const rOuter = 128;
  const rInner = 86;

  function wedge(hour: number, span = 1.6) {
    const start = ((hour - span / 2) / 24) * Math.PI * 2 - Math.PI / 2;
    const end = ((hour + span / 2) / 24) * Math.PI * 2 - Math.PI / 2;
    const x1 = cx + rOuter * Math.cos(start);
    const y1 = cy + rOuter * Math.sin(start);
    const x2 = cx + rOuter * Math.cos(end);
    const y2 = cy + rOuter * Math.sin(end);
    const x3 = cx + rInner * Math.cos(end);
    const y3 = cy + rInner * Math.sin(end);
    const x4 = cx + rInner * Math.cos(start);
    const y4 = cy + rInner * Math.sin(start);
    const large = end - start > Math.PI ? 1 : 0;
    return `M ${x1} ${y1} A ${rOuter} ${rOuter} 0 ${large} 1 ${x2} ${y2} L ${x3} ${y3} A ${rInner} ${rInner} 0 ${large} 0 ${x4} ${y4} Z`;
  }

  function labelPos(hour: number, radius = 148) {
    const a = (hour / 24) * Math.PI * 2 - Math.PI / 2;
    return { x: cx + radius * Math.cos(a), y: cy + radius * Math.sin(a) };
  }

  const nowAngle = (() => {
    const d = new Date();
    const h = d.getHours() + d.getMinutes() / 60;
    return (h / 24) * 360 - 90;
  })();

  return (
    <div className="ring-wrap" aria-label="Circadian day ring">
      <svg className="ring-svg" viewBox="0 0 320 320" role="img">
        <title>Circadian phase ring</title>
        <defs>
          <radialGradient id="ringGlow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="rgba(60,170,116,0.25)" />
            <stop offset="70%" stopColor="rgba(60,170,116,0.05)" />
            <stop offset="100%" stopColor="rgba(0,0,0,0)" />
          </radialGradient>
          <linearGradient id="track" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="rgba(238,243,239,0.08)" />
            <stop offset="100%" stopColor="rgba(238,243,239,0.03)" />
          </linearGradient>
        </defs>

        <circle cx={cx} cy={cy} r="150" fill="url(#ringGlow)" />
        <circle
          cx={cx}
          cy={cy}
          r={(rOuter + rInner) / 2}
          fill="none"
          stroke="url(#track)"
          strokeWidth={rOuter - rInner}
        />

        {PHASES.map((p) => {
          const selected = activePhase === p.id;
          const pos = labelPos(p.hour);
          return (
            <g key={p.id} className="ring-phase" opacity={selected ? 1 : 0.82}>
              <path
                d={wedge(p.hour)}
                fill={p.color}
                fillOpacity={selected ? 0.55 : 0.28}
                stroke={p.color}
                strokeOpacity={selected ? 0.95 : 0.45}
                strokeWidth={selected ? 2 : 1}
                onClick={() => onSelect(p.id, p.label)}
              >
                <title>
                  {p.label}: {p.hint}
                </title>
              </path>
              <text
                x={pos.x}
                y={pos.y}
                textAnchor="middle"
                dominantBaseline="middle"
                fill="#eef3ef"
                fontSize="10"
                fontFamily="var(--font-body)"
                style={{ pointerEvents: "none" }}
              >
                {p.label}
              </text>
            </g>
          );
        })}

        {/* now needle */}
        <g transform={`rotate(${nowAngle} ${cx} ${cy})`}>
          <line
            x1={cx}
            y1={cy}
            x2={cx + rOuter - 4}
            y2={cy}
            stroke="#e0b56a"
            strokeWidth="2"
            strokeLinecap="round"
          />
          <circle cx={cx + rOuter - 4} cy={cy} r="4" fill="#e0b56a" />
        </g>

        <circle cx={cx} cy={cy} r="62" fill="rgba(7,11,9,0.92)" stroke="rgba(238,243,239,0.1)" />
        <text className="ring-center-label" x={cx} y={cy - 6}>
          {hourLabel}
        </text>
        <text className="ring-center-sub" x={cx} y={cy + 16}>
          Living day · tap a phase
        </text>
      </svg>
    </div>
  );
}
