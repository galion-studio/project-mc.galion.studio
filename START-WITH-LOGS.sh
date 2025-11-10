#!/bin/bash
# Start Titan Server and show logs
# Server stays running even if you close this

cd /opt/mc

echo "⚡ STARTING TITAN SERVER ⚡"
echo ""

# Start in background
docker-compose up -d

echo "✅ Server started in background"
echo ""
echo "📊 Showing live logs..."
echo "   (Press Ctrl+C to exit logs, server keeps running)"
echo ""
echo "════════════════════════════════════════"
echo ""

# Show logs (can close anytime)
docker-compose logs -f

# After Ctrl+C
echo ""
echo "✅ Logs closed. Server is still running!"
echo ""
echo "View logs again: cd /opt/mc && docker-compose logs -f"

