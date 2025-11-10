# ⚡ DEPLOY RIGHT NOW - 2 MINUTES

## 🚀 STEP 1: CONNECT (30 seconds)

**Open PuTTY (Windows) or Terminal (Mac/Linux)**

```bash
ssh root@54.37.223.40
```

Password: `Phdhxdp10b@(05)A` ← **Right-click to paste in PuTTY**

---

## ⚡ STEP 2: RUN THIS ONE COMMAND (3 minutes)

**Copy-paste this ENTIRE block:**

```bash
apt update && apt install -y docker.io docker-compose && \
mkdir -p /opt/mc && cd /opt/mc && \
cat > docker-compose.yml << 'EOF'
version: '3.9'
services:
  minecraft:
    image: itzg/minecraft-server:java21
    container_name: mc
    ports:
      - "25565:25565"
    environment:
      EULA: "TRUE"
      TYPE: "PAPER"
      VERSION: "1.21.1"
      MEMORY: "6G"
      MAX_PLAYERS: "100"
      MOTD: "§6⚡ MC.GALION.STUDIO ⚡\n§7No Premium | Join Now!"
      ONLINE_MODE: "FALSE"
      VIEW_DISTANCE: "8"
      DIFFICULTY: "hard"
      ENABLE_RCON: "true"
      RCON_PASSWORD: "admin123"
    volumes:
      - ./data:/data
    restart: unless-stopped
EOF
docker-compose up -d && \
echo "⚡ SERVER STARTING - WAIT 60 SECONDS ⚡" && \
sleep 60 && \
docker-compose logs --tail=20
```

---

## ✅ STEP 3: VERIFY (10 seconds)

**Check if server is running:**

```bash
docker-compose ps
```

**Should show:** `Up`

---

## 🎮 STEP 4: CONNECT & PLAY!

**In TLauncher:**
- Server: `mc.galion.studio` or `54.37.223.40`
- Version: 1.21.1
- Join!

---

## 📊 USEFUL COMMANDS:

```bash
# View logs
docker-compose logs -f

# Restart
docker-compose restart

# Admin commands
docker-compose exec minecraft rcon-cli
# Then: /op YourName
```

---

**THAT'S IT! 3 COMMANDS. 3 MINUTES. DONE.** 🚀

---

## 🆘 IF PROBLEMS:

```bash
# Check status
docker-compose ps

# View errors
docker-compose logs

# Restart everything
docker-compose restart

# Nuclear option (restart fresh)
docker-compose down
docker-compose up -d
```

---

## 🎯 WHAT YOU HAVE:

✅ Minecraft 1.21.1 Server  
✅ Paper (optimized)  
✅ 100 player capacity  
✅ No premium needed  
✅ 6GB RAM allocated  
✅ Auto-restart on crash  
✅ Domain: mc.galion.studio  
✅ IP: 54.37.223.40:25565  

**GO CONNECT NOW!** 🎮

