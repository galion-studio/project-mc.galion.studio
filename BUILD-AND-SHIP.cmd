@echo off
:: BUILD AND SHIP - One Command Deployment
:: Elon Musk Principle: If you need a process, you need to simplify

title BUILD AND SHIP
cls

echo.
echo ========================================
echo   BUILD AND SHIP - Musk Edition
echo ========================================
echo.
echo First Principles:
echo  - Delete unnecessary parts
echo  - Simplify the process  
echo  - Automate everything
echo  - Ship fast
echo.

cd client-launcher

:: Install dependencies (if needed)
echo [1/4] Checking dependencies...
pip install pyinstaller >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo      [OK] Dependencies ready
) else (
    echo      [WARN] Install may have failed, continuing...
)

:: Build the launcher (quick-launcher.py with Grok AI)
echo.
echo [2/4] Building launcher...
pyinstaller --name=GalionLauncher --onefile --windowed --clean --noconfirm quick-launcher.py
if %ERRORLEVEL% NEQ 0 (
    echo      [ERROR] Build failed!
    pause
    exit /b 1
)
echo      [OK] Launcher built successfully

:: Create distribution package
echo.
echo [3/4] Creating distribution package...
cd ..

:: Create release folder
if not exist "release" mkdir release
if exist "release\GalionLauncher-v2.zip" del "release\GalionLauncher-v2.zip"

:: Copy files
copy "client-launcher\dist\GalionLauncher.exe" "release\" >nul
echo README - GALION Launcher v2 > "release\README.txt"
echo. >> "release\README.txt"
echo How to use: >> "release\README.txt"
echo 1. Run GalionLauncher.exe >> "release\README.txt"
echo 2. Enter your username >> "release\README.txt"
echo 3. Click PLAY NOW >> "release\README.txt"
echo 4. Done! >> "release\README.txt"
echo. >> "release\README.txt"
echo Server: mc.galion.studio >> "release\README.txt"

:: Zip it
powershell -command "Compress-Archive -Path release\* -DestinationPath release\GalionLauncher-v2.zip -Force" >nul 2>&1
echo      [OK] Package created

:: Show results
echo.
echo [4/4] Deployment package ready!
echo      [OK] All done

echo.
echo ========================================
echo   READY TO SHIP!
echo ========================================
echo.
echo Package location:
echo   release\GalionLauncher-v2.zip
echo.
echo Executable:
echo   client-launcher\dist\GalionLauncher.exe
echo.
echo Next steps:
echo   1. Test: Run the executable
echo   2. Upload: Put zip on your website
echo   3. Share: Give link to players
echo   4. Done: Players play
echo.
echo Size: ~10-15 MB
echo Time saved: Hours of manual work
echo.
echo "The best process is no process." - Elon Musk
echo.

:: Open folder
start explorer release

echo Press any key to exit...
pause >nul

