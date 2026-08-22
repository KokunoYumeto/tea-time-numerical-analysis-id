[CmdletBinding()]
param(
    [ValidateSet('en-baseline', 'id-ID')]
    [string]$Mode = 'id-ID',

    [string]$LaneRoot = ''
)

$ErrorActionPreference = 'Stop'
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
$comparison = [System.StringComparison]::OrdinalIgnoreCase
$sourceDateEpoch = '1787356800'

if ([string]::IsNullOrWhiteSpace($LaneRoot)) {
    $LaneRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
}

$lane = [System.IO.Path]::GetFullPath($LaneRoot)
$overlayScript = Join-Path $lane 'build\tools\New-PortableOverlay.ps1'
$stageRoot = Join-Path $lane "build\stage\$Mode"
$overlayManifest = Join-Path $lane "build\manifests\$Mode-overlay.json"
$workBase = [System.IO.Path]::GetFullPath((Join-Path $lane 'tmp\pdfs'))
$workRoot = [System.IO.Path]::GetFullPath((Join-Path $workBase $Mode))
$logRoot = Join-Path $lane 'build\logs'
$userDir = Join-Path $lane "build\lyx-user\$Mode"
$buildManifest = Join-Path $lane "build\manifests\$Mode-build.json"
$lyx = 'C:\Program Files\LyX 2.4\bin\LyX.exe'
$cprotectRoot = Join-Path $lane 'authority\toolchain\cprotect-1.0f\package\cprotect'
$cprotectSty = Join-Path $cprotectRoot 'cprotect.sty'

foreach ($required in @($overlayScript, $lyx, $cprotectSty)) {
    if (-not (Test-Path -LiteralPath $required -PathType Leaf)) {
        throw "Required build input is missing: $required"
    }
}

$overlayResult = & $overlayScript -Mode $Mode -LaneRoot $lane | Out-String
if (-not (Test-Path -LiteralPath $overlayManifest -PathType Leaf)) {
    throw "Overlay manifest was not produced: $overlayManifest"
}

