@echo off
title ⚡ TITAN AI - GROK CONSOLE CHAT
color 0B
cls

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║  ⚡ TITAN AI - GROK CONSOLE CHAT                               ║
echo ║  Ultra-fast AI chat + Minecraft server control                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check if .env.grok exists
if not exist ".env.grok.example" (
    echo ⚠️  WARNING: .env.grok.example not found!
    echo Please make sure you're in the project directory.
    echo.
    pause
    exit /b 1
)

REM Copy example if .env.grok doesn't exist
if not exist ".env.grok" (
    echo 📝 Creating .env.grok from example...
    copy ".env.grok.example" ".env.grok" >nul 2>&1
    echo.
    echo ✓ Created .env.grok
    echo.
    echo ⚠️  IMPORTANT: Edit .env.grok and set your OPENROUTER_API_KEY
    echo    Get your API key from: https://openrouter.ai/keys
    echo.
    notepad .env.grok
    echo.
    echo Press any key after you've saved your API key...
    pause >nul
)

echo 🚀 Launching Grok Console Chat...
echo.

REM Launch the console chat
py console-chat.py

echo.
echo.
echo Console chat closed.
pause

