#!/bin/bash
# TITAN DEPLOY - WITH LIVE LOGS
# Server runs in background, logs shown in terminal
# Close terminal = server keeps running

set -e

echo "⚡ TITAN SERVER DEPLOYMENT ⚡"
echo ""

# Install Docker
echo "[1/3] Installing Docker..."
apt-get update -qq
apt-get install -y -qq docker.io docker-compose screen

# Create server
echo "[2/3] Creating Minecraft server..."
mkdir -p /opt/mc && cd /opt/mc

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
      MOTD: "§6⚡ MC.GALION.STUDIO ⚡§r\n§7No Premium | Join & Play!"
      ONLINE_MODE: "FALSE"
      VIEW_DISTANCE: "8"
      SIMULATION_DISTANCE: "6"
      DIFFICULTY: "hard"
      MODE: "survival"
      PVP: "true"
      ENABLE_RCON: "true"
      RCON_PASSWORD: "admin123"
    volumes:
      - ./data:/data
    restart: unless-stopped
    tty: true
    stdin_open: true
EOF

# Start in detached mode (background)
echo "[3/3] Starting server (background mode)..."
docker-compose up -d

echo ""
echo "╔════════════════════════════════════════╗"
echo "║     ✅ SERVER STARTED! ✅             ║"
echo "╚════════════════════════════════════════╝"
echo ""
echo "🎮 CONNECT:"
echo "   mc.galion.studio:25565"
echo ""
echo "📊 WATCHING LIVE LOGS..."
echo "   Press Ctrl+C to exit logs (server stays running!)"
echo ""
echo "════════════════════════════════════════"
echo ""

# Show live logs (can be closed anytime)
docker-compose logs -f

# This won't execute until user presses Ctrl+C
echo ""
echo "✅ Logs closed. Server is still running!"
echo ""
echo "📊 VIEW LOGS AGAIN:"
echo "   cd /opt/mc && docker-compose logs -f"
echo ""

