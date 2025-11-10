@echo off
REM TITAN SERVER - View Live Logs

color 0B
cls

echo.
echo ========================================
echo    📊 TITAN SERVER - LIVE LOGS
echo ========================================
echo.
echo Press Ctrl+C to exit (server keeps running)
echo.

cd /d "%~dp0"

docker-compose logs -f

pause

