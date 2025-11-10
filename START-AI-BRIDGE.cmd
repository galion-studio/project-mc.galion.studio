@echo off
REM Start Titan AI Bridge - Ultra Fast Edition

color 0B
cls

echo.
echo ========================================
echo    ⚡ STARTING AI BRIDGE ⚡
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo [✓] Python found
echo.

REM Install dependencies (if needed)
echo [*] Installing dependencies...
pip install requests >nul 2>&1

echo [✓] Dependencies ready
echo.

REM Start bridge
echo [*] Starting AI bridge...
echo.
echo ========================================
echo    🤖 AI BRIDGE RUNNING
echo ========================================
echo.
echo Monitoring Minecraft chat...
echo Type 'console <question>' in game!
echo.
echo Press Ctrl+C to stop
echo ========================================
echo.

python ai-bridge\nano-bridge.py

pause

