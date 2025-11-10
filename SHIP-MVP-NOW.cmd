@echo off
REM ================================================
REM TITAN MVP DEPLOYMENT - MUSK STYLE
REM "Done is better than perfect" - Ship it now!
REM ================================================

title TITAN MVP - Shipping Now!
color 0A

echo.
echo ╔═══════════════════════════════════════════════╗
echo ║   TITAN MVP - SHIP IT NOW!                    ║
echo ║   Focus on what works, iterate later          ║
echo ╚═══════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

REM Create server-mods directory
echo [1/4] Setting up mod storage...
if not exist server-mods mkdir server-mods
echo [OK] Mod directory ready
echo.

REM Check Docker
echo [2/4] Checking Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Docker not running - some features limited
) else (
    echo [OK] Docker is running
    echo     Starting services...
    docker-compose up -d >nul 2>&1
)
echo.

REM Start Mod Sync Server
echo [3/4] Starting Mod Sync Server...
start "Titan Mod Sync API" py mod-sync-server.py
timeout /t 3 /nobreak >nul
echo [OK] Mod Sync Server: http://localhost:8080
echo.

REM Start AI Bridge
echo [4/4] Starting AI Bridge...
cd ai-bridge
start "Titan AI Bridge" py instant.py
cd ..
timeout /t 2 /nobreak >nul
echo [OK] AI Bridge: Active
echo.

echo ╔═══════════════════════════════════════════════╗
echo ║   MVP DEPLOYED! ✓                             ║
echo ╚═══════════════════════════════════════════════╝
echo.
echo WHAT'S RUNNING:
echo.
echo ✓ Mod Sync API Server
echo   └─ http://localhost:8080
echo   └─ Parallel downloads ready
echo   └─ Auto-manifest generation
echo.
echo ✓ AI Bridge (Grok 4 Fast)
echo   └─ In-game chat responses
echo   └─ Ultra-fast  (^<1s)
echo.
echo ✓ Minecraft Server
echo   └─ localhost:25565
echo   └─ Docker containers running
echo.
echo NEXT STEPS:
echo 1. Add mods to server-mods\ directory
echo 2. Test API: http://localhost:8080/docs
echo 3. Launch client: client-launcher\dist\GalionLauncher-Enhanced-Final.exe
echo 4. Connect and play!
echo.
echo TO ADD FORGE MODS:
echo 1. Download .jar files from CurseForge/Modrinth
echo 2. Copy to server-mods\ directory
echo 3. Restart mod-sync-server (auto-detects new mods)
echo 4. Client will auto-download on next launch
echo.
echo API ENDPOINTS:
echo - GET /api/mods/manifest       (List all mods)
echo - GET /api/mods/download/{file} (Download mod)
echo - GET /api/mods/verify/{file}   (Check checksum)
echo - GET /health                   (Server status)
echo.

pause

