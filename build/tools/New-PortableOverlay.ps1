[CmdletBinding()]
param(
    [ValidateSet('en-baseline', 'id-ID')]
    [string]$Mode = 'id-ID',

    [string]$LaneRoot = ''
)

$ErrorActionPreference = 'Stop'
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
$comparison = [System.StringComparison]::OrdinalIgnoreCase

if ([string]::IsNullOrWhiteSpace($LaneRoot)) {
    $LaneRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
}

$lane = [System.IO.Path]::GetFullPath($LaneRoot)
$sourceRoot = Join-Path $lane 'source\lqbrin-tea-time-numerical-1868821'
$translationRoot = Join-Path $lane 'translation\lyx-id'
$stageBase = [System.IO.Path]::GetFullPath((Join-Path $lane 'build\stage'))
$stageRoot = [System.IO.Path]::GetFullPath((Join-Path $stageBase $Mode))
$manifestRoot = Join-Path $lane 'build\manifests'
$manifestPath = Join-Path $manifestRoot "$Mode-overlay.json"

foreach ($required in @($sourceRoot, $translationRoot)) {
    if (-not (Test-Path -LiteralPath $required -PathType Container)) {
        throw "Required directory is missing: $required"
    }
}

$stagePrefix = $stageBase.TrimEnd('\') + '\'
if (-not $stageRoot.StartsWith($stagePrefix, $comparison)) {
    throw "Refusing unsafe stage path outside $stageBase`: $stageRoot"
}

if (Test-Path -LiteralPath $stageRoot) {
    Remove-Item -LiteralPath $stageRoot -Recurse -Force
}
New-Item -ItemType Directory -Path $stageRoot -Force | Out-Null
New-Item -ItemType Directory -Path $manifestRoot -Force | Out-Null

Get-ChildItem -LiteralPath $sourceRoot -Force | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination $stageRoot -Recurse -Force
}

$lyxNames = @(Get-ChildItem -LiteralPath $translationRoot -File -Filter '*.lyx' |
    Sort-Object Name |
    ForEach-Object { $_.Name })
if ($lyxNames.Count -ne 30) {
    throw "Expected 30 admitted LyX files, found $($lyxNames.Count)."
}

$overlayInputs = [System.Collections.Generic.List[object]]::new()
if ($Mode -eq 'id-ID') {
    foreach ($name in @($lyxNames + 'preamble.tex')) {
        $from = Join-Path $translationRoot $name
        $to = Join-Path $stageRoot $name
        Copy-Item -LiteralPath $from -Destination $to -Force
        $overlayInputs.Add([pscustomobject][ordered]@{
            path = $name
            bytes = (Get-Item -LiteralPath $from).Length
            sha256 = (Get-FileHash -LiteralPath $from -Algorithm SHA256).Hash.ToLowerInvariant()
        })
    }
}

$heunFrom = Join-Path $translationRoot 'references\heun1900\00000036.png'
$heunTo = Join-Path $stageRoot 'references\heun1900\00000036.png'
if (-not (Test-Path -LiteralPath $heunFrom -PathType Leaf)) {
    throw "The admitted Heun replacement is missing: $heunFrom"
}
New-Item -ItemType Directory -Path (Split-Path -Parent $heunTo) -Force | Out-Null
Copy-Item -LiteralPath $heunFrom -Destination $heunTo -Force

function Replace-ExactRegex {
    param(
        [Parameter(Mandatory)] [string]$Text,
        [Parameter(Mandatory)] [string]$Pattern,
        [Parameter(Mandatory)] [string]$Replacement,
        [Parameter(Mandatory)] [ref]$Count
    )
    $matches = [regex]::Matches($Text, $Pattern)
    $Count.Value = $matches.Count
    return [regex]::Replace($Text, $Pattern, [System.Text.RegularExpressions.MatchEvaluator]{
        param($match)
        return $Replacement
    })
}

