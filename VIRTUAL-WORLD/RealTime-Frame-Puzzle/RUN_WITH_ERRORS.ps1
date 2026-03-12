# ERROR FINDER - PowerShell Version
# Shows EXACT error messages

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "ERROR FINDER - Puzzle Game Diagnostic" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

Write-Host "[INFO] Directory: $scriptPath" -ForegroundColor Yellow
Write-Host ""

# Check for virtual environment
$venvPath = Resolve-Path "..\..\..\..\.venv\Scripts\python.exe" -ErrorAction SilentlyContinue
if ($venvPath) {
    Write-Host "[VENV] Using virtual environment" -ForegroundColor Green
    $python = $venvPath
} else {
    Write-Host "[SYSTEM] Using system Python" -ForegroundColor Yellow
    $python = "python"
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "STEP 1: Running Diagnostics" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

& $python "find_error.py"
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Red
    Write-Host "[FAILED] Diagnostic checks failed!" -ForegroundColor Red
    Write-Host "============================================" -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "STEP 2: Running main.py" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[INFO] If program fails, error will show below" -ForegroundColor Yellow
Write-Host "[INFO] Press Ctrl+C to stop anytime" -ForegroundColor Yellow
Write-Host ""

Start-Sleep -Seconds 1

# Run main.py and capture all output
Write-Host "Starting program..." -ForegroundColor Green
Write-Host ""

try {
    & $python "main.py" 2>&1 | Tee-Object -Variable output
    $exitCode = $LASTEXITCODE
    
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Cyan
    if ($exitCode -eq 0) {
        Write-Host "[SUCCESS] Program exited normally" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Program failed with exit code: $exitCode" -ForegroundColor Red
        Write-Host ""
        Write-Host "SCROLL UP to see the full error!" -ForegroundColor Yellow
        Write-Host "Copy the complete error message for debugging" -ForegroundColor Yellow
    }
    Write-Host "============================================" -ForegroundColor Cyan
} catch {
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Red
    Write-Host "[EXCEPTION] An error occurred:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host $_.ScriptStackTrace -ForegroundColor Yellow
    Write-Host "============================================" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"
