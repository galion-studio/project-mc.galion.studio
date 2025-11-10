@echo off
REM ================================================================
REM  🛑 STOP ALL SERVICES
REM  Gracefully stops all running services
REM ================================================================

echo.
echo ================================================================
echo   🛑 STOPPING ALL SERVICES
echo ================================================================
echo.

echo Stopping Python processes...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM pythonw.exe /T >nul 2>&1

echo Stopping Node.js processes (if any)...
taskkill /F /IM node.exe /T >nul 2>&1

echo.
echo ✅ All services stopped
echo.

pause

