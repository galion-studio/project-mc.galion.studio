@echo off
REM Start the new Titan Client-Server System

color 0B
cls

echo.
echo ============================================================
echo   TITAN CUSTOM MINECRAFT SYSTEM
echo   Client-Server Architecture with Mod Sync
echo ============================================================
echo.

echo This will start:
echo 1. Mod Sync Server (API for mods)
echo 2. Minecraft Server (if not running)
echo 3. New Titan Launcher (client)
echo.
pause

echo.
echo [1/3] Starting Mod Sync Server...
start "Mod Sync Server" cmd /k "python mod-sync-server.py"

timeout /t 3 /nobreak >nul

echo [2/3] Checking Minecraft Server...
docker-compose ps titan-hub | findstr "Up" >nul
if errorlevel 1 (
    echo Starting Minecraft Server...
    docker-compose up -d titan-hub
) else (
    echo Minecraft Server already running!
)

timeout /t 3 /nobreak >nul

echo [3/3] Starting Titan Launcher...
cd client-launcher
start "Titan Launcher" cmd /k "python titan-launcher.py"

echo.
echo ============================================================
echo   ALL SYSTEMS STARTED!
echo ============================================================
echo.
echo Mod Sync API: http://localhost:8080
echo Minecraft Server: localhost:25565
echo.
echo Check the Titan Launcher window!
echo.
pause

