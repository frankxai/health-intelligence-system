param(
  [string]$Version,
  [string]$SourceRef = "HEAD"
)

$ErrorActionPreference = "Stop"

function Assert-ContainedPath {
  param([string]$Parent, [string]$Child, [string]$Label)
  $parentFull = [System.IO.Path]::GetFullPath($Parent).TrimEnd([System.IO.Path]::DirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar
  $childFull = [System.IO.Path]::GetFullPath($Child)
  if (-not $childFull.StartsWith($parentFull, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "$Label escapes the repository boundary: $childFull"
  }
  return $childFull
}

function Write-GitBlob {
  param([string]$Repository, [string]$ObjectId, [string]$Destination)
  $parent = Split-Path -Parent $Destination
  if (-not (Test-Path -LiteralPath $parent -PathType Container)) {
    New-Item -ItemType Directory -Path $parent | Out-Null
  }
  $start = [System.Diagnostics.ProcessStartInfo]::new()
  $start.FileName = "git"
  $start.UseShellExecute = $false
  $start.RedirectStandardOutput = $true
  $start.RedirectStandardError = $true
  foreach ($argument in @("-C", $Repository, "cat-file", "blob", $ObjectId)) {
    [void]$start.ArgumentList.Add($argument)
  }
  $process = [System.Diagnostics.Process]::new()
  $process.StartInfo = $start
  if (-not $process.Start()) { throw "Unable to start git cat-file." }
  $output = [System.IO.File]::Open($Destination, [System.IO.FileMode]::CreateNew, [System.IO.FileAccess]::Write, [System.IO.FileShare]::None)
  try {
    $process.StandardOutput.BaseStream.CopyTo($output)
  } finally {
    $output.Dispose()
  }
  $errorText = $process.StandardError.ReadToEnd()
  $process.WaitForExit()
  if ($process.ExitCode -ne 0) {
    throw "git cat-file failed for $ObjectId`: $errorText"
  }
  $process.Dispose()
}

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
if (-not $Version) {
  $Version = if ($env:npm_package_version) {
    $env:npm_package_version
  } else {
    (Get-Content -LiteralPath (Join-Path $repoRoot "package.json") -Raw | ConvertFrom-Json).version
  }
}
if ($Version -notmatch "^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$") {
  throw "Version must be one strict SemVer value."
}
$gitTop = (& git -C $repoRoot rev-parse --show-toplevel).Trim().Replace("/", "\")
if ($LASTEXITCODE -ne 0 -or $gitTop -ne $repoRoot) {
  throw "Release packaging must run from the verified health-intelligence-system Git repository."
}

$sourceCommit = (& git -C $repoRoot rev-parse "$SourceRef^{commit}").Trim()
if ($LASTEXITCODE -ne 0 -or $sourceCommit -notmatch "^(?:[a-f0-9]{40}|[a-f0-9]{64})$") {
  throw "SourceRef must resolve to one Git commit."
}
$headCommit = (& git -C $repoRoot rev-parse HEAD).Trim()
if ($sourceCommit -ne $headCommit) {
  throw "SourceRef must equal HEAD; detached or alternate-tree release packaging is disabled."
}

# Do this before deleting or creating output. A release must be reproducible from one clean commit.
$dirty = @(& git -C $repoRoot status --porcelain=v1 --untracked-files=all --ignored)
if ($LASTEXITCODE -ne 0) {
  throw "Unable to inspect Git worktree state."
}
if ($dirty.Count -gt 0) {
  $sample = ($dirty | Select-Object -First 12) -join "; "
  throw "Release packaging requires a completely clean tree/index and no untracked or ignored artifacts. Found: $sample"
}

$admissionRelativePath = "release/research-preview-admission.json"
$admissionWorktreePath = Join-Path $repoRoot $admissionRelativePath
$admission = Get-Content -LiteralPath $admissionWorktreePath -Raw | ConvertFrom-Json
if (
  $admission.name -ne "health-intelligence-system-research-preview" -or
  $admission.schema_version -ne "0.1.0" -or
  $admission.status -ne "synthetic_source_review_only" -or
  $admission.data_policy -ne "no_real_person_or_patient_data" -or
  [int64]$admission.max_file_bytes -ne 262144
) {
  throw "Release admission manifest policy is invalid."
}
$admittedPaths = @($admission.admitted_paths)
$admittedExact = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::Ordinal)
$admittedFolded = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
foreach ($path in $admittedPaths) {
  if (-not $admittedExact.Add([string]$path) -or -not $admittedFolded.Add([string]$path)) {
    throw "Release admission manifest paths must be unique without case collisions."
  }
}
if ($admittedPaths.Count -eq 0) {
  throw "Release admission manifest paths must be non-empty and unique."
}
foreach ($path in $admittedPaths) {
  if ($path -notmatch "^[A-Za-z0-9._/-]+$" -or $path.StartsWith("/") -or $path -match "(^|/)\.\.(/|$)") {
    throw "Release admission manifest contains an unsafe path: $path"
  }
}
if ($admittedPaths -notcontains $admissionRelativePath) {
  throw "Release admission manifest must admit itself."
}

$treeRows = @(& git -C $repoRoot ls-tree -r $sourceCommit -- $admittedPaths)
if ($LASTEXITCODE -ne 0 -or $treeRows.Count -eq 0) {
  throw "Unable to enumerate the exact release tree."
}
$releaseEntries = @()
$forbidden = "(^|/)(apps|\.git|\.github|node_modules|\.next|dist|packages|_local|\.heart|\.machine)(/|$)|(^|/)(\.env($|\.)|.*\.(key|pem|p12|pfx|sqlite|duckdb|parquet|pyc))$|secret|credential"
foreach ($row in $treeRows) {
  if ($row -notmatch "^(?<mode>[0-9]{6})\s+(?<type>\w+)\s+(?<oid>[a-f0-9]{40,64})`t(?<path>.+)$") {
    throw "Unexpected Git tree row: $row"
  }
  if ($Matches.mode -notin @("100644", "100755") -or $Matches.type -ne "blob") {
    throw "Release tree contains a symlink, gitlink, or unsupported mode: $($Matches.path)"
  }
  if ($Matches.path -match $forbidden) {
    throw "Release tree contains a forbidden path: $($Matches.path)"
  }
  if ($Matches.path -notmatch "^[A-Za-z0-9._/-]+$") {
    throw "Release tree contains a non-canonical path: $($Matches.path)"
  }
  $releaseEntries += [pscustomobject]@{
    mode = $Matches.mode
    oid = $Matches.oid
    path = $Matches.path
  }
}
$actualReleasePaths = @($releaseEntries.path | Sort-Object -CaseSensitive)
$expectedReleasePaths = @($admittedPaths | Sort-Object -CaseSensitive)
if ($actualReleasePaths.Count -ne $expectedReleasePaths.Count) {
  throw "Release tree does not exactly match the admission manifest."
}
for ($index = 0; $index -lt $expectedReleasePaths.Count; $index++) {
  if ($actualReleasePaths[$index] -cne $expectedReleasePaths[$index]) {
    throw "Release tree path mismatch. Expected $($expectedReleasePaths[$index]), got $($actualReleasePaths[$index])."
  }
}

$versionName = "health-intelligence-system-v$Version"
$packagesRoot = Assert-ContainedPath -Parent $repoRoot -Child (Join-Path $repoRoot "packages") -Label "packages root"
$packageDir = Assert-ContainedPath -Parent $repoRoot -Child (Join-Path $packagesRoot $versionName) -Label "package directory"
$distDir = Assert-ContainedPath -Parent $repoRoot -Child (Join-Path $repoRoot "dist") -Label "distribution directory"
$zipPath = Assert-ContainedPath -Parent $repoRoot -Child (Join-Path $distDir "$versionName.zip") -Label "ZIP path"
$manifestPath = Join-Path $repoRoot "release-manifest.json"
$packageManifestPath = Join-Path $packageDir "release-manifest.json"
foreach ($outputPath in @($packagesRoot, $distDir, $manifestPath)) {
  if (Test-Path -LiteralPath $outputPath) {
    throw "Release output already exists; refusing overwrite: $outputPath"
  }
}

New-Item -ItemType Directory -Path $packagesRoot | Out-Null
New-Item -ItemType Directory -Path $packageDir | Out-Null
New-Item -ItemType Directory -Path $distDir | Out-Null
foreach ($outputRoot in @($packagesRoot, $packageDir, $distDir)) {
  $item = Get-Item -LiteralPath $outputRoot -Force
  if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
    throw "Release output root cannot be a reparse point: $outputRoot"
  }
}

foreach ($entry in $releaseEntries) {
  $destination = Assert-ContainedPath -Parent $packageDir -Child (Join-Path $packageDir $entry.path) -Label "release file"
  Write-GitBlob -Repository $repoRoot -ObjectId $entry.oid -Destination $destination
  $written = Get-Item -LiteralPath $destination -Force
  if ($written.Length -gt [int64]$admission.max_file_bytes) {
    throw "Release file exceeds the admission size ceiling: $($entry.path)"
  }
  $bytes = [System.IO.File]::ReadAllBytes($destination)
  if ($bytes -contains 0) {
    throw "Release candidate contains binary or NUL content outside the admitted text boundary: $($entry.path)"
  }
  $text = [System.Text.UTF8Encoding]::new($false, $true).GetString($bytes)
  if ($text -match '-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|AKIA[0-9A-Z]{16}|(?i)(api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*[^\s]{8,}') {
    throw "Release candidate contains prohibited secret-like content: $($entry.path)"
  }
  if ($text -match "(?i)[A-Z]:[\\/]Users[\\/]|/Users/[^/]+/|/home/[^/]+/") {
    throw "Release candidate contains a local-machine path: $($entry.path)"
  }
}

$files = @($releaseEntries | Sort-Object path | ForEach-Object {
  $fullPath = Join-Path $packageDir $_.path
  $file = Get-Item -LiteralPath $fullPath
  [ordered]@{
    path = $_.path
    mode = $_.mode
    git_blob = $_.oid
    bytes = $file.Length
    sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $fullPath).Hash.ToLowerInvariant()
  }
})

