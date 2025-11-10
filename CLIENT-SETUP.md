# 🎮 TLAUNCHER CLIENT SETUP GUIDE

## ✅ Server Configuration

**Titan Server is now configured for:**
- Minecraft Version: **1.21.1**
- Client: **TLauncher (Cracked)**
- Forge Compatible: **Yes (1.21.1)**
- Online Mode: **OFF** (No premium required)

---

## 📥 How to Connect with TLauncher

### Step 1: Launch TLauncher
- Open TLauncher 2.9343 (your current version)

### Step 2: Select Version
Choose one of these:
- **Option A**: Minecraft 1.21.1 (Vanilla) - Best performance
- **Option B**: Forge 1.21.1 (Latest) - For mods

### Step 3: Add Server
1. Click **"Multiplayer"**
2. Click **"Add Server"**
3. **Server Name**: Titan Server
4. **Server Address**: `localhost:25565`
5. Click **"Done"**

### Step 4: Connect
1. Select "Titan Server" from your server list
2. Click **"Join Server"**
3. **No authentication needed!** ✅

---

## 🎮 Recommended TLauncher Settings

### For Best Performance:
```
Version: Minecraft 1.21.1 (Vanilla)
RAM: 4GB minimum, 8GB recommended
Settings:
  - Render Distance: 8-12 chunks
  - Graphics: Fast
  - Smooth Lighting: Minimum
  - VSync: OFF (for higher FPS)
```

### For Mods:
```
Version: Forge 1.21.1-52.0.17
RAM: 6GB minimum, 10GB recommended
Mods: Place in .minecraft/mods folder
```

---

## 🔧 TLauncher Configuration

### Memory Allocation (Important!)

1. Click **Settings** (gear icon) in TLauncher
2. Go to **"Java"** tab
3. Set RAM:
   ```
   Minimum: -Xms2G
   Maximum: -Xmx4G
   
   (For mods: -Xms4G -Xmx8G)
   ```

### Java Arguments (Optional - Better Performance):
```bash
-XX:+UseG1GC 
-XX:+UnlockExperimentalVMOptions 
-XX:G1NewSizePercent=20 
-XX:G1ReservePercent=20 
-XX:MaxGCPauseMillis=50 
-XX:G1HeapRegionSize=32M
```

---

## 🌐 Connection Info

| Setting | Value |
|---------|-------|
| **Server IP** | `localhost:25565` |
| **Version** | 1.21.1 |
| **Online Mode** | OFF (Cracked OK) |
| **Username** | Any name you want |
| **Password** | Not required |

---

## 🐛 Troubleshooting

### "Incompatible Client" Error
**Solution**: Make sure you're using Minecraft 1.21.1
```
TLauncher → Select Version → 1.21.1
```

### Can't Connect
**Solution**: Check if server is running
```powershell
docker-compose ps
# All services should show "Up"
```

### Connection Timeout
**Solution**: Restart servers
```powershell
docker-compose restart titan-hub titan-survival
```

### Mods Not Working
**Solution**: 
1. Use Forge 1.21.1 (not vanilla)
2. Check mods are compatible with 1.21.1
3. Place mods in `.minecraft/mods` folder

---

## 📦 Recommended Mods (Optional)

Compatible with Titan Server 1.21.1:

### Performance Mods:
- **Optifine** - Better FPS and graphics
- **Sodium** - Rendering optimization
- **Lithium** - Server optimization
- **Phosphor** - Lighting engine optimization

### Utility Mods:
- **JEI (Just Enough Items)** - Recipe viewer
- **Minimap** - World navigation
- **Inventory Tweaks** - Better inventory management

---

## 🎯 Testing Your Connection

### Quick Test:
1. Start server: `docker-compose up -d`
2. Wait 60 seconds
3. Open TLauncher
4. Select Minecraft 1.21.1
5. Multiplayer → localhost:25565
6. Join!

### Check Server Status:
```powershell
# Is server running?
docker-compose ps

# View server logs
docker-compose logs titan-hub --tail=50

# Check for errors
docker-compose logs titan-hub | Select-String "error"
```

---

## ✅ What Works

- ✅ TLauncher (cracked client)
- ✅ Minecraft 1.21.1
- ✅ Forge 1.21.1 mods
- ✅ No premium account needed
- ✅ Multiple players (no authentication)
- ✅ Full gameplay features

---

## 🚀 Next Steps

1. **Connect with TLauncher** (localhost:25565)
2. **Test gameplay**
3. **Add friends** (they can use any cracked client)
4. **Install mods** (optional)
5. **Customize server** (plugins, worlds, etc.)

---

## 📞 Need Help?

**Connection issues?**
```powershell
# View detailed logs
docker-compose logs -f

# Restart everything
docker-compose restart
```

**Still problems?** Check:
- Server is running: `docker-compose ps`
- Correct version: Minecraft 1.21.1
- Port 25565 is open
- No firewall blocking

---

**✅ YOU'RE ALL SET! CONNECT AND PLAY! 🎮**

