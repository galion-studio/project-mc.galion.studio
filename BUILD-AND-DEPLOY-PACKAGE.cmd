@echo off
REM ============================================
REM BUILD COMPLETE MINECRAFT 1.21.1 PACKAGE
REM Creates ready-to-use .minecraft with all mods
REM ============================================

title TITAN - Building Minecraft Package
color 0B

echo.
echo ╔═══════════════════════════════════════════════╗
echo ║   TITAN MINECRAFT 1.21.1 PACKAGE BUILDER      ║
echo ║   Musk Style: One package with everything    ║
echo ╚═══════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

REM Step 1: Check Python
echo [1/4] Checking Python...
py --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    pause
    exit /b 1
)
echo [OK] Python is available
echo.

REM Step 2: Check for mods
echo [2/4] Checking for mods...
if not exist server-mods\ (
    mkdir server-mods
    echo [WARNING] No mods found in server-mods\
    echo           Add .jar files there first!
    echo.
    echo QUICK START:
    echo 1. Download Forge 1.21.1 mods from CurseForge
    echo 2. Copy .jar files to server-mods\
    echo 3. Run this script again
    echo.
    pause
    exit /b 1
)

set /a MOD_COUNT=0
for %%f in (server-mods\*.jar) do set /a MOD_COUNT+=1

echo [OK] Found %MOD_COUNT% mods
echo.

REM Step 3: Build package
echo [3/4] Building complete package...
echo This may take a few minutes...
echo.
py build-minecraft-package.py

if errorlevel 1 (
    echo [ERROR] Package build failed!
    pause
    exit /b 1
)

echo.
echo [OK] Package built successfully
echo.

REM Step 4: Restart mod-sync-server
echo [4/4] Restarting mod-sync-server...
taskkill /F /IM py.exe /FI "WINDOWTITLE eq Titan Mod Sync*" >nul 2>&1
timeout /t 2 /nobreak >nul
start "Titan Mod Sync API" py mod-sync-server.py
timeout /t 4 /nobreak >nul
echo [OK] Server restarted
echo.

echo ╔═══════════════════════════════════════════════╗
echo ║   PACKAGE BUILD COMPLETE! ✓                   ║
echo ╚═══════════════════════════════════════════════╝
echo.

REM Check if package exists
for %%f in (minecraft-packages\*.zip) do (
    set PACKAGE_FILE=%%~nxf
    set PACKAGE_SIZE=%%~zf
)

if defined PACKAGE_FILE (
    echo Package: %PACKAGE_FILE%
    set /a SIZE_MB=%PACKAGE_SIZE% / 1048576
    echo Size: %SIZE_MB% MB
    echo Location: minecraft-packages\
    echo.
    echo DOWNLOAD URL:
    echo http://localhost:8080/api/packages/download/%PACKAGE_FILE%
    echo.
    echo API ENDPOINTS:
    echo - List packages: http://localhost:8080/api/packages/list
    echo - Package info: http://localhost:8080/api/packages/info/[name]
    echo.
)

echo WHAT PLAYERS NEED TO DO:
echo 1. Download package from URL above
echo 2. Extract ZIP file
echo 3. Run INSTALL.cmd
echo 4. Play!
echo.
echo Setup time: ^<2 minutes (vs 5-7 minutes with mods)
echo.

pause

