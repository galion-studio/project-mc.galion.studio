@echo off
REM TITAN SERVER - Stop All Services

color 0C
cls

echo.
echo ========================================
echo    STOPPING TITAN SERVER
echo ========================================
echo.

cd /d "%~dp0"

echo [*] Stopping all services...
docker-compose down

if errorlevel 1 (
    echo [ERROR] Failed to stop services
    pause
    exit /b 1
)

color 0A
echo.
echo ========================================
echo    ✅ ALL SERVICES STOPPED ✅
echo ========================================
echo.
pause

