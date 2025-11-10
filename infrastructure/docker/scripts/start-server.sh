#!/bin/bash
# Galion Server Startup Script
# Runs inside Docker container

set -e

# Accept EULA automatically if MC_EULA=true
if [ "$MC_EULA" = "true" ]; then
    echo "eula=true" > eula.txt
    echo "EULA accepted automatically"
else
    echo "EULA not accepted. Set MC_EULA=true to accept."
    exit 1
fi

# Wait for database to be ready
echo "Waiting for database..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 1
done
echo "Database is ready"

# Wait for Redis to be ready
echo "Waiting for Redis..."
while ! nc -z $REDIS_HOST $REDIS_PORT; do
    sleep 1
done
echo "Redis is ready"

# Print startup information
echo "========================================"
echo "  Galion Minecraft Server"
echo "  Version: 1.20.4"
echo "  Type: Hybrid (Forge + Paper)"
echo "========================================"
echo ""
echo "Configuration:"
echo "  Memory: ${MC_INIT_MEMORY} - ${MC_MAX_MEMORY}"
echo "  Server Type: ${SERVER_TYPE:-unknown}"
echo "  Database: ${POSTGRES_HOST}:${POSTGRES_PORT}"
echo "  Redis: ${REDIS_HOST}:${REDIS_PORT}"
echo ""

# Start server
echo "Starting Minecraft server..."
exec java $JAVA_OPTS -jar server.jar nogui