$manifestCore = [ordered]@{
  name = "health-intelligence-system"
  version = $Version
  release = "v$Version"
  status = "nonmedical-synthetic-prerelease"
  source_commit = $sourceCommit
  admission_manifest_sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $packageDir $admissionRelativePath)).Hash.ToLowerInvariant()
  evidence_state = "all_shipped_claims_draft_not_user_facing"
  medical_functionality = "disabled"
  clinical_legal_gate = "pending"
  generated_at = [DateTimeOffset]::UtcNow.ToString("o")
  files = $files
}
$manifestCore | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $packageManifestPath -Encoding utf8

Compress-Archive -Path (Join-Path $packageDir "*") -DestinationPath $zipPath
$zip = Get-Item -LiteralPath $zipPath
$releaseManifest = [ordered]@{
  name = $manifestCore.name
  version = $manifestCore.version
  release = $manifestCore.release
  status = $manifestCore.status
  source_commit = $manifestCore.source_commit
  admission_manifest_sha256 = $manifestCore.admission_manifest_sha256
  evidence_state = $manifestCore.evidence_state
  medical_functionality = $manifestCore.medical_functionality
  clinical_legal_gate = $manifestCore.clinical_legal_gate
  generated_at = $manifestCore.generated_at
  files = $manifestCore.files
  canonical_repo = "https://github.com/frankxai/health-intelligence-system"
  zip_asset = [ordered]@{
    name = "$versionName.zip"
    bytes = $zip.Length
    sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $zipPath).Hash.ToLowerInvariant()
  }
}
$releaseManifest | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $manifestPath -Encoding utf8

Write-Host "Packaged exact admitted Git blobs from commit $sourceCommit to $zipPath"
Write-Host "Manifest $manifestPath"
