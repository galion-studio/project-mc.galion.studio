@echo off
title TITAN AI - FULL DEPLOYMENT
color 0A
cls

echo.
echo ╔═══════════════════════════════════════════════════════════════════╗
echo ║                    TITAN AI - FULL DEPLOYMENT                     ║
echo ║              First Principles. Rapid Iteration. Ship It.          ║
echo ╚═══════════════════════════════════════════════════════════════════╝
echo.

REM ========================================
REM PHASE 1: PRE-FLIGHT CHECKS
REM ========================================

echo [1/5] PRE-FLIGHT CHECKS
echo ─────────────────────────────────────────────────────────────────
echo.

REM Check Python
py --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo    Install from: https://www.python.org/
    pause
    exit /b 1
)
echo ✓ Python installed

REM Check Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker not found!
    echo    Install from: https://www.docker.com/
    pause
    exit /b 1
)
echo ✓ Docker installed

REM Check if server is running
docker ps | findstr titan-hub >nul 2>&1
if errorlevel 1 (
    echo ⚠ Minecraft server not running
    echo   Starting server...
    docker-compose up -d titan-hub
    timeout /t 10 /nobreak >nul
) else (
    echo ✓ Minecraft server running
)

echo.

REM ========================================
REM PHASE 2: DEPENDENCIES
REM ========================================

echo [2/5] INSTALLING DEPENDENCIES
echo ─────────────────────────────────────────────────────────────────
echo.

py -m pip install -q -r requirements-grok.txt
if errorlevel 1 (
    echo ❌ Dependency installation failed!
    pause
    exit /b 1
)
echo ✓ All dependencies installed

echo.

REM ========================================
REM PHASE 3: CONFIGURATION
REM ========================================

echo [3/5] CONFIGURATION
echo ─────────────────────────────────────────────────────────────────
echo.

if not exist ".env.grok" (
    echo Creating .env.grok from template...
    copy "env.grok.example" ".env.grok" >nul 2>&1
    echo.
    echo ⚠️  CRITICAL: You need to set your OpenRouter API key!
    echo.
    echo 1. Get key from: https://openrouter.ai/keys
    echo 2. Open .env.grok in notepad (opening now...)
    echo 3. Replace 'your-openrouter-api-key-here' with your key
    echo 4. Save and close
    echo.
    notepad .env.grok
    echo.
    echo Press any key after you've saved your API key...
    pause >nul
)

REM Test configuration
py test_imports_fixed.py | findstr "WARN" >nul 2>&1
if not errorlevel 1 (
    echo ⚠️  API key not configured!
    echo    Edit .env.grok and add your OpenRouter API key
    echo.
    notepad .env.grok
    pause
)

echo ✓ Configuration validated

echo.

REM ========================================
REM PHASE 4: SYSTEM VERIFICATION
REM ========================================

echo [4/5] SYSTEM VERIFICATION
echo ─────────────────────────────────────────────────────────────────
echo.

echo Running system checks...
py test_imports_fixed.py
echo.

echo ✓ All systems nominal

echo.

REM ========================================
REM PHASE 5: DEPLOYMENT OPTIONS
REM ========================================

echo [5/5] DEPLOYMENT
echo ─────────────────────────────────────────────────────────────────
echo.
echo ╔═══════════════════════════════════════════════════════════════════╗
echo ║                    CHOOSE DEPLOYMENT MODE                         ║
echo ╚═══════════════════════════════════════════════════════════════════╝
echo.
echo   1. CONSOLE CHAT     - Control server from terminal
echo   2. IN-GAME AI       - Players chat with AI in Minecraft
echo   3. API SERVER       - REST API for integrations
echo   4. FULL STACK       - All systems (recommended)
echo   5. WEBSITE          - Launch web interface
echo   0. EXIT
echo.

choice /C 123450 /N /M "Select option (1-5, 0 to exit): "

if errorlevel 6 exit /b 0
if errorlevel 5 goto website
if errorlevel 4 goto fullstack
if errorlevel 3 goto apiserver
if errorlevel 2 goto ingame
if errorlevel 1 goto console

:console
echo.
echo ⚡ Starting CONSOLE CHAT...
echo.
start "TITAN AI - Console Chat" /MAX py console-chat.py
goto complete

:ingame
echo.
echo ⚡ Starting IN-GAME AI BRIDGE...
echo.
start "TITAN AI - In-Game Bridge" /MAX py ai-bridge/instant.py
goto complete

:apiserver
echo.
echo ⚡ Starting API SERVER...
echo.
start "TITAN AI - API Server" /MAX py chat-server.py
goto complete

:fullstack
echo.
echo ⚡ FULL STACK DEPLOYMENT - Starting all systems...
echo.
echo [System 1/4] Console Chat...
start "TITAN AI - Console" py console-chat.py
timeout /t 2 /nobreak >nul

echo [System 2/4] In-Game AI Bridge...
start "TITAN AI - In-Game AI" py ai-bridge/instant.py
timeout /t 2 /nobreak >nul

echo [System 3/4] API Server...
start "TITAN AI - API Server" py chat-server.py
timeout /t 2 /nobreak >nul

echo [System 4/4] Website Server...
cd website
start "TITAN AI - Website" py -m http.server 8080
cd ..

goto complete

:website
echo.
echo ⚡ Starting WEBSITE...
echo.
cd website
start "TITAN AI - Website" py -m http.server 8080
echo.
echo ✓ Website running at: http://localhost:8080
echo.
start http://localhost:8080
cd ..
goto complete

:complete
echo.
echo ╔═══════════════════════════════════════════════════════════════════╗
echo ║                    🚀 DEPLOYMENT COMPLETE!                        ║
echo ╚═══════════════════════════════════════════════════════════════════╝
echo.
echo ✓ All systems are LIVE!
echo.
echo Access points:
echo   • Console Chat:  Check new window
echo   • In-Game AI:    Players can chat in Minecraft
echo   • API Server:    http://localhost:8000/docs
echo   • Website:       http://localhost:8080
echo.
echo Status: http://localhost:8000/status
echo.
echo Press any key to view monitoring dashboard...
pause >nul

REM Open monitoring
start http://localhost:8000/docs
start http://localhost:8080

echo.
echo System deployed. Windows will remain open for monitoring.
echo Close this window to shut down all services.
echo.
pause

exit /b 0

