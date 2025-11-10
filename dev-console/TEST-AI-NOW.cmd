@echo off
REM Quick AI Test Script
REM Test Grok 4 Fast integration immediately

echo ========================================
echo   AI INTEGRATION TEST
echo   Grok 4 Fast
echo ========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not installed!
    pause
    exit /b 1
)

echo Testing AI integration...
echo.

cd ..
python -c "import sys; sys.path.insert(0, '.'); from grok_client import GrokClient; import asyncio; client = GrokClient('test'); print('[OK] Grok client imported successfully')"

if errorlevel 0 (
    echo [OK] AI system ready!
    echo.
    echo To use:
    echo   1. Get API key from openrouter.ai/keys
    echo   2. Run DEV-CONSOLE.cmd
    echo   3. Click AI Chat tab
    echo   4. Enter API key and connect
    echo.
) else (
    echo [!] Install dependencies first:
    echo     pip install -r requirements-dev-console.txt
)

pause

