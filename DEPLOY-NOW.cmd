@echo off
REM DEPLOY - Musk Style: One command, everything works

color 0A
cls

echo.
echo ============================================================
echo   DEPLOYING TITAN SYSTEM NOW
echo   Musk Principle: Ship it, then iterate
echo ============================================================
echo.

REM Step 1: Create mods directory
if not exist "server-mods" mkdir server-mods

REM Step 2: Start Minecraft server
echo [1/3] Starting Minecraft Server...
docker-compose up -d titan-hub
timeout /t 2 /nobreak >nul

REM Step 3: Start mod server
echo [2/3] Starting Mod Server...
start "Mod Server" /MIN cmd /c "python simple-mod-server.py"
timeout /t 2 /nobreak >nul

REM Step 4: Launch client
echo [3/3] Launching Client...
cd client-launcher
start "Titan Launcher" py quick-launcher.py

cd ..
echo.
echo ============================================================
echo   DEPLOYED!
echo ============================================================
echo.
echo Minecraft Server: localhost:25565
echo Mod Server: http://localhost:8080
echo Client: Launcher window opening...
echo.
echo First launch takes 5-10 minutes to download everything.
echo After that, instant launch!
echo.
echo Add mods: Drop JAR files in server-mods/ folder
echo.
pause

