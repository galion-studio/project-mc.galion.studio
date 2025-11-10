@echo off
REM Quick Python Installer
REM Downloads and installs Python 3.12

title INSTALLING PYTHON
cls

echo.
echo ==========================================
echo   PYTHON INSTALLER
echo ==========================================
echo.

REM Check if Python already installed
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Python is already installed!
    python --version
    echo.
    pause
    exit /b 0
)

where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Python is already installed!
    py --version
    echo.
    pause
    exit /b 0
)

echo [!] Python not found. Installing...
echo.

REM Download Python installer
echo [1/3] Downloading Python 3.12...
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe' -OutFile '%TEMP%\python-installer.exe'"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Download failed!
    echo.
    echo Manual install:
    echo 1. Go to: https://www.python.org/downloads/
    echo 2. Download Python 3.12 or later
    echo 3. Run installer
    echo 4. CHECK "Add Python to PATH"
    echo 5. Click "Install Now"
    echo.
    pause
    exit /b 1
)

echo [OK] Download complete!
echo.

REM Install Python
echo [2/3] Installing Python...
echo.
echo IMPORTANT: When installer opens:
echo - CHECK "Add Python to PATH"
echo - Click "Install Now"
echo.
pause

"%TEMP%\python-installer.exe" /passive PrependPath=1 Include_test=0

echo.
echo [3/3] Verifying installation...
timeout /t 3 >nul

where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Python installed successfully!
    python --version
) else (
    echo [!] Please close and reopen this terminal
    echo Then run START-DEV-CONSOLE.cmd again
)

echo.
echo Installation complete!
pause

