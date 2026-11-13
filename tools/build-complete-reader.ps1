[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$Edition,
    [Parameter(Mandatory)][string]$Output,
    [ValidatePattern('^[a-zA-Z0-9_-]+$')][string]$JobName = 'jv-complete',
    [ValidateRange(1,180000)][int]$AcquireTimeoutMs = 1000,
    [ValidateRange(3,12)][int]$MaxPasses = 8
)
$ErrorActionPreference = 'Stop'
$Edition = (Resolve-Path -LiteralPath $Edition).Path
$Output = [IO.Path]::GetFullPath($Output)
[IO.Directory]::CreateDirectory($Output) | Out-Null
if (Get-ChildItem -LiteralPath $Output -Force | Select-Object -First 1) { throw 'Use a new, empty output directory.' }
if (-not (Test-Path -LiteralPath (Join-Path $Edition "$JobName.tex") -PathType Leaf)) { throw 'Missing reader source.' }
Add-Type -Path (Join-Path $PSScriptRoot 'WindowsTexJob.cs')
$mutex = [Threading.Mutex]::new($false, 'Global\InterlanguageTeXSlotV1')
$receipt = [ordered]@{status='pending'; acquired=$false; released=$false; memory_limit_bytes=5GB; commands=@()}
$oldBib, $oldBst, $oldEpoch, $oldDate = $env:BIBINPUTS, $env:BSTINPUTS, $env:SOURCE_DATE_EPOCH, $env:FORCE_SOURCE_DATE

function Run-TeXTool([string]$Name, [string]$Arguments, [string]$Directory) {
    $exe = (Get-Command $Name -CommandType Application).Source
    $sequence = $receipt.commands.Count + 1
    $log = Join-Path $Output ('{0:d2}-{1}.txt' -f $sequence,$Name)
    $job = [JvWindowsTexJob]::CreateJobObject([IntPtr]::Zero,$null)
    if ($job -eq [IntPtr]::Zero) { throw 'Could not create Windows process job.' }
    $process = $null
    try {
        [JvWindowsTexJob]::LimitMemory($job)
        $process = [JvWindowsTexJob]::Launch($exe,$Arguments,$Directory,$job,$log)
        $clock = [Diagnostics.Stopwatch]::StartNew()
        while (-not $process.HasExited -or [JvWindowsTexJob]::Active($job) -ne 0) {
            if ($clock.Elapsed.TotalSeconds -gt 300) { throw "$Name exceeded five minutes." }
            Start-Sleep -Milliseconds 100
        }
        $process.WaitForExit()
        $receipt.commands += @{tool=$Name; exit_code=$process.ExitCode}
        if ($process.ExitCode -ne 0) { throw "$Name failed. See $log." }
    } finally {
        if ([JvWindowsTexJob]::Active($job) -ne 0) {
            $null = [JvWindowsTexJob]::TerminateJobObject($job,125)
            while ([JvWindowsTexJob]::Active($job) -ne 0) { Start-Sleep -Milliseconds 100 }
        }
        $null = [JvWindowsTexJob]::CloseHandle($job)
        if ($process) { $process.Dispose() }
    }
}
try {
    try { $receipt.acquired=$mutex.WaitOne($AcquireTimeoutMs) }
    catch [Threading.AbandonedMutexException] { $receipt.acquired=$true }
    if (-not $receipt.acquired) {
        $receipt.status='slot_occupied'
        throw 'TeX slot occupied.'
    }
    $bibFolder = Join-Path (Split-Path -Parent $Edition) 'upstream/bib'
    $env:BIBINPUTS = "$Edition;$bibFolder;"
    $env:BSTINPUTS = "$bibFolder;"
    $env:SOURCE_DATE_EPOCH = '1794528000'
    $env:FORCE_SOURCE_DATE = '1'
    $engine = (Get-Command pdflatex -CommandType Application).Source
    $miktex = if ((& $engine --version | Select-Object -First 1) -match 'MiKTeX') {'--disable-installer '} else {''}
    $texArgs = $miktex + '-no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -recorder -output-directory="' + $Output + '" ' + $JobName + '.tex'
    $bibArgs = $miktex + $JobName
    $log = Join-Path $Output "$JobName.log"
    for ($pass=1; $pass -le $MaxPasses; $pass++) {
        Run-TeXTool pdflatex $texArgs $Edition
        if ($pass -le 2) { Run-TeXTool bibtex $bibArgs $Output; continue }
        $text = Get-Content -LiteralPath $log -Raw
        $unsettled = '(?i)undefined (references|citations)|(?:Reference|Citation) [^\r\n]{0,200} undefined|Label\(s\) may have changed|Rerun to get (cross-references|outlines) right|multiply defined|Missing character:|requested but not marked jv|Token [^\r\n]{0,200} undefined|destination with the same identifier'
        if (($text -replace '\r?\n',' ') -notmatch $unsettled) { break }
    }
    if ($pass -gt $MaxPasses) { throw "References or glyphs failed validation in $log." }
    $boxes = @([regex]::Matches($text,'Overfull \\[hv]box \(([\d.]+)pt') | ForEach-Object { [double]$_.Groups[1].Value })
    $receipt.overfull_count = $boxes.Count
    $receipt.overfull_over_2pt = @($boxes | Where-Object { $_ -gt 2 }).Count
    $receipt.overfull_max_pt = ($boxes | Measure-Object -Maximum).Maximum
    if ($receipt.overfull_over_2pt) { throw "Boxes exceed 2 pt in $log." }
    $pdf = Join-Path $Output "$JobName.pdf"
    $receipt.pdf_sha256=(Get-FileHash -LiteralPath $pdf -Algorithm SHA256).Hash.ToLowerInvariant()
    $receipt.status='complete'
    Write-Output $pdf
} catch {
    if ($receipt.status -ne 'slot_occupied') { $receipt.status='failed' }
    $receipt.error=$_.Exception.Message
    throw
} finally {
    $env:BIBINPUTS,$env:BSTINPUTS,$env:SOURCE_DATE_EPOCH,$env:FORCE_SOURCE_DATE=$oldBib,$oldBst,$oldEpoch,$oldDate
    if ($receipt.acquired) {
        $mutex.ReleaseMutex()
        $receipt.released=$true
    }
    $mutex.Dispose()
    $receipt | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $Output 'build.json') -Encoding utf8
}