$workPrefix = $workBase.TrimEnd('\') + '\'
if (-not $workRoot.StartsWith($workPrefix, $comparison)) {
    throw "Refusing unsafe work path outside $workBase`: $workRoot"
}
if (Test-Path -LiteralPath $workRoot) {
    Remove-Item -LiteralPath $workRoot -Recurse -Force
}
New-Item -ItemType Directory -Path $workRoot,$logRoot,$userDir -Force | Out-Null

function Invoke-CapturedProcess {
    param(
        [Parameter(Mandatory)] [string]$FilePath,
        [Parameter(Mandatory)] [string[]]$Arguments,
        [Parameter(Mandatory)] [string]$WorkingDirectory,
        [Parameter(Mandatory)] [string]$StdoutPath,
        [Parameter(Mandatory)] [string]$StderrPath
    )

    $psi = [System.Diagnostics.ProcessStartInfo]::new()
    $psi.FileName = $FilePath
    $psi.WorkingDirectory = $WorkingDirectory
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.Environment['SOURCE_DATE_EPOCH'] = $sourceDateEpoch
    $psi.Environment['FORCE_SOURCE_DATE'] = '1'
    foreach ($argument in $Arguments) {
        [void]$psi.ArgumentList.Add($argument)
    }

    $process = [System.Diagnostics.Process]::Start($psi)
    $stdoutTask = $process.StandardOutput.ReadToEndAsync()
    $stderrTask = $process.StandardError.ReadToEndAsync()
    $process.WaitForExit()
    [System.IO.File]::WriteAllText($StdoutPath, $stdoutTask.Result, $utf8NoBom)
    [System.IO.File]::WriteAllText($StderrPath, $stderrTask.Result, $utf8NoBom)
    return $process.ExitCode
}

$mainBase = "TeaTimeNumericalAnalysis-$Mode"
$stageMaster = Join-Path $stageRoot 'TeaTimeNumericalAnalysis.lyx'
$mainTex = Join-Path $workRoot "$mainBase.tex"
$lyxStdout = Join-Path $logRoot "$Mode-lyx.stdout.log"
$lyxStderr = Join-Path $logRoot "$Mode-lyx.stderr.log"

$lyxExit = Invoke-CapturedProcess -FilePath $lyx -Arguments @(
    '-batch',
    '-n',
    '-userdir', $userDir,
    '-f', 'all',
    '-E', 'pdflatex', $mainTex,
    $stageMaster
) -WorkingDirectory $lane -StdoutPath $lyxStdout -StderrPath $lyxStderr

if ($lyxExit -ne 0 -or -not (Test-Path -LiteralPath $mainTex -PathType Leaf)) {
    throw "LyX LaTeX export failed with exit code $lyxExit. See $lyxStdout and $lyxStderr."
}

$exportedTexCount = @(Get-ChildItem -LiteralPath $workRoot -File -Filter '*.tex').Count
if ($exportedTexCount -ne 30) {
    throw "Expected the master plus 29 child TeX exports, found $exportedTexCount."
}

Copy-Item -LiteralPath (Join-Path $stageRoot 'preamble.tex') -Destination (Join-Path $workRoot 'preamble.tex') -Force
Copy-Item -LiteralPath $cprotectSty -Destination (Join-Path $workRoot 'cprotect.sty') -Force
foreach ($logo in @('octaveLogo.png', 'geogebraLogo.png')) {
    $from = Join-Path (Join-Path $stageRoot 'figures') $logo
    $to = Join-Path (Join-Path $workRoot 'figures') $logo
    if (-not (Test-Path -LiteralPath $from -PathType Leaf)) {
        throw "Preamble graphic is missing: $from"
    }
    Copy-Item -LiteralPath $from -Destination $to -Force
}

$inputInventory = @(Get-ChildItem -LiteralPath $workRoot -Recurse -File -Force |
    Sort-Object { [System.IO.Path]::GetRelativePath($workRoot, $_.FullName).Replace('\', '/') } |
    ForEach-Object {
        [pscustomobject][ordered]@{
            path = [System.IO.Path]::GetRelativePath($workRoot, $_.FullName).Replace('\', '/')
            bytes = $_.Length
            sha256 = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
        }
    })

$latexmkCommand = (Get-Command latexmk -ErrorAction Stop).Source
$latexmkStdout = Join-Path $logRoot "$Mode-latexmk.stdout.log"
$latexmkStderr = Join-Path $logRoot "$Mode-latexmk.stderr.log"
$latexmkExit = Invoke-CapturedProcess -FilePath $latexmkCommand -Arguments @(
    '-pdf',
    '-interaction=nonstopmode',
    '-file-line-error',
    '-halt-on-error',
    "$mainBase.tex"
) -WorkingDirectory $workRoot -StdoutPath $latexmkStdout -StderrPath $latexmkStderr

$workPdf = Join-Path $workRoot "$mainBase.pdf"
if ($latexmkExit -ne 0 -or -not (Test-Path -LiteralPath $workPdf -PathType Leaf)) {
    $tail = if (Test-Path -LiteralPath $latexmkStdout) {
        (Get-Content -LiteralPath $latexmkStdout -Tail 80) -join "`n"
    } else {
        '<no latexmk stdout>'
    }
    throw "LaTeX build failed with exit code $latexmkExit.`n$tail"
}

$finalPdf = $null
if ($Mode -eq 'id-ID') {
    $outputRoot = Join-Path $lane 'output\pdf'
    New-Item -ItemType Directory -Path $outputRoot -Force | Out-Null
    $finalPdf = Join-Path $outputRoot 'Tea-Time-Numerical-Analysis-id-ID.pdf'
    Copy-Item -LiteralPath $workPdf -Destination $finalPdf -Force
}

$pdfPath = if ($finalPdf) { $finalPdf } else { $workPdf }
$pdfInfoCommand = (Get-Command pdfinfo -ErrorAction SilentlyContinue).Source
$pageCount = $null
if ($pdfInfoCommand) {
    $info = & $pdfInfoCommand $pdfPath 2>$null
    $pageLine = $info | Where-Object { $_ -match '^Pages:\s+(\d+)' } | Select-Object -First 1
    if ($pageLine -match '^Pages:\s+(\d+)') {
        $pageCount = [int]$Matches[1]
    }
}

$manifest = [pscustomobject][ordered]@{
    schema_id = 'ttna-edition-build-v1'
    recorded_date = '2026-08-22'
    mode = $Mode
    source_date_epoch = $sourceDateEpoch
    source_commit = '186882108a6da95c8dca5b81ce000fc3f8f3ca21'
    source_tree = '1e50d3756b695176008c602f0ee89712f5f32d10'
    overlay_manifest = [pscustomobject][ordered]@{
        path = [System.IO.Path]::GetRelativePath($lane, $overlayManifest).Replace('\', '/')
        bytes = (Get-Item -LiteralPath $overlayManifest).Length
        sha256 = (Get-FileHash -LiteralPath $overlayManifest -Algorithm SHA256).Hash.ToLowerInvariant()
    }
    toolchain = [pscustomobject][ordered]@{
        lyx_product_version = (Get-Item -LiteralPath $lyx).VersionInfo.ProductVersion
        lyx_bytes = (Get-Item -LiteralPath $lyx).Length
        lyx_sha256 = (Get-FileHash -LiteralPath $lyx -Algorithm SHA256).Hash.ToLowerInvariant()
        latexmk_path = $latexmkCommand
        latexmk_sha256 = (Get-FileHash -LiteralPath $latexmkCommand -Algorithm SHA256).Hash.ToLowerInvariant()
        cprotect_sty_sha256 = (Get-FileHash -LiteralPath $cprotectSty -Algorithm SHA256).Hash.ToLowerInvariant()
    }
    lyx_export = [pscustomobject][ordered]@{
        exit_code = $lyxExit
        tex_files = $exportedTexCount
        input_files = $inputInventory.Count
        input_inventory = $inputInventory
    }
    latexmk = [pscustomobject][ordered]@{
        exit_code = $latexmkExit
        stdout_log = [System.IO.Path]::GetRelativePath($lane, $latexmkStdout).Replace('\', '/')
        stderr_log = [System.IO.Path]::GetRelativePath($lane, $latexmkStderr).Replace('\', '/')
    }
    pdf = [pscustomobject][ordered]@{
        path = [System.IO.Path]::GetRelativePath($lane, $pdfPath).Replace('\', '/')
        bytes = (Get-Item -LiteralPath $pdfPath).Length
        sha256 = (Get-FileHash -LiteralPath $pdfPath -Algorithm SHA256).Hash.ToLowerInvariant()
        pages = $pageCount
    }
}

$json = $manifest | ConvertTo-Json -Depth 8
[System.IO.File]::WriteAllText($buildManifest, $json + "`n", $utf8NoBom)

[pscustomobject][ordered]@{
    mode = $Mode
    lyx_exit_code = $lyxExit
    latexmk_exit_code = $latexmkExit
    exported_tex_files = $exportedTexCount
    closure_files = $inputInventory.Count
    pdf = $pdfPath
    pdf_bytes = (Get-Item -LiteralPath $pdfPath).Length
    pdf_sha256 = (Get-FileHash -LiteralPath $pdfPath -Algorithm SHA256).Hash.ToLowerInvariant()
    pages = $pageCount
    build_manifest = $buildManifest
    build_manifest_sha256 = (Get-FileHash -LiteralPath $buildManifest -Algorithm SHA256).Hash.ToLowerInvariant()
} | ConvertTo-Json -Depth 4
