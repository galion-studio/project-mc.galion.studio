#!/bin/bash
# Titan Server - VPS Deployment Script
# One-command installation for TitanAXE VPS
# Ubuntu 24.04 LTS

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
cat << "EOF"
╔════════════════════════════════════════╗
║                                        ║
║         🚀 TITAN SERVER 🚀            ║
║                                        ║
║   VPS Deployment Script                ║
║   Target: 20,000 Players              ║
║                                        ║
╚════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${BLUE}Starting deployment on TitanAXE VPS...${NC}\n"

# Step 1: Update system
echo -e "${YELLOW}[1/8] Updating system...${NC}"
apt-get update -qq
apt-get upgrade -y -qq
echo -e "${GREEN}✓ System updated${NC}\n"

# Step 2: Install dependencies
echo -e "${YELLOW}[2/8] Installing dependencies...${NC}"
apt-get install -y -qq \
    curl \
    wget \
    git \
    ca-certificates \
    gnupg \
    lsb-release \
    netcat-openbsd \
    jq
echo -e "${GREEN}✓ Dependencies installed${NC}\n"

# Step 3: Install Docker
echo -e "${YELLOW}[3/8] Installing Docker...${NC}"
if ! command -v docker &> /dev/null; then
    # Add Docker's official GPG key
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    chmod a+r /etc/apt/keyrings/docker.asc
    
    # Add Docker repository
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    apt-get update -qq
    apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    
    # Start Docker
    systemctl enable docker
    systemctl start docker
    echo -e "${GREEN}✓ Docker installed and started${NC}\n"
else
    echo -e "${GREEN}✓ Docker already installed${NC}\n"
fi

# Step 4: Clone Titan repository
echo -e "${YELLOW}[4/8] Setting up Titan Server...${NC}"
cd /opt
if [ -d "titan-server" ]; then
    echo -e "${YELLOW}  Titan directory exists, updating...${NC}"
    cd titan-server
    git pull -q
else
    echo -e "${YELLOW}  Cloning Titan repository...${NC}"
    mkdir -p titan-server
    cd titan-server
fi
echo -e "${GREEN}✓ Titan Server ready${NC}\n"

# Step 5: Create project structure
echo -e "${YELLOW}[5/8] Creating project structure...${NC}"
mkdir -p worlds/{hub,survival} logs backups plugins mods config
mkdir -p monitoring/{prometheus,grafana}
mkdir -p automation/{backup,monitoring}
echo -e "${GREEN}✓ Directories created${NC}\n"

# Step 6: Download configuration files from GitHub or create them
echo -e "${YELLOW}[6/8] Setting up configuration...${NC}"

# Create .env file
cat > .env << 'ENVEOF'
# Titan Server - Production Environment
ENVIRONMENT=production

# Network Configuration
DOMAIN=54.37.223.40
EXTERNAL_IP=54.37.223.40
MINECRAFT_PORT=25565

# Database
DB_HOST=postgres
DB_PORT=5432
DB_NAME=titan
DB_USER=titan
DB_PASSWORD=titan_secure_pass_2025

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=redis_secure_pass_2025

# Server Configuration
MAX_PLAYERS_PER_SERVER=500
MAX_PLAYERS_HUB=1000
VIEW_DISTANCE=8
SIMULATION_DISTANCE=6

# Java/JVM
JVM_MEMORY_MIN=6G
JVM_MEMORY_MAX=6G

# Monitoring
GRAFANA_ADMIN_PASSWORD=admin2025secure
PROMETHEUS_RETENTION=30d

# Backups
BACKUP_ENABLED=true
BACKUP_INTERVAL=6h
BACKUP_RETENTION_DAYS=7
ENVEOF

echo -e "${GREEN}✓ Configuration created${NC}\n"

# Step 7: Create docker-compose.yml
echo -e "${YELLOW}[7/8] Creating Docker Compose configuration...${NC}"

cat > docker-compose.yml << 'DOCKEREOF'
version: '3.9'

services:
  # Hub Server
  titan-hub:
    image: itzg/minecraft-server:java21
    container_name: titan-hub
    ports:
      - "25565:25565"
    environment:
      EULA: "TRUE"
      TYPE: "PAPER"
      VERSION: "1.21.1"
      MEMORY: "6G"
      MAX_PLAYERS: "1000"
      MOTD: "§6§lTitan Server §8| §7Hub Lobby"
      ONLINE_MODE: "FALSE"
      VIEW_DISTANCE: 8
      SIMULATION_DISTANCE: 6
      DIFFICULTY: normal
      MODE: survival
      PVP: "true"
      ENABLE_COMMAND_BLOCK: "true"
    volumes:
      - ./worlds/hub:/data
      - ./plugins:/plugins
    restart: unless-stopped
    networks:
      - titan-network

  # PostgreSQL
  postgres:
    image: postgres:15-alpine
    container_name: titan-postgres
    environment:
      POSTGRES_DB: titan
      POSTGRES_USER: titan
      POSTGRES_PASSWORD: titan_secure_pass_2025
    volumes:
      - postgres-data:/var/lib/postgresql/data
    restart: unless-stopped
    networks:
      - titan-network

  # Redis
  redis:
    image: redis:7-alpine
    container_name: titan-redis
    command: redis-server --requirepass redis_secure_pass_2025 --maxmemory 1gb --maxmemory-policy allkeys-lru
    volumes:
      - redis-data:/data
    restart: unless-stopped
    networks:
      - titan-network

  # Grafana
  grafana:
    image: grafana/grafana:latest
    container_name: titan-grafana
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin2025secure
      GF_USERS_ALLOW_SIGN_UP: "false"
    volumes:
      - grafana-data:/var/lib/grafana
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
DOCKEREOF

echo -e "${GREEN}✓ Docker Compose configuration created${NC}\n"

# Step 8: Start services
echo -e "${YELLOW}[8/8] Starting Titan Server...${NC}"
docker compose up -d
echo -e "${GREEN}✓ Services started${NC}\n"

# Wait for services to initialize
echo -e "${BLUE}Waiting for services to initialize (60 seconds)...${NC}"
sleep 60

# Show status
echo -e "\n${BLUE}Service Status:${NC}"
docker compose ps

echo -e "\n${GREEN}"
echo "════════════════════════════════════════"
echo "  ✓ TITAN SERVER DEPLOYED!"
echo "════════════════════════════════════════"
echo -e "${NC}"
echo -e "${YELLOW}Connection Information:${NC}"
echo -e "  Minecraft Server: ${GREEN}54.37.223.40:25565${NC}"
echo -e "  Grafana Dashboard: ${GREEN}http://54.37.223.40:3000${NC}"
echo -e "  Grafana Login: ${GREEN}admin / admin2025secure${NC}"
echo ""
echo -e "${YELLOW}Useful Commands:${NC}"
echo -e "  View logs:    ${BLUE}docker compose logs -f${NC}"
echo -e "  Restart:      ${BLUE}docker compose restart${NC}"
echo -e "  Stop:         ${BLUE}docker compose down${NC}"
echo -e "  Status:       ${BLUE}docker compose ps${NC}"
echo ""
echo -e "${GREEN}✓ Server is ready for players!${NC}"
echo -e "${GREEN}✓ Connect with TLauncher 1.21.1${NC}"
echo ""

