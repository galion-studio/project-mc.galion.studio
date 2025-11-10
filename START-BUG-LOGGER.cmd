@echo off
title TITAN - Bug Report Logger
color 0E

cls
echo.
echo ========================================
echo    🐛 STARTING BUG LOGGER
echo ========================================
echo.
echo Players type: BUG: description
echo Reports saved to: bug-reports.txt
echo.
echo Press Ctrl+C to stop
echo.
echo ========================================
echo.

powershell -ExecutionPolicy Bypass -File BUG-LOGGER.ps1

pause

