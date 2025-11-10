#!/bin/bash
# Titan Server - Quick Deploy Script
# Rapid deployment for development/testing
# ELON MODE: Ship fast, iterate fast
#
# Usage: ./automation/deploy/quick-deploy.sh

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "========================================"
echo "  TITAN QUICK DEPLOY"
echo "  Ship fast. Iterate fast."
echo "========================================"
echo -e "${NC}"

# Pull latest changes (if git repo)
if [ -d .git ]; then
    echo -e "${BLUE}Pulling latest changes...${NC}"
    git pull
    echo -e "${GREEN}✓ Code updated${NC}"
fi

# Build
echo -e "${BLUE}Building...${NC}"
if [ -f gradlew ]; then
    ./gradlew clean build -x test --parallel
    echo -e "${GREEN}✓ Build complete${NC}"
fi

# Rebuild and restart Docker services
echo -e "${BLUE}Deploying to Docker...${NC}"
docker-compose down
docker-compose up -d --build

echo ""
echo -e "${GREEN}✓ Deployment complete!${NC}"
echo -e "${BLUE}Waiting for services to start...${NC}"
sleep 5

# Show status
docker-compose ps

echo ""
echo -e "${GREEN}✓ Titan is running!${NC}"
echo "Connect: localhost:25565"

