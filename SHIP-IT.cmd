@echo off
:: SHIP IT - One Command To Rule Them All
:: Elon Musk style: Simple. Fast. Works.

title SHIP IT
cls

echo.
echo ========================================
echo   GALION - SHIP IT
echo ========================================
echo.
echo Following Elon's principles:
echo  1. Delete unnecessary parts
echo  2. Simplify  
echo  3. Ship fast
echo.

:: Check if Docker is installed
docker --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker not found!
    echo Install Docker Desktop: https://docker.com/get-started
    pause
    exit /b 1
)

:: Start Docker server
echo [1/4] Starting Minecraft Server (1.21.1)...
docker-compose up -d
if %ERRORLEVEL% EQU 0 (
    echo      [OK] Server started
) else (
    echo      [WARN] Server might already be running
)

:: Wait for server to initialize
echo      Waiting for server to initialize...
timeout /t 5 /nobreak >nul

:: Start web control panel
echo.
echo [2/4] Starting Web Control Panel...
start "" /B py web-control-panel\server.py
timeout /t 2 /nobreak >nul
echo      [OK] Control panel starting...

:: Start client launcher (with Grok AI)
echo.
echo [3/4] Starting Client Launcher (Grok AI Integrated)...
if exist "client-launcher\dist\GalionLauncher.exe" (
    start "" "client-launcher\dist\GalionLauncher.exe"
    echo      [OK] Launcher started
) else if exist "client-launcher\quick-launcher.py" (
    start "" /B py client-launcher\quick-launcher.py
    echo      [OK] Launcher started (Python - with Grok AI)
) else (
    echo      [SKIP] Launcher not built yet
    echo      Run BUILD-AND-SHIP.cmd to build it
)

:: Open control panel in browser
echo.
echo [4/4] Opening control panel...
timeout /t 2 /nobreak >nul
start "" http://localhost:8080
echo      [OK] Opening in browser...

echo.
echo ========================================
echo   READY TO GO!
echo ========================================
echo.
echo Web Control Panel: http://localhost:8080
echo Server Address: mc.galion.studio:25565
echo Minecraft Version: 1.21.1
echo.
echo What's running:
echo  - Minecraft Server (Docker)
echo  - Web Control Panel (Port 8080)
echo  - Client Launcher (GUI)
echo.
echo "The best part is no part." - Elon Musk
echo.
echo Press any key to exit this window...
pause >nul

