param(
  [string]$Version = $(if ($env:npm_package_version) { $env:npm_package_version } else { "0.2.0" })
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$versionName = "health-intelligence-system-v$Version"
$packageDir = Join-Path $repoRoot "packages\$versionName"
$distDir = Join-Path $repoRoot "dist"
$zipPath = Join-Path $distDir "$versionName.zip"
$manifestPath = Join-Path $repoRoot "release-manifest.json"
$packageManifestPath = Join-Path $packageDir "release-manifest.json"

$allowList = @(
  "README.md",
  "QUICK-START.md",
  "VERIFY.md",
  "SAFETY.md",
  "PRIVACY.md",
  "VALIDATION.md",
  "REVIEW-GATE.md",
  "RELEASE.md",
  "RELEASE_NOTES_v0.1.0.md",
  "RELEASE_NOTES_v0.1.1.md",
  "RELEASE_NOTES_v0.2.0.md",
  "CHANGELOG.md",
  "CONTRIBUTING.md",
  "SKILL.md",
  "SOUL.md",
  "AGENTS.md",
  "STACK.md",
  "CANON.md",
  "MEMORY.md",
  "SUB-SYSTEMS.md",
  "package.json",
  "LICENSE",
  "scripts",
  "docs",
  "templates",
  "commands",
  "prompts",
  "plugins",
  ".agent-harness.json"
)

if (Test-Path $packageDir) {
  Remove-Item -LiteralPath $packageDir -Recurse -Force
}
if (Test-Path $zipPath) {
  Remove-Item -LiteralPath $zipPath -Force
}

New-Item -ItemType Directory -Path $packageDir -Force | Out-Null
New-Item -ItemType Directory -Path $distDir -Force | Out-Null

foreach ($item in $allowList) {
  $source = Join-Path $repoRoot $item
  if (-not (Test-Path $source)) {
    throw "Missing release file: $item"
  }
  $destination = Join-Path $packageDir $item
  if ((Get-Item $source).PSIsContainer) {
    Copy-Item -LiteralPath $source -Destination $destination -Recurse
  } else {
    $parent = Split-Path $destination -Parent
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
    Copy-Item -LiteralPath $source -Destination $destination
  }
}

$files = Get-ChildItem -LiteralPath $packageDir -File -Recurse |
  Sort-Object FullName |
  ForEach-Object {
    $relative = $_.FullName.Substring($packageDir.Length + 1).Replace("\", "/")
    [ordered]@{
      path = $relative
      bytes = $_.Length
      sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash.ToLowerInvariant()
    }
  }

$packageManifest = [ordered]@{
  name = "health-intelligence-system"
  version = $Version
  status = "preclinical-prerelease"
  evidence_checked = "2026-06-22"
  built_on = "SIP v1.1.1"
  clinical_legal_gate = "pending"
  files = $files
}

$packageManifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $packageManifestPath -Encoding utf8

Compress-Archive -Path (Join-Path $packageDir "*") -DestinationPath $zipPath -Force

$zip = Get-Item -LiteralPath $zipPath
$releaseManifest = [ordered]@{
  name = "health-intelligence-system"
  version = $Version
  release = "v$Version"
  status = "preclinical-prerelease"
  evidence_checked = "2026-06-22"
  built_on = "SIP v1.1.1"
  clinical_legal_gate = "pending"
  canonical_repo = "https://github.com/frankxai/health-intelligence-system"
  canonical_release = "https://github.com/frankxai/health-intelligence-system/releases/tag/v$Version"
  zip_asset = [ordered]@{
    name = "$versionName.zip"
    bytes = $zip.Length
    sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $zipPath).Hash.ToLowerInvariant()
  }
  files = $files
}

$releaseManifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $manifestPath -Encoding utf8

Write-Host "Packaged $zipPath"
Write-Host "Manifest $manifestPath"
