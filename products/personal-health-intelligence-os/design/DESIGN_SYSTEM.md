# Personal Health Intelligence OS design system

Version 0.1.0. The interface makes observations, evidence and ownership visible. No composite wellness score, implied diagnosis, decorative risk color, or ungrounded recommendation.

## System

Use `tokens.json` as the visual source. Warm paper canvas, white working surfaces, forest ink and clay accents. Georgia display typography is reserved for large page titles; system sans handles controls and records. Body text starts at 16 px. Every primary control has a 44 px touch target. Focus is visible with an offset outline. Text never relies on color alone.

## Components

| Component | Purpose | Required context |
| --- | --- | --- |
| Daily cockpit | One place to enter a concise check-in | Edition, profile, date and data origin |
| Metric card | Describe one measured quantity | Unit, period and observed count |
| Trend chart | Show change over ordered dates | Named axis, unit, readable labels, missingness and table alternative |
| Library record | Reuse a food or product definition | Quantity basis, source, verification and stable identifier |
| Exposure total | Add identical ingredients and units | Logged intake, label amount and completeness; no dose recommendation |
| Weekly review | Surface one bounded decision | Coverage, comparison period, confounders and uncertainty |
| Record receipt | Make a write inspectable | ID, source, changed values, time and actor |

## Platform adaptation

Notion: use full-width home, restrained callouts, two columns only on desktop, native inline database views, visible source/verification properties, concise mobile views and a single daily entry surface. Do not recreate a dashboard as a long prose document. Database filters are navigation, not permissions. Native workspace typography, mobile stacking and database controls take precedence over exact token reproduction.

Google Sheets: frozen data headers, concise column names with units, editable input fill, ink headers, and formula-driven dashboard summaries. Keep synthetic demo and blank customer data clearly separated. Use native charts with source-bound ranges, visible units and explicit missing values. No invented clinical thresholds.

Offline demonstration: `web/index.html` demonstrates the cockpit with fictional values in memory only. It is a demo and partner training aid, not a hosted health application or workspace synchronizer. Its controls recompute from the embedded synthetic data and can export that working demo. `web/product.html` is draft product-page copy, not a checkout.

## Accessibility and acceptance

Semantic landmarks and headings, keyboard reachable controls, labels for every input, visible error/status messages, programmatic active navigation, reduced-motion support and no network dependency. Charts have textual summaries and a data table. On 390 px width, no page-wide horizontal scrolling; wide record tables scroll inside labelled containers. Keep standard browser zoom and do not suppress selection.

## Preview truth

Every demo screen says synthetic. Marketing cannot imply wearable ingestion, background synchronization, automatic assistant writes, medical interpretation or validated health outcomes. The Complete Edition is a Stage 2 design until its connectors, conflict handling and installation are independently verified. Pricing is an unvalidated launch hypothesis.
