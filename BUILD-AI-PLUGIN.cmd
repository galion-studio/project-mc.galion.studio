@echo off
REM Build and Deploy TitanAI Plugin
REM Compiles the AI assistant and copies it to server

color 0B
cls

echo.
echo ========================================
echo    🤖 BUILDING TITAN AI ASSISTANT
echo ========================================
echo.

echo [1/3] Building plugin with Gradle...
call gradlew.bat :plugins:TitanAI:build -x test

if errorlevel 1 (
    color 0C
    echo.
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

echo [OK] Plugin built successfully
echo.

echo [2/3] Copying to server plugins folder...
mkdir worlds\hub\plugins 2>nul
copy /Y plugins\TitanAI\build\libs\TitanAI-1.0.0.jar worlds\hub\plugins\

if errorlevel 1 (
    echo [ERROR] Failed to copy plugin
    pause
    exit /b 1
)

echo [OK] Plugin copied
echo.

echo [3/3] Restarting server...
docker-compose restart titan-hub

echo.
color 0A
echo ========================================
echo    ✅ AI ASSISTANT DEPLOYED! ✅
echo ========================================
echo.
echo 🎮 Test in Minecraft:
echo    Type: @ai hello!
echo.
echo 📝 Configure API key in:
echo    plugins\TitanAI\src\main\resources\config.yml
echo.
echo    Get API key from:
echo    https://console.anthropic.com/
echo.
echo ========================================
echo.
pause

