@echo off
REM ================================================================
REM  🔍 CHECK SERVICES STATUS
REM  Show what's currently running
REM ================================================================

echo.
echo ================================================================
echo   🔍 SERVICES STATUS CHECK
echo ================================================================
echo.

echo Checking Python processes...
tasklist /FI "IMAGENAME eq python.exe" 2>nul | find /I "python.exe" >nul
if errorlevel 1 (
    echo ❌ No Python processes running
) else (
    echo ✅ Python processes running:
    tasklist /FI "IMAGENAME eq python.exe"
)

echo.
echo Checking ports...
echo.

netstat -ano | findstr ":8000" >nul 2>&1
if errorlevel 1 (
    echo ❌ Port 8000 (Chat Server) - Not in use
) else (
    echo ✅ Port 8000 (Chat Server) - Active
)

netstat -ano | findstr ":25565" >nul 2>&1
if errorlevel 1 (
    echo ❌ Port 25565 (Minecraft) - Not in use
) else (
    echo ✅ Port 25565 (Minecraft) - Active
)

netstat -ano | findstr ":25575" >nul 2>&1
if errorlevel 1 (
    echo ❌ Port 25575 (RCON) - Not in use
) else (
    echo ✅ Port 25575 (RCON) - Active
)

echo.
echo ================================================================
echo.

pause

