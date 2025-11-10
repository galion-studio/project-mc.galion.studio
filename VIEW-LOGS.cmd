@echo off
REM ================================================================
REM  📊 VIEW LOGS - Show recent log files
REM ================================================================

echo.
echo ================================================================
echo   📊 RECENT LOGS
echo ================================================================
echo.

if exist "logs" (
    cd logs
    echo Latest log files:
    echo.
    dir /O-D /B *.log 2>nul
    echo.
    echo To view a specific log: type "more filename.log"
    echo.
    cd ..
) else (
    echo No logs directory found.
)

pause
