@echo off
title GROK AI BRIDGE - In-Game Chat
color 0B
cls

echo.
echo =========================================================
echo   ⚡ GROK AI BRIDGE - In-Game Chat
echo   Connects Minecraft chat to Grok AI
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

REM Choose which bridge to run
echo.
echo Choose AI Bridge:
echo   1. NANO Bridge (Minimal, Fast)
echo   2. INSTANT Bridge (Ultra-fast)
echo   3. FAST Bridge (Full-featured)
echo.

choice /C 123 /N /M "Enter choice (1-3): "

if errorlevel 3 goto fast
if errorlevel 2 goto instant
if errorlevel 1 goto nano

:nano
echo.
echo 🚀 Starting NANO Bridge...
cd ai-bridge
python nano-bridge.py
goto end

:instant
echo.
echo 🚀 Starting INSTANT Bridge...
cd ai-bridge
python instant.py
goto end

:fast
echo.
echo 🚀 Starting FAST Bridge...
cd ai-bridge
python fast-ai-bridge.py
goto end

:end
if errorlevel 1 (
    echo.
    echo ❌ Bridge exited with an error!
    echo.
    pause
)

