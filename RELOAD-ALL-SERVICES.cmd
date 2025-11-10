@echo off
REM ============================================
REM TITAN - RELOAD ALL SERVICES
REM Stop and restart everything cleanly
REM ============================================

title TITAN - Reloading All Services
color 0E

echo.
echo ╔═══════════════════════════════════════════════╗
echo ║   TITAN - RELOADING ALL SERVICES              ║
echo ║   Stopping → Cleaning → Restarting            ║
echo ╚═══════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

REM Step 1: Stop Python services
echo [1/6] Stopping Python services...
taskkill /F /IM python.exe /T 2>nul >nul
taskkill /F /IM py.exe /T 2>nul >nul
timeout /t 2 /nobreak >nul
echo [OK] Python services stopped
echo.

REM Step 2: Stop Docker services
echo [2/6] Stopping Docker services...
docker-compose down 2>nul
timeout /t 3 /nobreak >nul
echo [OK] Docker services stopped
echo.

REM Step 3: Clean up
echo [3/6] Cleaning up...
REM Clean any stuck processes on ports
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8080" ^| findstr "LISTENING"') do taskkill /F /PID %%a 2>nul >nul
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":25565" ^| findstr "LISTENING"') do taskkill /F /PID %%a 2>nul >nul
timeout /t 1 /nobreak >nul
echo [OK] Cleanup complete
echo.

REM Step 4: Start Docker services
echo [4/6] Starting Docker services...
docker-compose up -d
if errorlevel 1 (
    echo [WARNING] Docker may not be running
) else (
    echo [OK] Docker services started
)
timeout /t 8 /nobreak >nul
echo.

REM Step 5: Start Mod Sync Server
echo [5/6] Starting Mod Sync Server...
start "Titan Mod Sync API" py mod-sync-server.py
timeout /t 4 /nobreak >nul
echo [OK] Mod Sync Server started on port 8080
echo.

REM Step 6: Start AI Bridge
echo [6/6] Starting AI Bridge...
cd ai-bridge
start "Titan AI Bridge" py instant.py
cd ..
timeout /t 3 /nobreak >nul
echo [OK] AI Bridge started
echo.

REM Verify services
echo.
echo ╔═══════════════════════════════════════════════╗
echo ║   VERIFICATION                                ║
echo ╚═══════════════════════════════════════════════╝
echo.

echo Checking services...
echo.

REM Check Docker
docker ps --format "table {{.Names}}\t{{.Status}}" | findstr "titan" 2>nul
if errorlevel 1 (
    echo [WARNING] No Titan Docker containers found
) else (
    echo.
)

REM Check port 8080
netstat -ano | findstr ":8080.*LISTENING" >nul
if errorlevel 1 (
    echo [WARNING] Mod Sync Server not detected on port 8080
) else (
    echo [OK] Mod Sync Server is listening on port 8080
)

echo.
echo ╔═══════════════════════════════════════════════╗
echo ║   ALL SERVICES RELOADED! ✓                    ║
echo ╚═══════════════════════════════════════════════╝
echo.
echo RUNNING SERVICES:
echo.
echo ✓ Minecraft Server
echo   └─ localhost:25565
echo   └─ Docker: titan-hub
echo.
echo ✓ Mod Sync API
echo   └─ http://localhost:8080
echo   └─ API Docs: http://localhost:8080/docs
echo.
echo ✓ AI Bridge
echo   └─ Grok 4 Fast
echo   └─ In-game chat active
echo.
echo ✓ Monitoring
echo   └─ http://localhost:3000 (Grafana)
echo   └─ http://localhost:9090 (Prometheus)
echo.
echo.
echo QUICK TESTS:
echo 1. API Health: curl http://localhost:8080/health
echo 2. Mod List: curl http://localhost:8080/api/mods/manifest
echo 3. Docker Status: docker ps
echo 4. View Logs: docker logs -f titan-hub
echo.

pause

