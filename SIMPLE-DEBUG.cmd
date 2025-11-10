@echo off
REM Simple Debug - Show what's wrong

title TITAN DEBUG
color 0E
cls

echo.
echo ========================================
echo    SIMPLE DEBUG
echo ========================================
echo.

echo [1] Checking Docker...
docker ps --filter "name=titan-hub" --format "{{.Names}} - {{.Status}}"
echo.

echo [2] Checking if server is ready...
docker exec titan-hub rcon-cli "list"
echo.

echo [3] Recent server logs (last 20 lines)...
docker logs titan-hub --tail=20
echo.

echo [4] Testing RCON directly...
docker exec titan-hub rcon-cli "say [DEBUG] If you see this, RCON works!"
echo.

echo ========================================
echo.
pause

