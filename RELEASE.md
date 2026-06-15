# Release Process

## Local Package

```powershell
npm run package:release
```

This generates:

- `packages/health-intelligence-system-v0.1.0/`
- `dist/health-intelligence-system-v0.1.0.zip`
- `release-manifest.json`

## GitHub Release

Use tag `v0.1.0` and mark it as a prerelease until [REVIEW-GATE.md](REVIEW-GATE.md) is closed.

Suggested release title:

```text
Health Intelligence System v0.1.0 - preclinical excellence pack
```

Suggested assets:

- `dist/health-intelligence-system-v0.1.0.zip`
- `release-manifest.json`

## Website Distribution

Both sites should link to GitHub Releases:

- Starlight: protocol and validation adoption surface.
- FrankX: guided human-facing download surface.

Do not duplicate ZIP files in site repos unless there is a deliberate mirror policy.

**Built on SIP** - Health Intelligence System release process v0.1
