@echo off
REM Development Minecraft Console Launcher
REM Quick startup script for Windows

echo ========================================
echo   DEVELOPMENT MINECRAFT CONSOLE
echo   Galion.Studio
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import customtkinter" >nul 2>&1
if errorlevel 1 (
    echo [!] Installing dependencies...
    pip install -r requirements-dev-console.txt
)

echo.
echo [OK] Starting Development Console...
echo.

REM Start the console
python console_main.py

pause

