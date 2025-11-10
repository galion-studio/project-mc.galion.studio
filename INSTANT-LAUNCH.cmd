@echo off
REM INSTANT LAUNCH - Super Fast Client + Server
REM Optimized for minimal startup time

REM Change to script directory
cd /d "%~dp0"

REM Start server immediately in background (no waiting)
start /MIN "" docker-compose up -d 2>nul

REM Start client immediately (using pre-built EXE for speed)
start "" "client-launcher\dist\GalionLauncher-Enhanced-Final.exe"

REM Show brief success message
cls
echo.
echo ╔════════════════════════════════════════╗
echo ║     ⚡ INSTANT LAUNCH - STARTED ⚡     ║
echo ╚════════════════════════════════════════╝
echo.
echo ✓ Server: Starting in background...
echo ✓ Client: Launched!
echo.
echo Server: localhost:25565
echo.
echo Window will close in 2 seconds...
timeout /t 2 /nobreak >nul

