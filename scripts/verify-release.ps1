param(
  [string]$Version,
  [string]$ZipPath,
  [string]$ManifestPath,
  [switch]$Download
)

$ErrorActionPreference = "Stop"
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
$releaseName = "health-intelligence-system-v$Version"
$tag = "v$Version"
$tempBase = [System.IO.Path]::GetFullPath([System.IO.Path]::GetTempPath()).TrimEnd([System.IO.Path]::DirectorySeparatorChar) + [System.IO.Path]::DirectorySeparatorChar
$tempRoot = [System.IO.Path]::GetFullPath((Join-Path $tempBase ("his-verify-" + [System.Guid]::NewGuid().ToString("N"))))
if (-not $tempRoot.StartsWith($tempBase, [System.StringComparison]::OrdinalIgnoreCase)) {
  throw "Verifier temporary directory escapes the operating-system temp root."
}
$downloadDir = Join-Path $tempRoot "download"

function Assert-Equal {
  param([string]$Label, [object]$Expected, [object]$Actual)
  if ($Expected -ne $Actual) {
    throw "$Label mismatch. Expected '$Expected', got '$Actual'."
  }
}

function Assert-ExactString {
  param([string]$Label, [string]$Expected, [string]$Actual)
  if (-not [System.String]::Equals($Expected, $Actual, [System.StringComparison]::Ordinal)) {
    throw "$Label mismatch. Expected '$Expected', got '$Actual'."
  }
}

