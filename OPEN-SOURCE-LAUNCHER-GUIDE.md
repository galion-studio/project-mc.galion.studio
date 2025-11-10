# Open Source Minecraft Launcher Deployment Guide

## 🎯 Recommended: Prism Launcher

**Prism Launcher** is the best open-source Minecraft launcher for custom deployments.

### Why Prism Launcher?
✅ **Most Popular** - Actively maintained, large community  
✅ **Cross-Platform** - Windows, Linux, macOS  
✅ **Customizable** - Can be branded for your server  
✅ **Pre-configured** - Set default servers and settings  
✅ **Mod Support** - Easy mod pack distribution  
✅ **Professional** - Used by many Minecraft servers  

---

## 🚀 Quick Deployment Options

### Option 1: Use Official Prism Launcher (Easiest)

**For Your Players:**

1. **Download Prism Launcher**  
   - Windows: https://prismlauncher.org/download/
   - Linux: Available via package managers
   
2. **Pre-configure for Your Server**  
   - Create a custom instance
   - Add mc.galion.studio to servers list
   - Export as modpack
   - Distribute to players

**Advantages:**
- No building required
- Professional and stable
- Regular updates
- Full mod support

---

### Option 2: Custom Branded Prism Launcher

You can fork and brand Prism Launcher with your server name/logo.

#### Steps:

1. **Fork the Repository**
```bash
git clone https://github.com/PrismLauncher/PrismLauncher.git
cd PrismLauncher
```

2. **Customize Branding**
   - Change name to "Galion Studio Launcher"
   - Replace icons/logos
   - Set default server: mc.galion.studio
   - Pre-configure settings

3. **Build for Windows**
```bash
# Install dependencies (see their docs)
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

4. **Distribute**
   - Package the built launcher
   - Share with your community

---

### Option 3: Python OpenLauncher (Simple Customization)

**OpenLauncher** is a lightweight Python launcher, easy to customize.

#### Quick Setup:

```bash
# Clone the repository
git clone https://github.com/CesarGarza55/OpenLauncher.git
cd OpenLauncher

# Install dependencies
pip install -r requirements.txt

# Customize for your server
# Edit config files to add mc.galion.studio

# Run
python main.py
```

**Advantages:**
- Easy to modify (Python code)
- Lightweight
- Simple branding

**Disadvantages:**
- Less features than Prism
- Smaller community

---

## 📦 Recommended Approach: Pre-configured Prism Instance

**Easiest for your players:**

### Step 1: Create Custom Instance

1. Download Prism Launcher
2. Create new instance with desired Minecraft version
3. Add mc.galion.studio to servers.dat
4. Install any required mods
5. Configure settings

### Step 2: Export Instance

1. Right-click instance → Export
2. Choose format (CurseForge, Modrinth, etc.)
3. Save as .zip

### Step 3: Distribute

**Create a simple guide:**

```
GALION STUDIO - QUICK CONNECT GUIDE
====================================

1. Download Prism Launcher:
   https://prismlauncher.org/download/

2. Download our instance pack:
   [Your hosted instance.zip]

3. In Prism Launcher:
   - Click "Add Instance"
   - Choose "Import from zip"
   - Select downloaded instance.zip

4. Click "Launch" - Done!
   Server is pre-configured!
