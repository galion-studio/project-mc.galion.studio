@echo off
REM ============================================
REM TITAN SERVER - Windows Quick Start
REM Double-click this file to start server
REM ============================================

color 0A
title TITAN SERVER - Starting...

echo.
echo ========================================
echo    TITAN SERVER - Quick Start
echo    MC.GALION.STUDIO
echo ========================================
echo.

REM Check if Docker is running
echo [1/4] Checking Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running!
    echo Please start Docker Desktop first.
    pause
    exit /b 1
)
echo [OK] Docker is running
echo.

REM Navigate to project directory
echo [2/4] Navigating to project...
cd /d "%~dp0"
echo [OK] In project directory: %CD%
echo.

REM Build project (optional, can skip for faster start)
echo [3/4] Building project...
if exist gradlew.bat (
    echo Building Titan modules...
    call gradlew.bat build -x test
    echo [OK] Build complete
) else (
    echo [SKIP] Gradle wrapper not found, skipping build
)
echo.

REM Start Docker Compose
echo [4/4] Starting Titan services...
echo.
echo Starting:
echo   - PostgreSQL (Database)
echo   - Redis (Cache)
echo   - Minecraft Hub Server
echo   - Minecraft Survival Server
echo   - Prometheus (Metrics)
echo   - Grafana (Monitoring)
echo.

docker-compose up -d

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start services!
    echo Check if ports are already in use.
    pause
    exit /b 1
)

echo.
echo ========================================
echo    SERVICES STARTED!
echo ========================================
echo.
echo Waiting for services to initialize...
timeout /t 10 /nobreak >nul

REM Check status
echo.
echo Service Status:
docker-compose ps
echo.

echo ========================================
echo    TITAN SERVER IS RUNNING!
echo ========================================
echo.
echo Connect to server:
echo   Minecraft: localhost:25565
echo.
echo Monitoring:
echo   Grafana:    http://localhost:3000
echo   Prometheus: http://localhost:9090
echo.
echo View logs:
echo   docker-compose logs -f
echo.
echo Stop server:
echo   docker-compose down
echo.
echo ========================================
echo.
echo Opening log viewer...
timeout /t 2 /nobreak >nul

REM Show logs in this window
echo.
echo === LIVE LOGS (Press Ctrl+C to stop viewing) ===
echo.
docker-compose logs -f

REM This runs after Ctrl+C
echo.
echo.
echo ========================================
echo Logs closed. Server is still running!
echo ========================================
echo.
pause

