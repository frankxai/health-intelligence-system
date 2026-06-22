# Marketplace And Distribution

**Current channel:** GitHub Releases  
**Canonical release:** https://github.com/frankxai/health-intelligence-system/releases  
**Current package:** `health-intelligence-agent-pack-v0.2.1.zip`

## Channel Strategy

| Channel | Status | What goes there | Notes |
| --- | --- | --- | --- |
| GitHub Release | Live | Full repo ZIP, agent-pack ZIP, manifests, release notes | Canonical public download |
| Starlight Intelligence | PR-ready | Intelligence-system download and validation surface | Should point to the GitHub Release, not mirror assets |
| FrankX | PR-ready | Human-facing founder/operator download surface | Should route to the GitHub Release |
| Codex plugin directory | Package-ready | `plugins/health-intelligence-system/` | Publish after public plugin review rules are satisfied |
| ChatGPT / Claude project templates | Package-ready | `prompts/` | Distribute as copyable prompts, not as a medical chatbot |
| Future marketplace | Pending | Signed plugin bundle, checksum, support path | Requires marketplace-specific packaging rules |

## Publication Gates

Before any marketplace submission:

- No secrets, private health data, local paths, or private strategy in the bundle.
- Safety language blocks diagnosis, test interpretation, treatment selection, medication changes, supplement dosing, and emergency triage.
- The download has version, date, checksum, manifest, install path, first workflow, and support/upgrade path.
- The bundle can be useful with fictional data or a private vault; it must not require public personal data.

## Recommended Links

- Full repo release: `https://github.com/frankxai/health-intelligence-system/releases/tag/v0.2.1`
- Full package ZIP: `https://github.com/frankxai/health-intelligence-system/releases/download/v0.2.1/health-intelligence-system-v0.2.1.zip`
- Agent pack ZIP: `https://github.com/frankxai/health-intelligence-system/releases/download/v0.2.1/health-intelligence-agent-pack-v0.2.1.zip`
- Agent pack manifest: `https://github.com/frankxai/health-intelligence-system/releases/download/v0.2.1/agent-pack-manifest.json`

**Built on SIP** - Health Intelligence System marketplace map
