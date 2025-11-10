# 📦 Plugin Download Guide

## Quick Plugin Installation

Most plugins require manual download due to website restrictions. Follow these steps:

### ✅ Method 1: Manual Download (Recommended)

Download these plugins and place them in `worlds/hub/plugins/` folder:

#### Essential Plugins

1. **WorldEdit** (Building tool)
   - Download: https://dev.bukkit.org/projects/worldedit/files
   - Get latest version for 1.21.1
   - File: `worldedit-bukkit-7.x.x.jar`

2. **EssentialsX** (Core commands)
   - Download: https://essentialsx.net/downloads.html
   - Get EssentialsX Core
   - File: `EssentialsX-2.x.x.jar`

3. **LuckPerms** (Permissions)
   - Download: https://luckperms.net/download
   - Select "Bukkit/Spigot"
   - File: `LuckPerms-Bukkit-5.x.x.jar`

4. **CoreProtect** (Logging/Rollback)
   - Download: https://www.spigotmc.org/resources/coreprotect.8631/
   - Or: https://github.com/PlayPro/CoreProtect/releases
   - File: `CoreProtect-xx.x.jar`

5. **Vault** ✅ (Already installed!)
   - Economy API
   - File: `Vault.jar`

6. **GriefPrevention** (Land protection)
   - Download: https://www.spigotmc.org/resources/griefprevention.1884/
   - File: `GriefPrevention-xx.x.x.jar`

#### Optional Plugins

7. **Citizens** (NPCs)
   - Download: https://ci.citizensnpcs.co/job/Citizens2/
   - File: `Citizens-2.x.x.jar`

8. **WorldGuard** (Region protection)
   - Download: https://dev.bukkit.org/projects/worldguard/files
   - File: `worldguard-bukkit-7.x.x.jar`

9. **Multiverse-Core** (Multiple worlds)
   - Download: https://dev.bukkit.org/projects/multiverse-core/files
   - File: `multiverse-core-4.x.x.jar`

### 📥 After Downloading

1. Place all `.jar` files in: `worlds/hub/plugins/`
2. Restart your server
3. Check plugins loaded: `/plugins` command

### 🎮 First Time Setup

```bash
# 1. Make yourself admin
/op YourUsername

# 2. Check plugins
/plugins

# 3. Test WorldEdit
//wand
```

### 📖 Quick Commands

**WorldEdit:**
- `//wand` - Get selection tool
- `//set [block]` - Fill selection
- `//copy` - Copy selection
- `//paste` - Paste copied blocks
- `//undo` - Undo last action

**EssentialsX:**
- `/spawn` - Go to spawn
- `/sethome [name]` - Set home
- `/home [name]` - Teleport home
- `/tpa [player]` - Request teleport
- `/tpaccept` - Accept teleport

**GriefPrevention:**
- `/abandonclaim` - Remove claim
- `/trust [player]` - Give access
- `/untrust [player]` - Remove access
- `/claimlist` - List your claims

---

Made with ❤️ by galion.studio

