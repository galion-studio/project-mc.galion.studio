@echo off
REM Galion Studio Launcher - Windows Launch Script
REM This script launches the Minecraft launcher on Windows

echo ================================================
echo Galion Studio Minecraft Launcher
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.7 or higher from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Launch the launcher
echo Starting launcher...
echo.
python launcher.py

REM Check if there was an error
if errorlevel 1 (
    echo.
    echo ERROR: Launcher failed to start
    echo.
    pause
    exit /b 1
)

echo.
echo Launcher closed.
pause

