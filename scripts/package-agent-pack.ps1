param(
  [string]$Version = $(if ($env:npm_package_version) { $env:npm_package_version } else { "0.2.1" })
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$packName = "health-intelligence-agent-pack-v$Version"
$packDir = Join-Path $repoRoot "packages\$packName"
$distDir = Join-Path $repoRoot "dist"
$zipPath = Join-Path $distDir "$packName.zip"
$manifestPath = Join-Path $repoRoot "agent-pack-manifest.json"
$packManifestPath = Join-Path $packDir "agent-pack-manifest.json"

$allowList = @(
  "AGENT_PACK.md",
  "MARKETPLACE.md",
  "README.md",
  "QUICK-START.md",
  "SAFETY.md",
  "PRIVACY.md",
  "VALIDATION.md",
  "LICENSE",
  "plugins",
  "prompts",
  "commands",
  "templates"
)

if (Test-Path $packDir) {
  Remove-Item -LiteralPath $packDir -Recurse -Force
}
if (Test-Path $zipPath) {
  Remove-Item -LiteralPath $zipPath -Force
}

New-Item -ItemType Directory -Path $packDir -Force | Out-Null
New-Item -ItemType Directory -Path $distDir -Force | Out-Null

foreach ($item in $allowList) {
  $source = Join-Path $repoRoot $item
  if (-not (Test-Path $source)) {
    throw "Missing agent-pack file: $item"
  }

  $destination = Join-Path $packDir $item
  if ((Get-Item $source).PSIsContainer) {
    Copy-Item -LiteralPath $source -Destination $destination -Recurse
  } else {
    $parent = Split-Path $destination -Parent
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
    Copy-Item -LiteralPath $source -Destination $destination
  }
}

$files = Get-ChildItem -LiteralPath $packDir -File -Recurse |
  Sort-Object FullName |
  ForEach-Object {
    $relative = $_.FullName.Substring($packDir.Length + 1).Replace("\", "/")
    [ordered]@{
      path = $relative
      bytes = $_.Length
      sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash.ToLowerInvariant()
    }
  }

$packManifest = [ordered]@{
  name = "health-intelligence-agent-pack"
  version = $Version
  release = "v$Version"
  status = "preclinical-prerelease"
  clinical_legal_gate = "pending"
  canonical_repo = "https://github.com/frankxai/health-intelligence-system"
  canonical_release = "https://github.com/frankxai/health-intelligence-system/releases/tag/v$Version"
  install_surfaces = @(
    "Codex plugin",
    "Codex skill",
    "ChatGPT Project prompt",
    "Custom GPT instructions",
    "Claude Project prompt",
    "local redaction prompt",
    "slash-command workflows",
    "private-vault templates"
  )
  files = $files
}

$packManifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $packManifestPath -Encoding utf8

Compress-Archive -Path (Join-Path $packDir "*") -DestinationPath $zipPath -Force

$zip = Get-Item -LiteralPath $zipPath
$releaseManifest = [ordered]@{
  name = "health-intelligence-agent-pack"
  version = $Version
  release = "v$Version"
  status = "preclinical-prerelease"
  canonical_repo = "https://github.com/frankxai/health-intelligence-system"
  canonical_release = "https://github.com/frankxai/health-intelligence-system/releases/tag/v$Version"
  zip_asset = [ordered]@{
    name = "$packName.zip"
    bytes = $zip.Length
    sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $zipPath).Hash.ToLowerInvariant()
  }
  files = $files
}

$releaseManifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $manifestPath -Encoding utf8

Write-Host "Packaged $zipPath"
Write-Host "Manifest $manifestPath"
