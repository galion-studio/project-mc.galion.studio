#!/bin/bash
# Titan Server - Deployment Test Script
# Verifies deployment is working correctly
# SHIP FAST - TEST FAST

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

FAILED_TESTS=0
PASSED_TESTS=0

print_test() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

print_pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
    ((PASSED_TESTS++))
}

print_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
    ((FAILED_TESTS++))
}

# Test function
test_service() {
    local name=$1
    local host=$2
    local port=$3
    
    print_test "Testing $name connectivity ($host:$port)"
    
    if nc -z -w5 "$host" "$port" 2>/dev/null; then
        print_pass "$name is accessible"
        return 0
    else
        print_fail "$name is NOT accessible"
        return 1
    fi
}

echo -e "${BLUE}"
echo "========================================"
echo "  TITAN DEPLOYMENT TEST"
echo "  Verify everything works"
echo "========================================"
echo -e "${NC}"

# Test 1: Docker is running
print_test "Docker daemon"
if docker info > /dev/null 2>&1; then
    print_pass "Docker is running"
else
    print_fail "Docker is not running"
fi

# Test 2: Docker Compose services
print_test "Docker Compose services"
RUNNING=$(docker-compose ps --services --filter "status=running" | wc -l)
if [ "$RUNNING" -ge 5 ]; then
    print_pass "At least 5 services running ($RUNNING total)"
else
    print_fail "Not enough services running (expected 5+, got $RUNNING)"
fi

# Test 3: Network connectivity
test_service "Minecraft Proxy" "localhost" "25565"
test_service "PostgreSQL" "localhost" "5432"
test_service "Redis" "localhost" "6379"
test_service "Prometheus" "localhost" "9090"
test_service "Grafana" "localhost" "3000"

# Test 4: Database connectivity
print_test "PostgreSQL connection"
if docker-compose exec -T postgres psql -U titan -d titan -c "SELECT 1;" > /dev/null 2>&1; then
    print_pass "PostgreSQL connection successful"
else
    print_fail "PostgreSQL connection failed"
fi

# Test 5: Redis connectivity
print_test "Redis connection"
REDIS_RESPONSE=$(docker-compose exec -T redis redis-cli ping 2>/dev/null || echo "FAIL")
if [ "$REDIS_RESPONSE" = "PONG" ]; then
    print_pass "Redis connection successful"
else
    print_fail "Redis connection failed"
fi

# Test 6: Database schema
print_test "Database schema"
TABLE_COUNT=$(docker-compose exec -T postgres psql -U titan -d titan -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null | xargs)
if [ "$TABLE_COUNT" -gt 5 ]; then
    print_pass "Database schema created ($TABLE_COUNT tables)"
else
    print_fail "Database schema incomplete (found $TABLE_COUNT tables)"
fi

# Test 7: Container health
print_test "Container health status"
HEALTHY=$(docker-compose ps --format json | jq -r '.Health // "N/A"' | grep -c "healthy" || echo "0")
if [ "$HEALTHY" -gt 0 ]; then
    print_pass "$HEALTHY containers report healthy status"
else
    print_fail "No containers reporting healthy (health checks may not be configured)"
fi

# Test 8: Log output
print_test "Server startup logs"
if docker-compose logs titan-proxy 2>/dev/null | grep -q "started" || \
   docker-compose logs titan-hub 2>/dev/null | grep -q "Done" || \
   docker-compose logs titan-proxy 2>/dev/null | grep -q "Listening"; then
    print_pass "Server startup detected in logs"
else
    print_fail "No startup confirmation in logs (servers may still be starting)"
fi

# Summary
echo ""
echo -e "${BLUE}========================================"
echo "  TEST SUMMARY"
echo "========================================${NC}"
echo -e "${GREEN}Passed: $PASSED_TESTS${NC}"
echo -e "${RED}Failed: $FAILED_TESTS${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ ALL TESTS PASSED!${NC}"
    echo -e "${GREEN}Deployment is working correctly.${NC}"
    echo ""
    echo "Next steps:"
    echo "  • Connect: minecraft client to localhost:25565"
    echo "  • Monitor: http://localhost:3000 (Grafana)"
    echo "  • View logs: docker-compose logs -f"
    exit 0
else
    echo ""
    echo -e "${YELLOW}⚠ SOME TESTS FAILED${NC}"
    echo "Check logs: docker-compose logs"
    echo "Common issues:"
    echo "  • Services still starting (wait 30-60 seconds)"
    echo "  • Ports already in use"
    echo "  • Docker resources insufficient"
    exit 1
fi

