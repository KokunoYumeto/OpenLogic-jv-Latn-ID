[CmdletBinding()]
param(
    [ValidateRange(1, 180000)][int]$AcquireTimeoutMs = 1000,
    [string]$PreparedTree,
    [switch]$Cumulative
)

$ErrorActionPreference = 'Stop'
if ($PreparedTree) {
    $stage = (Resolve-Path -LiteralPath $PreparedTree).Path
    $inputTree = [pscustomobject]@{
        olp = Join-Path $stage 'olp'
        book = Join-Path $stage 'olp/locale/jv/courses/sets-logic-computation'
        source_units = 722
    }
} else {
    if ($Cumulative) { throw 'Cumulative mode requires the extracted source tree.' }
    $source = & python (Join-Path $PSScriptRoot 'prepare.py')
    if ($LASTEXITCODE -ne 0) { throw 'Source staging failed.' }
    $inputTree = $source | ConvertFrom-Json
    $stage = $inputTree.stage
}
$book = $inputTree.book
$jobName = if ($Cumulative) { 'slc-screen-jv' } else { 'slc-screen' }
$pdf = Join-Path $book "$jobName.pdf"
$outName = if ($Cumulative) { 'slc-screen-jv-cumulative.pdf' } else { 'slc-screen-jv.pdf' }
$out = Join-Path $PSScriptRoot $outName
$receiptFile = Join-Path $stage 'build.json'
$receipt = [ordered]@{
    status = 'not_started'
    locale_input_units = $inputTree.source_units
    localized_identifiers = $inputTree.localized_ids
    terminology_replacements = $inputTree.terminology_replacements
    commands = @()
    mutex_acquired = $false
    mutex_released = $false
}

function Invoke-SlcTool([string]$Name, [string[]]$Arguments) {
    $exe = (Get-Command $Name -CommandType Application).Source
    $sequence = $receipt.commands.Count + 1
    $log = Join-Path $stage ('{0:D2}-{1}.txt' -f $sequence, $Name)
    $code = $null
    if ($IsWindows) {
        $job = [JvWindowsTexJob]::CreateJobObject([IntPtr]::Zero, $null)
        if ($job -eq [IntPtr]::Zero) { throw 'Could not create a Windows process job.' }
        $proc = $null
        try {
            [JvWindowsTexJob]::LimitMemory($job)
            $proc = [JvWindowsTexJob]::Launch($exe, ($Arguments -join ' '), $book, $job, $log)
            $clock = [Diagnostics.Stopwatch]::StartNew()
            while (-not $proc.HasExited -or [JvWindowsTexJob]::Active($job) -gt 0) {
                if ($clock.Elapsed.TotalSeconds -gt 240) { throw "$Name exceeded four minutes." }
                Start-Sleep -Milliseconds 100
            }
            $proc.WaitForExit()
            $code = $proc.ExitCode
        } finally {
            if ([JvWindowsTexJob]::Active($job) -gt 0) {
                $null = [JvWindowsTexJob]::TerminateJobObject($job, 125)
                while ([JvWindowsTexJob]::Active($job) -gt 0) { Start-Sleep -Milliseconds 100 }
            }
            $null = [JvWindowsTexJob]::CloseHandle($job)
            if ($proc) { $proc.Dispose() }
        }
    } else {
        Push-Location -LiteralPath $book
        try {
            & $exe @Arguments *> $log
            $code = $LASTEXITCODE
        } finally {
            Pop-Location
        }
    }
    $receipt.commands += @{tool = $Name; log = (Split-Path -Leaf $log); exit_code = $code}
    if ($code -ne 0 -or $null -eq $code) { throw "$Name failed. See $log." }
}

