@echo off
REM TITAN SERVER - Quick Restart

color 0E
cls

echo.
echo ========================================
echo    🔄 RESTARTING TITAN SERVER
echo ========================================
echo.

cd /d "%~dp0"

echo [*] Restarting services...
docker-compose restart

if errorlevel 1 (
    color 0C
    echo [ERROR] Failed to restart
    pause
    exit /b 1
)

color 0A
echo.
echo ✅ Server restarted!
echo.
timeout /t 5 /nobreak >nul

echo Showing logs...
echo.
docker-compose logs --tail=50

pause