$transformations = [System.Collections.Generic.List[object]]::new()
$totalInput = 0
$totalMaster = 0
$totalLanguage = 0
$totalPaper = 0
$totalHeunScale = 0

foreach ($name in $lyxNames) {
    $path = Join-Path $stageRoot $name
    $before = [System.IO.File]::ReadAllText($path)
    $text = $before

    $count = 0
    $text = Replace-ExactRegex -Text $text -Pattern '(?m)^\\input \$HOME/Documents/(?:Book-Numerical|textbook)/preamble$' -Replacement '\input preamble' -Count ([ref]$count)
    $inputCount = $count
    $totalInput += $inputCount

    $count = 0
    $text = Replace-ExactRegex -Text $text -Pattern '(?m)^\\master .*TeaTimeNumericalAnalysis\.lyx$' -Replacement '\master TeaTimeNumericalAnalysis.lyx' -Count ([ref]$count)
    $masterCount = $count
    $totalMaster += $masterCount

    $count = 0
    if ($Mode -eq 'id-ID') {
        $text = Replace-ExactRegex -Text $text -Pattern '(?m)^\\language english$' -Replacement '\language bahasa' -Count ([ref]$count)
    }
    $languageCount = $count
    $totalLanguage += $languageCount

    $count = 0
    $text = Replace-ExactRegex -Text $text -Pattern '(?m)^\\papersize default$' -Replacement '\papersize letter' -Count ([ref]$count)
    $paperCount = $count
    $totalPaper += $paperCount

    $count = 0
    if ($name -eq 'ode-adaptive.lyx') {
        $text = Replace-ExactRegex -Text $text -Pattern '(?m)^\tscale 400$' -Replacement "`tscale 100" -Count ([ref]$count)
    }
    $heunScaleCount = $count
    $totalHeunScale += $heunScaleCount

    [System.IO.File]::WriteAllText($path, $text, $utf8NoBom)
    $transformations.Add([pscustomobject][ordered]@{
        path = $name
        input_preamble = $inputCount
        master_pointer = $masterCount
        language = $languageCount
        paper_size = $paperCount
        heun_scale = $heunScaleCount
        before_sha256 = [System.Convert]::ToHexString([System.Security.Cryptography.SHA256]::HashData($utf8NoBom.GetBytes($before))).ToLowerInvariant()
        after_sha256 = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
    })
}

if ($totalInput -ne 30) {
    throw "Expected 30 preamble-path rewrites, observed $totalInput."
}
if ($totalMaster -ne 29) {
    throw "Expected 29 master-pointer matches, observed $totalMaster."
}
if ($Mode -eq 'id-ID' -and $totalLanguage -ne 30) {
    throw "Expected 30 language rewrites, observed $totalLanguage."
}
if ($Mode -eq 'en-baseline' -and $totalLanguage -ne 0) {
    throw "English baseline unexpectedly rewrote language metadata."
}
if ($totalPaper -ne 30) {
    throw "Expected 30 paper-size rewrites, observed $totalPaper."
}
if ($totalHeunScale -ne 1) {
    throw "Expected one Heun replacement scale rewrite, observed $totalHeunScale."
}

