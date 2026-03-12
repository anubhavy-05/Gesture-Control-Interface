@echo off
REM Diagnostic script to check why main.py won't run
echo ============================================
echo DIAGNOSTIC - RealTime Frame Puzzle
echo ============================================
echo.

REM Change to correct directory
cd /d "%~dp0"
echo [1/5] Current directory: %CD%
echo.

REM Check if venv exists
echo [2/5] Checking virtual environment...
if exist "..\..\..\..\.venv\Scripts\python.exe" (
    echo ✓ Virtual environment found
    set PYTHON="..\..\..\..\.venv\Scripts\python.exe"
) else (
    echo ✗ Virtual environment NOT found, using system Python
    set PYTHON=python
)
echo.

REM Check Python version
echo [3/5] Checking Python version...
%PYTHON% --version
echo.

REM Check if main.py exists
echo [4/5] Checking main.py...
if exist "main.py" (
    echo ✓ main.py found
) else (
    echo ✗ main.py NOT found!
    pause
    exit /b 1
)
echo.

REM Try to compile (syntax check)
echo [5/5] Checking syntax...
%PYTHON% -m py_compile main.py
if %ERRORLEVEL% EQU 0 (
    echo ✓ Syntax check passed!
) else (
    echo ✗ SYNTAX ERROR FOUND!
    echo.
    echo ============================================
    echo DIAGNOSIS: Syntax error in main.py
    echo ============================================
    pause
    exit /b 1
)
echo.

REM Try to run
echo ============================================
echo All checks passed! Attempting to run...
echo ============================================
echo.
echo Press Ctrl+C to stop anytime
echo.
%PYTHON% main.py 2>&1
echo.

REM Show exit code
echo.
echo ============================================
if %ERRORLEVEL% EQU 0 (
    echo Program exited successfully
) else (
    echo Program exited with error code: %ERRORLEVEL%
)
echo ============================================
pause
