@echo off
REM Start Minecraft AI Chat Bridge
REM Monitors Minecraft chat and responds with Grok 4 Fast

echo ========================================
echo   MINECRAFT AI CHAT BRIDGE
echo   Grok 4 Fast Integration
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    pause
    exit /b 1
)

echo [OK] Starting AI Chat Bridge...
echo.
echo Players can type: ai ^<question^>
echo Example: ai what is redstone?
echo.

REM Start bridge
cd ai
python minecraft_chat_bridge.py

pause

