@echo off
echo ============================================
echo EXACT ERROR FINDER
echo ============================================
echo.

cd /d "%~dp0"

REM Check if venv exists
if exist "..\..\..\..\.venv\Scripts\python.exe" (
    set PYTHON="..\..\..\..\.venv\Scripts\python.exe"
    echo Using virtual environment Python
) else (
    set PYTHON=python
    echo Using system Python
)
echo.

echo ============================================
echo STEP 1: Running diagnostic checks...
echo ============================================
%PYTHON% find_error.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [FAILED] Diagnostic checks failed!
    echo Fix the issues above before running main.py
    pause
    exit /b 1
)
echo.
echo.

echo ============================================
echo STEP 2: Running main.py...
echo ============================================
echo If it fails, you'll see the EXACT error below:
echo.
echo Press Ctrl+C to stop anytime
timeout /t 2 >nul
echo.

REM Run main.py and capture ALL output
%PYTHON% main.py 2>&1
set EXITCODE=%ERRORLEVEL%

echo.
echo ============================================
if %EXITCODE% EQU 0 (
    echo Program exited normally
) else (
    echo.
    echo [ERROR] Program failed with exit code: %EXITCODE%
    echo.
    echo SCROLL UP to see the error message!
    echo Copy the FULL error and send it to debug.
    echo.
)
echo ============================================
pause
