# 🌐 GALION.studio Server Modes Guide

## Overview

GALION.studio Minecraft Server supports **two distinct server modes** to give you flexibility in how you run your server:

1. **🏠 LOCAL MODE** - Self-hosted, offline, no AI features
2. **🌐 OFFICIAL MODE** - Full-featured with AI, requires internet

---

## 🏠 LOCAL MODE (Self-Hosted)

### What is Local Mode?

Local Mode allows you to run your own Minecraft server on localhost **without any internet connection**. This is the **open source mode** available on GitHub.

### Features

✅ **Fully Offline**
- No internet connection required
- Perfect for LAN parties
- Full control over your server

✅ **Self-Hosted Control**
- You own and control everything
- No external dependencies
- Privacy-focused

✅ **Open Source**
- Available on GitHub
- Fully transparent code
- Community-driven development

❌ **Limitations**
- No AI features (Grok, chat assistance)
- No OpenRouter API integration
- Limited to local network play
- No official server features

### When to Use Local Mode

- Playing on LAN without internet
- Testing and development
- Privacy-focused hosting
- Learning server administration
- Running a private server for friends

### Requirements

- **Internet:** Not required
- **API Keys:** Not required
- **Docker:** Optional (recommended)
- **RAM:** 4GB minimum
- **Platform:** Windows, Linux, or Mac

---

## 🌐 OFFICIAL MODE (Online with AI)

### What is Official Mode?

Official Mode connects you to the full-featured GALION.studio server with **complete AI integration** and premium features. This is the **production mode** with all capabilities enabled.

### Features

✅ **Full AI Integration**
- Grok 4 Fast AI responses (<1 second)
- In-game chat assistance
- Natural language commands
- AI-powered features

✅ **Multiplayer Community**
- Connect to official server
- Play with others worldwide
- Regular events and updates

✅ **Premium Features**
- Advanced monitoring
- Auto-updates
- Cloud backup
- Priority support

✅ **24/7 Uptime**
- Always online
- Professional hosting
- Load balanced

### When to Use Official Mode

- Want AI-powered gameplay
- Playing with others online
- Need professional hosting
- Want latest features
- Prefer managed solution

### Requirements

- **Internet:** Required ✓
- **API Keys:** Required (for AI features)
- **Server Address:** mc.galion.studio
- **Account:** GALION.studio account
- **Platform:** Any with internet

---

## 🚀 Quick Start

### Starting Local Server

**Windows:**
```cmd
START-LOCAL-SERVER.cmd
```

**Linux/Mac:**
```bash
./START-LOCAL-SERVER.sh
```

This will:
1. Set server mode to LOCAL
2. Disable AI features
3. Start Minecraft server on localhost:25565

### Starting Official Server

**Windows:**
```cmd
START-OFFICIAL-SERVER.cmd
```

**Linux/Mac:**
```bash
./START-OFFICIAL-SERVER.sh
```

This will:
1. Check internet connection
2. Set server mode to OFFICIAL
3. Verify API keys
4. Start all services (Server + AI)

---

## 🎮 Using the Launcher

### Server Mode Selection in Launcher

The GALION.studio launcher includes a **Server Mode Selector** that lets you choose your mode visually.

**To Access:**
1. Open the launcher
2. Go to **Settings** or **Server Mode** tab
3. Choose your preferred mode
4. Click **Confirm Selection**

**The selector shows:**
- Mode description
- Features comparison
- Internet requirement
- AI availability
- Server address

---

## ⚙️ Configuration

### Switching Modes Manually

You can switch modes programmatically using Python:

```python
from server_mode_config import ServerModeManager, ServerMode

# Create manager
manager = ServerModeManager()

# Set to LOCAL mode
manager.set_mode(ServerMode.LOCAL)

# Set to OFFICIAL mode
manager.set_mode(ServerMode.OFFICIAL)

# Check current mode
current = manager.get_current_mode()
print(f"Current mode: {current.value}")
```

### Configuration Files

Server mode is stored in:
```
config/server_mode.json
```

Example config:
```json
{
    "mode": "local"
}
```

Valid values: `"local"` or `"official"`

---

## 🤖 AI Features

### AI in LOCAL Mode

**Status:** ❌ Disabled

In LOCAL mode, all AI features are automatically disabled:
- No API calls
- No OpenRouter connection
- No Grok integration
- No chat assistance

This allows the server to run completely offline.

### AI in OFFICIAL Mode

**Status:** ✅ Enabled

In OFFICIAL mode, full AI features are available:
- Grok 4 Fast responses
- In-game AI chat
- Natural language commands
- AI-powered assistance

**Setup AI:**
```cmd
SETUP-GROK-NOW.cmd
```

This will:
1. Create `.env.grok` file
2. Prompt for API key
3. Test connection
4. Enable AI features

---

## 📊 Comparison Table

