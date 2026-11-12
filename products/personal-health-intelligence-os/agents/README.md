# Portable health agent instructions

Version 0.1.0. These are instruction files to use with an assistant in a customer-controlled account. They do not install a runtime, establish a provider connection, grant permissions, or start a scheduled agent.

Load `00-operation-contract.md` plus the relevant role file. Provide the edition, owner workspace, schema version and explicitly authorized data scope. Prefer one active role per task. The same instruction does not establish identical capabilities across ChatGPT, Claude, Gemini or another assistant.

| Role | File | Primary output |
| --- | --- | --- |
| Health Data Steward | `health-data-steward.md` | Validation report, dedupe proposal and change receipt |
| Supplement Intelligence Agent | `supplement-intelligence.md` | Label reconciliation and arithmetic exposure report |
| Nutrition Intelligence Agent | `nutrition-intelligence.md` | Sourced food/recipe records and descriptive patterns |
| Daily Health Companion | `daily-health-companion.md` | Concise check-in with unknowns preserved |
| Experiment Analyst | `experiment-analyst.md` | Predeclared analysis with missingness and confounders |
| Evidence Research Agent | `evidence-research.md` | Dated source summary with population and limitations |
| Weekly Health Strategist | `weekly-health-strategist.md` | Bounded review and one capture or wellness action |

Use manual copy/paste of owner-selected records when a connector is absent. An assistant must not claim to read or save a record it cannot access. Credentials belong in the provider's authentication flow or the customer's runtime, never in a prompt or template cell.

Output format for all roles: **scope read → source facts → uncertainty → proposed action/output → applied changes and receipt**. Omit sections that do not apply; never invent an apply receipt.
