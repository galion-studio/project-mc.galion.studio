@echo off
REM Start Client Console (standalone mode)
REM Quick access to AI chat and RCON control

echo ============================================
echo   CLIENT CONSOLE - mc.galion.studio
echo   Interactive AI and Server Control
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

REM Check if .env.grok exists
if not exist ".env.grok" (
    echo [WARNING] .env.grok not found!
    echo Copy env.grok.example to .env.grok and add your API key
    echo.
    echo Press any key to continue anyway...
    pause >nul
)

echo [INFO] Starting client console...
echo.

REM Run the standalone console
cd /d "%~dp0"
python console-chat.py

echo.
echo Console closed.
pause

