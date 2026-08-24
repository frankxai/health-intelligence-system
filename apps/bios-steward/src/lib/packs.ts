import type { EvidenceFixture } from "./types";

/**
 * Synthetic catalog labels only. These are not protocols, interventions, or advice.
 * The governed Python runtime remains authoritative and currently blocks every fixture.
 */
export const EVIDENCE_FIXTURES: EvidenceFixture[] = [
  {
    id: "fixture-circadian",
    domain: "Circadian evidence",
    title: "Light and daily-rhythm review fixture",
    status: "draft_synthetic",
    purpose: "Demonstrate how an evidence question may be queued for independent review.",
    blockedActions: ["No duration", "No timing rule", "No protocol start"],
  },
  {
    id: "fixture-caffeine",
    domain: "Caffeine evidence",
    title: "Caffeine-timing review fixture",
    status: "draft_synthetic",
    purpose: "Demonstrate source, correction, conflict, and population review fields.",
    blockedActions: ["No cutoff", "No amount", "No taper guidance"],
  },
  {
    id: "fixture-breath",
    domain: "Breathing evidence",
    title: "Breathing-practice review fixture",
    status: "draft_synthetic",
    purpose: "Demonstrate structured contraindication and hard-block contracts.",
    blockedActions: ["No pattern", "No duration", "No claimed effect"],
  },
  {
    id: "fixture-nutrition",
    domain: "Nutrition evidence",
    title: "Meal-observation privacy fixture",
    status: "draft_synthetic",
    purpose: "Demonstrate exact consent scopes without collecting food images or notes.",
    blockedActions: ["No image upload", "No tracking", "No nutrition target"],
  },
  {
    id: "fixture-botanical",
    domain: "Culinary-botanical evidence",
    title: "Botanical rights and safety review fixture",
    status: "draft_synthetic",
    purpose: "Demonstrate provenance, rights, interaction, and scope review fields.",
    blockedActions: ["No preparation", "No amount", "No product recommendation"],
  },
];
