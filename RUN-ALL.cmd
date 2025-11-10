@echo off
REM RUN ALL - Start Everything at Once
REM Server + Client + Both Consoles

title LAUNCHING EVERYTHING
cls

echo.
echo ==========================================
echo   STARTING ALL SYSTEMS
echo ==========================================
echo.

REM Check server
echo [1/4] Checking Minecraft server...
docker ps | findstr titan-hub >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo  [OK] Server already running
) else (
    echo  [!] Starting server...
    start /MIN docker-compose up -d
    timeout /t 3 /nobreak >nul
)
echo.

REM Start client launcher
echo [2/4] Starting Minecraft client launcher...
if exist "client-launcher\dist\GalionLauncher-Enhanced-Final.exe" (
    start "" "client-launcher\dist\GalionLauncher-Enhanced-Final.exe"
    echo  [OK] Client launcher started
) else (
    echo  [!] Client launcher not found
)
echo.

REM Start GUI dev console
echo [3/4] Starting GUI Developer Console...
start "Dev Console - Grok 4 Fast" py dev-console\console_main.py
echo  [OK] GUI console starting...
echo.

REM Start terminal console
echo [4/4] Starting Terminal Console...
start "Terminal Console - Grok" py console-chat.py
echo  [OK] Terminal console starting...
echo.

echo ==========================================
echo   ALL SYSTEMS LAUNCHED!
echo ==========================================
echo.
echo Windows opening:
echo  - Minecraft Client Launcher
echo  - GUI Developer Console
echo  - Terminal Console Chat
echo.
echo Server: localhost:25565
echo.
echo Next: Add your OpenRouter API key to .env.grok
echo Get FREE key: https://openrouter.ai/keys
echo.
timeout /t 5 /nobreak

