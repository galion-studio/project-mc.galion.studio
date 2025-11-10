@echo off
REM ================================================================
REM  🚀 RESTART AND RUN ALL - Master Launcher
REM  Stops everything, installs deps, launches all services
REM  mc.galion.studio - Full System Launch
REM ================================================================

echo.
echo ================================================================
echo   🚀 MASTER LAUNCHER - RESTART AND RUN ALL
echo   mc.galion.studio - Full System Startup
echo ================================================================
echo.

REM Step 1: Stop any running processes
echo [1/5] 🛑 Stopping any running services...
echo.

taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM pythonw.exe /T >nul 2>&1
echo    ✅ Python processes stopped

timeout /t 2 /nobreak >nul

REM Step 2: Check Python installation
echo.
echo [2/5] 🐍 Checking Python installation...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo    ❌ ERROR: Python is not installed!
    echo    📥 Please install Python 3.8+ from python.org
    echo.
    pause
    exit /b 1
)

python --version
echo    ✅ Python is installed

REM Step 3: Install/Update dependencies
echo.
echo [3/5] 📦 Installing/Updating dependencies...
echo.

python -m pip install --upgrade pip >nul 2>&1
echo    ✅ pip updated

pip install -r requirements.txt
echo    ✅ Dependencies installed

REM Step 4: Validate configuration
echo.
echo [4/5] 🔧 Validating configuration...
echo.

cd dev-console
python config_manager.py
cd ..

REM Step 5: Launch services
echo.
echo [5/5] 🚀 Launching all services...
echo.

echo Starting services in background...

REM Launch Transparent Console (main GUI)
start "Transparent Console" cmd /c "cd dev-console && python transparent_console.py"
echo    ✅ Transparent Console launched

timeout /t 2 /nobreak >nul

REM Launch Chat Server (if you want AI features)
start "Chat Server" cmd /c "python chat-server.py"
echo    ✅ Chat Server launched

timeout /t 1 /nobreak >nul

REM Launch AI Bridge (optional)
if exist "ai-bridge" (
    start "AI Bridge" cmd /c "cd ai-bridge && python bridge.py"
    echo    ✅ AI Bridge launched
)

echo.
echo ================================================================
echo   ✅ ALL SERVICES LAUNCHED!
echo ================================================================
echo.
echo   Running Services:
echo   • Transparent Console (GUI)
echo   • Chat Server (Port 8000)
echo   • AI Bridge (if available)
echo.
echo   📝 Quick Access:
echo   • Transparent Console - Check the GUI window
echo   • Chat: http://localhost:8000
echo   • Logs: VIEW-LOGS.cmd
echo.
echo   🛑 To stop all: STOP-ALL-SERVICES.cmd
echo.
echo ================================================================
echo.

REM Keep window open
echo Press any key to close this launcher window...
echo (Services will continue running in background)
pause >nul