function Get-Sha256 {
  param([string]$Path)
  return (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToLowerInvariant()
}

function Get-SafeZipPath {
  param([string]$RawPath)
  if (-not $RawPath -or $RawPath.Length -gt 1024) {
    throw "ZIP entry path is empty or too long."
  }
  if ($RawPath.Contains("\")) {
    throw "ZIP entry uses a non-canonical backslash path: $RawPath"
  }
  if ($RawPath.StartsWith("/") -or $RawPath -match "^[A-Za-z]:") {
    throw "ZIP entry is absolute: $RawPath"
  }
  $segments = @($RawPath.Split("/"))
  if ($segments.Count -eq 0 -or @($segments | Where-Object { -not $_ }).Count -gt 0) {
    throw "ZIP entry contains an empty path segment: $RawPath"
  }
  $reserved = @("CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9")
  foreach ($segment in $segments) {
    if ($segment -in @(".", "..")) {
      throw "ZIP entry contains a traversal segment: $RawPath"
    }
    if ($segment.TrimEnd([char[]]" .") -ne $segment) {
      throw "ZIP entry contains a Windows-ambiguous trailing dot or space: $RawPath"
    }
    if ($segment -match "[:\x00-\x1f]") {
      throw "ZIP entry contains a forbidden character: $RawPath"
    }
    $stem = ($segment -split "\.", 2)[0].ToUpperInvariant()
    if ($reserved -contains $stem) {
      throw "ZIP entry contains a reserved Windows device name: $RawPath"
    }
  }
  return $RawPath
}

function Get-ZipEntrySha256 {
  param([System.IO.Compression.ZipArchiveEntry]$Entry)
  $sha = [System.Security.Cryptography.SHA256]::Create()
  $stream = $Entry.Open()
  try {
    $bytes = $sha.ComputeHash($stream)
    return ([System.BitConverter]::ToString($bytes)).Replace("-", "").ToLowerInvariant()
  } finally {
    $stream.Dispose()
    $sha.Dispose()
  }
}

function Read-ZipEntryText {
  param([System.IO.Compression.ZipArchiveEntry]$Entry)
  $stream = $Entry.Open()
  $encoding = [System.Text.UTF8Encoding]::new($false, $true)
  $reader = [System.IO.StreamReader]::new($stream, $encoding, $true)
  try {
    return $reader.ReadToEnd()
  } finally {
    $reader.Dispose()
    $stream.Dispose()
  }
}

function Get-GitBlobSha256 {
  param([string]$Repository, [string]$ObjectId)
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
  $sha = [System.Security.Cryptography.SHA256]::Create()
  try {
    $hash = $sha.ComputeHash($process.StandardOutput.BaseStream)
    $errorText = $process.StandardError.ReadToEnd()
    $process.WaitForExit()
    if ($process.ExitCode -ne 0) {
      throw "git cat-file failed for $ObjectId`: $errorText"
    }
    return ([System.BitConverter]::ToString($hash)).Replace("-", "").ToLowerInvariant()
  } finally {
    $sha.Dispose()
    $process.Dispose()
  }
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
    if (-not $ZipPath) { $ZipPath = Join-Path $repoRoot "dist\$releaseName.zip" }
    if (-not $ManifestPath) { $ManifestPath = Join-Path $repoRoot "release-manifest.json" }
    if (-not [System.IO.Path]::IsPathRooted($ZipPath)) { $ZipPath = Join-Path $repoRoot $ZipPath }
    if (-not [System.IO.Path]::IsPathRooted($ManifestPath)) { $ManifestPath = Join-Path $repoRoot $ManifestPath }
  }

  if (-not (Test-Path -LiteralPath $ZipPath -PathType Leaf)) { throw "Missing ZIP: $ZipPath" }
  if (-not (Test-Path -LiteralPath $ManifestPath -PathType Leaf)) { throw "Missing manifest: $ManifestPath" }

  $manifest = Get-Content -LiteralPath $ManifestPath -Raw | ConvertFrom-Json
  $zip = Get-Item -LiteralPath $ZipPath
  Assert-Equal "release" $tag $manifest.release
  Assert-Equal "status" "nonmedical-synthetic-prerelease" $manifest.status
  Assert-Equal "evidence state" "all_shipped_claims_draft_not_user_facing" $manifest.evidence_state
  Assert-Equal "medical functionality" "disabled" $manifest.medical_functionality
  Assert-Equal "clinical/legal gate" "pending" $manifest.clinical_legal_gate
  if ($manifest.source_commit -notmatch "^(?:[a-f0-9]{40}|[a-f0-9]{64})$") { throw "Manifest source_commit is invalid." }
  $expectedCommit = if ($Download) {
    (& git -C $repoRoot rev-parse "refs/tags/$tag^{commit}" 2>$null).Trim()
  } else {
    (& git -C $repoRoot rev-parse "HEAD^{commit}" 2>$null).Trim()
  }
  if ($LASTEXITCODE -ne 0 -or $expectedCommit -notmatch "^(?:[a-f0-9]{40}|[a-f0-9]{64})$") {
    throw "Unable to bind the candidate to the expected local commit/tag. Fetch the exact tag before download verification."
  }
  Assert-Equal "source commit binding" $expectedCommit $manifest.source_commit
  if ($manifest.PSObject.Properties.Name -contains "evidence_checked") {
    throw "Manifest must not claim a hardcoded evidence_checked date."
  }
  Assert-Equal "zip name" "$releaseName.zip" $manifest.zip_asset.name
  Assert-Equal "zip bytes" ([int64]$manifest.zip_asset.bytes) ([int64]$zip.Length)
  Assert-Equal "zip sha256" $manifest.zip_asset.sha256 (Get-Sha256 -Path $zip.FullName)

  Add-Type -AssemblyName System.IO.Compression.FileSystem
  $archive = [System.IO.Compression.ZipFile]::OpenRead($zip.FullName)
  try {
    $entryByPath = [System.Collections.Generic.Dictionary[string,System.IO.Compression.ZipArchiveEntry]]::new([System.StringComparer]::Ordinal)
    $entryPathsFolded = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
    $directoryPaths = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::Ordinal)
    foreach ($entry in $archive.Entries) {
      if (-not $entry.Name) {
        if (-not $entry.FullName.EndsWith("/")) {
          throw "ZIP contains an unnamed non-directory entry: $($entry.FullName)"
        }
        $directoryPath = Get-SafeZipPath -RawPath $entry.FullName.Substring(0, $entry.FullName.Length - 1)
        if (-not $entryPathsFolded.Add($directoryPath) -or -not $directoryPaths.Add($directoryPath)) {
          throw "ZIP contains a duplicate or case-colliding directory path: $directoryPath"
        }
        $directoryAttributes = [uint32]$entry.ExternalAttributes
        $directoryUnixType = (($directoryAttributes -shr 16) -band 0xF000)
        if ($directoryUnixType -ne 0 -and $directoryUnixType -ne 0x4000) {
          throw "ZIP contains a symlink or special directory entry: $directoryPath"
        }
        continue
      }
      $path = Get-SafeZipPath -RawPath $entry.FullName
      if ($path -match "(^|/)(apps|\.git|\.github|node_modules|\.next|_local|\.heart|\.machine)(/|$)|(^|/)(\.env($|\.)|.*\.(key|pem|p12|pfx|sqlite|duckdb|parquet|pyc))$|secret|credential") {
        throw "ZIP contains a forbidden path: $path"
      }
      if ($entryByPath.ContainsKey($path) -or -not $entryPathsFolded.Add($path)) {
        throw "ZIP contains a duplicate or case-colliding path: $path"
      }
      $externalAttributes = [uint32]$entry.ExternalAttributes
      $unixType = (($externalAttributes -shr 16) -band 0xF000)
      if ($unixType -ne 0 -and $unixType -ne 0x8000) {
        throw "ZIP contains a symlink or special-file entry: $path"
      }
      if (($externalAttributes -band 0x10) -ne 0) {
        throw "ZIP file entry carries a directory attribute: $path"
      }
      $entryByPath[$path] = $entry
    }

    $requiredSafetyFiles = @(
      "README.md", "SAFETY.md", "PRIVACY.md", "VALIDATION.md", "REVIEW-GATE.md",
      "bios/requirements.txt",
      "bios/schemas/claim.schema.json", "bios/schemas/protocol.schema.json",
      "bios/schemas/consent.schema.json", "bios/schemas/handoff-receipt.schema.json",
      "bios/schemas/domain-agent-registry.schema.json",
      "bios/registry/public-domain-agents.json",
      "bios/src/bios_substrate/privacy.py", "bios/src/bios_substrate/audit.py",
      "bios/tests/test_bios.py", "docs/evidence-admission-and-copyright.md",
      "docs/public-core-private-runtime-boundary.md", "release/research-preview-admission.json"
    )
    foreach ($required in $requiredSafetyFiles) {
      if (-not $entryByPath.ContainsKey($required)) {
        throw "Missing required safety file in ZIP: $required"
      }
    }
    if (-not $entryByPath.ContainsKey("release-manifest.json")) {
      throw "ZIP is missing its embedded release-manifest.json."
    }

    $manifestPaths = @($manifest.files | ForEach-Object { Get-SafeZipPath -RawPath ([string]$_.path) })
    $manifestExact = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::Ordinal)
    $manifestFolded = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
    foreach ($path in $manifestPaths) {
      if (-not $manifestExact.Add($path) -or -not $manifestFolded.Add($path)) {
        throw "Manifest contains duplicate or case-colliding file paths."
      }
    }
    $actualPaths = @($entryByPath.Keys | Where-Object { $_ -cne "release-manifest.json" } | Sort-Object -CaseSensitive)
    $expectedPaths = @($manifestPaths | Sort-Object -CaseSensitive)
    $embeddedManifest = Read-ZipEntryText -Entry $entryByPath["release-manifest.json"] | ConvertFrom-Json
    foreach ($field in @("name", "version", "release", "status", "source_commit", "admission_manifest_sha256", "evidence_state", "medical_functionality", "clinical_legal_gate", "generated_at")) {
      Assert-Equal "embedded manifest $field" $manifest.$field $embeddedManifest.$field
    }
    Assert-Equal "embedded manifest file count" @($manifest.files).Count @($embeddedManifest.files).Count
    for ($index = 0; $index -lt @($manifest.files).Count; $index++) {
      foreach ($field in @("path", "mode", "git_blob", "bytes", "sha256")) {
        if ($field -in @("path", "mode", "git_blob", "sha256")) {
          Assert-ExactString "embedded manifest files[$index].$field" ([string]$manifest.files[$index].$field) ([string]$embeddedManifest.files[$index].$field)
        } else {
          Assert-Equal "embedded manifest files[$index].$field" $manifest.files[$index].$field $embeddedManifest.files[$index].$field
        }
      }
    }
    $admissionEntry = $entryByPath["release/research-preview-admission.json"]
    Assert-Equal "admission manifest sha256" $manifest.admission_manifest_sha256 (Get-ZipEntrySha256 -Entry $admissionEntry)
    $admission = Read-ZipEntryText -Entry $admissionEntry | ConvertFrom-Json
    Assert-Equal "admission status" "synthetic_source_review_only" $admission.status
    Assert-Equal "admission data policy" "no_real_person_or_patient_data" $admission.data_policy
    Assert-Equal "admission size ceiling" 262144 ([int64]$admission.max_file_bytes)
    $admittedPaths = @($admission.admitted_paths | Sort-Object -CaseSensitive)
    Assert-Equal "admission path count" $expectedPaths.Count $admittedPaths.Count
    for ($index = 0; $index -lt $expectedPaths.Count; $index++) {
      Assert-ExactString "admission exact path[$index]" $expectedPaths[$index] $admittedPaths[$index]
    }
    foreach ($directoryPath in $directoryPaths) {
      $prefix = "$directoryPath/"
      $isRequiredParent = $false
      foreach ($path in $expectedPaths) {
        if ($path.StartsWith($prefix, [System.StringComparison]::Ordinal)) {
          $isRequiredParent = $true
          break
        }
      }
      if (-not $isRequiredParent) {
        throw "ZIP contains an unnecessary explicit directory entry: $directoryPath"
      }
    }
    Assert-Equal "manifest file count" $expectedPaths.Count $actualPaths.Count
    for ($index = 0; $index -lt $expectedPaths.Count; $index++) {
      Assert-ExactString "manifest exact path[$index]" $expectedPaths[$index] $actualPaths[$index]
    }
    foreach ($file in $manifest.files) {
      $path = [string]$file.path
      if (-not $entryByPath.ContainsKey($path)) {
        throw "Manifest-listed ZIP entry is missing: $path"
      }
      $entry = $entryByPath[$path]
      if ([int64]$entry.Length -gt [int64]$admission.max_file_bytes) {
        throw "ZIP entry exceeds the admission size ceiling: $path"
      }
      Assert-Equal "bytes for $path" ([int64]$file.bytes) ([int64]$entry.Length)
      Assert-Equal "sha256 for $path" $file.sha256 (Get-ZipEntrySha256 -Entry $entry)
      $treeRow = @(& git -C $repoRoot ls-tree $manifest.source_commit -- $path)
      if ($LASTEXITCODE -ne 0 -or $treeRow.Count -ne 1 -or $treeRow[0] -notmatch "^(?<mode>[0-9]{6})\s+(?<type>\w+)\s+(?<oid>[a-f0-9]{40,64})`t(?<treePath>.+)$") {
        throw "Manifest path is not an exact blob in the bound source commit: $path"
      }
      if ($Matches.mode -notin @("100644", "100755") -or $Matches.type -ne "blob") {
        throw "Bound source path is a symlink, gitlink, or unsupported mode: $path"
      }
      Assert-ExactString "bound Git path for $path" $path $Matches.treePath
      Assert-ExactString "git mode for $path" $Matches.mode ([string]$file.mode)
      Assert-ExactString "git blob for $path" $Matches.oid ([string]$file.git_blob)
      Assert-Equal "ZIP bytes bound to Git blob for $path" (Get-GitBlobSha256 -Repository $repoRoot -ObjectId $Matches.oid) (Get-ZipEntrySha256 -Entry $entry)
      $entryText = Read-ZipEntryText -Entry $entry
      if ($entryText -match '-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|AKIA[0-9A-Z]{16}|(?i)(api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*[^\s]{8,}') {
        throw "ZIP entry contains prohibited secret-like content: $path"
      }
      if ($entryText -match "(?i)[A-Z]:[\\/]Users[\\/]|/Users/[^/]+/|/home/[^/]+/") {
        throw "ZIP entry contains a local-machine path: $path"
      }
    }

    foreach ($claimPath in @($entryByPath.Keys | Where-Object { $_ -match "^bios/packs/.+/claims/.+\.json$" })) {
      $claim = Read-ZipEntryText -Entry $entryByPath[$claimPath] | ConvertFrom-Json
      Assert-Equal "claim discovery hold $($claim.claim_id)" "draft" $claim.status
      Assert-Equal "claim user-facing gate $($claim.claim_id)" $false $claim.admission.user_facing_allowed
    }
    foreach ($protocolPath in @($entryByPath.Keys | Where-Object { $_ -match "^bios/packs/.+/protocols/.+\.json$" })) {
      $protocol = Read-ZipEntryText -Entry $entryByPath[$protocolPath] | ConvertFrom-Json
      Assert-Equal "protocol synthetic hold $($protocol.protocol_id)" "draft_synthetic" $protocol.release_status
      Assert-Equal "medical gate $($protocol.protocol_id)" $true $protocol.safety.medical_functionality_disabled
    }

    $readme = Read-ZipEntryText -Entry $entryByPath["README.md"]
    $safety = Read-ZipEntryText -Entry $entryByPath["SAFETY.md"]
    if ($readme -notmatch "Not medical advice" -or $safety -notmatch "does not provide medical advice") {
      throw "Safety boundary language is missing."
    }

    Write-Host "Verified $releaseName from commit $($manifest.source_commit)"
    Write-Host "ZIP SHA-256: $($manifest.zip_asset.sha256)"
    Write-Host "Files checked: $($manifest.files.Count)"
  } finally {
    $archive.Dispose()
  }
} finally {
  if (Test-Path -LiteralPath $tempRoot) {
    $tempItem = Get-Item -LiteralPath $tempRoot -Force
    if (-not $tempItem.FullName.StartsWith($tempBase, [System.StringComparison]::OrdinalIgnoreCase) -or ($tempItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
      throw "Refusing to remove an unsafe verifier temporary directory: $($tempItem.FullName)"
    }
    Remove-Item -LiteralPath $tempRoot -Recurse -Force
  }
}
