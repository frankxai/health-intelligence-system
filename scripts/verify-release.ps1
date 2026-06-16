param(
  [string]$Version = $(if ($env:npm_package_version) { $env:npm_package_version } else { "0.1.1" }),
  [string]$ZipPath,
  [string]$ManifestPath,
  [switch]$Download
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$releaseName = "health-intelligence-system-v$Version"
$tag = "v$Version"
$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("his-verify-" + [System.Guid]::NewGuid().ToString("N"))
$extractDir = Join-Path $tempRoot "extract"
$downloadDir = Join-Path $tempRoot "download"

function Assert-Equal {
  param(
    [string]$Label,
    [object]$Expected,
    [object]$Actual
  )

  if ($Expected -ne $Actual) {
    throw "$Label mismatch. Expected '$Expected', got '$Actual'."
  }
}

function Get-Sha256 {
  param([string]$Path)
  return (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToLowerInvariant()
}

try {
  New-Item -ItemType Directory -Path $tempRoot -Force | Out-Null

  if ($Download) {
    New-Item -ItemType Directory -Path $downloadDir -Force | Out-Null
    $ZipPath = Join-Path $downloadDir "$releaseName.zip"
    $ManifestPath = Join-Path $downloadDir "release-manifest.json"
    $baseUrl = "https://github.com/frankxai/health-intelligence-system/releases/download/$tag"

    Invoke-WebRequest -Uri "$baseUrl/$releaseName.zip" -OutFile $ZipPath
    Invoke-WebRequest -Uri "$baseUrl/release-manifest.json" -OutFile $ManifestPath
  } else {
    if (-not $ZipPath) {
      $ZipPath = Join-Path $repoRoot "dist\$releaseName.zip"
    }
    if (-not $ManifestPath) {
      $ManifestPath = Join-Path $repoRoot "release-manifest.json"
    }
    if (-not [System.IO.Path]::IsPathRooted($ZipPath)) {
      $ZipPath = Join-Path $repoRoot $ZipPath
    }
    if (-not [System.IO.Path]::IsPathRooted($ManifestPath)) {
      $ManifestPath = Join-Path $repoRoot $ManifestPath
    }
  }

  if (-not (Test-Path -LiteralPath $ZipPath)) {
    throw "Missing ZIP: $ZipPath"
  }
  if (-not (Test-Path -LiteralPath $ManifestPath)) {
    throw "Missing manifest: $ManifestPath"
  }

  $manifest = Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json
  $zip = Get-Item -LiteralPath $ZipPath

  Assert-Equal "release" $tag $manifest.release
  Assert-Equal "zip name" "$releaseName.zip" $manifest.zip_asset.name
  Assert-Equal "zip bytes" ([int64]$manifest.zip_asset.bytes) ([int64]$zip.Length)
  Assert-Equal "zip sha256" $manifest.zip_asset.sha256 (Get-Sha256 -Path $zip.FullName)

  New-Item -ItemType Directory -Path $extractDir -Force | Out-Null
  Expand-Archive -LiteralPath $zip.FullName -DestinationPath $extractDir -Force

  $requiredSafetyFiles = @(
    "README.md",
    "SAFETY.md",
    "PRIVACY.md",
    "VALIDATION.md",
    "REVIEW-GATE.md",
    "docs/cancer-detection-prep-treatment.md",
    "docs/evidence-sources.md"
  )

  foreach ($required in $requiredSafetyFiles) {
    $requiredPath = Join-Path $extractDir ($required.Replace("/", [System.IO.Path]::DirectorySeparatorChar))
    if (-not (Test-Path -LiteralPath $requiredPath)) {
      throw "Missing required safety file in ZIP: $required"
    }
  }

  foreach ($file in $manifest.files) {
    $relativePath = $file.path.Replace("/", [System.IO.Path]::DirectorySeparatorChar)
    $expandedPath = Join-Path $extractDir $relativePath

    if (-not (Test-Path -LiteralPath $expandedPath)) {
      throw "Manifest-listed file missing after extraction: $($file.path)"
    }

    $expanded = Get-Item -LiteralPath $expandedPath
    Assert-Equal "bytes for $($file.path)" ([int64]$file.bytes) ([int64]$expanded.Length)
    Assert-Equal "sha256 for $($file.path)" $file.sha256 (Get-Sha256 -Path $expanded.FullName)
  }

  $readme = Get-Content -LiteralPath (Join-Path $extractDir "README.md") -Raw
  $safety = Get-Content -LiteralPath (Join-Path $extractDir "SAFETY.md") -Raw
  if ($readme -notmatch "Not medical advice" -or $safety -notmatch "does not provide medical advice" -or $safety -notmatch "diagnose cancer") {
    throw "Safety boundary language is missing from README.md or SAFETY.md."
  }

  Write-Host "Verified $releaseName"
  Write-Host "ZIP SHA-256: $($manifest.zip_asset.sha256)"
  Write-Host "Files checked: $($manifest.files.Count)"
} finally {
  if (Test-Path -LiteralPath $tempRoot) {
    Remove-Item -LiteralPath $tempRoot -Recurse -Force
  }
}
