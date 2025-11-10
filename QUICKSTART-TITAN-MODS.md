# 🚀 TITAN FORGE MOD SYSTEM - QUICKSTART

## ONE-COMMAND DEPLOYMENT

```cmd
SHIP-MVP-NOW.cmd
```

**That's it!** Everything else is automatic.

---

## WHAT YOU GET

### ✅ Running Services

1. **Mod Sync API** - `http://localhost:8080`
   - Automatically discovers mods
   - Serves parallel downloads
   - Verifies checksums

2. **AI Bridge** - Grok 4 Fast
   - In-game chat responses
   - <1 second latency
   - Natural language

3. **Minecraft Server** - `localhost:25565`
   - Docker-based
   - Auto-configured
   - Ready to connect

---

## ADD MODS (2 MINUTES)

### Step 1: Download Mods
Go to [CurseForge](https://www.curseforge.com/minecraft/mc-mods) or [Modrinth](https://modrinth.com/)

**Requirements:**
- Minecraft version: **1.21.1**
- Mod Loader: **Forge 52.0.29**

### Step 2: Copy to Server
```cmd
# Copy .jar files to:
server-mods\
```

### Step 3: Restart Mod Sync
```cmd
# Just stop and start the server
# It auto-detects new mods
py mod-sync-server.py
```

**Done!** Clients will auto-download on next launch.

---

## CLIENT SETUP

### Option 1: Use Our Launcher (Easiest)
```cmd
client-launcher\dist\GalionLauncher-Enhanced-Final.exe
```

The launcher:
- Auto-connects to server
- Downloads required mods
- Installs Forge
- One-click launch

### Option 2: Manual Setup
1. Install Forge 1.21.1-52.0.29
2. Download mods from `http://localhost:8080/api/mods/manifest`
3. Place in `.minecraft/mods/`
4. Connect to `localhost:25565`

---

## TEST THE SYSTEM

### Test 1: Check API
```bash
curl http://localhost:8080/health
```

Expected response:
```json
{
  "status": "healthy",
  "mods_available": 2,
  "total_size_mb": 10.5,
  "supports_parallel": true
}
```

### Test 2: View Mod List
```bash
curl http://localhost:8080/api/mods/manifest
```

### Test 3: Download a Mod
```
http://localhost:8080/api/mods/download/YourMod-1.0.0.jar
```

### Test 4: In-Game AI
1. Connect to server
2. Type in chat: `hey console, what is redstone?`
3. Get instant AI response

---

## DIRECTORY STRUCTURE

```
project-mc-serv-mc.galion.studio/
├── server-mods/              # ← Add your .jar mods here
├── mod-sync-server.py        # Mod distribution server
├── ai-bridge/
│   └── instant.py            # AI chat bridge
├── client-launcher/
│   └── dist/
│       └── GalionLauncher-Enhanced-Final.exe
├── titan-mod-api/            # Forge mod API (Java)
├── examples/
│   └── example-mod/          # Example Forge mod
└── SHIP-MVP-NOW.cmd          # ← Run this!
```

---

## COMMON TASKS

### Add a New Mod
```cmd
# 1. Download .jar
# 2. Copy to server-mods\
copy Downloads\CoolMod-1.0.jar server-mods\

# 3. Restart mod-sync-server
# Clients auto-update on next launch
```

### Remove a Mod
```cmd
# 1. Delete from server-mods\
del server-mods\OldMod-1.0.jar

# 2. Restart mod-sync-server
```

### Update a Mod
```cmd
# 1. Replace old version with new
copy Downloads\CoolMod-2.0.jar server-mods\
del server-mods\CoolMod-1.0.jar

# 2. Restart mod-sync-server
```

### View Server Logs
```cmd
docker logs -f titan-hub
```

### Check What's Running
```cmd
docker ps
```

---

## TROUBLESHOOTING

### Mod Sync Server Won't Start
```cmd
# Check if port 8080 is in use
netstat -ano | findstr :8080

# Or use different port
# Edit mod-sync-server.py: port=8080 → port=8081
```

### Client Can't Download Mods
1. Check firewall allows port 8080
2. Verify server is running: `curl localhost:8080/health`
3. Check `server-mods\` has .jar files

### AI Bridge Not Responding
1. Check `.env.grok` has API key
2. Verify Docker is running
3. Check AI bridge window for errors

### Mods Not Loading in Minecraft
1. Verify Forge version: 1.21.1-52.0.29
2. Check mod compatibility
3. Look at client logs: `.minecraft/logs/latest.log`

---

## PERFORMANCE TIPS

### Speed Up Downloads
- **Parallel**: Client downloads 5 mods at once automatically
- **Cache**: Mods cached locally (won't re-download)
- **Resume**: Failed downloads auto-resume

### Optimize Server
- Use SSD for `server-mods/`
- Enable caching in reverse proxy
- Consider CDN for public servers

---

## ADVANCED: BUILD JAVA MODS

**When Gradle is installed:**

```cmd
# 1. Create Gradle wrapper
gradle wrapper

# 2. Build all mods
.\gradlew build

# 3. Auto-collect to server-mods
.\BUILD-ALL-MODS.cmd
```

**Mod Development:**
```java
@Mod("your_mod_id")
public class YourMod extends TitanMod {
    public YourMod(IEventBus bus, ModContainer container) {
        super(bus, container);
    }
    
    @Override
    protected void commonSetup(FMLCommonSetupEvent event) {
        // Your mod logic here
    }
}
```

See `examples/example-mod/` for complete example.

---

## API REFERENCE (Quick)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/mods/manifest` | GET | List all mods |
| `/api/mods/download/{file}` | GET | Download mod |
| `/api/mods/verify/{file}` | GET | Check checksum |
| `/health` | GET | Server status |
| `/` | GET | API info |

**Full API Docs**: `http://localhost:8080/docs`

---

## SUPPORT & DOCS

- **Full Documentation**: `TITAN-MVP-COMPLETE.md`
- **Architecture Plan**: `TITAN-BUILD-PLAN-MUSK-STYLE.md`
- **Deployment Guide**: `SHIP-MVP-NOW.cmd`

---

## 🎯 SUCCESS CHECKLIST

Before connecting clients:

- [ ] `SHIP-MVP-NOW.cmd` executed
- [ ] Mod sync server responding at port 8080
- [ ] At least 1 mod in `server-mods/`
- [ ] Docker services running
- [ ] AI bridge active (optional)

---

**Time to First Mod**: <5 minutes  
**Time to Add More Mods**: <1 minute  
**Client Setup**: Automatic

**SHIP IT!** 🚀

