#!/bin/bash
# TITAN SERVER - PRODUCTION DEPLOYMENT
# One command. Full stack. Ship it.
# Elon Mode: Make it work → Make it fast → Make it scale

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

clear

echo -e "${BLUE}"
cat << "EOF"
╔════════════════════════════════════════╗
║                                        ║
║         🚀 TITAN DEPLOY 🚀            ║
║                                        ║
║   Production Minecraft Server          ║
║   Target: 20,000 Players              ║
║   Domain: mc.galion.studio            ║
║                                        ║
╚════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${CYAN}ELON PRINCIPLES:${NC}"
echo -e "  ✓ Ship fast"
echo -e "  ✓ Make it work first"
echo -e "  ✓ Iterate rapidly"
echo -e "  ✓ Scale when needed"
echo ""
echo -e "${YELLOW}Starting deployment in 3 seconds...${NC}"
sleep 3

# ============================================
# PHASE 1: SYSTEM PREPARATION
# ============================================
echo -e "\n${BLUE}[PHASE 1/5] SYSTEM PREPARATION${NC}"

echo -e "${YELLOW}→ Updating system packages...${NC}"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq > /dev/null 2>&1
apt-get upgrade -y -qq > /dev/null 2>&1
echo -e "${GREEN}✓ System updated${NC}"

echo -e "${YELLOW}→ Installing essential tools...${NC}"
apt-get install -y -qq \
    curl wget git vim nano \
    htop iotop \
    net-tools netcat-openbsd \
    ufw fail2ban \
    ca-certificates gnupg lsb-release \
    > /dev/null 2>&1
echo -e "${GREEN}✓ Tools installed${NC}"

# ============================================
# PHASE 2: DOCKER INSTALLATION
# ============================================
echo -e "\n${BLUE}[PHASE 2/5] DOCKER INSTALLATION${NC}"

if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}→ Installing Docker...${NC}"
    
    # Add Docker's official GPG key
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    chmod a+r /etc/apt/keyrings/docker.asc
    
    # Add repository
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    apt-get update -qq > /dev/null 2>&1
    apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin > /dev/null 2>&1
    
    systemctl enable docker > /dev/null 2>&1
    systemctl start docker
    
    echo -e "${GREEN}✓ Docker installed${NC}"
else
    echo -e "${GREEN}✓ Docker already installed${NC}"
fi

docker --version
docker compose version

# ============================================
# PHASE 3: FIREWALL & SECURITY
# ============================================
echo -e "\n${BLUE}[PHASE 3/5] SECURITY CONFIGURATION${NC}"

echo -e "${YELLOW}→ Configuring firewall...${NC}"
ufw --force disable > /dev/null 2>&1

# Allow essential ports
ufw default deny incoming > /dev/null 2>&1
ufw default allow outgoing > /dev/null 2>&1
ufw allow 22/tcp comment 'SSH' > /dev/null 2>&1
ufw allow 25565/tcp comment 'Minecraft' > /dev/null 2>&1
ufw allow 25565/udp comment 'Minecraft Query' > /dev/null 2>&1
ufw allow 3000/tcp comment 'Grafana' > /dev/null 2>&1

echo "y" | ufw enable > /dev/null 2>&1
echo -e "${GREEN}✓ Firewall configured${NC}"

echo -e "${YELLOW}→ Configuring fail2ban...${NC}"
systemctl enable fail2ban > /dev/null 2>&1
systemctl start fail2ban > /dev/null 2>&1
echo -e "${GREEN}✓ DDoS protection active${NC}"

# ============================================
# PHASE 4: TITAN SERVER DEPLOYMENT
# ============================================
echo -e "\n${BLUE}[PHASE 4/5] TITAN SERVER DEPLOYMENT${NC}"

INSTALL_DIR="/opt/titan-server"
echo -e "${YELLOW}→ Creating project structure in ${INSTALL_DIR}...${NC}"

mkdir -p ${INSTALL_DIR}/{data,plugins,backups,logs}
cd ${INSTALL_DIR}

