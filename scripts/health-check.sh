#!/bin/bash
# Galion Health Check Script
# Verifies all components are running correctly

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "========================================"
echo "  Galion Server Health Check"
echo "========================================"
echo ""

# Check PostgreSQL
echo -n "PostgreSQL: "
if kubectl exec -it postgresql-0 -n galion-data -- \
    psql -U mcserver -c "SELECT 1" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Healthy${NC}"
else
    echo -e "${RED}❌ Failed${NC}"
fi

# Check Redis
echo -n "Redis: "
if kubectl exec -it redis-0 -n galion-data -- \
    redis-cli ping > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Healthy${NC}"
else
    echo -e "${RED}❌ Failed${NC}"
fi

# Check Velocity Proxy
echo -n "Velocity Proxy: "
VELOCITY_COUNT=$(kubectl get pods -n galion-proxy -l app=velocity \
    --field-selector=status.phase=Running --no-headers 2>/dev/null | wc -l)
if [ "$VELOCITY_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✅ ${VELOCITY_COUNT} instances running${NC}"
else
    echo -e "${RED}❌ No instances running${NC}"
fi

# Check Minecraft Servers
echo -n "Minecraft Servers: "
SERVER_COUNT=$(kubectl get pods -n galion-servers -l app=mc-server \
    --field-selector=status.phase=Running --no-headers 2>/dev/null | wc -l)
if [ "$SERVER_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✅ ${SERVER_COUNT} instances running${NC}"
else
    echo -e "${RED}❌ No instances running${NC}"
fi

echo ""
echo "=== Resource Usage ==="
kubectl top nodes 2>/dev/null || echo "Metrics server not available"

echo ""
echo "=== Server Details (Top 10) ==="
kubectl top pods -n galion-servers 2>/dev/null | head -11 || echo "Metrics server not available"

echo ""
echo "=== External Access ==="
EXTERNAL_IP=$(kubectl get svc velocity-proxy -n galion-proxy \
    -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null)
if [ -n "$EXTERNAL_IP" ]; then
    echo -e "${GREEN}Server Address: ${EXTERNAL_IP}:25565${NC}"
else
    echo -e "${YELLOW}External IP not yet assigned${NC}"
fi

echo ""
echo "Health check complete!"

