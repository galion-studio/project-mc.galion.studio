@echo off
REM SHIP IT - Direct server start, Musk style
REM No Docker, No BS, Just RUN

echo ================================================
echo   GALION.STUDIO - STARTING SERVER NOW
echo ================================================
echo.

cd worlds\hub

echo Server directory: %CD%
echo.
echo [1/2] Checking Java...
java -version
echo.

echo [2/2] STARTING MINECRAFT SERVER...
echo.
echo Server will generate NEW WORLD with seed: GALION2025
echo.
echo ================================================

REM Start server with optimal JVM flags (Aikar's flags)
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
     -Dusing.aikars.flags=https://mcflags.emc.gs ^
     -Daikars.new.flags=true ^
     -jar paper-1.21.1-133.jar nogui

