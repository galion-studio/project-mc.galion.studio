@echo off
REM Simple direct start - no background processes

cd /d "%~dp0"

echo Starting Mod Sync Server...
echo Press Ctrl+C to stop
echo.

py mod-sync-server.py

pause

