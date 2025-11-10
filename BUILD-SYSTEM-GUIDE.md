# GALION Platform Build System Guide

**Version:** 1.0.0  
**Last Updated:** November 10, 2025  
**Status:** Production Ready

---

## Overview

The GALION Platform build system provides comprehensive building capabilities for all platform components including Developer Console, Client Launcher, Gradle modules, and server mods.

---

## Build Methods

### Method 1: One-Command Build (Recommended)

**Windows:**
```cmd
BUILD-GALION-PLATFORM.cmd
```

**Linux/Mac:**
```bash
chmod +x BUILD-GALION-PLATFORM.sh
./BUILD-GALION-PLATFORM.sh
```

**Python:**
```bash
py build_system.py
```

### Method 2: From Developer Console

1. Launch console: `py dev-console\console_main.py`
2. Enter PIN (default: 1234)
3. Click **🔨 Builder** in sidebar
4. Configure build options
5. Click **🔨 BUILD PROJECT**

### Method 3: Individual Component Builds

**Developer Console:**
```bash
cd dev-console
py -m pip install -r requirements-dev-console.txt
```

**Client Launcher:**
```bash
cd client-launcher
py -m pip install -r requirements.txt
```

**Gradle Modules:**
```bash
# Windows
gradlew.bat buildAll

# Linux/Mac
./gradlew buildAll
```

---

## Build System Components

### 1. Modern Builder UI

**Location:** `dev-console/ide/modern_builder.py`

**Features:**
- Beautiful modern interface matching platform style
- Large 60px build buttons with colors
- Real-time build output streaming
- Build status indicator (60px animated circle)
- Build metrics (time, success rate)
- Auto-deploy to server-mods
- Clean before build option
- Stop running builds

**Build Tasks Available:**
- `build` - Standard build
- `clean build` - Clean then build
- `jar` - Create JAR only
- `shadowJar` - Create fat JAR with dependencies
- `buildAll` - Build all subprojects
- `cleanAll` - Clean all subprojects

**UI Elements:**
- 100px modern header with subtitle
- 140px status card with 60px indicator
- 60px action buttons (BUILD/CLEAN/STOP)
- Real-time output with color coding
- Build metrics display

### 2. Python Build System

**Location:** `build_system.py`

**Class:** `GalionBuilder`

**Usage:**
```python
from build_system import GalionBuilder

builder = GalionBuilder()
success = builder.build_all(clean=False, deploy=True)
```

**Methods:**
- `build_all()` - Build all components
- `build_console()` - Build console only
- `build_launcher()` - Build launcher only
- `build_gradle()` - Build Gradle modules only
- `deploy_artifacts()` - Deploy built JARs
- `print_summary()` - Show build summary

**Command-Line Arguments:**
```bash
# Build all with clean
py build_system.py --clean

# Build without deploying
py build_system.py --no-deploy

# Build console only
py build_system.py --console-only

# Build launcher only
py build_system.py --launcher-only

# Build Gradle modules only
py build_system.py --gradle-only
```

### 3. Shell Scripts

**Windows:** `BUILD-GALION-PLATFORM.cmd`  
**Linux/Mac:** `BUILD-GALION-PLATFORM.sh`

**Build Phases:**
1. Check prerequisites (Python, Gradle)
2. Build Developer Console (install dependencies)
3. Build Client Launcher (install dependencies)
4. Build Gradle modules (all subprojects)
5. Copy artifacts to server-mods
6. Validate build results

**Exit Codes:**
- `0` - Build successful
- `1` - Build failed or missing prerequisites

---

## Build Configuration

### Gradle Configuration

**File:** `build.gradle.kts`

**Key Settings:**
- Java Version: 17
- Kotlin Version: 1.9.20
- Shadow Plugin: 8.1.1
- Minecraft: 1.21.1
- Paper: 1.21.1-R0.1-SNAPSHOT
- Forge: 1.21.1-52.0.17

**Subprojects:**
- `titan-core` - Core server functionality
- `titan-api` - API definitions
- `titan-common` - Shared utilities
- `titan-database` - Database integration
- `titan-redis` - Redis cache integration
- `titan-mod-api` - Mod API

