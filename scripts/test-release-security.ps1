param(
  [switch]$IncludeCandidateTamper
)

$ErrorActionPreference = "Stop"
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$version = (Get-Content -LiteralPath (Join-Path $repoRoot "package.json") -Raw | ConvertFrom-Json).version
$headCommit = (& git -C $repoRoot rev-parse "HEAD^{commit}").Trim()
$tempBase = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath()).TrimEnd([System.IO.Path]::DirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar
$caseRoot = [System.IO.Path]::GetFullPath((Join-Path $tempBase ("his-release-security-" + [System.Guid]::NewGuid().ToString("N"))))
if (-not $caseRoot.StartsWith($tempBase, [System.StringComparison]::OrdinalIgnoreCase)) {
  throw "Security-test directory escapes the operating-system temp root."
}

function Invoke-ExpectedFailure {
  param([string[]]$Arguments, [string]$ExpectedPattern, [string]$Label)
  $output = & pwsh @Arguments 2>&1 | Out-String
  if ($LASTEXITCODE -eq 0 -or $output -notmatch $ExpectedPattern) {
    throw "$Label did not fail closed as expected. Output: $output"
  }
}

function Write-ZipTextEntry {
  param([System.IO.Compression.ZipArchive]$Archive, [string]$Path, [string]$Text)
  $entry = $Archive.CreateEntry($Path)
  $stream = $entry.Open()
  $writer = [System.IO.StreamWriter]::new($stream, [System.Text.UTF8Encoding]::new($false))
  try {
    $writer.Write($Text)
  } finally {
    $writer.Dispose()
    $stream.Dispose()
  }
}

try {
  New-Item -ItemType Directory -Path $caseRoot | Out-Null

  Invoke-ExpectedFailure -Label "package version traversal" -ExpectedPattern "strict SemVer" -Arguments @(
    "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", (Join-Path $repoRoot "scripts/package-release.ps1"),
    "-Version", "\..\..\outside"
  )

  Add-Type -AssemblyName System.IO.Compression.FileSystem
  $maliciousZip = Join-Path $caseRoot "malicious.zip"
  $fileStream = [System.IO.File]::Open($maliciousZip, [System.IO.FileMode]::CreateNew)
  $archive = [System.IO.Compression.ZipArchive]::new($fileStream, [System.IO.Compression.ZipArchiveMode]::Create, $false)
  try {
    Write-ZipTextEntry -Archive $archive -Path ".. /escape.txt" -Text "synthetic"
  } finally {
    $archive.Dispose()
    $fileStream.Dispose()
  }
  $maliciousManifest = [ordered]@{
    name = "health-intelligence-system"
    version = $version
    release = "v$version"
    status = "nonmedical-synthetic-prerelease"
    source_commit = $headCommit
    admission_manifest_sha256 = "0" * 64
    evidence_state = "all_shipped_claims_draft_not_user_facing"
    medical_functionality = "disabled"
    clinical_legal_gate = "pending"
    generated_at = [DateTimeOffset]::UtcNow.ToString("o")
    files = @()
    zip_asset = [ordered]@{
      name = "health-intelligence-system-v$version.zip"
      bytes = (Get-Item -LiteralPath $maliciousZip).Length
      sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $maliciousZip).Hash.ToLowerInvariant()
    }
  }
  $maliciousManifestPath = Join-Path $caseRoot "malicious-manifest.json"
  $maliciousManifest | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $maliciousManifestPath -Encoding utf8
  Invoke-ExpectedFailure -Label "Windows ZIP traversal" -ExpectedPattern "Windows-ambiguous trailing dot or space" -Arguments @(
    "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", (Join-Path $repoRoot "scripts/verify-release.ps1"),
    "-Version", $version, "-ZipPath", $maliciousZip, "-ManifestPath", $maliciousManifestPath
  )

  if ($IncludeCandidateTamper) {
    $candidateZip = Join-Path $repoRoot "dist/health-intelligence-system-v$version.zip"
    $candidateManifest = Join-Path $repoRoot "release-manifest.json"
    if (-not (Test-Path -LiteralPath $candidateZip -PathType Leaf) -or -not (Test-Path -LiteralPath $candidateManifest -PathType Leaf)) {
      throw "Candidate tamper test requires a locally packaged candidate."
    }
    $tamperedZip = Join-Path $caseRoot "tampered.zip"
    $tamperedManifestPath = Join-Path $caseRoot "tampered-manifest.json"
    Copy-Item -LiteralPath $candidateZip -Destination $tamperedZip
    $external = Get-Content -LiteralPath $candidateManifest -Raw | ConvertFrom-Json
    $zip = [System.IO.Compression.ZipFile]::Open($tamperedZip, [System.IO.Compression.ZipArchiveMode]::Update)
    try {
      $embeddedEntry = $zip.GetEntry("release-manifest.json")
      $reader = [System.IO.StreamReader]::new($embeddedEntry.Open(), [System.Text.Encoding]::UTF8)
      try { $embedded = $reader.ReadToEnd() | ConvertFrom-Json } finally { $reader.Dispose() }

      $readmeEntry = $zip.GetEntry("README.md")
      $readmeEntry.Delete()
      $tamperedText = "synthetic tamper that is valid UTF-8 but not the bound Git blob"
      Write-ZipTextEntry -Archive $zip -Path "README.md" -Text $tamperedText
      $tamperedBytes = [System.Text.Encoding]::UTF8.GetBytes($tamperedText)
      $tamperedSha = [System.Convert]::ToHexString([System.Security.Cryptography.SHA256]::HashData($tamperedBytes)).ToLowerInvariant()
      foreach ($manifestObject in @($external, $embedded)) {
        $row = @($manifestObject.files | Where-Object { $_.path -eq "README.md" })
        if ($row.Count -ne 1) { throw "Candidate manifest must contain one README.md row." }
        $row[0].bytes = $tamperedBytes.Length
        $row[0].sha256 = $tamperedSha
      }
      $embeddedEntry.Delete()
      Write-ZipTextEntry -Archive $zip -Path "release-manifest.json" -Text ($embedded | ConvertTo-Json -Depth 10)
    } finally {
      $zip.Dispose()
    }
    $external.zip_asset.bytes = (Get-Item -LiteralPath $tamperedZip).Length
    $external.zip_asset.sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $tamperedZip).Hash.ToLowerInvariant()
    $external | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $tamperedManifestPath -Encoding utf8
    Invoke-ExpectedFailure -Label "Git blob substitution" -ExpectedPattern "ZIP bytes bound to Git blob" -Arguments @(
      "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", (Join-Path $repoRoot "scripts/verify-release.ps1"),
      "-Version", $version, "-ZipPath", $tamperedZip, "-ManifestPath", $tamperedManifestPath
    )
  }

  Write-Host "Release security regressions: PASS"
} finally {
  if (Test-Path -LiteralPath $caseRoot) {
    $caseItem = Get-Item -LiteralPath $caseRoot -Force
    if (-not $caseItem.FullName.StartsWith($tempBase, [System.StringComparison]::OrdinalIgnoreCase) -or ($caseItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
      throw "Refusing to remove an unsafe security-test directory: $($caseItem.FullName)"
    }
    Remove-Item -LiteralPath $caseRoot -Recurse -Force
  }
}