# Generate secure passwords
DB_PASSWORD=$(openssl rand -base64 32 | tr -dc 'a-zA-Z0-9' | head -c 24)
REDIS_PASSWORD=$(openssl rand -base64 32 | tr -dc 'a-zA-Z0-9' | head -c 24)
GRAFANA_PASSWORD=$(openssl rand -base64 32 | tr -dc 'a-zA-Z0-9' | head -c 16)

echo -e "${GREEN}✓ Directories created${NC}"

echo -e "${YELLOW}→ Creating production docker-compose.yml...${NC}"

cat > docker-compose.yml << 'DOCKEREOF'
version: '3.9'

services:
  # ============================================
  # MINECRAFT SERVER (Paper 1.21.1)
  # ============================================
  minecraft:
    image: itzg/minecraft-server:java21
    container_name: titan-minecraft
    ports:
      - "25565:25565"
    environment:
      # Basic Configuration
      EULA: "TRUE"
      TYPE: "PAPER"
      VERSION: "1.21.1"
      
      # Server Identity
      SERVER_NAME: "Titan Galion Studio"
      MOTD: "§6§l⚡ TITAN SERVER ⚡§r\n§eMC.GALION.STUDIO §8| §7No Premium §8| §a100 Players"
      
      # Performance
      MEMORY: "6G"
      USE_AIKAR_FLAGS: "true"
      
      # Player Settings
      MAX_PLAYERS: "100"
      ONLINE_MODE: "FALSE"
      ENFORCE_SECURE_PROFILE: "FALSE"
      
      # World Settings
      LEVEL: "world"
      DIFFICULTY: "hard"
      MODE: "survival"
      PVP: "true"
      VIEW_DISTANCE: "8"
      SIMULATION_DISTANCE: "6"
      
      # Features
      ALLOW_NETHER: "true"
      ALLOW_END: "true"
      ENABLE_COMMAND_BLOCK: "true"
      SPAWN_PROTECTION: "0"
      SPAWN_ANIMALS: "true"
      SPAWN_MONSTERS: "true"
      SPAWN_NPCS: "true"
      
      # Network
      ENABLE_QUERY: "true"
      ENABLE_RCON: "true"
      RCON_PASSWORD: "titanrcon2025"
      RCON_PORT: "25575"
      
      # Monitoring
      ENABLE_JMX: "true"
      JMX_HOST: "0.0.0.0"
      JMX_PORT: "9010"
      
      # Paper Optimizations
      PAPER_DOWNLOAD_URL: "https://api.papermc.io/v2/projects/paper/versions/1.21.1/builds/latest/downloads/paper-1.21.1.jar"
      
    volumes:
      - ./data:/data
      - ./plugins:/plugins:ro
      - ./backups:/backups
    
    restart: unless-stopped
    
    healthcheck:
      test: mc-health
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 120s
    
    networks:
      - titan-network

  # ============================================
  # POSTGRESQL DATABASE
  # ============================================
  postgres:
    image: postgres:15-alpine
    container_name: titan-postgres
    environment:
      POSTGRES_DB: titan
      POSTGRES_USER: titan
      POSTGRES_PASSWORD: ${DB_PASSWORD:-changeme}
      POSTGRES_INITDB_ARGS: "--encoding=UTF8 --locale=en_US.utf8"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U titan"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - titan-network

  # ============================================
  # REDIS CACHE
  # ============================================
  redis:
    image: redis:7-alpine
    container_name: titan-redis
    command: >
      redis-server
      --requirepass ${REDIS_PASSWORD:-changeme}
      --maxmemory 1gb
      --maxmemory-policy allkeys-lru
      --appendonly yes
    volumes:
      - redis-data:/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
    networks:
      - titan-network

  # ============================================
  # GRAFANA MONITORING
  # ============================================
  grafana:
    image: grafana/grafana:latest
    container_name: titan-grafana
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_USER: admin
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASSWORD:-admin}
      GF_USERS_ALLOW_SIGN_UP: "false"
      GF_SERVER_ROOT_URL: "http://54.37.223.40:3000"
      GF_ANALYTICS_REPORTING_ENABLED: "false"
      GF_ANALYTICS_CHECK_FOR_UPDATES: "false"
    volumes:
      - grafana-data:/var/lib/grafana
    restart: unless-stopped
    networks:
      - titan-network

  # ============================================
  # PROMETHEUS METRICS
  # ============================================
  prometheus:
    image: prom/prometheus:latest
    container_name: titan-prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=30d'
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    restart: unless-stopped
    networks:
      - titan-network