$mutex = $null
$previousBst = $env:BSTINPUTS
$previousEpoch = $env:SOURCE_DATE_EPOCH
$previousForceDate = $env:FORCE_SOURCE_DATE
try {
    if ($IsWindows) {
        $jobSource = Join-Path $PSScriptRoot 'WindowsTexJob.cs'
        if (-not (Test-Path -LiteralPath $jobSource)) {
            $jobSource = Join-Path $PSScriptRoot '../../tools/WindowsTexJob.cs'
        }
        Add-Type -Path $jobSource
        $mutex = [Threading.Mutex]::new($false, 'Global\InterlanguageTeXSlotV1')
        try { $receipt.mutex_acquired = $mutex.WaitOne($AcquireTimeoutMs) }
        catch [Threading.AbandonedMutexException] { $receipt.mutex_acquired = $true }
        if (-not $receipt.mutex_acquired) {
            $receipt.status = 'slot_occupied'
            throw 'The TeX slot is occupied. No compiler was started.'
        }
    }

    $env:BSTINPUTS = (Join-Path $inputTree.olp 'bib') + [IO.Path]::PathSeparator
    $env:SOURCE_DATE_EPOCH = '1783832456'
    $env:FORCE_SOURCE_DATE = '1'
    $version = & pdflatex --version | Select-Object -First 1
    $platformOptions = if ($version -match 'MiKTeX') { @('--disable-installer') } else { @() }
    $texArgs = @($platformOptions) + @('-no-shell-escape','-interaction=nonstopmode',
        '-halt-on-error','-file-line-error','-recorder',"$jobName.tex")
    $bibArgs = @($platformOptions) + @($jobName)
    $indexArgs = @('-s',"$jobName.ist",'-t',"$jobName.glg",'-o',"$jobName.gls","$jobName.glo")
    Invoke-SlcTool pdflatex $texArgs
    $firstLog = Get-Content -LiteralPath (Join-Path $book "$jobName.log") -Raw
    if (($firstLog -replace '\s+', ' ') -match 'requested but not marked jv') {
        throw "A localized import was skipped. See $book/slc-screen.log."
    }
    Invoke-SlcTool bibtex $bibArgs
    Invoke-SlcTool makeindex $indexArgs
    Invoke-SlcTool pdflatex $texArgs
    Invoke-SlcTool bibtex $bibArgs
    Invoke-SlcTool makeindex $indexArgs

    $checks = @(
        'There were undefined (?:references|citations)',
        '(?:Reference|Citation) [^\r\n]{0,200} undefined',
        'Label\(s\) may have changed',
        'Rerun to get (?:cross-references|outlines) right',
        'multiply defined',
        'Token [^\r\n]{0,200} undefined',
        'requested but not marked jv',
        'Missing character:',
        'destination with the same identifier'
    )
    $warnings = @()
    for ($pass = 3; $pass -le 7; $pass++) {
        Invoke-SlcTool pdflatex $texArgs
        $texLog = Get-Content -LiteralPath (Join-Path $book "$jobName.log") -Raw
        $warnings = @($checks | Where-Object { $texLog -match $_ })
        if ($warnings.Count -eq 0) { break }
    }
    $receipt.remaining_log_checks = $warnings
    if ($warnings.Count -gt 0) { throw "Unsettled build. See $book/slc-screen.log." }
    if (-not (Test-Path -LiteralPath $pdf -PathType Leaf)) { throw 'The screen PDF is absent.' }
    $mode = @()
    if ($Cumulative) { $mode += '--cumulative' }
    $inventory = & python (Join-Path $PSScriptRoot 'check-build.py') $book @mode
    if ($LASTEXITCODE -ne 0) { throw 'Textbook content inventory did not pass.' }
    $receipt.inventory = $inventory | ConvertFrom-Json
    $boxes = @([regex]::Matches($texLog,'Overfull \\[hv]box \(([\d.]+)pt') |
        ForEach-Object { [double]$_.Groups[1].Value })
    $receipt.overfull_count = $boxes.Count
    $receipt.overfull_over_2pt = @($boxes | Where-Object { $_ -gt 2 }).Count
    $receipt.overfull_max_pt = ($boxes | Measure-Object -Maximum).Maximum
    if ($receipt.overfull_over_2pt) { throw "Boxes exceed 2 pt in $book/$jobName.log." }
    Copy-Item -LiteralPath $pdf -Destination $out
    $receipt.pdf_sha256 = (Get-FileHash -LiteralPath $out -Algorithm SHA256).Hash.ToLowerInvariant()
    $receipt.status = 'complete'
} catch {
    if ($receipt.status -ne 'slot_occupied') { $receipt.status = 'failed' }
    $receipt.error = $_.Exception.Message
    throw
} finally {
    $env:BSTINPUTS = $previousBst
    $env:SOURCE_DATE_EPOCH = $previousEpoch
    $env:FORCE_SOURCE_DATE = $previousForceDate
    if ($mutex) {
        if ($receipt.mutex_acquired) {
            $mutex.ReleaseMutex()
            $receipt.mutex_released = $true
        }
        $mutex.Dispose()
    }
    $receipt | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $receiptFile -Encoding utf8
}
Write-Output $out
