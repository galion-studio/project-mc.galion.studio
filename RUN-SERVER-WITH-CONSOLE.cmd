@echo off
REM VISIBLE SERVER CONSOLE - See everything happening

title GALION.STUDIO Minecraft Server

echo ================================================
echo   GALION.STUDIO - SERVER STARTING
echo ================================================
echo.
echo Server: localhost:25565
echo Version: 1.21.1
echo Seed: GALION2025
echo.
echo ================================================
echo.

cd worlds\hub

REM Start server with visible console
java -Xms4G -Xmx4G ^
     -XX:+UseG1GC ^
     -XX:+ParallelRefProcEnabled ^
     -XX:MaxGCPauseMillis=200 ^
     -XX:+UnlockExperimentalVMOptions ^
     -XX:+DisableExplicitGC ^
     -XX:+AlwaysPreTouch ^
     -XX:G1NewSizePercent=30 ^
     -XX:G1MaxNewSizePercent=40 ^
     -XX:G1HeapRegionSize=8M ^
     -XX:G1ReservePercent=20 ^
     -XX:G1HeapWastePercent=5 ^
     -XX:G1MixedGCCountTarget=4 ^
     -XX:InitiatingHeapOccupancyPercent=15 ^
     -XX:G1MixedGCLiveThresholdPercent=90 ^
     -XX:G1RSetUpdatingPauseTimePercent=5 ^
     -XX:SurvivorRatio=32 ^
     -XX:+PerfDisableSharedMem ^
     -XX:MaxTenuringThreshold=1 ^
     -jar paper-1.21.1-133.jar nogui

pause