```

---

## 🎨 Custom Branding Guide

If you want a fully branded launcher:

### Prism Launcher Branding

1. **Fork the Repo**
```bash
git clone https://github.com/PrismLauncher/PrismLauncher.git
```

2. **Edit Branding Files**
   - `program_info/CMakeLists.txt` - Change name
   - `launcher/resources/` - Replace icons
   - `launcher/Application.cpp` - Default settings

3. **Set Default Server**
   - Edit default servers.dat
   - Pre-configure mc.galion.studio

4. **Build & Distribute**

---

## 🔧 Alternative Open Source Launchers

### 1. **MultiMC** (Original, Very Stable)
- Repository: https://github.com/MultiMC/Launcher
- Best for: Stability and simplicity
- License: Apache 2.0

### 2. **ATLauncher** (Modpack Focused)
- Repository: https://github.com/ATLauncher/ATLauncher
- Best for: Heavy mod pack usage
- License: GPL-3.0

### 3. **GDLauncher** (Modern UI)
- Repository: https://github.com/gorilla-devs/GDLauncher
- Best for: Modern design
- Built with: Electron (JavaScript)

### 4. **OpenLauncher** (Lightweight Python)
- Repository: https://github.com/CesarGarza55/OpenLauncher
- Best for: Easy customization
- Built with: Python + PyQt5

---

## 💡 My Recommendation

**For mc.galion.studio, I recommend:**

### Approach: Pre-configured Prism Instance

**Why:**
1. **No building required** - Use official Prism Launcher
2. **Professional** - Trusted by millions
3. **Easy for players** - One-click install
4. **Mod support** - If you add mods later
5. **Auto-updates** - Prism handles updates

**Setup Time:** 30 minutes  
**Player Experience:** Download → Import → Play

---

## 🚀 Quick Start: Deploy Prism Instance

Let me help you create a pre-configured instance right now:

### Step 1: Download Prism Launcher
```bash
# Windows
# Download from: https://prismlauncher.org/download/

# Linux
sudo apt install prismlauncher  # Ubuntu/Debian
```

### Step 2: Create Instance
1. Open Prism Launcher
2. Click "Add Instance"
3. Select Minecraft version
4. Name it "Galion Studio"
5. Click "OK"

### Step 3: Configure Server
1. Launch the instance once
2. Go to Multiplayer
3. Add server: mc.galion.studio
4. Save & exit

### Step 4: Export Instance
1. Right-click "Galion Studio" instance
2. Choose "Export Instance"
3. Select "CurseForge" format
4. Save as `GalionStudio-Instance.zip`

### Step 5: Create Player Guide
```markdown
# Quick Connect to Galion Studio

1. Download Prism Launcher: https://prismlauncher.org
2. Download our instance: [link to your hosted zip]
3. Open Prism → Add Instance → Import from zip
4. Select GalionStudio-Instance.zip
5. Click "Launch"
6. Server is already added - just click Join!
```

---

## 📊 Comparison: Custom vs Open Source

### Our Custom Python Launcher
✅ Fully customized branding  
✅ Simple, focused  
✅ Small size (10 MB)  
❌ Limited features  
❌ We maintain it  

### Prism Launcher (Open Source)
✅ Full-featured  
✅ Active development  
✅ Mod support  
✅ Trusted by community  
✅ Auto-updates  
⚠️ Need to customize branding (optional)  

---

## 🎯 Next Steps

**What do you want to do?**

### Option A: Quick & Easy (Recommended)
Use Prism Launcher with pre-configured instance
- **Time:** 30 minutes
- **Effort:** Low
- **Result:** Professional launcher

### Option B: Custom Branded
Fork and build custom Prism Launcher
- **Time:** 2-4 hours
- **Effort:** Medium
- **Result:** Fully branded launcher

### Option C: Keep Our Launcher
Use the Python launcher we built
- **Time:** Already done!
- **Effort:** None
- **Result:** Simple, working launcher

---

## 📝 Licensing Note

All mentioned launchers are open source:
- **Prism Launcher**: GPL-3.0
- **MultiMC**: Apache-2.0
- **OpenLauncher**: MIT

Make sure to comply with their licenses if distributing modified versions.

---

## 🤝 Support Resources

**Prism Launcher:**
- Website: https://prismlauncher.org
- GitHub: https://github.com/PrismLauncher/PrismLauncher
- Discord: https://discord.gg/prismlauncher
- Docs: https://prismlauncher.org/wiki

**Need help?** Let me know which approach you want to take!

