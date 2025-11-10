@echo off
REM ULTRA FAST LAUNCH - Maximum Speed Edition
REM Launches client + server with ZERO delays
REM Uses all optimizations: fast docker-compose, instant launcher, parallel execution

REM Change to script directory
cd /d "%~dp0"

REM Clear screen for speed
cls

REM Show quick splash
echo.
echo   ⚡⚡⚡ ULTRA FAST LAUNCH ⚡⚡⚡
echo.

REM Launch server with fast config (background, no output)
start /B docker-compose -f docker-compose.fast.yml up -d >nul 2>&1

REM Launch client instantly (parallel execution)
cd client-launcher
start /B "" py quick-launcher.py

REM Quick success message
cd ..
echo   ✓ Server starting...
echo   ✓ Client launched!
echo.
echo   Ready in seconds!

REM Auto-close in 1 second
timeout /t 1 /nobreak >nul
exit

