@echo off
REM Test Transparent Console Configuration

echo ================================================
echo   TEST TRANSPARENT CONSOLE
echo   Configuration Validator
echo ================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    echo Install Python from python.org
    pause
    exit /b 1
)
echo [OK] Python installed

REM Check customtkinter
python -c "import customtkinter" >nul 2>&1
if errorlevel 1 (
    echo [WARN] customtkinter not installed
    echo Installing...
    pip install customtkinter
) else (
    echo [OK] customtkinter installed
)

REM Check dotenv
python -c "import dotenv" >nul 2>&1
if errorlevel 1 (
    echo [WARN] python-dotenv not installed
    echo Installing...
    pip install python-dotenv
) else (
    echo [OK] python-dotenv installed
)

REM Test configuration manager
echo.
echo Testing configuration manager...
cd dev-console
python config_manager.py

echo.
echo ================================================
echo   TEST COMPLETE
echo ================================================
echo.
echo Ready to launch: START-TRANSPARENT-CONSOLE.cmd
echo.

pause

