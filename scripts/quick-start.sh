#!/bin/bash
# Titan Server - Quick Start Script
# ELON MODE: One command to rule them all
# Usage: curl -sSL <url> | bash

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}"
cat << "EOF"
╔════════════════════════════════════════╗
║                                        ║
║         🚀 TITAN SERVER 🚀            ║
║                                        ║
║   Next-Gen Minecraft Server Platform  ║
║        Target: 20,000 Players         ║
║                                        ║
╚════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo ""
echo -e "${BLUE}Starting Titan Quick Setup...${NC}"
echo ""

# Check prerequisites
echo -e "${BLUE}[1/5]${NC} Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}⚠ Docker not found!${NC}"
    echo "Install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${YELLOW}⚠ Docker Compose not found!${NC}"
    echo "Install Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites OK${NC}"

# Setup environment
echo -e "${BLUE}[2/5]${NC} Setting up environment..."

if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ Created .env file${NC}"
else
    echo -e "${GREEN}✓ .env already exists${NC}"
fi

# Create directories
echo -e "${BLUE}[3/5]${NC} Creating directories..."
mkdir -p worlds/{hub,survival} logs backups plugins mods config
echo -e "${GREEN}✓ Directories created${NC}"

# Pull Docker images
echo -e "${BLUE}[4/5]${NC} Pulling Docker images..."
docker-compose pull
echo -e "${GREEN}✓ Images pulled${NC}"

# Start services
echo -e "${BLUE}[5/5]${NC} Starting Titan services..."
docker-compose up -d
echo -e "${GREEN}✓ Services started${NC}"

echo ""
echo -e "${BLUE}Waiting for services to initialize...${NC}"
sleep 10

# Show status
echo ""
docker-compose ps

echo ""
echo -e "${GREEN}"
echo "════════════════════════════════════════"
echo "  🎉 TITAN IS RUNNING! 🎉"
echo "════════════════════════════════════════"
echo -e "${NC}"
echo ""
echo "Connect to server:"
echo -e "  ${GREEN}localhost:25565${NC} (Minecraft client)"
echo ""
echo "Monitoring:"
echo -e "  ${GREEN}http://localhost:3000${NC} (Grafana - admin/admin)"
echo -e "  ${GREEN}http://localhost:9090${NC} (Prometheus)"
echo ""
echo "Useful commands:"
echo "  • View logs:    docker-compose logs -f"
echo "  • Stop server:  docker-compose down"
echo "  • Restart:      docker-compose restart"
echo "  • Status:       docker-compose ps"
echo ""
echo -e "${YELLOW}Note: Services may take 1-2 minutes to fully start${NC}"
echo ""
echo -e "${BLUE}Built with first principles. Shipped fast. Scales infinitely.${NC}"
echo ""

