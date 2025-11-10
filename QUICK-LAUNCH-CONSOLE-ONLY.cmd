@echo off
REM ================================================================
REM  ⚡ QUICK LAUNCH - Console Only
REM  Fast launch of just the Transparent Console
REM ================================================================

echo.
echo ================================================================
echo   ⚡ QUICK LAUNCH - TRANSPARENT CONSOLE
echo ================================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Install from python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo 🚀 Launching Transparent Console...
echo.

cd dev-console
python transparent_console.py

pause

