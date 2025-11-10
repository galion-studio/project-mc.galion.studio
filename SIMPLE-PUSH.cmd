@echo off
REM Simple push script - just the essential commands

echo Pushing to GitHub...
echo.

cd "C:\Users\Gigabyte\Documents\project-mc-serv-mc.galion.studio"

git push -u origin main

if errorlevel 1 (
    echo.
    echo FAILED! Make sure you created the repository on GitHub first:
    echo https://github.com/organizations/galion-studio/repositories/new
    echo Name: project-mc.galion.studio
    pause
    exit /b 1
)

echo.
echo SUCCESS! View at: https://github.com/galion-studio/project-mc.galion.studio
echo.

REM Optional: Create release tag
git tag -a v1.0.0-alpha -m "Initial alpha release"
git push origin v1.0.0-alpha

pause

