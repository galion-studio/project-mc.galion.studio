@echo off
:: GALION - Complete System Launcher
:: Simple. Fast. Works.

title GALION Launcher
cls

echo.
echo ==========================================
echo   GALION - Minecraft 1.21.1
echo ==========================================
echo.
echo Starting all services...
echo.

:: 1. Start Minecraft Server
echo [1/4] Starting Minecraft Server...
docker-compose up -d >nul 2>&1
timeout /t 3 /nobreak >nul
echo      [OK] Server starting

:: 2. Start Web Control Panel
echo.
echo [2/4] Starting Web Control Panel...
start /B "" py web-control-panel\server.py
timeout /t 2 /nobreak >nul
echo      [OK] Control panel starting

:: 3. Start GALION Client Launcher (Grok AI Integrated)
echo.
echo [3/4] Starting GALION Launcher (with Grok AI)...
start "" py client-launcher\galion-launcher.py
timeout /t 1 /nobreak >nul
echo      [OK] GALION Launcher started

:: 4. Open browser
echo.
echo [4/4] Opening Control Panel...
timeout /t 2 /nobreak >nul
start http://localhost:8080
echo      [OK] Browser opened

echo.
echo ==========================================
echo   ALL SYSTEMS RUNNING!
echo ==========================================
echo.
echo [LAUNCHER] GALION Custom Client Launcher (Grok AI)
echo [WEB] Control Panel: http://localhost:8080
echo [SERVER] mc.galion.studio:25565
echo [CLIENT] Custom GALION Engine
echo.
echo Features:
echo  - Grok 4 Fast AI Assistant
echo  - Transparent download tracking
echo  - One-click play
echo  - Auto mod sync
echo.
echo Close this window anytime.
echo.
pause

