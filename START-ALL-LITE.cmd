@echo off
REM ============================================
REM TITAN - START LITE MODE (No Docker Required)
REM Starts services that work without Docker
REM ============================================

title TITAN - Lite Mode
color 0B

echo.
echo ╔═══════════════════════════════════════════════╗
echo ║   TITAN LITE MODE - QUICK START               ║
echo ║   Starting available services...              ║
echo ╚═══════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

REM Step 1: Check what's needed
echo [1/4] Checking system...

REM Check Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo [INFO] Docker not available - will skip Minecraft server
    set DOCKER_AVAILABLE=0
) else (
    echo [OK] Docker is available
    set DOCKER_AVAILABLE=1
)
echo.

REM Step 2: Start Mod Sync Server
echo [2/4] Starting Mod Sync Server...
if not exist server-mods mkdir server-mods
start "Titan Mod Sync API" py mod-sync-server.py
timeout /t 4 /nobreak >nul
echo [OK] Mod Sync Server starting on port 8080
echo.

REM Step 3: Start AI Bridge
echo [3/4] Starting AI Bridge...
cd ai-bridge
start "Titan AI Bridge" py instant.py
cd ..
timeout /t 3 /nobreak >nul
echo [OK] AI Bridge starting
echo.

REM Step 4: Start Docker (if available)
if %DOCKER_AVAILABLE%==1 (
    echo [4/4] Starting Docker services...
    docker-compose up -d
    if errorlevel 1 (
        echo [WARNING] Docker start failed - check Docker Desktop
    ) else (
        echo [OK] Docker services started
    )
) else (
    echo [4/4] Skipping Docker services (not available)
)
echo.

REM Wait for services to initialize
echo Waiting for services to initialize...
timeout /t 5 /nobreak >nul
echo.

REM Test services
echo ╔═══════════════════════════════════════════════╗
echo ║   SERVICES STATUS                             ║
echo ╚═══════════════════════════════════════════════╝
echo.

REM Test Mod Sync API
echo Testing Mod Sync API...
powershell -Command "try { $r = Invoke-WebRequest -Uri 'http://localhost:8080/health' -UseBasicParsing -TimeoutSec 3; Write-Host '[OK] Mod Sync API is responding'; Write-Host '     ' $r.Content } catch { Write-Host '[WAIT] Mod Sync API starting...' }"
echo.

REM Check Docker
if %DOCKER_AVAILABLE%==1 (
    echo Docker containers:
    docker ps --format "table {{.Names}}\t{{.Status}}" | findstr "titan" 2>nul
    if errorlevel 1 (
        echo [INFO] No Titan containers running yet
    )
)
echo.

echo ╔═══════════════════════════════════════════════╗
echo ║   READY TO USE! ✓                             ║
echo ╚═══════════════════════════════════════════════╝
echo.
echo AVAILABLE SERVICES:
echo.
echo ✓ Mod Sync API
echo   └─ http://localhost:8080
echo   └─ API Docs: http://localhost:8080/docs
echo   └─ Test: Invoke-WebRequest http://localhost:8080/health
echo.
echo ✓ AI Bridge (Grok 4 Fast)
echo   └─ Monitoring in-game chat
echo   └─ Responds to: "console", "@ai", "hey"
echo.

if %DOCKER_AVAILABLE%==1 (
    echo ✓ Minecraft Server
    echo   └─ localhost:25565
    echo   └─ View logs: docker logs -f titan-hub
    echo.
) else (
    echo ⚠ Minecraft Server (Docker Required)
    echo   └─ Start Docker Desktop to enable
    echo   └─ Then run: docker-compose up -d
    echo.
)

echo.
echo NEXT STEPS:
echo 1. Add mods to server-mods\ directory
echo 2. Test API: http://localhost:8080/docs
echo 3. Launch client: client-launcher\dist\GalionLauncher-Enhanced-Final.exe
echo.
echo TO START DOCKER:
echo 1. Open Docker Desktop
echo 2. Wait for it to start
echo 3. Run: docker-compose up -d
echo.

pause

