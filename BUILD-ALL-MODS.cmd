@echo off
REM ============================================
REM TITAN FORGE MODS - BUILD ALL
REM Musk-Style: Build fast, ship fast
REM ============================================

title TITAN BUILD - Building All Mods
color 0B

echo.
echo ╔═══════════════════════════════════════════╗
echo ║   TITAN FORGE MODS - COMPLETE BUILD      ║
echo ║   "The best part is no part"  - Musk     ║
echo ╚═══════════════════════════════════════════╝
echo.

REM Change to project directory
cd /d "%~dp0"

REM Step 1: Clean previous builds
echo [1/5] Cleaning previous builds...
call gradlew clean
if errorlevel 1 (
    echo [ERROR] Clean failed!
    pause
    exit /b 1
)
echo [OK] Clean complete
echo.

REM Step 2: Build Titan Common (dependency for all)
echo [2/5] Building Titan Common...
call gradlew :titan-common:build -x test
if errorlevel 1 (
    echo [ERROR] Titan Common build failed!
    pause
    exit /b 1
)
echo [OK] Titan Common built
echo.

REM Step 3: Build Titan Mod API
echo [3/5] Building Titan Mod API...
call gradlew :titan-mod-api:build -x test
if errorlevel 1 (
    echo [ERROR] Titan Mod API build failed!
    pause
    exit /b 1
)
echo [OK] Titan Mod API built
echo.

REM Step 4: Build Example Mod
echo [4/5] Building Example Mod...
call gradlew :examples:example-mod:build -x test
if errorlevel 1 (
    echo [ERROR] Example Mod build failed!
    pause
    exit /b 1
)
echo [OK] Example Mod built
echo.

REM Step 5: Collect all mods
echo [5/5] Collecting mods to server-mods directory...
if not exist server-mods mkdir server-mods

REM Copy Titan Mod API
if exist titan-mod-api\build\libs\TitanModAPI-*.jar (
    copy /Y titan-mod-api\build\libs\TitanModAPI-*.jar server-mods\
    echo [OK] Copied Titan Mod API
)

REM Copy Example Mod
if exist examples\example-mod\build\libs\TitanExampleMod-*.jar (
    copy /Y examples\example-mod\build\libs\TitanExampleMod-*.jar server-mods\
    echo [OK] Copied Example Mod
)

echo.
echo ╔═══════════════════════════════════════════╗
echo ║   BUILD COMPLETE! ✓                       ║
echo ╚═══════════════════════════════════════════╝
echo.

REM List built mods
echo Built mods in server-mods\:
dir /B server-mods\*.jar
echo.

echo.
echo NEXT STEPS:
echo 1. Review mods in server-mods\ directory
echo 2. Run: python mod-sync-server.py
echo 3. Test client launcher
echo.

pause

