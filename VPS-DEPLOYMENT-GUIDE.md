# 🚀 TITAN SERVER - VPS DEPLOYMENT GUIDE

## 📋 YOUR VPS INFORMATION

```
IP Address:    54.37.223.40
Username:      root
Password:      Phdhxdp10b@(05)A
OS:            Ubuntu 24.04 LTS
RAM:           8 GB
Storage:       60 GB SSD
```

---

## 🔌 STEP 1: CONNECT TO YOUR VPS

### Windows (Using PuTTY):

1. **Download PuTTY**: https://www.putty.org/
2. **Open PuTTY**
3. **Configure connection:**
   - Host Name: `54.37.223.40`
   - Port: `22`
   - Connection type: `SSH`
4. **Click "Open"**
5. **Login:**
   - login as: `root`
   - Password: `Phdhxdp10b@(05)A` (right-click to paste)

### Linux/Mac (Using Terminal):

```bash
ssh root@54.37.223.40
# Password: Phdhxdp10b@(05)A
```

---

## 🚀 STEP 2: RUN ONE-COMMAND INSTALLER

After you're connected via SSH, copy and paste this **entire command**:

```bash
curl -sSL https://raw.githubusercontent.com/yourusername/titan/main/deploy-vps.sh | bash
```

**OR** if that doesn't work, use this manual method:

```bash
# Download the script
wget https://raw.githubusercontent.com/yourusername/titan/main/deploy-vps.sh

# Make it executable
chmod +x deploy-vps.sh

# Run it
./deploy-vps.sh
```

**ALTERNATIVE** - Copy-paste the script manually:

```bash
# Create the script file
nano deploy.sh

# Paste the entire deploy-vps.sh content
# Press Ctrl+X, then Y, then Enter to save

# Make executable and run
chmod +x deploy.sh
./deploy.sh
```

---

## ⏱️ STEP 3: WAIT (5-10 minutes)

The script will automatically:
- ✅ Update Ubuntu system
- ✅ Install Docker & Docker Compose
- ✅ Download Minecraft server (Paper 1.21.1)
- ✅ Set up PostgreSQL database
- ✅ Set up Redis cache
- ✅ Set up Grafana monitoring
- ✅ Start everything

**You'll see progress messages. Just wait!**

---

## ✅ STEP 4: VERIFY DEPLOYMENT

After the script completes, check if services are running:

```bash
cd /opt/titan-server
docker compose ps
```

**Expected output**: All services should show "Up" status.

---

## 🎮 STEP 5: CONNECT & PLAY!

### In TLauncher:

1. **Select Minecraft 1.21.1** (or Forge 1.21.1)
2. **Multiplayer** → **Add Server**
3. **Server Address**: `54.37.223.40:25565`
4. **Join!**

### Share with Friends:

Anyone can connect (no premium needed):
```
Server IP: 54.37.223.40:25565
```

---

## 📊 MONITORING DASHBOARD

Access Grafana:
- **URL**: http://54.37.223.40:3000
- **Username**: admin
- **Password**: admin2025secure

---

## 🔧 USEFUL COMMANDS

### View Logs:
```bash
cd /opt/titan-server

# All logs
docker compose logs -f

# Just Minecraft server
docker compose logs -f titan-hub

# Last 100 lines
docker compose logs --tail=100
```

### Restart Server:
```bash
cd /opt/titan-server
docker compose restart titan-hub
```

### Stop Everything:
```bash
cd /opt/titan-server
docker compose down
```

### Start Everything:
```bash
cd /opt/titan-server
docker compose up -d
```

### Check Status:
```bash
cd /opt/titan-server
docker compose ps
```

### Check Resource Usage:
```bash
docker stats
```

---

## 🛠️ TROUBLESHOOTING

### Can't Connect to Server?

**1. Check if server is running:**
```bash
docker compose ps
```

**2. Check Minecraft logs:**
```bash
docker compose logs titan-hub --tail=50
```

**3. Verify port is open:**
```bash
netstat -tulpn | grep 25565
```

**4. Restart Minecraft server:**
```bash
docker compose restart titan-hub
```

### Server is Slow?

**Check resource usage:**
```bash
free -h  # Check RAM
df -h    # Check disk space
docker stats  # Check container resources
```

**If RAM is full, restart:**
```bash
docker compose restart
```

### Forgot Grafana Password?

**Reset it:**
```bash
docker compose exec grafana grafana-cli admin reset-admin-password admin2025secure
```

---

## 📦 BACKUPS

### Manual Backup:

```bash
cd /opt/titan-server

# Backup worlds
tar -czf backup-worlds-$(date +%Y%m%d).tar.gz worlds/

# Backup database
docker compose exec -T postgres pg_dump -U titan titan > backup-db-$(date +%Y%m%d).sql
```

### Automatic Backups:

Create cron job:
```bash
crontab -e

# Add this line (backup every 6 hours):
0 */6 * * * cd /opt/titan-server && tar -czf /opt/backups/worlds-$(date +\%Y\%m\%d-\%H\%M).tar.gz worlds/
```

---

## 🔐 SECURITY

### Change Root Password:

```bash
passwd
# Enter new password twice
```

### Set up Firewall (if needed):

```bash
# Allow SSH
ufw allow 22/tcp

# Allow Minecraft
ufw allow 25565/tcp
ufw allow 25565/udp

# Allow Grafana (optional, if you want external access)
ufw allow 3000/tcp

# Enable firewall
ufw enable
```

---

## 🆘 GET HELP

### View System Information:
```bash
# OS version
cat /etc/os-release

# RAM usage
free -h

# Disk usage
df -h

# Docker version
docker --version
docker compose version
```

### Share Logs for Support:
```bash
# Save all logs to file
docker compose logs > logs-$(date +%Y%m%d).txt

# Download with FileZilla or similar
```

---

## 📈 PERFORMANCE TUNING

### For 100+ Players:

Edit docker-compose.yml:
```yaml
titan-hub:
  environment:
    MEMORY: "7G"  # Increase to 7GB
    MAX_PLAYERS: "150"
```

Then restart:
```bash
docker compose up -d
```

---

## ✅ SUCCESS CHECKLIST

- [ ] Connected to VPS via SSH
- [ ] Ran deployment script
- [ ] All services showing "Up"
- [ ] Connected to server from TLauncher
- [ ] Can play Minecraft
- [ ] Grafana dashboard accessible
- [ ] Shared server IP with friends

---

## 🎯 WHAT YOU HAVE NOW

✅ **Minecraft 1.21.1 Server** (Paper)  
✅ **TLauncher Compatible** (No premium)  
✅ **50-100 Player Capacity**  
✅ **Monitoring Dashboard** (Grafana)  
✅ **Database** (PostgreSQL)  
✅ **Cache** (Redis)  
✅ **Auto-restart** (if crash)  
✅ **DDoS Protection** (TitanAXE)  
✅ **Public IP** (54.37.223.40)

---

**🚀 YOU'RE ALL SET! GO CONNECT TO YOUR SERVER!** 🎮

Server Address: **54.37.223.40:25565**

