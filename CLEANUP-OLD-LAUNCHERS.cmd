@echo off
REM Cleanup Old Launch Scripts
REM Removes obsolete slow launchers, keeps new optimized ones

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║  CLEANUP OLD LAUNCH SCRIPTS                           ║
echo ║  Removing obsolete launchers...                       ║
echo ╚════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo Removing old server launch scripts...
echo.

REM Old server launchers (replaced by ULTRA-FAST-LAUNCH.cmd)
if exist "START-SERVER.cmd" (
    echo [X] Removing: START-SERVER.cmd
    del /F "START-SERVER.cmd"
)

if exist "START-NEW-SYSTEM.cmd" (
    echo [X] Removing: START-NEW-SYSTEM.cmd
    del /F "START-NEW-SYSTEM.cmd"
)

if exist "START-ALL-LITE.cmd" (
    echo [X] Removing: START-ALL-LITE.cmd
    del /F "START-ALL-LITE.cmd"
)

if exist "START-LOCAL.cmd" (
    echo [X] Removing: START-LOCAL.cmd
    del /F "START-LOCAL.cmd"
)

if exist "START-LOCAL-SERVER.cmd" (
    echo [X] Removing: START-LOCAL-SERVER.cmd
    del /F "START-LOCAL-SERVER.cmd"
)

if exist "START-OFFICIAL-SERVER.cmd" (
    echo [X] Removing: START-OFFICIAL-SERVER.cmd
    del /F "START-OFFICIAL-SERVER.cmd"
)

REM Old deployment scripts
if exist "DEPLOY-NOW.cmd" (
    echo [X] Removing: DEPLOY-NOW.cmd
    del /F "DEPLOY-NOW.cmd"
)

if exist "DEPLOY-TITAN.cmd" (
    echo [X] Removing: DEPLOY-TITAN.cmd
    del /F "DEPLOY-TITAN.cmd"
)

if exist "SHIP-MVP-NOW.cmd" (
    echo [X] Removing: SHIP-MVP-NOW.cmd
    del /F "SHIP-MVP-NOW.cmd"
)

REM Old utility scripts
if exist "SIMPLE-START.cmd" (
    echo [X] Removing: SIMPLE-START.cmd
    del /F "SIMPLE-START.cmd"
)

if exist "RELOAD-ALL-SERVICES.cmd" (
    echo [X] Removing: RELOAD-ALL-SERVICES.cmd
    del /F "RELOAD-ALL-SERVICES.cmd"
)

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║  CLEANUP COMPLETE!                                     ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo Old slow launchers removed.
echo.
echo NEW OPTIMIZED LAUNCHERS:
echo ✓ ULTRA-FAST-LAUNCH.cmd        - Fastest (^<1 sec)
echo ✓ START-HERE-FAST.cmd          - Smart launcher
echo ✓ INSTANT-LAUNCH.cmd            - EXE-based
echo.
echo KEPT (Specialized tools):
echo ✓ START-GROK-BRIDGE.cmd         - AI assistant
echo ✓ START-CHAT-SERVER.cmd         - Chat server
echo ✓ START-AI-BRIDGE.cmd           - AI bridge
echo ✓ START-BUG-LOGGER.cmd          - Bug logger
echo.
pause

