@echo off
REM Launch script for RealTime-Frame-Puzzle with hand tracking
REM This script automatically activates the virtual environment

echo ============================================
echo  RealTime-Frame-Puzzle Launcher
echo ============================================
echo.

REM Navigate to the gesture directory
cd /d "c:\Users\ay840\OneDrive\Desktop\gesture"

REM Activate virtual environment
echo [1/2] Activating virtual environment...
call ".venv\Scripts\activate.bat"

if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    echo Please ensure .venv exists in c:\Users\ay840\OneDrive\Desktop\gesture\
    pause
    exit /b 1
)

echo [2/2] Launching puzzle game...
echo.
python "Gesture-Control-Interface\VIRTUAL-WORLD\RealTime-Frame-Puzzle\main.py"

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ============================================
    echo  Program exited with an error
    echo ============================================
    pause
)
