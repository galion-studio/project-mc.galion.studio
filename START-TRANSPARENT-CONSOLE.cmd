@echo off
REM Transparent Developer Console Launcher
REM Full configuration visibility and control

echo ================================================
echo   TRANSPARENT DEVELOPER CONSOLE
echo   Full Configuration Visibility
echo   mc.galion.studio
echo ================================================
echo.

REM Check Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

REM Install requirements if needed
if not exist "venv" (
    echo Installing Python dependencies...
    pip install -r requirements.txt
    echo.
)

REM Launch console
echo Starting Transparent Console...
echo.

cd dev-console
python transparent_console.py

pause