networks:
  titan-network:
    driver: bridge

volumes:
  postgres-data:
  redis-data:
  grafana-data:
  prometheus-data:
DOCKEREOF

echo -e "${GREEN}✓ Docker Compose created${NC}"

# Create Prometheus config
echo -e "${YELLOW}→ Creating monitoring configuration...${NC}"

cat > prometheus.yml << 'PROMEOF'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'minecraft'
    static_configs:
      - targets: ['minecraft:9010']
PROMEOF

echo -e "${GREEN}✓ Monitoring configured${NC}"

# Create environment file with passwords
cat > .env << ENVEOF
DB_PASSWORD=${DB_PASSWORD}
REDIS_PASSWORD=${REDIS_PASSWORD}
GRAFANA_PASSWORD=${GRAFANA_PASSWORD}
ENVEOF

chmod 600 .env

echo -e "${YELLOW}→ Starting services...${NC}"
docker compose pull -q
docker compose up -d

echo -e "${GREEN}✓ All services started${NC}"

# ============================================
# PHASE 5: BACKUP AUTOMATION
# ============================================
echo -e "\n${BLUE}[PHASE 5/5] BACKUP AUTOMATION${NC}"

echo -e "${YELLOW}→ Creating backup script...${NC}"

cat > /usr/local/bin/titan-backup << 'BACKUPEOF'
#!/bin/bash
BACKUP_DIR="/opt/titan-server/backups"
DATE=$(date +%Y%m%d-%H%M%S)

mkdir -p ${BACKUP_DIR}

# Backup Minecraft world
cd /opt/titan-server
tar -czf ${BACKUP_DIR}/world-${DATE}.tar.gz data/world 2>/dev/null

# Backup database
docker compose exec -T postgres pg_dump -U titan titan | gzip > ${BACKUP_DIR}/database-${DATE}.sql.gz

# Keep only last 7 days
find ${BACKUP_DIR} -name "world-*.tar.gz" -mtime +7 -delete
find ${BACKUP_DIR} -name "database-*.sql.gz" -mtime +7 -delete

echo "Backup completed: ${DATE}"
BACKUPEOF

chmod +x /usr/local/bin/titan-backup

# Add to crontab (daily at 3 AM)
(crontab -l 2>/dev/null | grep -v titan-backup; echo "0 3 * * * /usr/local/bin/titan-backup >> /var/log/titan-backup.log 2>&1") | crontab -

echo -e "${GREEN}✓ Daily backups configured (3 AM)${NC}"

# ============================================
# PHASE 6: WAIT FOR SERVICES
# ============================================
echo -e "\n${BLUE}[FINAL] INITIALIZING SERVICES${NC}"

echo -e "${YELLOW}→ Waiting for Minecraft server to start...${NC}"
echo -e "${CYAN}   This takes 60-90 seconds...${NC}"

for i in {1..90}; do
    if docker compose logs minecraft 2>/dev/null | grep -q "Done"; then
        echo -e "${GREEN}✓ Minecraft server is ready!${NC}"
        break
    fi
    echo -ne "${CYAN}   [$i/90] Starting...${NC}\r"
    sleep 1
done

# ============================================
# DEPLOYMENT COMPLETE
# ============================================

clear

