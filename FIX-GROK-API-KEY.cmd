@echo off
:: Fix Grok API Key - Quick Setup
:: This script helps you update your OpenRouter API key

echo ============================================================
echo  GROK API KEY SETUP - Fix Instructions
echo ============================================================
echo.
echo PROBLEM: Your current API key is invalid
echo          Error: "User not found" (401)
echo.
echo SOLUTION: Get a FREE OpenRouter API key
echo.
echo ============================================================
echo  STEP 1: Get Your FREE API Key
echo ============================================================
echo.
echo 1. Open this URL in your browser:
echo    https://openrouter.ai/keys
echo.
echo 2. Sign in (free account, no credit card needed)
echo.
echo 3. Click "Create Key" button
echo.
echo 4. Copy the key (starts with "sk-or-v1-")
echo.
echo ============================================================
echo  STEP 2: Update .env.grok File
echo ============================================================
echo.
echo Opening .env.grok file for you now...
echo.
timeout /t 2 /nobreak >nul

:: Open the file in notepad
if exist ".env.grok" (
    notepad .env.grok
    echo.
    echo [OK] File opened in Notepad
    echo.
    echo INSTRUCTIONS:
    echo 1. Find the line: OPENROUTER_API_KEY=...
    echo 2. Replace the old key with your new key from OpenRouter
    echo 3. Make sure it starts with "sk-or-v1-"
    echo 4. Save and close Notepad
    echo.
) else (
    echo [ERROR] .env.grok file not found!
    echo Creating from template...
    copy env.grok.example .env.grok
    notepad .env.grok
    echo.
    echo INSTRUCTIONS:
    echo 1. Find the line: OPENROUTER_API_KEY=your-openrouter-api-key-here
    echo 2. Replace "your-openrouter-api-key-here" with your key from OpenRouter
    echo 3. Make sure it starts with "sk-or-v1-"
    echo 4. Save and close Notepad
    echo.
)

echo ============================================================
echo  STEP 3: Test Connection
echo ============================================================
echo.
echo After saving your API key, press any key to test...
pause >nul

echo.
echo Testing connection...
echo.
py test-grok-connection-debug.py

echo.
echo ============================================================
echo  NEXT STEPS
echo ============================================================
echo.
echo If the test shows [OK] SUCCESS:
echo   - Your API key is working!
echo   - Go back to your AI Control Center
echo   - Click "Connect" button again
echo   - Send a message to test
echo.
echo If the test still fails:
echo   1. Make sure you copied the ENTIRE key
echo   2. Make sure it starts with "sk-or-v1-"
echo   3. Make sure you saved the .env.grok file
echo   4. Try running this script again
echo.
echo ============================================================
echo.
pause

