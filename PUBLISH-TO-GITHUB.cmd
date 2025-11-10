@echo off
REM ============================================================================
REM PROJECT TITAN - PUBLISH TO GITHUB
REM ============================================================================
REM
REM This script helps you publish Project Titan to GitHub
REM Make sure you've created the repository on GitHub first!
REM
REM Repository: https://github.com/galion-studio/project-mc.galion.studio
REM ============================================================================

echo.
echo ================================================================================
echo PROJECT TITAN - PUBLISH TO GITHUB
echo ================================================================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed!
    echo.
    echo Please install Git from: https://git-scm.com/download/win
    echo Then run this script again.
    echo.
    pause
    exit /b 1
)

echo Git is installed: 
git --version
echo.

REM Check if already a git repository
if exist ".git" (
    echo WARNING: This is already a git repository!
    echo.
    echo Do you want to continue? This will add and commit all changes.
    choice /M "Continue"
    if errorlevel 2 exit /b 0
) else (
    echo Initializing git repository...
    git init
    if errorlevel 1 (
        echo ERROR: Failed to initialize git repository
        pause
        exit /b 1
    )
    echo ✓ Git repository initialized
    echo.
)

REM Configure git user (you may need to change these)
echo Configuring git user...
git config user.name "Galion Studio"
git config user.email "contact@galion.studio"
echo ✓ Git user configured
echo.

REM Show what will be committed
echo ============================================================================
echo Files that will be committed:
echo ============================================================================
git add .
git status --short
echo.

echo ============================================================================
echo IMPORTANT: Review the files above
echo ============================================================================
echo.
echo Make sure there are NO sensitive files (passwords, API keys, etc.)
echo Press any key if everything looks good, or Ctrl+C to cancel...
pause >nul
echo.

REM Create initial commit
echo Creating initial commit...
git commit -m "feat: initial commit - Project Titan open source release" ^
           -m "" ^
           -m "- Complete Minecraft server platform for 20k+ players" ^
           -m "- Distributed architecture with microservices" ^
           -m "- Full documentation and contribution guidelines" ^
           -m "- Docker and Kubernetes deployment ready" ^
           -m "- AI integration features" ^
           -m "- Client launcher system"

if errorlevel 1 (
    echo ERROR: Failed to create commit
    echo.
    echo This might be because there are no changes to commit.
    echo Check 'git status' for more information.
    pause
    exit /b 1
)
echo ✓ Initial commit created
echo.

REM Add remote (check if already exists)
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo Adding GitHub remote...
    git remote add origin https://github.com/galion-studio/project-mc.galion.studio.git
    echo ✓ Remote added
) else (
    echo Remote 'origin' already exists
)
echo.

REM Show remote
echo Remote repository:
git remote -v
echo.

REM Rename branch to main
echo Renaming branch to 'main'...
git branch -M main
echo ✓ Branch renamed to main
echo.

REM Push to GitHub
echo ============================================================================
echo Ready to push to GitHub!
echo ============================================================================
echo.
echo This will upload your code to:
echo https://github.com/galion-studio/project-mc.galion.studio
echo.
echo You may be prompted for your GitHub credentials.
echo Use a Personal Access Token instead of password.
echo.
echo Press any key to push to GitHub, or Ctrl+C to cancel...
pause >nul
echo.

echo Pushing to GitHub...
git push -u origin main

if errorlevel 1 (
    echo.
    echo ============================================================================
    echo PUSH FAILED
    echo ============================================================================
    echo.
    echo Common issues:
    echo 1. Repository doesn't exist on GitHub
    echo    - Create it at: https://github.com/organizations/galion-studio/repositories/new
    echo.
    echo 2. Authentication failed
    echo    - Use a Personal Access Token instead of password
    echo    - Get one at: https://github.com/settings/tokens
    echo.
    echo 3. Permission denied
    echo    - Make sure you have write access to galion-studio organization
    echo.
    pause
    exit /b 1
)

echo ✓ Code pushed to GitHub!
echo.

REM Create and push tag
echo ============================================================================
echo Creating first release tag...
echo ============================================================================
echo.

git tag -a v1.0.0-alpha -m "Initial alpha release of Project Titan" ^
                        -m "" ^
                        -m "First public release of the Titan Minecraft server platform." ^
                        -m "" ^
                        -m "Features:" ^
                        -m "- Distributed architecture design" ^
                        -m "- Complete documentation" ^
                        -m "- Docker deployment setup" ^
                        -m "- Database schemas" ^
                        -m "- Client launcher" ^
                        -m "- AI integration framework" ^
                        -m "" ^
                        -m "Status: Alpha - Foundation phase"

echo Pushing tag to GitHub...
git push origin v1.0.0-alpha

if errorlevel 1 (
    echo WARNING: Failed to push tag
    echo You can try again later with: git push origin v1.0.0-alpha
    echo.
) else (
    echo ✓ Release tag created and pushed!
    echo.
)

echo ============================================================================
echo SUCCESS! 🎉
echo ============================================================================
echo.
echo Your project is now on GitHub:
echo https://github.com/galion-studio/project-mc.galion.studio
echo.
echo Next steps:
echo 1. Visit the repository on GitHub
echo 2. Configure repository settings (Issues, Discussions, Wiki)
echo 3. Add repository topics and description
echo 4. Set up branch protection
echo 5. Monitor issues and pull requests
echo.
echo For detailed next steps, see: PUBLISHING-GUIDE.md
echo.
pause

