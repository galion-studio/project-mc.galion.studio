#!/bin/bash
# Titan Server - Log Monitoring Script
# Tail logs from all services with color coding
#
# Usage: ./automation/monitoring/tail-logs.sh [service]

SERVICE=${1:-""}

if [ -z "$SERVICE" ]; then
    # Show all logs
    echo "Tailing logs from all services..."
    echo "Press Ctrl+C to stop"
    echo ""
    docker-compose logs -f --tail=100
else
    # Show specific service logs
    echo "Tailing logs from $SERVICE..."
    echo "Press Ctrl+C to stop"
    echo ""
    docker-compose logs -f --tail=100 "$SERVICE"
fi

