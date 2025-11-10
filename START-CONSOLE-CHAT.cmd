@echo off
title GROK CONSOLE CHAT - mc.galion.studio
color 0B
cls

echo.
echo =========================================================
echo   ⚡ GROK CONSOLE CHAT
echo   Ultra-fast AI chat + Minecraft server control
echo =========================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python not found!
    echo.
    echo Please install Python 3.8+ from: https://www.python.org/
    echo.
    pause
    exit /b 1
)

REM Check if .env.grok exists
if not exist ".env.grok" (
    echo ⚠️  WARNING: .env.grok not found!
    echo.
    echo Creating from example...
    copy ".env.grok.example" ".env.grok" >nul 2>&1
    echo.
    echo ✓ Created .env.grok
    echo.
    echo 📝 IMPORTANT: Edit .env.grok and set your XAI_API_KEY
    echo    Get your API key from: https://console.x.ai/
    echo.
    pause
)

REM Install dependencies if needed
if not exist "venv" (
    echo 📦 Installing dependencies...
    echo.
    pip install -r requirements-grok.txt
    echo.
    echo ✓ Dependencies installed
    echo.
)

REM Run the console chat
echo 🚀 Starting console chat...
echo.

python console-chat.py

if errorlevel 1 (
    echo.
    echo ❌ Console chat exited with an error!
    echo.
    pause
)

