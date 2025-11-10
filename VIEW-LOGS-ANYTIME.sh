#!/bin/bash
# View Titan Server Logs
# Run this anytime to see live logs

cd /opt/mc

echo "╔════════════════════════════════════════╗"
echo "║     📊 TITAN SERVER LOGS 📊           ║"
echo "╚════════════════════════════════════════╝"
echo ""
echo "Showing live logs..."
echo "Press Ctrl+C to exit (server keeps running)"
echo ""
echo "════════════════════════════════════════"
echo ""

docker-compose logs -f

