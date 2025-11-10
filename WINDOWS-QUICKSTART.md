# 🎮 TITAN SERVER - Windows Quick Start

**For**: Local development and testing  
**Time**: 2 minutes  
**Requirements**: Docker Desktop

---

## ⚡ ULTRA-FAST START (3 Steps)

### 1. Make Sure Docker Desktop is Running
- Look for Docker icon in system tray
- Should say "Docker Desktop is running"

### 2. Double-Click This File
```
START-SERVER.cmd
```

### 3. Wait for "Done!" Message
- Window will show server starting
- Wait 1-2 minutes
- Look for: `[Server thread/INFO]: Done!`

**That's it!** ✅

---

## 🎮 CONNECT TO SERVER

**Open Minecraft TLauncher:**
1. Select version: **1.21.1**
2. Multiplayer → Add Server
3. Server address: `localhost:25565`
4. Join and play!

---

## 🎯 ONE-CLICK MANAGEMENT

| File | What It Does |
|------|-------------|
| **START-SERVER.cmd** | Start server + show logs |
| **STOP-SERVER.cmd** | Stop all services |
| **VIEW-LOGS.cmd** | Watch live logs |
| **RESTART-SERVER.cmd** | Quick restart |

**Just double-click!** No commands needed!

---

## 🔧 Try These Commands In-Game

Once connected, type:

```
/titan          Show server info
/players        List online players
/tps            Check performance
/server         Server menu
```

---

## 📊 Access Monitoring

**Grafana Dashboard:**
- URL: `http://localhost:3000`
- Username: `admin`
- Password: `admin`

**Prometheus:**
- URL: `http://localhost:9090`

---

## 🐛 Troubleshooting

### Server won't start?

**Check Docker:**
```powershell
docker ps
```

**Restart Docker Desktop**, then run `START-SERVER.cmd` again

### Can't connect?

**Check if server is ready:**
```powershell
docker-compose logs | Select-String "Done"
```

Look for: `[Server thread/INFO]: Done!`

### Port already in use?

```powershell
# Find what's using port 25565
netstat -ano | findstr :25565

# Kill the process or restart computer
```

---

## 💡 Tips

**Faster Restarts:**
- Use `RESTART-SERVER.cmd` instead of stop + start
- Keeps data, just restarts services

**View Logs Without Restarting:**
- Double-click `VIEW-LOGS.cmd` anytime
- Press Ctrl+C to close (server keeps running)

**Share with Friends (LAN):**
- Find your local IP: `ipconfig`
- Share: `YOUR_IP:25565`
- Friends on same network can join!

---

## ✅ What You Get

- ✅ Full Minecraft server running
- ✅ Monitoring dashboards
- ✅ Database (PostgreSQL)
- ✅ Cache (Redis)
- ✅ Custom commands
- ✅ Performance tracking
- ✅ Easy management (double-click)

---

## 🚀 Ready for Production?

See: **VPS-DEPLOYMENT-GUIDE.md**

Deploy to VPS (mc.galion.studio) for:
- Public access
- 100+ players
- 24/7 uptime
- Better performance

---

**🎮 DOUBLE-CLICK START-SERVER.cmd AND PLAY!** ⚡



