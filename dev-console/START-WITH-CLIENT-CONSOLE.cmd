@echo off
REM Start Dev Console with Client Console pre-opened
REM Opens directly to the client console view

echo ============================================
echo   DEV CONSOLE with CLIENT CONSOLE
echo   mc.galion.studio
echo ============================================
echo.

REM Check if Python is available
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found!
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

REM Check for required packages
echo [INFO] Checking dependencies...
python -c "import customtkinter" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] customtkinter not installed
    echo Installing dependencies...
    pip install -r requirements-dev-console.txt
)

echo [INFO] Starting dev console...
echo.

REM Set environment variable to open client console by default
set DEVCONSOLE_DEFAULT_VIEW=client_console

REM Run the dev console
cd /d "%~dp0"
python console_main.py

echo.
echo Console closed.
pause

