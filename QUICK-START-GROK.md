# 🚀 Grok Console Chat - QUICK START

Get up and running in 5 minutes!

## Step 1: Get Your API Key

1. Go to: **https://console.x.ai/**
2. Sign up or log in
3. Create an API key
4. Copy your key (starts with `xai-...`)

## Step 2: Configure

1. **Copy the example config:**
   ```cmd
   copy .env.grok.example .env.grok
   ```

2. **Edit `.env.grok`** and replace `your-xai-api-key-here` with your actual key:
   ```
   XAI_API_KEY=xai-your-actual-key-here
   ```

## Step 3: Install Dependencies

```cmd
pip install -r requirements-grok.txt
```

This installs:
- FastAPI (API server)
- aiohttp (async HTTP)
- colorama (colored console)
- prompt_toolkit (rich console)
- mcrcon (Minecraft RCON)
- python-dotenv (environment config)

## Step 4: Choose Your Mode

### Option A: Interactive Console (Recommended)

**Windows:**
```cmd
START-CONSOLE-CHAT.cmd
```

**Linux/Mac:**
```bash
python console-chat.py
```

**What you get:**
- Interactive terminal with colors
- AI chat with Grok
- Minecraft server commands
- Project control (git, build, docker)
- Command history

**Try these commands:**
```
@ai What is redstone?
/say Hello from console!
@project status
/status
```

### Option B: In-Game AI Bridge

Players can chat with AI in Minecraft!

**Windows:**
```cmd
START-GROK-BRIDGE.cmd
```

Choose:
1. **NANO Bridge** - Minimal, fastest startup
2. **INSTANT Bridge** - Ultra-fast responses
3. **FAST Bridge** - Full-featured with streaming

**In Minecraft, players type:**
```
console what is redstone?
@ai how do I craft a piston?
hey console help me
```

### Option C: REST API Server

For web apps, mobile apps, or automation.

**Windows:**
```cmd
START-CHAT-SERVER.cmd
```

**Linux/Mac:**
```bash
python chat-server.py
```

**Access:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

**Example API call:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What is redstone?","player_name":"Console"}'
```

## 🎯 Common Tasks

### Ask AI a Question
```
@ai How do I create a Bukkit plugin?
@ai What is the /give command?
```

### Control Minecraft Server
```
/say Server restarting in 5 minutes!
/list
/time set day
/gamemode creative PlayerName
/whitelist add NewPlayer
```

### Manage Your Project
```
@project status        # Git status
@project log           # Recent commits
@project docker        # List containers
@project logs          # View logs
@project build         # Build project
```

### System Status
```
/status    # See stats, response times, cache hit rates
/help      # Show all commands
```

## 🔧 Troubleshooting

### "XAI_API_KEY not set"
➡️ Edit `.env.grok` and add your API key

### "RCON not connected"
➡️ Make sure Minecraft server is running:
```cmd
docker ps
```
If not running, start it with:
```cmd
docker-compose up -d
```

### "Module not found"
➡️ Install dependencies:
```cmd
pip install -r requirements-grok.txt
```

### Slow Responses
1. Check your internet connection
2. Check Grok API status: https://x.ai/status
3. Try clearing cache (in console: check `/status` for cache stats)

## 📊 Performance

Expected performance:
- **AI responses:** 0.3 - 0.8 seconds (typical)
- **Cache hits:** < 0.01 seconds (instant!)
- **RCON commands:** 30 - 50 ms
- **Complete workflow:** < 1.5 seconds

## 🎓 Learn More

**Full Documentation:** `GROK-CONSOLE-README.md`

**Test the System:**
```bash
python test-grok-system.py
```

**API Documentation:**
Start the server and visit: http://localhost:8000/docs

## 💡 Pro Tips

1. **Use short questions** for faster AI responses
2. **Cache hits are instant** - ask the same question twice to see!
3. **Use /status** to monitor performance
4. **Arrow keys** navigate command history
5. **Tab** for auto-completion hints

## 🎮 Example Session

```
> @ai What is redstone?
🤔 Asking Grok...
⚡ Grok responded in 0.487s
🤖 Grok: Redstone is Minecraft's electrical system...

> /say Hello everyone!
✓ Sent to Minecraft

> @project status
 M console-chat.py
 M README.md

> /status
==========================================================
  SYSTEM STATUS
==========================================================

✓ Grok AI:
  Requests: 5
  Cache hits: 2 (40.0%)
  Avg response: 0.521s
  Fastest: 0.312s

✓ Minecraft RCON:
  Commands: 3
  Success rate: 100.0%
  Avg time: 0.042s
```

## 🆘 Need Help?

1. Check `GROK-CONSOLE-README.md` for detailed docs
2. Run `/help` in the console
3. Check API docs at `/docs` endpoint
4. Review `GROK-SYSTEM-COMPLETE.md` for architecture

## ✅ You're Ready!

Start with:
```cmd
START-CONSOLE-CHAT.cmd
```

Then type:
```
@ai Hello, can you help me with Minecraft?
```

**Enjoy your ultra-fast AI-powered console!** ⚡

---

**Project:** mc.galion.studio | **Powered by:** Grok-4 Fast | **Status:** ✅ READY

