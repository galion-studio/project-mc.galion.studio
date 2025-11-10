#!/bin/bash
# Titan Server - Startup Script
# Prepares server configuration and starts the server

set -e

echo "========================================="
echo "  TITAN SERVER - Starting..."
echo "========================================="
echo "Server Type: $SERVER_TYPE"
echo "Server Name: $SERVER_NAME"
echo "Max Players: $MAX_PLAYERS"
echo "JVM Memory: $JVM_MEMORY"
echo "========================================="

# Generate server.properties from template
echo "Generating server.properties..."
envsubst < /app/server.properties.template > /app/server.properties

# Accept EULA automatically
echo "eula=true" > /app/eula.txt

# Create ops.json if it doesn't exist
if [ ! -f /app/ops.json ]; then
    echo "[]" > /app/ops.json
fi

# Wait for database to be ready
echo "Waiting for database..."
until nc -z $DB_HOST $DB_PORT 2>/dev/null; do
    echo "Database not ready, waiting..."
    sleep 2
done
echo "Database is ready!"

# Wait for Redis to be ready
echo "Waiting for Redis..."
until nc -z $REDIS_HOST $REDIS_PORT 2>/dev/null; do
    echo "Redis not ready, waiting..."
    sleep 2
done
echo "Redis is ready!"

# Start server
echo "========================================="
echo "  Starting Minecraft server..."
echo "========================================="

exec java $JAVA_OPTS \
    -Dtitan.server.name=$SERVER_NAME \
    -Dtitan.server.type=$SERVER_TYPE \
    -Dtitan.redis.host=$REDIS_HOST \
    -Dtitan.database.host=$DB_HOST \
    -jar paper.jar \
    --nogui \
    --world-dir /app/world

