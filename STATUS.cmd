@echo off
REM System Status Check
REM Quick diagnostic for server and consoles

title SYSTEM STATUS
cls

echo.
echo ==========================================
echo   SYSTEM STATUS CHECK
echo ==========================================
echo.

REM Check Python
echo [1/4] Checking Python...
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo  [OK] Python found
    python --version 2>nul
) else (
    where py >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo  [OK] Python found ^(py launcher^)
        py --version 2>nul
    ) else (
        echo  [X] Python NOT found - Install with INSTALL-PYTHON.cmd
    )
)
echo.

REM Check Docker
echo [2/4] Checking Docker...
docker --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo  [OK] Docker installed
) else (
    echo  [X] Docker NOT found
)
echo.

REM Check Server
echo [3/4] Checking Minecraft Server...
docker ps 2>nul | findstr titan-hub >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo  [OK] Server RUNNING ^(titan-hub^)
    docker ps --format "table {{.Names}}\t{{.Status}}" | findstr titan
) else (
    echo  [X] Server NOT running
    echo     Start with: INSTANT-LAUNCH.cmd
)
echo.

REM Check Config
echo [4/4] Checking Configuration...
if exist ".env.grok" (
    echo  [OK] .env.grok exists
    findstr "OPENROUTER_API_KEY=" .env.grok | findstr "your-openrouter-api-key-here" >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo  [!] API key not set - Edit .env.grok
    ) else (
        echo  [OK] API key configured
    )
) else (
    echo  [!] .env.grok missing - Copy from env.grok.example
)
echo.

echo ==========================================
echo   AVAILABLE COMMANDS
echo ==========================================
echo.
echo  INSTALL-PYTHON.cmd      - Install Python
echo  START-DEV-CONSOLE.cmd   - GUI Console
echo  START-CONSOLE-CHAT.cmd  - Terminal Console  
echo  INSTANT-LAUNCH.cmd      - Start Server+Client
echo.
pause

