@echo off
:: START ALL - Silent Mode
:: Launches everything without visible console windows

:: Start Minecraft server (if not running)
docker ps | findstr titan-hub >nul 2>&1
if not %ERRORLEVEL% EQU 0 (
    start /MIN docker-compose up -d
)

:: Start client launcher
if exist "client-launcher\dist\GalionLauncher-Enhanced-Final.exe" (
    start "" /MIN "client-launcher\dist\GalionLauncher-Enhanced-Final.exe"
)

:: Start GUI developer console (no console window)
start /B pythonw dev-console\console_main.py

:: Start terminal console (no console window)
start /B pythonw console-chat.py

:: Exit immediately without showing anything
exit

