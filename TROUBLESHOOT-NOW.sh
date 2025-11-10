#!/bin/bash
# TROUBLESHOOT MINECRAFT SERVER
# Find out why it's not working

echo "═══════════════════════════════════════"
echo "    🔍 TITAN SERVER DIAGNOSTICS 🔍"
echo "═══════════════════════════════════════"
echo ""

# Check 1: Is Docker running?
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[1/7] Checking Docker..."
if systemctl is-active --quiet docker; then
    echo "✅ Docker is running"
else
    echo "❌ Docker is NOT running"
    echo "   Fix: systemctl start docker"
fi
echo ""

# Check 2: Is server directory present?
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[2/7] Checking server directory..."
if [ -d "/opt/mc" ]; then
    echo "✅ Directory exists: /opt/mc"
    cd /opt/mc
else
    echo "❌ Directory missing: /opt/mc"
    echo "   Fix: Run deployment command again"
    exit 1
fi
echo ""

# Check 3: Is docker-compose.yml present?
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[3/7] Checking configuration..."
if [ -f "docker-compose.yml" ]; then
    echo "✅ docker-compose.yml found"
else
    echo "❌ docker-compose.yml missing"
    echo "   Fix: Run deployment command again"
    exit 1
fi
echo ""

# Check 4: Are containers running?
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[4/7] Checking Minecraft container..."
docker-compose ps
echo ""

CONTAINER_STATUS=$(docker-compose ps -q | wc -l)
if [ "$CONTAINER_STATUS" -gt 0 ]; then
    echo "✅ Container exists"
    
    # Check if it's actually running
    if docker-compose ps | grep -q "Up"; then
        echo "✅ Container is UP"
    else
        echo "❌ Container is NOT running"
        echo "   Checking logs for errors..."
        docker-compose logs --tail=50
    fi
else
    echo "❌ No containers found"
    echo "   Fix: docker-compose up -d"
fi
echo ""

# Check 5: Is port 25565 open?
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[5/7] Checking if Minecraft port is listening..."
if netstat -tulpn | grep -q ":25565"; then
    echo "✅ Port 25565 is OPEN"
    netstat -tulpn | grep ":25565"
else
    echo "❌ Port 25565 is NOT listening"
    echo "   This means server is not started or crashed"
fi
echo ""

# Check 6: Firewall status
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[6/7] Checking firewall..."
if command -v ufw >/dev/null 2>&1; then
    UFW_STATUS=$(ufw status | grep "Status:" | awk '{print $2}')
    echo "Firewall status: $UFW_STATUS"
    
    if ufw status | grep -q "25565"; then
        echo "✅ Port 25565 is allowed in firewall"
    else
        echo "⚠️  Port 25565 not explicitly allowed"
        echo "   TitanAXE should have it open, but check panel"
    fi
else
    echo "ℹ️  UFW not installed (TitanAXE manages firewall)"
fi
echo ""

# Check 7: Recent logs
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[7/7] Recent server logs (last 30 lines)..."
echo ""
docker-compose logs --tail=30
echo ""

# Summary and recommendations
echo "═══════════════════════════════════════"
echo "    📊 DIAGNOSTIC SUMMARY"
echo "═══════════════════════════════════════"
echo ""
echo "Quick fixes to try:"
echo ""
echo "1️⃣  Restart server:"
echo "   cd /opt/mc && docker-compose restart"
echo ""
echo "2️⃣  Start server if stopped:"
echo "   cd /opt/mc && docker-compose up -d"
echo ""
echo "3️⃣  View live logs:"
echo "   cd /opt/mc && docker-compose logs -f"
echo ""
echo "4️⃣  Check if 'Done' appears in logs"
echo "   (Server ready when you see this)"
echo ""
echo "5️⃣  Test from VPS itself:"
echo "   nc -zv localhost 25565"
echo ""
echo "═══════════════════════════════════════"

