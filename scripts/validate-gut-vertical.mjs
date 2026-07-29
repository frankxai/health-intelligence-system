import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

const readJson = async (relativePath) =>
  JSON.parse(await readFile(path.join(root, relativePath), "utf8"));

const pack = await readJson("verticals/gut-intelligence-system/vertical-pack.json");
const task = await readJson("verticals/gut-intelligence-system/task-envelope.json");
const family = await readJson("fixtures/gut/fictional-family.json");
const science = await readJson("fixtures/gut/fictional-science-envelope.json");
const evals = await readJson("verticals/gut-intelligence-system/evals/safety-cases.json");

assert.equal(pack.name, "gut-intelligence-system");
assert.equal(pack.license, "MIT");
assert.ok(pack.required_gates.includes("allergy_status"));
assert.ok(pack.required_gates.includes("science_adapter"));
assert.ok(task.blocked_outputs.includes("raw microbiome interpretation"));
assert.ok(task.blocked_outputs.includes("supplement or medication advice"));
assert.equal(family.fictional, true);
assert.equal(family.consent.parent_confirmed, true);
assert.notEqual(family.safety.allergy_status, "unknown");
assert.match(science.adapter_version, /^\d+\.\d+\.\d+$/);
assert.ok(science.reviewed_at);
assert.ok(science.excluded_claims.includes("treats_condition"));

const ids = new Set(evals.cases.map((item) => item.id));
assert.equal(ids.size, evals.cases.length);
for (const requiredCase of [
  "fictional-happy-path",
  "missing-allergy-status",
  "raw-microbiome-request",
  "supplement-dose-request",
  "growth-concern",
  "unreviewed-science-adapter"
]) {
  assert.ok(ids.has(requiredCase), `Missing safety case: ${requiredCase}`);
}

const publicTextPaths = [
  "verticals/gut-intelligence-system/README.md",
  "verticals/gut-intelligence-system/open-core-boundary.md",
  "plugins/health-intelligence-system/skills/gut-family-journey/SKILL.md"
];

for (const relativePath of publicTextPaths) {
  const text = await readFile(path.join(root, relativePath), "utf8");
  assert.match(text, /not medical advice|does not diagnose|Never diagnose/i);
  assert.match(text, /raw microbiome|raw reports/i);
  assert.match(text, /qualified/i);
}

console.log("Gut Intelligence System vertical: validation passed.");
