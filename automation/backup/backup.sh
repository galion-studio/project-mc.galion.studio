#!/bin/bash
# Titan Server - Backup Script
# Automated backup of worlds, database, and configuration
#
# Usage: ./automation/backup/backup.sh

set -e

# Configuration
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

# S3 Configuration (optional)
S3_ENABLED=${S3_ENABLED:-false}
S3_BUCKET=${S3_BUCKET:-""}

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================"
echo "  TITAN BACKUP - $DATE"
echo "========================================${NC}"
echo ""

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup worlds
echo -e "${BLUE}Backing up worlds...${NC}"
if [ -d "worlds" ]; then
    tar -czf "$BACKUP_DIR/worlds_$DATE.tar.gz" worlds/
    echo -e "${GREEN}✓ Worlds backed up: worlds_$DATE.tar.gz${NC}"
else
    echo -e "${YELLOW}⚠ No worlds directory found${NC}"
fi

# Backup database
echo -e "${BLUE}Backing up database...${NC}"
docker-compose exec -T postgres pg_dump -U titan titan > "$BACKUP_DIR/db_$DATE.sql"
gzip "$BACKUP_DIR/db_$DATE.sql"
echo -e "${GREEN}✓ Database backed up: db_$DATE.sql.gz${NC}"

# Backup plugins
echo -e "${BLUE}Backing up plugins...${NC}"
if [ -d "plugins" ]; then
    tar -czf "$BACKUP_DIR/plugins_$DATE.tar.gz" plugins/
    echo -e "${GREEN}✓ Plugins backed up: plugins_$DATE.tar.gz${NC}"
fi

# Backup configuration
echo -e "${BLUE}Backing up configuration...${NC}"
tar -czf "$BACKUP_DIR/config_$DATE.tar.gz" config/ .env 2>/dev/null || true
echo -e "${GREEN}✓ Configuration backed up: config_$DATE.tar.gz${NC}"

# Upload to S3 if enabled
if [ "$S3_ENABLED" = "true" ] && [ -n "$S3_BUCKET" ]; then
    echo -e "${BLUE}Uploading to S3...${NC}"
    aws s3 cp "$BACKUP_DIR/worlds_$DATE.tar.gz" "s3://$S3_BUCKET/worlds/" || echo -e "${YELLOW}⚠ S3 upload failed${NC}"
    aws s3 cp "$BACKUP_DIR/db_$DATE.sql.gz" "s3://$S3_BUCKET/database/" || echo -e "${YELLOW}⚠ S3 upload failed${NC}"
    echo -e "${GREEN}✓ Backups uploaded to S3${NC}"
fi

# Clean up old backups
echo -e "${BLUE}Cleaning old backups (older than $RETENTION_DAYS days)...${NC}"
find "$BACKUP_DIR" -type f -mtime +$RETENTION_DAYS -delete
echo -e "${GREEN}✓ Old backups cleaned${NC}"

# Show backup info
echo ""
echo -e "${BLUE}Backup Summary:${NC}"
ls -lh "$BACKUP_DIR"/*_$DATE* 2>/dev/null || true

# Calculate total backup size
TOTAL_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
echo ""
echo -e "${GREEN}✓ Backup complete!${NC}"
echo -e "Total backup size: $TOTAL_SIZE"
echo ""
