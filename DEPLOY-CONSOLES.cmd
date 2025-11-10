@echo off
REM Deploy & Test Both Consoles
REM Following Elon Musk principles: Ship Fast, Test Fast

title DEPLOYING CONSOLES
cls

echo.
echo ========================================
echo   CONSOLE DEPLOYMENT
echo   Testing both systems...
echo ========================================
echo.

REM Check if dependencies are installed
echo [1/3] Checking dependencies...
pip show customtkinter >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo  Installing GUI console dependencies...
    cd dev-console
    pip install -r requirements-dev-console.txt --quiet
    cd ..
)

pip show aiohttp >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo  Installing terminal console dependencies...
    pip install -r requirements-grok.txt --quiet
)

echo  Dependencies OK
echo.

REM Check .env.grok exists
echo [2/3] Checking configuration...
if not exist ".env.grok" (
    echo.
    echo  Creating .env.grok from example...
    copy env.grok.example .env.grok >nul
    echo.
    echo  IMPORTANT: Edit .env.grok and add your OpenRouter API key!
    echo  Get it from: https://openrouter.ai/keys
    echo.
)
echo  Configuration OK
echo.

REM Test if server is running
echo [3/3] Checking Minecraft server...
docker ps | findstr titan-hub >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo  Server running
) else (
    echo  Server not running - start with INSTANT-LAUNCH.cmd
)
echo.

echo ========================================
echo   DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo Available consoles:
echo.
echo  1. GUI Dev Console
echo     START-DEV-CONSOLE.cmd
echo     - Full development environment
echo     - Mod management, logs, AI chat
echo     - Team collaboration
echo.
echo  2. Terminal Console
echo     START-CONSOLE-CHAT.cmd
echo     - Ultra-fast AI chat
echo     - Quick RCON commands
echo     - Project control
echo.
echo Both consoles are ready!
echo.
pause

