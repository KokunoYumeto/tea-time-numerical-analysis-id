[CmdletBinding()]
param(
    [string]$RepositoryRoot = ''
)

$ErrorActionPreference = 'Stop'
$comparison = [System.StringComparison]::OrdinalIgnoreCase
$sourceDateEpoch = '1787356800'

if ([string]::IsNullOrWhiteSpace($RepositoryRoot)) {
    $RepositoryRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
}

$root = [System.IO.Path]::GetFullPath($RepositoryRoot)
$source = Join-Path $root 'source\latex-id-ID'
$workBase = [System.IO.Path]::GetFullPath((Join-Path $root 'build\work'))
$work = [System.IO.Path]::GetFullPath((Join-Path $workBase 'id-ID'))
$output = Join-Path $root 'output\pdf\Tea-Time-Numerical-Analysis-id-ID.pdf'
$main = 'TeaTimeNumericalAnalysis-id-ID'

if (-not (Test-Path -LiteralPath (Join-Path $source "$main.tex") -PathType Leaf)) {
    throw "Portable LaTeX closure is missing: $source"
}

if (-not $work.StartsWith($workBase.TrimEnd('\') + '\', $comparison)) {
    throw "Refusing unsafe work path outside $workBase`: $work"
}

if (Test-Path -LiteralPath $work) {
    Remove-Item -LiteralPath $work -Recurse -Force
}
New-Item -ItemType Directory -Path $work,(Split-Path -Parent $output) -Force | Out-Null
Copy-Item -Path (Join-Path $source '*') -Destination $work -Recurse -Force

$oldEpoch = $env:SOURCE_DATE_EPOCH
$oldForce = $env:FORCE_SOURCE_DATE
try {
    $env:SOURCE_DATE_EPOCH = $sourceDateEpoch
    $env:FORCE_SOURCE_DATE = '1'
    Push-Location $work
    try {
        & latexmk -pdf -interaction=nonstopmode -file-line-error -halt-on-error "$main.tex"
        if ($LASTEXITCODE -ne 0) {
            throw "latexmk failed with exit code $LASTEXITCODE"
        }
    } finally {
        Pop-Location
    }
} finally {
    $env:SOURCE_DATE_EPOCH = $oldEpoch
    $env:FORCE_SOURCE_DATE = $oldForce
}

$built = Join-Path $work "$main.pdf"
if (-not (Test-Path -LiteralPath $built -PathType Leaf)) {
    throw "Expected PDF was not produced: $built"
}
Copy-Item -LiteralPath $built -Destination $output -Force

[pscustomobject]@{
    pdf = [System.IO.Path]::GetRelativePath($root, $output).Replace('\', '/')
    bytes = (Get-Item -LiteralPath $output).Length
    sha256 = (Get-FileHash -LiteralPath $output -Algorithm SHA256).Hash.ToLowerInvariant()
} | ConvertTo-Json
