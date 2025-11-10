#!/bin/bash
# Titan Server - Health Check Script
# Check health of all services
#
# Usage: ./automation/monitoring/health-check.sh

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================"
echo "  TITAN HEALTH CHECK"
echo "========================================${NC}"
echo ""

# Check Docker containers
echo -e "${BLUE}Checking Docker containers...${NC}"
docker-compose ps
echo ""

# Check if services are responding
check_service() {
    local name=$1
    local host=$2
    local port=$3
    
    if nc -z "$host" "$port" 2>/dev/null; then
        echo -e "${GREEN}✓ $name is responding${NC}"
        return 0
    else
        echo -e "${RED}✗ $name is NOT responding${NC}"
        return 1
    fi
}

# Check Minecraft server
echo -e "${BLUE}Checking services...${NC}"
check_service "Minecraft Proxy" "localhost" "25565"

# Check databases
check_service "PostgreSQL" "localhost" "5432"
check_service "Redis" "localhost" "6379"

# Check monitoring
check_service "Prometheus" "localhost" "9090"
check_service "Grafana" "localhost" "3000"

echo ""

# Check database connectivity
echo -e "${BLUE}Checking PostgreSQL connectivity...${NC}"
docker-compose exec -T postgres psql -U titan -d titan -c "SELECT version();" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ PostgreSQL connection successful${NC}"
else
    echo -e "${RED}✗ PostgreSQL connection failed${NC}"
fi

# Check Redis connectivity
echo -e "${BLUE}Checking Redis connectivity...${NC}"
docker-compose exec -T redis redis-cli ping > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Redis connection successful${NC}"
else
    echo -e "${RED}✗ Redis connection failed${NC}"
fi

echo ""

# Show resource usage
echo -e "${BLUE}Resource Usage:${NC}"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

echo ""
echo -e "${BLUE}Health check complete!${NC}"
