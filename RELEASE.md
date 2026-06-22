# Release Process

## Local Package

```powershell
npm run package:all
```

This generates:

- `packages/health-intelligence-system-v0.2.1/`
- `dist/health-intelligence-system-v0.2.1.zip`
- `release-manifest.json`
- `packages/health-intelligence-agent-pack-v0.2.1/`
- `dist/health-intelligence-agent-pack-v0.2.1.zip`
- `agent-pack-manifest.json`

Replace `0.2.1` with the current `package.json` version.

## Local Verification

```powershell
npm run verify:release
npm run verify:agent-pack
```

The verifier checks:

- Full release ZIP file name, size, and SHA-256 digest against `release-manifest.json`.
- Agent-pack ZIP file name, size, and SHA-256 digest against `agent-pack-manifest.json`.
- Every manifest-listed file exists after extraction.
- Every manifest-listed file byte count and SHA-256 digest matches.
- Safety-critical documents exist in the package.

## GitHub Release

Use tag `v0.2.1` and mark it as a prerelease until [REVIEW-GATE.md](REVIEW-GATE.md) is closed.

Suggested release title:

```text
Health Intelligence System v0.2.1 - visual agent-pack release
```

Suggested assets:

- `dist/health-intelligence-system-v0.2.1.zip`
- `release-manifest.json`
- `dist/health-intelligence-agent-pack-v0.2.1.zip`
- `agent-pack-manifest.json`

## Website Distribution

Both sites should link to GitHub Releases:

- Starlight: protocol and validation adoption surface.
- FrankX: guided human-facing download surface.

Do not duplicate ZIP files in site repos unless there is a deliberate mirror policy.

**Built on SIP** - Health Intelligence System release process v0.1
