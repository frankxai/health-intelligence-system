# Verify a Research-Preview Candidate

**Status:** local candidate verification only; public upload is disabled.

Use this guide to inspect a minimal synthetic BIOS archive built from one clean reviewed commit.
Verification proves file integrity and safety-contract shape only. It does not admit evidence,
medical functionality, an agent pack, real-data storage, or clinical use.

## Quick Check

From this repo:

```powershell
npm run verify:release
```

That checks the local ZIP in `dist/` against `release-manifest.json`.

## Public downloads

Do not treat existing v0.2.1 downloads as current verified artifacts. They predate the 2026-08-24
gates. The verifier retains a `-Download` inspection mode for maintainers, but no public artifact is
recommended or supported by this research-preview branch.

## Manual Check

For an explicitly approved future candidate, compare the ZIP and manifest from the same build:

- `health-intelligence-system-v<package-version>.zip`
- `release-manifest.json`

Then compare the ZIP SHA-256 in `release-manifest.json` with:

```powershell
Get-FileHash -Algorithm SHA256 .\health-intelligence-system-v<package-version>.zip
```

If the values differ, do not use the package.

## Trust Boundary

Verification proves package integrity, exact manifest coverage, draft fixture status, and required
safety files. It does not prove clinical correctness or authorize a supported health tool. Every
gate in [REVIEW-GATE.md](REVIEW-GATE.md), independent review, and an explicit human release decision
remain required before reopening even a synthetic prerelease. Production clinical use is outside
the current product claim.

**Built on SIP** - Health Intelligence System verification guide
