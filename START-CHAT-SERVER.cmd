@echo off
title GROK CHAT SERVER - API
color 0B
cls

echo.
echo =========================================================
echo   ⚡ GROK CHAT SERVER - FastAPI
echo   REST API for AI chat and server control
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
    exit /b 1
)

REM Install dependencies if needed
echo 📦 Checking dependencies...
pip install -q -r requirements-grok.txt

REM Run the chat server
echo.
echo 🚀 Starting Chat Server...
echo.
echo 📍 API will be available at: http://localhost:8000
echo 📖 API docs at: http://localhost:8000/docs
echo.

python chat-server.py

if errorlevel 1 (
    echo.
    echo ❌ Chat server exited with an error!
    echo.
    pause
)

