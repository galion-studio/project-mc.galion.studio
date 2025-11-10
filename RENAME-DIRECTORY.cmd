@echo off
REM ============================================================================
REM RENAME PROJECT DIRECTORY
REM ============================================================================
REM
REM This script renames the project directory from:
REM   project-mc-serv-mc.galion.studio
REM to:
REM   project-mc.galion.studio
REM
REM ============================================================================

echo.
echo ================================================================================
echo RENAME PROJECT DIRECTORY
echo ================================================================================
echo.

REM Get current directory name
for %%I in (.) do set CURRENT_DIR=%%~nxI

echo Current directory: %CURRENT_DIR%
echo.

if not "%CURRENT_DIR%"=="project-mc-serv-mc.galion.studio" (
    echo ERROR: This script must be run from the project-mc-serv-mc.galion.studio directory
    echo Current directory: %CURRENT_DIR%
    echo.
    pause
    exit /b 1
)

echo This will rename the project directory from:
echo   FROM: project-mc-serv-mc.galion.studio
echo   TO:   project-mc.galion.studio
echo.
echo WARNING: Make sure no files are open in the directory!
echo.

choice /M "Do you want to continue"
if errorlevel 2 (
    echo Cancelled.
    exit /b 0
)

echo.
echo Renaming directory...
echo.

REM Move to parent directory and rename
cd ..
if errorlevel 1 (
    echo ERROR: Failed to change to parent directory
    pause
    exit /b 1
)

REM Rename the directory
ren "project-mc-serv-mc.galion.studio" "project-mc.galion.studio"
if errorlevel 1 (
    echo ERROR: Failed to rename directory
    echo.
    echo Make sure:
    echo - No files are open from this directory
    echo - No command prompts are in this directory
    echo - No applications are using files from this directory
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================================================
echo SUCCESS! Directory renamed
echo ================================================================================
echo.
echo Old name: project-mc-serv-mc.galion.studio
echo New name: project-mc.galion.studio
echo.
echo New path: %CD%\project-mc.galion.studio
echo.
echo You can now open the project in the new location.
echo.
pause

