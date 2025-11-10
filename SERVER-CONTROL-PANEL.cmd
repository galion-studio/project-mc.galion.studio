@echo off
REM GALION.STUDIO Server Control Panel
REM Choose your server mode and features

:MENU
cls
echo ========================================================================
echo                   GALION.STUDIO SERVER CONTROL PANEL
echo ========================================================================
echo.
echo   [1] START LOCAL SERVER (Offline, No AI)
echo   [2] START OFFICIAL SERVER (Online with AI)
echo   [3] VIEW SERVER MODE STATUS
echo   [4] CONFIGURE AI FEATURES
echo   [5] VIEW SERVER LOGS
echo   [6] STOP SERVER
echo   [7] GENERATE NEW WORLD
echo   [8] INSTALL PLUGINS
echo   [9] EXIT
echo.
echo ========================================================================

set /p choice="Select option (1-9): "

if "%choice%"=="1" goto LOCAL_SERVER
if "%choice%"=="2" goto OFFICIAL_SERVER
if "%choice%"=="3" goto STATUS
if "%choice%"=="4" goto AI_CONFIG
if "%choice%"=="5" goto LOGS
if "%choice%"=="6" goto STOP
if "%choice%"=="7" goto NEW_WORLD
if "%choice%"=="8" goto PLUGINS
if "%choice%"=="9" goto EXIT

goto MENU

:LOCAL_SERVER
cls
echo ========================================================================
echo   STARTING LOCAL SERVER (OFFLINE MODE)
echo ========================================================================
echo.
echo Mode: LOCAL
echo Internet: Not Required
echo AI Features: DISABLED
echo Host: localhost:25565
echo.
echo ========================================================================
echo.

REM Set server mode to LOCAL
py -c "from server_mode_config import ServerModeManager, ServerMode; m = ServerModeManager(); m.set_mode(ServerMode.LOCAL); print('[OK] Server mode set to LOCAL')"

echo.
echo Starting server...
echo.
pause

cd worlds\hub
start cmd /k "title GALION.STUDIO LOCAL SERVER && java -Xms4G -Xmx4G -XX:+UseG1GC -jar paper-1.21.1-133.jar nogui"

echo.
echo [OK] Local server started in new window!
echo.
pause
goto MENU

:OFFICIAL_SERVER
cls
echo ========================================================================
echo   STARTING OFFICIAL SERVER (ONLINE MODE)
echo ========================================================================
echo.
echo Mode: OFFICIAL
echo Internet: Required
echo AI Features: ENABLED
echo Host: mc.galion.studio:25565
echo.
echo ========================================================================
echo.

REM Check internet
py -c "from server_mode_config import ServerModeManager; import sys; m = ServerModeManager(); sys.exit(0 if m.check_internet_connection() else 1)"
if errorlevel 1 (
    echo.
    echo [ERROR] No internet connection detected!
    echo Official mode requires internet for AI features.
    echo.
    echo Press any key to return to menu...
    pause >nul
    goto MENU
)

echo [OK] Internet connection verified
echo.

REM Set server mode to OFFICIAL
py -c "from server_mode_config import ServerModeManager, ServerMode; m = ServerModeManager(); m.set_mode(ServerMode.OFFICIAL); print('[OK] Server mode set to OFFICIAL')"

REM Check AI
py -c "from ai_feature_controller import AIFeatureController; c = AIFeatureController(); print('[AI STATUS]', 'ENABLED' if c.is_ai_available() else 'DISABLED - Run SETUP-GROK-NOW.cmd')"

echo.
echo Starting server with AI bridge...
echo.
pause

cd worlds\hub
start cmd /k "title GALION.STUDIO OFFICIAL SERVER && java -Xms4G -Xmx4G -XX:+UseG1GC -jar paper-1.21.1-133.jar nogui"

echo.
echo [OK] Official server started in new window!
echo.
pause
goto MENU

