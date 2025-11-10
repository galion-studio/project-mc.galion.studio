# 🎮 GALION Custom .minecraft Folder

**Custom Minecraft configuration for mc.galion.studio**

This is YOUR custom `.minecraft` folder with:
- ✅ Optimized settings for the server
- ✅ Grok AI integration
- ✅ Custom launcher profile
- ✅ Admin account configuration

---

## 📦 What's Inside

```
.minecraft-custom/
├── galion-launcher-profile.json    # Custom launcher profile
├── options.txt                      # Optimized game settings
├── servers.dat                      # Pre-configured server
├── grok-config.json                 # Grok AI settings
└── README.md                        # This file
```

---

## 🚀 How It Works

### **The Launcher Uses This Folder**

When you click PLAY in the GALION launcher:
1. Uses settings from this custom folder
2. Applies optimizations
3. Connects to mc.galion.studio automatically
4. Enables Grok AI features

### **Settings Included:**

✅ **Performance Optimized**
- 12 chunk render distance
- 120 FPS cap
- G1GC garbage collector
- 4GB RAM allocation

✅ **Server Pre-Configured**
- Default server: mc.galion.studio
- Auto-connect ready
- Optimized for multiplayer

✅ **Grok AI Integration**
- API key from .env.grok
- AI chat enabled
- Smart assistance
- Voice commands (future)

✅ **Admin Account**
- Default username: galion.studio
- Admin privileges
- Saved preferences

---

## ⚙️ Configuration Files

### **galion-launcher-profile.json**
Custom launcher profile with:
- Optimized JVM arguments
- Resolution settings
- Grok AI configuration
- Custom features

### **options.txt**
Game settings:
- Graphics optimized
- Server pre-set
- Controls configured
- Audio balanced

### **grok-config.json**
AI settings:
- Model: grok-4-fast
- Timeout: 30s
- Max tokens: 200
- Auto-repair: enabled

---

## 🔧 Customization

Edit these files to customize:

**Change server:**
```json
"galion": {
  "server": "your-server.com"
}
```

**Change RAM:**
```
-Xmx4G  →  -Xmx8G  (8GB RAM)
```

**Disable Grok AI:**
```json
"aiEnabled": false
```

---

## 📝 Notes

- This folder is **version controlled** in GitHub
- Players download this with the launcher
- Auto-updates when you push changes
- Transparent and open source

---

**Built with ❤️ for mc.galion.studio**

