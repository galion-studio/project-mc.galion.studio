# 🎮 Master Control - All Launch Commands

**Quick reference for all launch and control commands**

---

## 🚀 Main Launchers

### Recommended: Quick Launch Console
```bash
QUICK-LAUNCH-CONSOLE-ONLY.cmd
```
✅ Fastest way to launch just the GUI console

### PowerShell Version
```powershell
.\Launch-Console.ps1
```
✅ PowerShell-friendly launcher with validation

### Full System Restart
```bash
RESTART-AND-RUN-ALL.cmd
```
✅ Stops everything, installs deps, launches all services

### Terminal Version (No GUI)
```bash
VIEW-CONFIG-TERMINAL.cmd
```
✅ Command-line interface, perfect for SSH

---

## 🛑 Stop & Control

### Stop All Services
```bash
STOP-ALL-SERVICES.cmd
```

### Check What's Running
```bash
CHECK-SERVICES-STATUS.cmd
```

### View Logs
```bash
VIEW-LOGS.cmd
```

---

## 🧪 Testing & Validation

### Test Setup
```bash
TEST-TRANSPARENT-CONSOLE.cmd
```
Validates:
- Python installation
- Required packages
- Configuration files

### Test Config Manager
```bash
cd dev-console
py config_manager.py
```

### Test Terminal Viewer
```bash
cd dev-console
py terminal_config_viewer.py
```

---

## 📊 Status & Monitoring

### Current Status
```bash
# Read status file
type RUNNING-NOW-STATUS.md
```

### Check Services
```bash
CHECK-SERVICES-STATUS.cmd
```

### View Running Processes
```powershell
Get-Process python
```

---

## 🔧 Direct Python Commands

### Launch Console (Python)
```bash
cd dev-console
py transparent_console.py
```

### Launch Terminal Viewer (Python)
```bash
cd dev-console
py terminal_config_viewer.py
```

### Test Configuration (Python)
```bash
cd dev-console
py config_manager.py
```

---

## 📝 Configuration Files

### Edit AI Configuration
```bash
notepad .env.grok
```

### Edit Server Configuration
```bash
notepad .env
```

### View in Console
```bash
QUICK-LAUNCH-CONSOLE-ONLY.cmd
# Then go to Configuration tab
```

---

## 💡 Common Workflows

### First Time Setup
```bash
1. TEST-TRANSPARENT-CONSOLE.cmd       # Validate setup
2. QUICK-LAUNCH-CONSOLE-ONLY.cmd      # Launch console
3. Go to "Secrets & API Keys" tab     # Add your keys
4. Click "Save All Changes"           # Save
```

### Daily Use
```bash
QUICK-LAUNCH-CONSOLE-ONLY.cmd        # Fast launch
```

### Full System Restart
```bash
1. STOP-ALL-SERVICES.cmd              # Stop everything
2. RESTART-AND-RUN-ALL.cmd            # Restart all
```

### Quick Config Check
```bash
VIEW-CONFIG-TERMINAL.cmd              # Terminal viewer
# Choose option 7 (Validate)
```

### SSH/Remote Access
```bash
VIEW-CONFIG-TERMINAL.cmd              # No GUI needed
```

---

## 🎯 Which Launcher Should I Use?

### For Normal Use:
```bash
QUICK-LAUNCH-CONSOLE-ONLY.cmd
```
**Why:** Fast, simple, launches just the GUI

### For PowerShell Users:
```powershell
.\Launch-Console.ps1
```
**Why:** Better PowerShell integration

### For Full System:
```bash
RESTART-AND-RUN-ALL.cmd
```
**Why:** Launches console + chat server + AI bridge

### For SSH/Terminal:
```bash
VIEW-CONFIG-TERMINAL.cmd
```
**Why:** No GUI required

### For Testing:
```bash
TEST-TRANSPARENT-CONSOLE.cmd
```
**Why:** Validates everything first

---

## 🔍 Troubleshooting Commands

### Python Not Found
```bash
py --version                          # Check if Python installed
where py                              # Find Python location
```

### Dependencies Missing
```bash
py -m pip install -r requirements.txt # Install all
py -m pip install customtkinter       # Install specific package
```

### Configuration Issues
```bash
cd dev-console
py config_manager.py                  # Test config
```

### Port Already in Use
```bash
netstat -ano | findstr :8000         # Check port 8000
taskkill /F /IM python.exe           # Stop Python processes
```

### Console Won't Start
```bash
TEST-TRANSPARENT-CONSOLE.cmd         # Diagnose issues
```

---

## 📱 Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│  QUICK COMMANDS                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Launch Console:        QUICK-LAUNCH-CONSOLE-ONLY.cmd  │
│  PowerShell:            .\Launch-Console.ps1           │
│  Terminal:              VIEW-CONFIG-TERMINAL.cmd       │
│  Full Restart:          RESTART-AND-RUN-ALL.cmd        │
│                                                         │
│  Stop All:              STOP-ALL-SERVICES.cmd          │
│  Check Status:          CHECK-SERVICES-STATUS.cmd      │
│  Test Setup:            TEST-TRANSPARENT-CONSOLE.cmd   │
│  View Logs:             VIEW-LOGS.cmd                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🎨 GUI Console Tabs

Once launched, you have 4 tabs:

1. **📋 Configuration** - View all settings
2. **💻 Console** - Interactive terminal
3. **🎮 Server Control** - Quick actions
4. **🔑 Secrets & API Keys** - Edit everything

---

## 📚 Documentation Quick Links

- **This File:** `MASTER-CONTROL.md`
- **Complete Guide:** `TRANSPARENT-CONSOLE-COMPLETE.md`
- **Quick Start:** `QUICK-START-CONSOLE.txt`
- **Current Status:** `RUNNING-NOW-STATUS.md`
- **Launch Info:** `README-CONSOLE-LAUNCH.txt`
- **Features:** `dev-console/FEATURES.md`
- **Visual Guide:** `dev-console/VISUAL-GUIDE.md`

---

## ⚡ Power User Tips

### 1. Create Shortcut
Right-click `QUICK-LAUNCH-CONSOLE-ONLY.cmd` → Send to → Desktop

### 2. Run from Anywhere
Add project directory to PATH

### 3. Alias in PowerShell
```powershell
Set-Alias console "C:\path\to\Launch-Console.ps1"
```

### 4. Background Launch
```bash
start /b QUICK-LAUNCH-CONSOLE-ONLY.cmd
```

### 5. Auto-start
Add to Windows Startup folder

---

**Remember:** The console shows all secrets for transparency!

Keep it secure 🔒

---

*Built with ❤️ for mc.galion.studio*

*Full Transparency • Complete Control • Developer First*

