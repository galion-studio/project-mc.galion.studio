@echo off
REM Quick setup script for Grok 4 Fast on OpenRouter
REM Run this to get started in 2 minutes!

echo ========================================
echo   GROK 4 FAST - QUICK SETUP
echo ========================================
echo.

REM Step 1: Copy example config
echo Step 1/3: Creating .env.grok file...
if not exist .env.grok (
    copy env.grok.example .env.grok
    echo [OK] Created .env.grok
) else (
    echo [!] .env.grok already exists
)
echo.

REM Step 2: Prompt for API key
echo Step 2/3: OpenRouter API Key
echo.
echo Get your FREE API key here:
echo https://openrouter.ai/keys
echo.
echo (OpenRouter gives you $1 free credit = ~1000 questions!)
echo.

set /p API_KEY="Paste your API key here (or press Enter to skip): "

if not "%API_KEY%"=="" (
    REM Update the .env.grok file with the API key
    powershell -Command "(Get-Content .env.grok) -replace 'OPENROUTER_API_KEY=.*', 'OPENROUTER_API_KEY=%API_KEY%' | Set-Content .env.grok"
    echo [OK] API key saved!
) else (
    echo [!] Skipped - You'll need to edit .env.grok manually
)
echo.

REM Step 3: Test connection
echo Step 3/3: Testing connection...
echo.

if "%API_KEY%"=="" (
    echo [!] Can't test without API key
    echo.
    echo NEXT STEPS:
    echo 1. Edit .env.grok and paste your API key
    echo 2. Run: python test-grok-system.py
    echo 3. Run: START-GROK-BRIDGE.cmd
) else (
    echo Running test...
    python test-grok-system.py
    echo.
    echo ========================================
    echo   SETUP COMPLETE!
    echo ========================================
    echo.
    echo TO USE GROK:
    echo - Run: START-GROK-BRIDGE.cmd
    echo - Or test: python test-grok-system.py
    echo.
    echo See GROK-QUICK-START.md for full guide
)

pause