:STATUS
cls
echo ========================================================================
echo   SERVER MODE STATUS
echo ========================================================================
echo.

py -c "from server_mode_config import ServerModeManager; from ai_feature_controller import AIFeatureController; import json; m = ServerModeManager(); c = AIFeatureController(); mode = m.get_current_mode(); config = m.get_mode_config(); status = c.get_ai_status(); print('Current Mode:', mode.value.upper()); print('Server:', config['host'] + ':' + str(config['port'])); print('AI Enabled:', 'YES' if config['ai_enabled'] else 'NO'); print('Internet Required:', 'YES' if config['requires_internet'] else 'NO'); print('AI Available:', 'YES' if status['ai_available'] else 'NO'); print('Has API Keys:', 'YES' if status['has_api_keys'] else 'NO'); print('Internet Status:', 'CONNECTED' if status['internet_available'] else 'OFFLINE')"

echo.
echo ========================================================================
echo.
pause
goto MENU

:AI_CONFIG
cls
echo ========================================================================
echo   AI CONFIGURATION
echo ========================================================================
echo.
echo Launching AI setup wizard...
echo.
call SETUP-GROK-NOW.cmd
goto MENU

:LOGS
cls
echo ========================================================================
echo   SERVER LOGS (Last 30 lines)
echo ========================================================================
echo.

if exist "worlds\hub\logs\latest.log" (
    powershell -Command "Get-Content worlds\hub\logs\latest.log -Tail 30"
) else (
    echo No logs found. Server not started yet.
)

echo.
echo ========================================================================
pause
goto MENU

:STOP
cls
echo ========================================================================
echo   STOP SERVER
echo ========================================================================
echo.
echo This will stop all running Minecraft servers.
echo.
set /p confirm="Are you sure? (Y/N): "

if /i "%confirm%"=="Y" (
    echo.
    echo Stopping servers...
    taskkill /F /IM java.exe /T >nul 2>&1
    echo [OK] Servers stopped
    echo.
) else (
    echo Cancelled.
)

pause
goto MENU

:NEW_WORLD
cls
echo ========================================================================
echo   GENERATE NEW WORLD
echo ========================================================================
echo.
echo WARNING: This will DELETE your current world!
echo.
set /p confirm="Are you sure? (Y/N): "

if /i "%confirm%"=="Y" (
    echo.
    echo Backing up old world...
    
    if exist "worlds\hub\world" (
        powershell -Command "Rename-Item 'worlds\hub\world' -NewName ('world_backup_' + (Get-Date -Format 'yyyyMMdd_HHmmss')) -ErrorAction SilentlyContinue"
    )
    
    echo Deleting dimensions...
    rmdir /s /q "worlds\hub\world_nether" 2>nul
    rmdir /s /q "worlds\hub\world_the_end" 2>nul
    
    echo.
    echo [OK] World reset! New world will generate on next start.
    echo.
) else (
    echo Cancelled.
)

pause
goto MENU

:PLUGINS
cls
echo ========================================================================
echo   PLUGIN MANAGEMENT
echo ========================================================================
echo.
echo Installed Plugins:
echo.

if exist "worlds\hub\plugins\*.jar" (
    dir /b worlds\hub\plugins\*.jar
) else (
    echo No plugins installed yet.
)

echo.
echo ========================================================================
echo.
echo [1] Download Plugin Guide
echo [2] Install Plugins Automatically
echo [3] Back to Menu
echo.

set /p pchoice="Select option (1-3): "

if "%pchoice%"=="1" (
    echo.
    echo Opening plugin download guide...
    notepad DOWNLOAD-PLUGINS-GUIDE.md
    goto PLUGINS
)

if "%pchoice%"=="2" (
    echo.
    echo Running automatic plugin installer...
    py INSTALL-PLUGINS-AUTO.py
    pause
    goto PLUGINS
)

goto MENU

:EXIT
cls
echo.
echo Thanks for using GALION.STUDIO Server Control Panel!
echo.
exit /b 0

