@echo off
REM ============================================================================
REM PUSH TO GITHUB - MANUAL SCRIPT
REM ============================================================================
REM
REM This script pushes your code to GitHub
REM Make sure you created the repository first!
REM
REM ============================================================================

echo.
echo ================================================================================
echo PUSH PROJECT TO GITHUB
echo ================================================================================
echo.

echo Repository: https://github.com/galion-studio/project-mc.galion.studio
echo.

echo IMPORTANT: Make sure you created the repository on GitHub first!
echo Go to: https://github.com/organizations/galion-studio/repositories/new
echo Name: project-mc.galion.studio
echo.

choice /M "Have you created the repository on GitHub"
if errorlevel 2 (
    echo.
    echo Please create the repository first, then run this script again.
    echo.
    pause
    exit /b 0
)

echo.
echo Pushing to GitHub...
echo.
echo You may be asked for credentials:
echo - Username: Your GitHub username
echo - Password: Use a Personal Access Token (not your password!)
echo   Get token at: https://github.com/settings/tokens
echo.

git push -u origin main

if errorlevel 1 (
    echo.
    echo ============================================================================
    echo PUSH FAILED
    echo ============================================================================
    echo.
    echo Common issues:
    echo.
    echo 1. Repository doesn't exist on GitHub
    echo    Create it at: https://github.com/organizations/galion-studio/repositories/new
    echo    Name must be exactly: project-mc.galion.studio
    echo.
    echo 2. Authentication failed
    echo    Use a Personal Access Token instead of password
    echo    Get one at: https://github.com/settings/tokens
    echo    - Click "Generate new token (classic)"
    echo    - Select "repo" scope
    echo    - Copy and use as password
    echo.
    echo 3. Permission denied
    echo    Make sure you have write access to galion-studio organization
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo SUCCESS! Code pushed to GitHub
echo ============================================================================
echo.
echo Your project is now live at:
echo https://github.com/galion-studio/project-mc.galion.studio
echo.

echo.
echo Do you want to create a release tag? (v1.0.0-alpha)
choice /M "Create release tag"
if errorlevel 2 (
    echo.
    echo Skipping release tag.
    echo You can create it later with:
    echo   git tag -a v1.0.0-alpha -m "Initial alpha release"
    echo   git push origin v1.0.0-alpha
    echo.
    goto :end
)

echo.
echo Creating release tag v1.0.0-alpha...
git tag -a v1.0.0-alpha -m "Initial alpha release of Project Titan"

echo Pushing tag to GitHub...
git push origin v1.0.0-alpha

if errorlevel 1 (
    echo.
    echo WARNING: Failed to push tag
    echo You can try again later with:
    echo   git push origin v1.0.0-alpha
    echo.
) else (
    echo.
    echo ✓ Release tag created and pushed!
    echo.
    echo GitHub will automatically create a release.
    echo Check it at: https://github.com/galion-studio/project-mc.galion.studio/releases
    echo.
)

:end
echo ============================================================================
echo NEXT STEPS
echo ============================================================================
echo.
echo 1. Visit your repository:
echo    https://github.com/galion-studio/project-mc.galion.studio
echo.
echo 2. Configure repository settings:
echo    - Go to Settings -^> General
echo    - Enable: Issues, Discussions, Wiki, Projects
echo.
echo 3. Add repository topics (click ⚙️ next to "About"):
echo    minecraft, minecraft-server, distributed-systems, microservices,
echo    docker, kubernetes, java, open-source, gaming, scalability
echo.
echo 4. Set up branch protection:
echo    - Go to Settings -^> Branches
echo    - Add branch protection rule for "main"
echo.
echo 5. Share your project!
echo.
pause

