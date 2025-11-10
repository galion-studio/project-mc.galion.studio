@echo off
REM Start Developer Console with Grok 4 Fast
REM GUI development environment with AI integration

title DEV CONSOLE - Grok 4 Fast
cls

echo.
echo ==========================================
echo   DEVELOPER CONSOLE + Grok 4 Fast
echo   Starting...
echo ==========================================
echo.

cd /d "%~dp0\dev-console"

REM Check for Python
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Found python
    python console_main.py
    goto :done
)

where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Found py launcher
    py console_main.py
    goto :done
)

REM Python not found
echo [ERROR] Python not found!
echo.
echo Please install Python 3.8+ from python.org
echo.
pause
exit /b 1

:done

