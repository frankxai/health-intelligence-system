# Release Process

**Status:** research-preview candidate verification only. Public upload is disabled. The legacy
agent pack is outside the admitted package boundary.

## Local Package

```powershell
npm run package:all
```

This generates only the minimal synthetic BIOS candidate:

- `packages/health-intelligence-system-v<package-version>/`
- `dist/health-intelligence-system-v<package-version>.zip`
- `release-manifest.json`

## Local Verification

```powershell
npm run verify:release
```

The verifier checks:

- Full release ZIP file name, size, and SHA-256 digest against `release-manifest.json`.
- Every manifest-listed file exists after extraction.
- Every manifest-listed file byte count and SHA-256 digest matches.
- Safety-critical documents exist in the package.

## GitHub Release

Do not tag or upload this candidate. `.github/workflows/release.yml` has read-only permissions and
performs verification only. Reopening public release requires every gate in
[`REVIEW-GATE.md`](REVIEW-GATE.md), a clean reviewed commit, and an explicit human release decision.

## Website Distribution

Future sites may link to an admitted GitHub release only after the release hold is removed:

- Starlight: protocol and validation adoption surface.
- FrankX: guided human-facing download surface.

Do not duplicate ZIP files in site repos unless there is a deliberate mirror policy.

**Built on SIP** - Health Intelligence System release process v0.1