$preamblePath = Join-Path $stageRoot 'preamble.tex'
$preambleBefore = [System.IO.File]::ReadAllText($preamblePath)
$graphicCount = 0
$preambleAfter = Replace-ExactRegex -Text $preambleBefore -Pattern '(?m)^\\graphicspath\{\{\$HOME/Documents/scsu/Book-Numerical/figures/\}\}$' -Replacement '\graphicspath{{figures/}}' -Count ([ref]$graphicCount)
if ($graphicCount -ne 1) {
    throw "Expected one graphics-path rewrite, observed $graphicCount."
}
$variorefLocalizationCount = 0
if ($Mode -eq 'id-ID') {
    $variorefLines = @(
        '% Indonesian reader strings for varioref; the package has Malay but no Indonesian option.'
        '\renewcommand{\reftextfaceafter}{pada \reftextvario{halaman sebelah}{halaman berikutnya}}'
        '\renewcommand{\reftextfacebefore}{pada \reftextvario{halaman sebelah}{halaman sebelumnya}}'
        '\renewcommand{\reftextafter}{pada \reftextvario{halaman berikutnya}{halaman selanjutnya}}'
        '\renewcommand{\reftextbefore}{pada \reftextvario{halaman sebelumnya}{halaman terdahulu}}'
        '\renewcommand{\reftextcurrent}{pada \reftextvario{halaman ini}{halaman sekarang}}'
        '\renewcommand{\reftextfaraway}[1]{pada halaman~\pageref{#1}}'
        '\renewcommand{\reftextpagerange}[2]{pada halaman~\pageref{#1}--\pageref{#2}}'
        '\renewcommand{\reftextlabelrange}[2]{\ref{#1}--\ref{#2}}'
    )
    $preambleAfter = $preambleAfter.TrimEnd([char]13, [char]10) + [char]10 + [char]10 + ($variorefLines -join [char]10) + [char]10
    $variorefLocalizationCount = $variorefLines.Count - 1
}
[System.IO.File]::WriteAllText($preamblePath, $preambleAfter, $utf8NoBom)

$heunHash = (Get-FileHash -LiteralPath $heunTo -Algorithm SHA256).Hash.ToLowerInvariant()
if ($heunHash -ne 'd34c3f99ae1740e9ac7f97bec473b44a3d28353ae503bda1c2bf55e4ee8999d7') {
    throw "Heun replacement hash mismatch: $heunHash"
}

$stageFiles = @(Get-ChildItem -LiteralPath $stageRoot -Recurse -File -Force |
    Sort-Object { [System.IO.Path]::GetRelativePath($stageRoot, $_.FullName).Replace('\', '/') } |
    ForEach-Object {
        [pscustomobject][ordered]@{
            path = [System.IO.Path]::GetRelativePath($stageRoot, $_.FullName).Replace('\', '/')
            bytes = $_.Length
            sha256 = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
        }
    })

$manifest = [pscustomobject][ordered]@{
    schema_id = 'ttna-portable-overlay-v1'
    recorded_date = '2026-08-22'
    mode = $Mode
    source_commit = '186882108a6da95c8dca5b81ce000fc3f8f3ca21'
    source_tree = '1e50d3756b695176008c602f0ee89712f5f32d10'
    admitted_lyx_files = $lyxNames.Count
    overlay_inputs = @($overlayInputs)
    transformations = @($transformations)
    transformation_totals = [pscustomobject][ordered]@{
        input_preamble = $totalInput
        master_pointer = $totalMaster
        language = $totalLanguage
        paper_size = $totalPaper
        graphics_path = $graphicCount
        heun_scale = $totalHeunScale
        varioref_localization = $variorefLocalizationCount
    }
    heun_replacement = [pscustomobject][ordered]@{
        path = 'references/heun1900/00000036.png'
        bytes = (Get-Item -LiteralPath $heunTo).Length
        sha256 = $heunHash
        rights_uri = 'https://creativecommons.org/publicdomain/mark/1.0/'
    }
    stage_inventory = $stageFiles
}

$json = $manifest | ConvertTo-Json -Depth 8
[System.IO.File]::WriteAllText($manifestPath, $json + "`n", $utf8NoBom)

[pscustomobject][ordered]@{
    mode = $Mode
    stage_root = $stageRoot
    stage_files = $stageFiles.Count
    stage_bytes = ($stageFiles | Measure-Object -Property bytes -Sum).Sum
    manifest_path = $manifestPath
    manifest_bytes = (Get-Item -LiteralPath $manifestPath).Length
    manifest_sha256 = (Get-FileHash -LiteralPath $manifestPath -Algorithm SHA256).Hash.ToLowerInvariant()
    master = Join-Path $stageRoot 'TeaTimeNumericalAnalysis.lyx'
} | ConvertTo-Json -Depth 4
