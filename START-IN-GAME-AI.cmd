@echo off
title GROK IN-GAME AI BRIDGE
color 0B
cls

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  🤖 GROK IN-GAME AI BRIDGE                                ║
echo ║  Players can chat with AI directly in Minecraft!          ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check if .env.grok exists
if not exist ".env.grok" (
    echo ⚠️  ERROR: .env.grok not found!
    echo.
    echo Please run SETUP-CONSOLE.cmd first to configure your API key.
    echo.
    pause
    exit /b 1
)

echo 🎮 How to use IN-GAME AI:
echo.
echo   Players type in Minecraft chat:
echo     console what is redstone?
echo     @ai how do I craft a piston?
echo     hey console help me
echo.
echo   The AI will respond in chat within 1 second!
echo.

echo Starting AI bridge...
echo.

cd ai-bridge
py instant.py

if errorlevel 1 (
    echo.
    echo ❌ AI Bridge failed to start!
    echo.
    echo Make sure:
    echo   1. .env.grok has your OpenRouter API key
    echo   2. Minecraft server is running (docker ps)
    echo   3. All dependencies installed (py -m pip install -r requirements-grok.txt)
    echo.
    pause
)

