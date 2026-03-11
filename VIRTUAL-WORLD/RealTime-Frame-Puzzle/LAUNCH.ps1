# PowerShell launch script for RealTime-Frame-Puzzle
# Automatically activates virtual environment and runs the game

Write-Host "============================================" -ForegroundColor Cyan
Write-Host " RealTime-Frame-Puzzle Launcher" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to gesture directory
Set-Location "c:\Users\ay840\OneDrive\Desktop\gesture"

# Activate virtual environment
Write-Host "[1/2] Activating virtual environment..." -ForegroundColor Yellow
& ".venv\Scripts\Activate.ps1"

if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE) {
    Write-Host "ERROR: Failed to activate virtual environment" -ForegroundColor Red
    Write-Host "Please ensure .venv exists in c:\Users\ay840\OneDrive\Desktop\gesture\" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[2/2] Launching puzzle game..." -ForegroundColor Yellow
Write-Host ""

# Run the game
python "Gesture-Control-Interface\VIRTUAL-WORLD\RealTime-Frame-Puzzle\main.py"

# Keep window open if there's an error
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Red
    Write-Host " Program exited with an error (Code: $LASTEXITCODE)" -ForegroundColor Red
    Write-Host "============================================" -ForegroundColor Red
    Read-Host "Press Enter to exit"
}
