@echo off
REM ⚡ ONE-CLICK FAST LAUNCH ⚡
REM Double-click this file to start playing!

title FAST LAUNCH

REM Go to project directory
cd /d "%~dp0"

REM Simple ASCII art (fast render)
cls
echo.
echo  ========================================
echo       FAST LAUNCH - Starting...
echo  ========================================
echo.

REM Start server (background, quiet)
start /MIN cmd /c docker-compose -f docker-compose.fast.yml up -d 2^>nul

REM Launch client (using fastest method available)
cd client-launcher

REM Try pre-built EXE first (fastest)
if exist "dist\GalionLauncher-Enhanced-Final.exe" (
    echo  [1/2] Launching client ^(EXE^)...
    start "" "dist\GalionLauncher-Enhanced-Final.exe"
    goto :launched
)

REM Try instant launcher (fast)
if exist "instant-launcher.py" (
    echo  [1/2] Launching client ^(Instant^)...
    start "" python instant-launcher.py
    goto :launched
)

REM Fallback to quick launcher
echo  [1/2] Launching client ^(Quick^)...
start "" python quick-launcher.py

:launched
cd ..
echo  [2/2] Server starting...
echo.
echo  ========================================
echo   ✓ READY TO PLAY!
echo  ========================================
echo.
echo   Server: localhost:25565
echo   Status: Starting (ready in ~10 sec)
echo.
echo   Window closes in 2 seconds...
echo  ========================================
timeout /t 2 /nobreak >nul

