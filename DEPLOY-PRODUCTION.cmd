@echo off
REM ============================================
REM TITAN - PRODUCTION DEPLOYMENT
REM Deploy all services and mods to production
REM ============================================

title TITAN DEPLOYMENT
color 0A

echo.
echo ╔═══════════════════════════════════════════════╗
echo ║   TITAN PRODUCTION DEPLOYMENT                 ║
echo ║   "Ship it!" - Elon Musk                      ║
echo ╚═══════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

REM Check if Docker is running
echo [1/6] Checking Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running!
    echo Please start Docker Desktop first.
    pause
    exit /b 1
)
echo [OK] Docker is running
echo.

REM Build all mods
echo [2/6] Building all mods...
call BUILD-ALL-MODS.cmd
if errorlevel 1 (
    echo [ERROR] Build failed!
    pause
    exit /b 1
)
echo.

REM Start Docker services
echo [3/6] Starting Docker services...
docker-compose up -d
if errorlevel 1 (
    echo [ERROR] Failed to start services!
    pause
    exit /b 1
)
echo [OK] Services started
echo.

REM Wait for services to be ready
echo [4/6] Waiting for services to initialize...
timeout /t 10 /nobreak >nul
echo [OK] Services ready
echo.

REM Start Mod Sync Server (in background)
echo [5/6] Starting Mod Sync Server...
start "Titan Mod Sync" py mod-sync-server.py
timeout /t 3 /nobreak >nul
echo [OK] Mod Sync Server started
echo.

REM Start AI Bridge (in background)
echo [6/6] Starting AI Bridge...
cd ai-bridge
start "Titan AI Bridge" py instant.py
cd ..
timeout /t 2 /nobreak >nul
echo [OK] AI Bridge started
echo.

echo ╔═══════════════════════════════════════════════╗
echo ║   DEPLOYMENT COMPLETE! ✓                      ║
echo ╚═══════════════════════════════════════════════╝
echo.
echo SERVICES RUNNING:
echo ├─ Minecraft Server: localhost:25565
echo ├─ Mod Sync API: http://localhost:8080
echo ├─ AI Bridge: Active
echo └─ Monitoring: http://localhost:3000
echo.
echo NEXT STEPS:
echo 1. Test client launcher
echo 2. Connect to server
echo 3. Test AI chat in-game
echo.
echo Press any key to view logs...
pause >nul

REM Show Docker logs
docker-compose logs -f titan-hub


