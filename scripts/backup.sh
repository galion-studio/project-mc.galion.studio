#!/bin/bash
# Galion Backup Script
# Creates backups of database, worlds, and configurations

set -e

# Configuration
BACKUP_DIR="backups"
TIMESTAMP=$(date +%Y-%m-%d-%H-%M)
BACKUP_FILE="${BACKUP_DIR}/galion-backup-${TIMESTAMP}.tar.gz"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Create backup directory
mkdir -p "${BACKUP_DIR}"

log_info "Starting backup at ${TIMESTAMP}"

# Backup PostgreSQL
log_info "Backing up PostgreSQL database..."
kubectl exec postgresql-0 -n galion-data -- \
    pg_dump -U mcserver galion_mc > "${BACKUP_DIR}/database-${TIMESTAMP}.sql"

# Backup Redis (if persistence enabled)
log_info "Backing up Redis data..."
kubectl exec redis-0 -n galion-data -- \
    redis-cli BGSAVE > /dev/null 2>&1 || log_warn "Redis backup skipped (no persistence)"

# Backup world data
log_info "Backing up world data..."
# This creates a temporary pod to copy world data
kubectl run backup-helper --image=alpine --restart=Never -n galion-servers \
    --overrides='{"spec":{"volumes":[{"name":"server-data","persistentVolumeClaim":{"claimName":"server-data"}}],"containers":[{"name":"backup","image":"alpine","command":["sleep","3600"],"volumeMounts":[{"name":"server-data","mountPath":"/data"}]}]}}'

# Wait for pod to be ready
sleep 10

# Copy world data
kubectl cp galion-servers/backup-helper:/data "${BACKUP_DIR}/worlds-${TIMESTAMP}" || log_warn "World backup may be incomplete"

# Cleanup helper pod
kubectl delete pod backup-helper -n galion-servers

# Backup configurations
log_info "Backing up configurations..."
mkdir -p "${BACKUP_DIR}/configs-${TIMESTAMP}"
cp -r infrastructure/kubernetes "${BACKUP_DIR}/configs-${TIMESTAMP}/"
cp -r infrastructure/docker/config "${BACKUP_DIR}/configs-${TIMESTAMP}/"
cp .env "${BACKUP_DIR}/configs-${TIMESTAMP}/" 2>/dev/null || log_warn ".env not found"

# Create compressed archive
log_info "Creating compressed archive..."
tar -czf "${BACKUP_FILE}" \
    "${BACKUP_DIR}/database-${TIMESTAMP}.sql" \
    "${BACKUP_DIR}/configs-${TIMESTAMP}" \
    2>/dev/null || log_warn "Some files may not be included"

# Cleanup temporary files
rm -rf "${BACKUP_DIR}/database-${TIMESTAMP}.sql"
rm -rf "${BACKUP_DIR}/configs-${TIMESTAMP}"
rm -rf "${BACKUP_DIR}/worlds-${TIMESTAMP}"

log_info "Backup complete: ${BACKUP_FILE}"

# Optional: Upload to S3 (if configured)
if [ -n "$AWS_ACCESS_KEY_ID" ] && [ -n "$S3_BACKUP_BUCKET" ]; then
    log_info "Uploading to S3..."
    aws s3 cp "${BACKUP_FILE}" "s3://${S3_BACKUP_BUCKET}/" || log_warn "S3 upload failed"
fi

# Cleanup old backups (keep last 7 days)
log_info "Cleaning up old backups..."
find "${BACKUP_DIR}" -name "galion-backup-*.tar.gz" -mtime +7 -delete

log_info "Backup process complete!"

