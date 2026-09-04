param([int]$Passes = 3, [string]$BuildName = 'tex-sets', [string]$ReferencePdf = '', [int]$AcquireTimeoutMs = 30000)
$ErrorActionPreference = 'Stop'
if ($AcquireTimeoutMs -lt 1 -or $AcquireTimeoutMs -gt 60000) { throw 'Mutex timeout must be between 1 and 60000 milliseconds' }
$taskRepo = Split-Path -Parent $PSScriptRoot
$taskState = Join-Path $taskRepo '.build'
if ($BuildName -notmatch '^tex-sets(?:-[a-z0-9]+)?$') { throw 'Invalid task build directory name' }
$taskBuild = Join-Path (Join-Path $taskState 'work') $BuildName
if ($ReferencePdf) {
    $taskReferenceResolved = [IO.Path]::GetFullPath($ReferencePdf)
    if (-not $taskReferenceResolved.StartsWith((Join-Path $taskState 'work') + '\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Reference PDF must be in this task work directory' }
    if (-not (Test-Path -LiteralPath $taskReferenceResolved)) { throw 'Reference PDF is absent' }
    if ((Test-Path -LiteralPath $taskBuild) -and (Get-ChildItem -LiteralPath $taskBuild -Force | Select-Object -First 1)) { throw 'A reproducibility replay requires an empty build directory' }
}
$taskEdition = Join-Path $taskRepo 'edition'
New-Item -ItemType Directory -Force -Path $taskBuild | Out-Null
$taskProfilePath = [Environment]::GetFolderPath('UserProfile')
Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
using System.Diagnostics;
using System.ComponentModel;
public static class JvTexJob {
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode)] public static extern IntPtr CreateJobObject(IntPtr attrs,string name);
 [DllImport("kernel32.dll",SetLastError=true)] public static extern bool AssignProcessToJobObject(IntPtr job,IntPtr process);
 [DllImport("kernel32.dll")] public static extern bool TerminateJobObject(IntPtr job,uint code);
 [DllImport("kernel32.dll")] public static extern bool CloseHandle(IntPtr h);
 [StructLayout(LayoutKind.Sequential)] public struct Accounting {
 public long a,b,c,d; public uint faults,total,active,terminated;
 }
 [DllImport("kernel32.dll",SetLastError=true)] public static extern bool QueryInformationJobObject(IntPtr job,int info,out Accounting data,uint size,IntPtr ret);
 public static uint Active(IntPtr job) {
 Accounting a;
 if(!QueryInformationJobObject(job,1,out a,(uint)Marshal.SizeOf(typeof(Accounting)),IntPtr.Zero)) throw new Exception("Job accounting unavailable");
 return a.active;
 }
 [StructLayout(LayoutKind.Sequential)] public struct Security { public int length; public IntPtr descriptor; public int inherit; }
 [StructLayout(LayoutKind.Sequential,CharSet=CharSet.Unicode)] public struct Startup {
 public int cb; public string reserved,desktop,title; public uint x,y,xSize,ySize,xChars,yChars,fill,flags;
 public ushort show,reserved2; public IntPtr reservedPtr,input,output,error;
 }
 [StructLayout(LayoutKind.Sequential)] public struct ProcessInfo { public IntPtr process,thread; public uint pid,tid; }
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)] static extern IntPtr CreateFile(string name,uint access,uint share,ref Security security,uint disposition,uint attributes,IntPtr template);
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)] static extern bool CreateProcess(string application,System.Text.StringBuilder command,IntPtr pa,IntPtr ta,bool inherit,uint flags,IntPtr environment,string directory,ref Startup startup,out ProcessInfo info);
 [DllImport("kernel32.dll",SetLastError=true)] static extern uint ResumeThread(IntPtr thread);
 [DllImport("kernel32.dll")] static extern bool TerminateProcess(IntPtr process,uint code);
 [DllImport("kernel32.dll")] static extern uint WaitForSingleObject(IntPtr handle,uint milliseconds);
 public static Process Launch(string exe,string args,string cwd,IntPtr job,string outputFile) {
 Security sa=new Security{length=Marshal.SizeOf(typeof(Security)),inherit=1};
 IntPtr output=CreateFile(outputFile,0x40000000,1,ref sa,2,0,IntPtr.Zero);
 if(output==new IntPtr(-1)) throw new Win32Exception(Marshal.GetLastWin32Error());
 ProcessInfo pi=new ProcessInfo();
 try {
 Startup si=new Startup{cb=Marshal.SizeOf(typeof(Startup)),flags=0x100,output=output,error=output,input=IntPtr.Zero};
 var command=new System.Text.StringBuilder("\""+exe+"\" "+args);
 if(!CreateProcess(exe,command,IntPtr.Zero,IntPtr.Zero,true,0x08000004,IntPtr.Zero,cwd,ref si,out pi)) throw new Win32Exception(Marshal.GetLastWin32Error());
 if(!AssignProcessToJobObject(job,pi.process)) {
 int err=Marshal.GetLastWin32Error();TerminateProcess(pi.process,125);WaitForSingleObject(pi.process,10000);
 throw new Win32Exception(err,"Suspended TeX process was not captured; it never ran.");
 }
 var process=Process.GetProcessById((int)pi.pid);
 var retainedHandle=process.Handle;
 if(ResumeThread(pi.thread)==0xffffffff) {
 TerminateJobObject(job,125);WaitForSingleObject(pi.process,10000);process.Dispose();
 throw new Win32Exception(Marshal.GetLastWin32Error(),"Could not resume captured TeX process");
 }
 return process;
 } finally {
 CloseHandle(output);
 if(pi.thread!=IntPtr.Zero) CloseHandle(pi.thread);
 if(pi.process!=IntPtr.Zero) CloseHandle(pi.process);
 }
 }
}
'@
$taskMutex = [System.Threading.Mutex]::new($false, 'Global\InterlanguageTeXSlotV1')
$taskAcquired = $false
$taskAbandoned = $false
$taskReceipt = [ordered]@{schema='jv-tex-build/1';utc=[DateTime]::UtcNow.ToString('o');mutex='Global\InterlanguageTeXSlotV1';timeout_ms=$AcquireTimeoutMs;acquired=$false;abandoned_recovery=$false;passes=@();status='not_started';tex_started=$false}
try {
    try { $taskAcquired = $taskMutex.WaitOne($AcquireTimeoutMs) }
    catch [System.Threading.AbandonedMutexException] { $taskAcquired=$true; $taskAbandoned=$true }
    $taskReceipt.acquired=$taskAcquired
    $taskReceipt.abandoned_recovery=$taskAbandoned
    if (-not $taskAcquired) {
        $taskReceipt.status='slot_occupied'
    } else {
        $taskTexExe=(Get-Command pdflatex -ErrorAction Stop).Source
        $taskBibExe=(Get-Command bibtex -ErrorAction Stop).Source
        $taskOperations=@('tex','bib') + @(2..$Passes | ForEach-Object {'tex'})
        for ($taskPass=1; $taskPass -le $taskOperations.Count; $taskPass++) {
            $taskKind=$taskOperations[$taskPass-1]
            $taskJob=[JvTexJob]::CreateJobObject([IntPtr]::Zero,$null)
            if ($taskJob -eq [IntPtr]::Zero) { throw 'Could not create captured process job' }
            $taskProcess=$null
            try {
                if ($taskKind -eq 'tex') {
                    $taskExe=$taskTexExe
                    $taskWorkingDirectory=$taskEdition
                    $taskArguments='--disable-installer -no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -recorder -output-directory="' + $taskBuild + '" jv-sets.tex'
                } else {
                    $taskExe=$taskBibExe
                    $taskWorkingDirectory=$taskBuild
                    $taskArguments='--disable-installer jv-sets'
                }
                $taskOldBib=$env:BIBINPUTS
                $taskOldBst=$env:BSTINPUTS
                $taskOutputPath=Join-Path $taskBuild "pass-$taskPass.txt"
                try {
                    $env:BIBINPUTS=(Join-Path $taskRepo 'upstream\bib') + ';'
                    $env:BSTINPUTS=(Join-Path $taskRepo 'upstream\bib') + ';'
                    $taskProcess=[JvTexJob]::Launch($taskExe,$taskArguments,$taskWorkingDirectory,$taskJob,$taskOutputPath)
                } finally {
                    $env:BIBINPUTS=$taskOldBib
                    $env:BSTINPUTS=$taskOldBst
                }
                $taskReceipt.tex_started=$true
                $taskClock=[Diagnostics.Stopwatch]::StartNew()
                while (-not $taskProcess.HasExited -or [JvTexJob]::Active($taskJob) -gt 0) {
                    if ($taskClock.Elapsed.TotalSeconds -gt 180) {
                        $null=[JvTexJob]::TerminateJobObject($taskJob,124)
                        $taskProcess.WaitForExit()
                        while ([JvTexJob]::Active($taskJob) -gt 0) { Start-Sleep -Milliseconds 100 }
                        throw 'Captured TeX process tree exceeded 180 seconds'
                    }
                    Start-Sleep -Milliseconds 100
                }
                $taskProcess.WaitForExit()
                $taskOutput=[IO.File]::ReadAllText($taskOutputPath).Replace($taskProfilePath,'[PROFILE]').Replace($taskProfilePath.Replace('\','/'),'[PROFILE]')
                [IO.File]::WriteAllText($taskOutputPath,$taskOutput)
                foreach ($taskLogName in @('jv-sets.log','jv-sets.fls','jv-sets.blg')) {
                    $taskLogPath=Join-Path $taskBuild $taskLogName
                    if (Test-Path -LiteralPath $taskLogPath) {
                        $taskLogText=[IO.File]::ReadAllText($taskLogPath).Replace($taskProfilePath,'[PROFILE]').Replace($taskProfilePath.Replace('\','/'),'[PROFILE]')
                        [IO.File]::WriteAllText($taskLogPath,$taskLogText)
                    }
                }
                $taskExitCode=$taskProcess.ExitCode
                if ($null -eq $taskExitCode) { throw 'Captured process exited but no exit code was available; build not accepted' }
                $taskEntry=[ordered]@{pass=$taskPass;kind=$taskKind;exit_code=$taskExitCode;seconds=[math]::Round($taskClock.Elapsed.TotalSeconds,2);captured_active_processes=[JvTexJob]::Active($taskJob)}
                $taskReceipt.passes+=,$taskEntry
                if ($taskProcess.ExitCode -ne 0) {
                    $taskReceipt.status='tex_error'
                    $taskReceipt.error_excerpt=($taskOutput -split "\r?\n" | Select-Object -Last 18) -join [Environment]::NewLine
                    break
                }
                $taskReceipt.status='passes_complete'
            } finally {
                if ($taskJob -ne [IntPtr]::Zero) {
                    if ([JvTexJob]::Active($taskJob) -gt 0) {
                        $null=[JvTexJob]::TerminateJobObject($taskJob,125)
                        while ([JvTexJob]::Active($taskJob) -gt 0) { Start-Sleep -Milliseconds 100 }
                    }
                    $null=[JvTexJob]::CloseHandle($taskJob)
                }
                if ($null -ne $taskProcess) { $taskProcess.Dispose() }
            }
        }
        $taskLog=Join-Path $taskBuild 'jv-sets.log'
        if (Test-Path -LiteralPath $taskLog) {
            $taskLogData=Get-Content -LiteralPath $taskLog -Raw
            $taskReceipt.log_checks=[ordered]@{undefined_references=([regex]::Matches($taskLogData,'(?:Reference .* undefined|There were undefined references)').Count);missing_characters=([regex]::Matches($taskLogData,'Missing character:').Count);overfull_boxes=([regex]::Matches($taskLogData,'Overfull \\[hv]box').Count);errors=([regex]::Matches($taskLogData,'(?m)^!|LaTeX Error:|Undefined control sequence|Fatal error occurred').Count)}
        }
        $taskPdf=Join-Path $taskBuild 'jv-sets.pdf'
        if (Test-Path -LiteralPath $taskPdf) {
            $taskReceipt.pdf=[ordered]@{filename='jv-sets.pdf';bytes=(Get-Item -LiteralPath $taskPdf).Length;sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $taskPdf).Hash.ToLowerInvariant()}
            if ($ReferencePdf) {
                $taskReferenceHash=(Get-FileHash -Algorithm SHA256 -LiteralPath $taskReferenceResolved).Hash.ToLowerInvariant()
                $taskReceipt.reproducibility=[ordered]@{reference_sha256=$taskReferenceHash;replay_sha256=$taskReceipt.pdf.sha256;identical=($taskReferenceHash -eq $taskReceipt.pdf.sha256);fresh_build_directory=$BuildName;compared_while_mutex_held=$true}
                if (-not $taskReceipt.reproducibility.identical) { $taskReceipt.status='reproducibility_mismatch' }
            }
        }
    }
} catch {
    $taskReceipt.status='operational_error'
    $taskReceipt.error=$_.Exception.Message.Replace($taskProfilePath,'[PROFILE]')
} finally {
    $taskReceipt.finished_utc=[DateTime]::UtcNow.ToString('o')
    if ($taskAcquired) { $taskMutex.ReleaseMutex() }
    $taskMutex.Dispose()
    $taskReceipt.mutex_released=$taskAcquired
    $taskReceipt | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $taskState 'BUILD_SETS.json') -Encoding utf8
}
$taskReceipt | ConvertTo-Json -Depth 8
