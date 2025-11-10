@echo off
REM Fix Minecraft installation and launch
color 0B
cls

echo ========================================
echo   FIXING MINECRAFT INSTALLATION
echo ========================================
echo.
echo This will:
echo 1. Download Minecraft 1.21.1 files
echo 2. Install all required libraries
echo 3. Launch Minecraft
echo.
echo This may take 2-5 minutes...
echo.
pause

cd /d "%~dp0"

echo.
echo [*] Starting installation...
py fix-minecraft-install.py

if errorlevel 1 (
    color 0C
    echo.
    echo [ERROR] Installation failed!
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   SUCCESS! LAUNCHING MINECRAFT
echo ========================================
echo.
pause

