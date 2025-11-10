@echo off
REM Quick status check for all Titan services

title TITAN - Status Check
color 0F

echo.
echo ╔═══════════════════════════════════════════════╗
echo ║   TITAN SERVICES - STATUS CHECK               ║
echo ╚═══════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo [1] Checking Mod Sync API (Port 8080)...
netstat -ano | findstr ":8080.*LISTENING" >nul 2>&1
if errorlevel 1 (
    echo     ❌ NOT RUNNING
) else (
    echo     ✓ RUNNING
    powershell -Command "try { $r = Invoke-WebRequest -Uri 'http://localhost:8080/health' -UseBasicParsing -TimeoutSec 2; Write-Host '     Response:' $r.Content } catch { Write-Host '     (Port open but not responding)' }" 2>nul
)
echo.

echo [2] Checking AI Bridge...
tasklist | findstr /I "py.exe python.exe" >nul 2>&1
if errorlevel 1 (
    echo     ❌ NOT RUNNING
) else (
    echo     ✓ RUNNING (Python process detected)
)
echo.

echo [3] Checking Docker Services...
docker ps >nul 2>&1
if errorlevel 1 (
    echo     ❌ Docker Desktop not running
) else (
    echo     ✓ Docker Desktop running
    echo.
    echo     Titan Containers:
    docker ps --format "table {{.Names}}\t{{.Status}}" | findstr "titan"
    if errorlevel 1 (
        echo     (No Titan containers found)
    )
)
echo.

echo [4] Checking Minecraft Server (Port 25565)...
netstat -ano | findstr ":25565.*LISTENING" >nul 2>&1
if errorlevel 1 (
    echo     ❌ NOT LISTENING
) else (
    echo     ✓ LISTENING on port 25565
)
echo.

echo ═══════════════════════════════════════════════
echo.
echo SUMMARY:
echo.
echo To start services:    START-ALL-LITE.cmd
echo To reload everything: RELOAD-ALL-SERVICES.cmd
echo To deploy full stack: SHIP-MVP-NOW.cmd
echo.
echo API Documentation: http://localhost:8080/docs
echo.

pause

