#!/bin/bash
# Titan Server - Restore Script
# Restores from backup

set -e

# Configuration
BACKUP_DIR="${BACKUP_DIR:-./backups}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check arguments
if [ -z "$1" ]; then
    echo -e "${RED}ERROR: No backup specified${NC}"
    echo "Usage: $0 <backup_name>"
    echo ""
    echo "Available backups:"
    ls -1 "$BACKUP_DIR" | grep "titan_backup_" | sed 's/_worlds.tar.gz//;s/_database.sql//;s/_config.tar.gz//' | sort -u
    exit 1
fi

BACKUP_NAME=$1

echo "========================================="
echo "  TITAN RESTORE - Starting"
echo "========================================="
echo "Restoring from: $BACKUP_NAME"
echo ""

# Confirmation
read -p "This will overwrite current data. Continue? (yes/no): " CONFIRM
if [ "$CONFIRM" != "yes" ]; then
    echo "Restore cancelled"
    exit 0
fi

# Stop servers
echo -e "${YELLOW}Stopping servers...${NC}"
docker-compose down
echo ""

# Restore worlds
echo -e "${YELLOW}[1/3]${NC} Restoring worlds..."
if [ -f "$BACKUP_DIR/${BACKUP_NAME}_worlds.tar.gz" ]; then
    tar -xzf "$BACKUP_DIR/${BACKUP_NAME}_worlds.tar.gz"
    echo -e "${GREEN}✓${NC} Worlds restored"
else
    echo -e "${RED}ERROR: Worlds backup not found${NC}"
fi
echo ""

# Restore database
echo -e "${YELLOW}[2/3]${NC} Restoring database..."
if [ -f "$BACKUP_DIR/${BACKUP_NAME}_database.sql" ]; then
    # Start PostgreSQL
    docker-compose up -d postgres
    sleep 5
    
    # Restore
    docker-compose exec -T postgres psql -U titan titan < "$BACKUP_DIR/${BACKUP_NAME}_database.sql"
    echo -e "${GREEN}✓${NC} Database restored"
else
    echo -e "${RED}ERROR: Database backup not found${NC}"
fi
echo ""

# Restore config
echo -e "${YELLOW}[3/3]${NC} Restoring configuration..."
if [ -f "$BACKUP_DIR/${BACKUP_NAME}_config.tar.gz" ]; then
    tar -xzf "$BACKUP_DIR/${BACKUP_NAME}_config.tar.gz"
    echo -e "${GREEN}✓${NC} Configuration restored"
else
    echo -e "${RED}ERROR: Config backup not found${NC}"
fi
echo ""

echo "========================================="
echo -e "  ${GREEN}RESTORE COMPLETE${NC}"
echo "========================================="
echo ""
echo "Start servers:"
echo "  docker-compose up -d"
echo ""

