# Tooling paths

Documentation checked 2026-09-06. Recheck before integration or availability claims. Documented capability is not an implemented connector or entitlement.

| Preference | Path | Boundary |
|---|---|---|
| No new app/device | Selected notes/exports and one private destination | Manual is a complete starting mode |
| ChatGPT Work | Skill, selected-file analysis, research, reports, connected apps | Inspect tools; no automatic access to every chat or health record |
| Codex | Build/test adapters and interfaces; analyze authorized exports | Code execution is not an unattended health service |
| Notion / Drive | Reviewed summaries, decisions, groceries, selected exports | Cloud copies remain sensitive; no E2E encryption claim |
| Obsidian / local | Private Markdown plus CSV/JSON | User owns backup and device/encryption configuration |
| Health Connect | Future permissioned Android companion | Browser/MCP alone cannot read the device store |
| HealthKit | Future native companion or deliberate export | Native authorization; no direct website access promised |
| WHOOP / Strava | Registered app, OAuth, narrow scopes, tested adapter | OAuth documentation is not an active connection |
| Garmin | Evaluate Connect Developer Program access | Verify program and supported APIs before promising |
| Oura / other apps | Verify export/API and user's actual access | Do not invent scopes or unavailable tools |

For a future ChatGPT plugin, separate data from rendering. Return scoped review data or opaque IDs from private authenticated tools. A render tool resolves authorized IDs server-side; do not trust client-supplied tenant IDs or approval flags. Attach _meta.ui.resourceUri to that render tool. Annotations describe behavior; backend enforcement provides authority. This skill installs no remote server.

Sources:
- https://learn.chatgpt.com/docs/plugins
- https://developers.openai.com/plugins/concepts/mcp-server
- https://developers.openai.com/plugins/build/chatgpt-ui
- https://developers.openai.com/plugins/guides/security-privacy
- https://developer.android.com/health-and-fitness/health-connect/get-started
- https://developer.apple.com/documentation/healthkit/authorizing-access-to-health-data (rendering limited during this review; reverify specifics)
- https://developer.whoop.com/docs/developing/oauth/
- https://developers.strava.com/docs/authentication/
- https://developer.garmin.com/gc-developer-program/overview/

Account, region, plan and device matter. Never buy hardware/services, accept terms, submit a public plugin or transmit health data merely to fill a matrix. Build with synthetic data first. Name the actual missing credential or decision when blocked.
