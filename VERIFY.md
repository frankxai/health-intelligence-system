# Verify a Release

Use this guide before trusting a downloaded package.

## Quick Check

From this repo:

```powershell
npm run verify:release
```

That checks the local ZIP in `dist/` against `release-manifest.json`.

## Verify a GitHub Release Download

```powershell
pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/verify-release.ps1 -Version 0.1.1 -Download
```

This downloads the release ZIP and manifest from GitHub, then checks:

- the release tag;
- ZIP file name;
- ZIP byte size;
- ZIP SHA-256 digest;
- every file listed in the manifest;
- safety-critical documents.

## Manual Check

Download both files from the same release:

- `health-intelligence-system-v0.1.1.zip`
- `release-manifest.json`

Then compare the ZIP SHA-256 in `release-manifest.json` with:

```powershell
Get-FileHash -Algorithm SHA256 .\health-intelligence-system-v0.1.1.zip
```

If the values differ, do not use the package.

## Trust Boundary

Verification proves package integrity. It does not prove clinical correctness. This release still requires the clinical/legal review gate before production clinical use.

**Built on SIP** - Health Intelligence System verification guide