| Feature | LOCAL Mode | OFFICIAL Mode |
|---------|------------|---------------|
| **Internet Required** | ❌ No | ✅ Yes |
| **AI Features** | ❌ Disabled | ✅ Enabled |
| **Open Source** | ✅ Yes | ⚠️ Partial |
| **Self-Hosted** | ✅ Yes | ❌ No |
| **Multiplayer** | ⚠️ LAN Only | ✅ Global |
| **API Keys Needed** | ❌ No | ✅ Yes |
| **Setup Time** | 2 minutes | 5 minutes |
| **Cost** | 🆓 Free | 💰 Premium |
| **Uptime** | Your control | 24/7 |
| **Updates** | Manual | Automatic |

---

## 🛠️ Technical Details

### Architecture Differences

**LOCAL Mode:**
```
┌─────────────────────────┐
│   Minecraft Server      │
│   (localhost:25565)     │
├─────────────────────────┤
│   PostgreSQL            │
│   Redis                 │
│   Grafana/Prometheus    │
└─────────────────────────┘
```

**OFFICIAL Mode:**
```
┌─────────────────────────────┐
│   Minecraft Server          │
│   (mc.galion.studio:25565) │
├─────────────────────────────┤
│   AI Bridge (Grok 4 Fast)   │
│   Chat Integration          │
│   OpenRouter API            │
├─────────────────────────────┤
│   PostgreSQL                │
│   Redis                     │
│   Grafana/Prometheus        │
└─────────────────────────────┘
```

### Docker Compose Files

**LOCAL Mode:**
- Uses: `docker-compose.simple.yml`
- Services: Minecraft, PostgreSQL, Redis, Monitoring
- No AI services

**OFFICIAL Mode:**
- Uses: `docker-compose.yml`
- Services: Full stack + AI Bridge
- All features enabled

---

## 🐛 Troubleshooting

### Local Mode Issues

**Problem:** Server won't start
```cmd
# Check Docker is running
docker --version

# Check ports are free
netstat -ano | findstr ":25565"

# View logs
docker-compose -f docker-compose.simple.yml logs -f
```

**Problem:** Can't connect to localhost
- Check firewall settings
- Verify server is running
- Use `127.0.0.1` instead of `localhost`

### Official Mode Issues

**Problem:** "No internet connection" error
```cmd
# Test internet
ping google.com

# Check DNS
nslookup mc.galion.studio

# Test with different network
```

**Problem:** AI features not working
```cmd
# Setup API keys
SETUP-GROK-NOW.cmd

# Verify configuration
type .env.grok

# Test AI connection
py test-grok-system.py
```

---

## 📖 For Developers

### Checking AI Availability

```python
from ai_feature_controller import AIFeatureController

controller = AIFeatureController()

# Check if AI is available
if controller.is_ai_available():
    print("AI features are enabled")
else:
    print("AI features are disabled")

# Get detailed status
status = controller.get_ai_status()
print(status)
```

### Conditional AI Import

```python
from ai_feature_controller import import_ai_module

# Import AI module only if available
grok = import_ai_module('grok_client', fallback=None)

if grok:
    # Use AI features
    response = grok.get_response("Hello")
else:
    # Graceful fallback
    response = "AI not available"
```

---

## 🔐 Security & Privacy

### LOCAL Mode
- ✅ **No external connections** - completely offline
- ✅ **No data collection** - everything stays local
- ✅ **Full control** - you own all data
- ✅ **Open source** - auditable code

### OFFICIAL Mode
- ⚠️ **Requires internet** - connects to external services
- ⚠️ **API calls** - to OpenRouter for AI features
- ⚠️ **Some data shared** - for AI processing only
- ✅ **Encrypted connections** - TLS for all API calls

---

## 📝 Best Practices

### For LOCAL Mode
1. Use for development and testing
2. Perfect for LAN parties
3. No API keys needed
4. Backup your world regularly
5. Use Docker for easy management

### For OFFICIAL Mode
1. Keep API keys secure
2. Monitor usage to avoid costs
3. Enable automatic backups
4. Use strong passwords
5. Keep server updated

---

## 🆘 Getting Help

### Documentation
- [README.md](README.md) - Main documentation
- [QUICKSTART-TITAN-MODS.md](QUICKSTART-TITAN-MODS.md) - Quick start guide
- [GROK-QUICK-START.md](GROK-QUICK-START.md) - AI setup guide

### Support Channels
- **Website:** [galion.studio](https://galion.studio)
- **GitHub Issues:** Report bugs and feature requests
- **Developer:** Maciej Grajczyk

---

## 📜 License

**LOCAL Mode (Open Source):**
- MIT License
- Free for any use
- Available on GitHub

**OFFICIAL Mode (Premium):**
- Some features not in open source
- Subject to terms of service
- API usage may incur costs

---

## 🎉 Summary

**Choose LOCAL Mode if you want:**
- ✓ Offline play
- ✓ Full control
- ✓ No API keys
- ✓ Open source

**Choose OFFICIAL Mode if you want:**
- ✓ AI features
- ✓ Online multiplayer
- ✓ Managed hosting
- ✓ Latest features

**Both modes are great** - choose based on your needs!

---

**Made with ❤️ by [galion.studio](https://galion.studio)**  
**Developer:** Maciej Grajczyk  
**AI Assistant:** Cursor + Claude Sonnet 4.5  
**Project:** Hobby/Personal

---

*Last Updated: November 2025*

