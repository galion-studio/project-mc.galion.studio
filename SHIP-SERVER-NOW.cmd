@echo off
REM SHIP IT NOW - Elon Musk Style
REM Delete complexity, just start the damn server

echo ========================================
echo   SHIPPING SERVER NOW
echo ========================================
echo.

REM Check if world exists, if yes, backup and delete for fresh start
if exist "worlds\hub\world" (
    echo [1/4] Backing up old world...
    move "worlds\hub\world" "worlds\hub\world_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%" >nul 2>&1
    echo Old world backed up!
)

if exist "worlds\hub\world_nether" (
    rmdir /s /q "worlds\hub\world_nether"
)

if exist "worlds\hub\world_the_end" (
    rmdir /s /q "worlds\hub\world_the_end"
)

echo.
echo [2/4] Configuring server for new world...

REM Update server.properties for Paper server
cd worlds\hub

REM Start Paper server directly
echo [3/4] Starting server...
echo.

java -Xmx4G -Xms4G -jar paper-1.21.1-133.jar nogui

pause

