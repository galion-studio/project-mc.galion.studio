# 🚀 Server Modes - Quick Start

## Choose Your Mode

### 🏠 LOCAL MODE - Self-Hosted (Offline)

**Perfect for:**
- Playing without internet
- LAN parties
- Development/Testing
- Privacy-focused hosting

**Start Now:**
```cmd
START-LOCAL-SERVER.cmd
```

**Features:**
- ✅ Fully offline
- ✅ No API keys needed
- ✅ Open source
- ❌ No AI features

**Server:** `localhost:25565`

---

### 🌐 OFFICIAL MODE - Full Featured (Online)

**Perfect for:**
- AI-powered gameplay
- Online multiplayer
- Premium features
- Managed hosting

**Start Now:**
```cmd
START-OFFICIAL-SERVER.cmd
```

**Features:**
- ✅ AI integration (Grok 4 Fast)
- ✅ Online multiplayer
- ✅ Premium features
- ⚠️ Requires internet

**Server:** `mc.galion.studio:25565`

---

## Setup AI (Official Mode Only)

```cmd
SETUP-GROK-NOW.cmd
```

Get API key: https://openrouter.ai/keys ($1 free credit)

---

## Switch Modes Anytime

**Using Launcher:**
1. Open launcher
2. Go to **Server Mode** tab
3. Choose mode
4. Click **Confirm**

**Using Command Line:**
```python
from server_mode_config import ServerModeManager, ServerMode

manager = ServerModeManager()
manager.set_mode(ServerMode.LOCAL)  # or ServerMode.OFFICIAL
```

---

## Need Help?

See full documentation: [SERVER-MODES-GUIDE.md](SERVER-MODES-GUIDE.md)

---

**Made with ❤️ by [galion.studio](https://galion.studio)**

