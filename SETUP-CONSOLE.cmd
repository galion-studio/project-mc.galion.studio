@echo off
title Setup - Grok Console Chat
color 0B
cls

echo.
echo ============================================================
echo   GROK CONSOLE CHAT - SETUP
echo ============================================================
echo.

echo Step 1: Setting up API Key...
echo.
echo You need an OpenRouter API key to use Grok AI.
echo.
echo 1. Go to: https://openrouter.ai/keys
echo 2. Sign up (free credits available!)
echo 3. Create an API key
echo 4. Copy the key (starts with sk-or-v1-...)
echo.

echo Opening .env.grok file for you to paste your key...
echo.
pause

REM Open the .env.grok file in notepad
notepad .env.grok

echo.
echo ============================================================
echo   IMPORTANT: Replace 'your-openrouter-api-key-here' 
echo   with your actual API key, then SAVE the file!
echo ============================================================
echo.
echo After saving, the console will be ready to use.
echo.
echo Press any key when done...
pause >nul

echo.
echo Testing configuration...
py test_imports_fixed.py

echo.
echo ============================================================
echo   Setup Complete!
echo ============================================================
echo.
echo You can now run the console by double-clicking:
echo   LAUNCH-CONSOLE.cmd
echo.
pause

