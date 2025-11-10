@echo off
REM Start Development API Server
REM Extended API with dev endpoints

echo ========================================
echo   DEVELOPMENT API SERVER
echo   Galion.Studio
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    pause
    exit /b 1
)

REM Check dependencies
echo Checking dependencies...
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo [!] Installing FastAPI...
    pip install fastapi uvicorn python-multipart
)

echo.
echo [OK] Starting Development API...
echo API will be available at: http://localhost:8080
echo.

REM Start the API
cd api
python dev_api_server.py

pause

