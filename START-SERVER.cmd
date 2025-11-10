@echo off
REM TITAN SERVER - Ultra Quick Start
REM Double-click to start server instantly

color 0B
cls

echo.
echo      ████████╗██╗████████╗ █████╗ ███╗   ██╗
echo      ╚══██╔══╝██║╚══██╔══╝██╔══██╗████╗  ██║
echo         ██║   ██║   ██║   ███████║██╔██╗ ██║
echo         ██║   ██║   ██║   ██╔══██║██║╚██╗██║
echo         ██║   ██║   ██║   ██║  ██║██║ ╚████║
echo         ╚═╝   ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝
echo.
echo      MC.GALION.STUDIO - Quick Start
echo.
echo ========================================
echo.

cd /d "%~dp0"

REM Start services
echo [*] Starting Titan services...
docker-compose up -d

if errorlevel 1 (
    color 0C
    echo.
    echo [ERROR] Failed to start!
    echo.
    echo Make sure Docker Desktop is running.
    pause
    exit /b 1
)

echo.
echo [OK] Services started!
echo.
timeout /t 5 /nobreak >nul

color 0A
cls

echo.
echo ═══════════════════════════════════════
echo    ✅ TITAN SERVER IS RUNNING! ✅
echo ═══════════════════════════════════════
echo.
echo 🎮 CONNECT:
echo    localhost:25565
echo.
echo 📊 MONITORING:
echo    http://localhost:3000 (Grafana)
echo.
echo 📝 VIEW LOGS:
echo    Press any key...
echo.
echo ═══════════════════════════════════════
echo.
pause >nul

REM Show logs
cls
echo.
echo === LIVE MINECRAFT LOGS ===
echo (Press Ctrl+C to exit, server keeps running)
echo.
docker-compose logs -f titan-hub

pause

