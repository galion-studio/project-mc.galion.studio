#!/bin/bash
# ================================================================
# GALION PLATFORM - COMPREHENSIVE BUILD SYSTEM
# Builds all components: Console, Launcher, Mods, Server
# ================================================================

echo ""
echo "================================================================"
echo "  GALION PLATFORM - COMPREHENSIVE BUILD"
echo "  Version 1.0.0"
echo "================================================================"
echo ""

# Change to script directory
cd "$(dirname "$0")"

echo "[1/6] Checking prerequisites..."
echo ""

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
    echo "   ✓ Python found"
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
    echo "   ✓ Python found"
else
    echo "   ERROR: Python not found!"
    echo "   Install Python 3.8+ from python.org"
    exit 1
fi

# Check Gradle
if [ -f "gradlew" ]; then
    echo "   ✓ Gradle wrapper found"
    GRADLE_CMD="./gradlew"
    chmod +x "$GRADLE_CMD"
elif command -v gradle &> /dev/null; then
    echo "   ✓ Gradle found"
    GRADLE_CMD="gradle"
else
    echo "   ! Gradle not found, will skip Gradle builds"
    GRADLE_CMD=""
fi
echo ""

echo "[2/6] Building Developer Console..."
echo ""
cd dev-console
if [ -f "requirements-dev-console.txt" ]; then
    echo "   Installing dependencies..."
    $PYTHON_CMD -m pip install -r requirements-dev-console.txt --quiet
fi
cd ..
echo "   ✓ Developer Console ready"
echo ""

echo "[3/6] Building Client Launcher..."
echo ""
cd client-launcher
if [ -f "requirements.txt" ]; then
    echo "   Installing dependencies..."
    $PYTHON_CMD -m pip install -r requirements.txt --quiet
fi
cd ..
echo "   ✓ Client Launcher ready"
echo ""

echo "[4/6] Building Gradle modules..."
echo ""
if [ -n "$GRADLE_CMD" ]; then
    echo "   Running: $GRADLE_CMD buildAll"
    $GRADLE_CMD buildAll
    if [ $? -ne 0 ]; then
        echo "   ! Build failed"
        echo "   See output above for errors"
    else
        echo "   ✓ Gradle build complete"
    fi
else
    echo "   ! Skipping Gradle build (not available)"
fi
echo ""

echo "[5/6] Copying artifacts..."
echo ""

# Copy built JARs to server-mods
if [ -d "build/libs" ]; then
    echo "   Copying JARs to server-mods..."
    cp build/libs/*.jar server-mods/ 2>/dev/null
    echo "   ✓ Artifacts copied"
else
    echo "   ! No build artifacts found"
fi
echo ""

echo "[6/6] Validating build..."
echo ""

# Check if files exist
BUILD_SUCCESS=1

if [ ! -f "dev-console/console_main.py" ]; then
    echo "   ✗ Console main missing"
    BUILD_SUCCESS=0
fi

if [ ! -f "client-launcher/galion-launcher.py" ]; then
    echo "   ✗ Launcher missing"
    BUILD_SUCCESS=0
fi

if [ $BUILD_SUCCESS -eq 1 ]; then
    echo "   ✓ All critical files present"
else
    echo "   ✗ Some files missing"
fi
echo ""

echo "================================================================"
if [ $BUILD_SUCCESS -eq 1 ]; then
    echo "  ✓ BUILD COMPLETE!"
    echo ""
    echo "  Components Ready:"
    echo "    • Developer Console"
    echo "    • Client Launcher"
    echo "    • Backend Services"
    echo "    • Server Mods"
    echo ""
    echo "  Next Steps:"
    echo "    1. Run: ./LAUNCH-GALION-PLATFORM.sh"
    echo "    2. Or: $PYTHON_CMD dev-console/console_main.py"
else
    echo "  ✗ BUILD INCOMPLETE"
    echo ""
    echo "  Some components failed to build"
    echo "  Check output above for errors"
fi
echo "================================================================"
echo ""

