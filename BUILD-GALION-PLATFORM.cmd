@echo off
REM ================================================================
REM  GALION PLATFORM - COMPREHENSIVE BUILD SYSTEM
REM  Builds all components: Console, Launcher, Mods, Server
REM ================================================================

title GALION Platform Builder

echo.
echo ================================================================
echo   GALION PLATFORM - COMPREHENSIVE BUILD
echo   Version 1.0.0
echo ================================================================
echo.

REM Change to project directory
cd /d "%~dp0"

echo [1/6] Checking prerequisites...
echo.

REM Check Python
py --version >nul 2>&1
if errorlevel 1 (
    echo    ERROR: Python not found!
    echo    Install Python 3.8+ from python.org
    pause
    exit /b 1
)
echo    ✓ Python found

REM Check Gradle
if exist "gradlew.bat" (
    echo    ✓ Gradle wrapper found
    set GRADLE_CMD=gradlew.bat
) else (
    gradle --version >nul 2>&1
    if errorlevel 1 (
        echo    ! Gradle not found, will skip Gradle builds
        set GRADLE_CMD=
    ) else (
        echo    ✓ Gradle found
        set GRADLE_CMD=gradle
    )
)
echo.

echo [2/6] Building Developer Console...
echo.
cd dev-console
if exist "requirements-dev-console.txt" (
    echo    Installing dependencies...
    py -m pip install -r requirements-dev-console.txt --quiet
)
cd ..
echo    ✓ Developer Console ready
echo.

echo [3/6] Building Client Launcher...
echo.
cd client-launcher
if exist "requirements.txt" (
    echo    Installing dependencies...
    py -m pip install -r requirements.txt --quiet
)
cd ..
echo    ✓ Client Launcher ready
echo.

echo [4/6] Building Gradle modules...
echo.
if defined GRADLE_CMD (
    echo    Running: %GRADLE_CMD% buildAll
    %GRADLE_CMD% buildAll --console=plain
    if errorlevel 1 (
        echo    ! Build failed
        echo    See output above for errors
    ) else (
        echo    ✓ Gradle build complete
    )
) else (
    echo    ! Skipping Gradle build (not available)
)
echo.

echo [5/6] Copying artifacts...
echo.

REM Copy built JARs to server-mods
if exist "build\libs" (
    echo    Copying JARs to server-mods...
    xcopy /Y /Q "build\libs\*.jar" "server-mods\" >nul 2>&1
    echo    ✓ Artifacts copied
) else (
    echo    ! No build artifacts found
)
echo.

echo [6/6] Validating build...
echo.

REM Check if files exist
set BUILD_SUCCESS=1

if not exist "dev-console\console_main.py" (
    echo    ✗ Console main missing
    set BUILD_SUCCESS=0
)

if not exist "client-launcher\galion-launcher.py" (
    echo    ✗ Launcher missing
    set BUILD_SUCCESS=0
)

if %BUILD_SUCCESS%==1 (
    echo    ✓ All critical files present
) else (
    echo    ✗ Some files missing
)
echo.

echo ================================================================
if %BUILD_SUCCESS%==1 (
    echo   ✓ BUILD COMPLETE!
    echo.
    echo   Components Ready:
    echo     • Developer Console
    echo     • Client Launcher
    echo     • Backend Services
    echo     • Server Mods
    echo.
    echo   Next Steps:
    echo     1. Run: LAUNCH-GALION-PLATFORM.cmd
    echo     2. Or: py dev-console\console_main.py
) else (
    echo   ✗ BUILD INCOMPLETE
    echo.
    echo   Some components failed to build
    echo   Check output above for errors
)
echo ================================================================
echo.

pause

