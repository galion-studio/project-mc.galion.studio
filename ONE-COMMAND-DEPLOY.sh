#!/bin/bash
# TITAN ONE-COMMAND DEPLOY
# Elon Mode: Ship it in one command

set -e

echo "⚡ TITAN DEPLOY - STARTING ⚡"
echo "This will take 3-4 minutes..."
echo ""

# Update and install Docker
echo "[1/4] Installing Docker..."
apt-get update -qq && apt-get install -y -qq docker.io docker-compose

# Create directory
echo "[2/4] Setting up directories..."
mkdir -p /opt/mc && cd /opt/mc

# Create docker-compose
echo "[3/4] Creating server configuration..."
cat > docker-compose.yml << 'EOF'
version: '3.9'

services:
  minecraft:
    image: itzg/minecraft-server:java21
    container_name: titan-mc
    ports:
      - "25565:25565"
    environment:
      EULA: "TRUE"
      TYPE: "PAPER"
      VERSION: "1.21.1"
      MEMORY: "6G"
      USE_AIKAR_FLAGS: "true"
      MAX_PLAYERS: "100"
      MOTD: "§6⚡ TITAN SERVER ⚡§r\n§eMC.GALION.STUDIO §8| §7No Premium Required!"
      ONLINE_MODE: "FALSE"
      VIEW_DISTANCE: "8"
      SIMULATION_DISTANCE: "6"
      DIFFICULTY: "hard"
      MODE: "survival"
      PVP: "true"
      ALLOW_NETHER: "true"
      SPAWN_PROTECTION: "0"
      ENABLE_QUERY: "true"
      ENABLE_RCON: "true"
      RCON_PASSWORD: "titan2025"
      RCON_PORT: "25575"
    volumes:
      - ./data:/data
    restart: unless-stopped
    healthcheck:
      test: mc-health
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 120s
EOF

# Start server
echo "[4/4] Starting Minecraft server..."
docker-compose up -d

echo ""
echo "⚡ WAITING FOR SERVER TO START (60 seconds)..."
sleep 60

# Show logs
docker-compose logs --tail=30

echo ""
echo "╔════════════════════════════════════════╗"
echo "║     ✅ DEPLOYMENT COMPLETE! ✅        ║"
echo "╚════════════════════════════════════════╝"
echo ""
echo "🎮 CONNECT NOW:"
echo "   Domain: mc.galion.studio"
echo "   IP:     54.37.223.40:25565"
echo ""
echo "📊 COMMANDS:"
echo "   cd /opt/mc"
echo "   docker-compose logs -f     (view logs)"
echo "   docker-compose restart     (restart server)"
echo "   docker-compose ps          (check status)"
echo ""
echo "🔧 ADMIN:"
echo "   docker-compose exec minecraft rcon-cli"
echo "   Password: titan2025"
echo ""
echo "⚡ SERVER IS LIVE! ⚡"