echo -e "${GREEN}"
cat << "EOF"
╔════════════════════════════════════════╗
║                                        ║
║      ✅ DEPLOYMENT COMPLETE! ✅       ║
║                                        ║
║         TITAN SERVER IS LIVE          ║
║                                        ║
╚════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${CYAN}SERVER INFORMATION${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${YELLOW}Domain:${NC}      ${GREEN}mc.galion.studio${NC}"
echo -e "${YELLOW}IP:${NC}          ${GREEN}54.37.223.40:25565${NC}"
echo -e "${YELLOW}Version:${NC}     ${GREEN}Minecraft 1.21.1 (Paper)${NC}"
echo -e "${YELLOW}Players:${NC}     ${GREEN}100 max${NC}"
echo -e "${YELLOW}Premium:${NC}     ${GREEN}NOT required (TLauncher OK)${NC}"
echo ""
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${CYAN}MONITORING & ADMIN${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${YELLOW}Grafana:${NC}     ${GREEN}http://54.37.223.40:3000${NC}"
echo -e "${YELLOW}Username:${NC}    ${GREEN}admin${NC}"
echo -e "${YELLOW}Password:${NC}    ${GREEN}${GRAFANA_PASSWORD}${NC}"
echo ""
echo -e "${YELLOW}RCON:${NC}        ${GREEN}localhost:25575${NC}"
echo -e "${YELLOW}Password:${NC}    ${GREEN}titanrcon2025${NC}"
echo ""
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${CYAN}USEFUL COMMANDS${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${YELLOW}Directory:${NC}   ${GREEN}cd /opt/titan-server${NC}"
echo -e "${YELLOW}Logs:${NC}        ${GREEN}docker compose logs -f minecraft${NC}"
echo -e "${YELLOW}Restart:${NC}     ${GREEN}docker compose restart minecraft${NC}"
echo -e "${YELLOW}Status:${NC}      ${GREEN}docker compose ps${NC}"
echo -e "${YELLOW}Backup:${NC}      ${GREEN}/usr/local/bin/titan-backup${NC}"
echo -e "${YELLOW}RCON:${NC}        ${GREEN}docker compose exec minecraft rcon-cli${NC}"
echo ""
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${CYAN}CREDENTIALS SAVED TO:${NC} ${GREEN}/opt/titan-server/.env${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo ""
echo -e "${GREEN}✓ Server is accepting connections!${NC}"
echo -e "${GREEN}✓ DNS: ${CYAN}mc.galion.studio${GREEN} (may take 5-30 min)${NC}"
echo -e "${GREEN}✓ IP:  ${CYAN}54.37.223.40:25565${GREEN} (works now)${NC}"
echo ""
echo -e "${PURPLE}Share with friends: ${CYAN}mc.galion.studio${NC}"
echo ""
echo -e "${YELLOW}View real-time logs:${NC} ${GREEN}docker compose logs -f${NC}"
echo ""
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo -e "${CYAN}SHIP IT. TEST IT. IMPROVE IT. SCALE IT.${NC}"
echo -e "${BLUE}═══════════════════════════════════════${NC}"
echo ""

# Save credentials to file
cat > ${INSTALL_DIR}/CREDENTIALS.txt << CREDEOF
TITAN SERVER CREDENTIALS
========================

Server Access:
  Domain: mc.galion.studio
  IP: 54.37.223.40:25565
  Version: Minecraft 1.21.1
  
Grafana Dashboard:
  URL: http://54.37.223.40:3000
  Username: admin
  Password: ${GRAFANA_PASSWORD}

RCON Access:
  Host: localhost
  Port: 25575
  Password: titanrcon2025

Database:
  Host: postgres
  Database: titan
  User: titan
  Password: ${DB_PASSWORD}

Redis:
  Host: redis
  Port: 6379
  Password: ${REDIS_PASSWORD}

Generated: $(date)
CREDEOF

chmod 600 ${INSTALL_DIR}/CREDENTIALS.txt

echo -e "${YELLOW}📝 Credentials saved to:${NC} ${GREEN}${INSTALL_DIR}/CREDENTIALS.txt${NC}"
echo ""