**Custom Tasks:**
```bash
# Build all modules
gradle buildAll

# Clean all modules
gradle cleanAll
```

### Python Dependencies

**Developer Console:**
```
customtkinter>=5.2.0
pillow>=10.0.0
python-dotenv>=1.0.0
aiohttp>=3.9.0
```

**Client Launcher:**
```
tkinter
requests>=2.31.0
minecraft-launcher-lib>=6.0
```

---

## Build Process Details

### Phase 1: Prerequisites Check
- Verify Python installation (3.8+)
- Detect Python command (py, python, python3)
- Verify Gradle installation
- Detect Gradle wrapper or system Gradle

### Phase 2: Console Build
- Navigate to `dev-console/`
- Install Python dependencies from `requirements-dev-console.txt`
- Verify imports work
- Time: ~10-30 seconds

### Phase 3: Launcher Build
- Navigate to `client-launcher/`
- Install Python dependencies from `requirements.txt`
- Verify Minecraft launcher lib
- Time: ~10-30 seconds

### Phase 4: Gradle Build
- Run `gradlew buildAll` or `gradle buildAll`
- Build all subprojects in parallel
- Generate JAR artifacts
- Run tests (optional)
- Time: ~30-120 seconds (depends on modules)

### Phase 5: Artifact Deployment
- Scan `build/libs/` directories
- Filter out sources/javadoc JARs
- Copy to `server-mods/`
- Calculate checksums
- Time: ~1-5 seconds

### Phase 6: Validation
- Check all critical files exist
- Verify JAR integrity
- Test imports (optional)
- Generate build report

---

## Build Artifacts

### Output Locations

**Gradle Build Output:**
```
build/
├── libs/
│   ├── titan-core-1.0.0-ALPHA.jar
│   ├── titan-api-1.0.0-ALPHA.jar
│   └── ...
└── reports/
    └── tests/
```

**Subproject Outputs:**
```
titan-core/build/libs/
titan-api/build/libs/
titan-common/build/libs/
...
```

**Deployment Location:**
```
server-mods/
├── titan-core-1.0.0-ALPHA.jar
├── titan-api-1.0.0-ALPHA.jar
└── ...
```

---

## Build from Developer Console

### Using Modern Builder UI

**Step 1: Open Builder**
- Launch console
- Navigate to **🔨 Builder** in sidebar

**Step 2: Configure Build**
- **Project Path:** Auto-detected (or browse)
- **Build Task:** Select from dropdown
  - `build` - Standard build
  - `clean build` - Clean first
  - `jar` - JAR only
  - `shadowJar` - Fat JAR
  - `buildAll` - All modules
  - `cleanAll` - Clean all
- **Options:**
  - ☑ Auto-deploy to server-mods
  - ☐ Clean before build

**Step 3: Execute Build**
- Click **🔨 BUILD PROJECT** button
- Watch real-time output
- Monitor status indicator
- Wait for completion

**Step 4: Results**
- **Success:** Green indicator, "SUCCESS" status
- **Failed:** Red indicator, "FAILED" status
- View detailed output in console
- Check server-mods for deployed JARs

### Quick Actions
- **🔨 BUILD PROJECT** - Start build with current settings
- **🧹 CLEAN PROJECT** - Clean build artifacts
- **⏹ STOP BUILD** - Terminate running build

---

## Troubleshooting

### Build Fails: "Python not found"
**Solution:** Install Python 3.8+ from python.org

### Build Fails: "Gradle not found"
**Solution:** 
1. Use Gradle wrapper (gradlew.bat or ./gradlew)
2. Or install Gradle: https://gradle.org/install/

### Build Fails: "build.gradle not found"
**Solution:** Ensure you're in correct project directory

### Build Fails: "Permission denied"
**Windows:** Run as Administrator  
**Linux/Mac:** `chmod +x BUILD-GALION-PLATFORM.sh`

### Build Fails: Dependencies error
**Solution:**
```bash
# Reinstall dependencies
py -m pip install -r requirements.txt --force-reinstall
```

### Build Hangs
**Solution:** Click **⏹ STOP BUILD** in console or Ctrl+C in terminal

---

## Performance Optimization

### Fast Builds
```bash
# Skip tests
gradle build -x test

# Parallel builds (default in buildAll)
gradle buildAll --parallel

# Offline mode (if dependencies cached)
gradle build --offline
```

### Incremental Builds
Gradle automatically handles incremental builds:
- Only rebuilds changed files
- Caches dependencies
- Reuses artifacts

**Average Times:**
- First Build: 60-120 seconds
- Incremental: 10-30 seconds
- Console/Launcher: 10-20 seconds each

---

## Continuous Integration

### Automated Builds

**On Code Change:**
```bash
# Watch and rebuild
gradle build --continuous
```

**Pre-commit Hook:**
```bash
# .git/hooks/pre-commit
#!/bin/bash
py build_system.py --console-only --launcher-only
```

---

## Build Profiles

### Development Build (Fast)
```bash
py build_system.py --no-deploy
```
- No artifact deployment
- Faster iteration

### Production Build (Complete)
```bash
py build_system.py --clean
```
- Clean build
- All components
- Deploy artifacts
- Validate integrity

### Testing Build
```bash
gradle test
gradle buildAll
```
- Run all tests
- Generate test reports
- Check coverage

---

## Success Criteria

### Successful Build Indicators
- ✅ All components show "SUCCESS"
- ✅ Build time reasonable (< 2 minutes)
- ✅ JARs present in build/libs
- ✅ Artifacts deployed to server-mods
- ✅ No error messages
- ✅ Console launches successfully

### Build Output Verification
```bash
# Check JARs exist
ls build/libs/*.jar
ls server-mods/*.jar

# Check console
py dev-console/console_main.py

# Check launcher
py client-launcher/galion-launcher.py
```

---

## Advanced Usage

### Custom Build Scripts

**Build Specific Module:**
```bash
gradle :titan-core:build
```

**Build with Profile:**
```bash
gradle build -Pprofile=production
```

**Generate Distribution:**
```bash
gradle assembleDist
```

### Integration with IDEs

**IntelliJ IDEA:**
1. Import Gradle project
2. Sync Gradle
3. Run > Build Project
4. Or use terminal: `./gradlew build`

**VS Code:**
1. Open folder
2. Terminal > Run Task
3. Select "gradle: build"

---

## Maintenance

### Clean Old Builds
```bash
gradle cleanAll
rm -rf build/
rm -rf */build/
```

### Update Dependencies
```bash
# Python
py -m pip install --upgrade -r requirements.txt

# Gradle
gradle wrapper --gradle-version 8.5
```

### Reset Build System
```bash
# Delete caches
rm -rf .gradle/
rm -rf build/
gradle clean
```

---

## FAQ

**Q: How long does a full build take?**  
A: First build: 1-2 minutes. Incremental: 10-30 seconds.

**Q: Can I build without Gradle?**  
A: Yes, console and launcher are Python-only. Use `py build_system.py --console-only`

**Q: Where are built JARs?**  
A: `build/libs/` for each module, deployed to `server-mods/`

**Q: How do I stop a build?**  
A: Click **⏹ STOP BUILD** in console or press Ctrl+C in terminal

**Q: Can I build on Linux/Mac?**  
A: Yes, use BUILD-GALION-PLATFORM.sh or build_system.py

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `BUILD-GALION-PLATFORM.cmd` | Build all (Windows) |
| `./BUILD-GALION-PLATFORM.sh` | Build all (Linux/Mac) |
| `py build_system.py` | Build all (Python) |
| `py build_system.py --clean` | Clean build |
| `py build_system.py --console-only` | Console only |
| `gradle buildAll` | Gradle modules only |

---

## Support

**Documentation:** This file  
**Logs:** Check build output in console  
**Issues:** Review error messages in build output  

---

**STATUS: BUILD SYSTEM COMPLETE** ✅

All build methods implemented and tested.  
Ready for production use.

