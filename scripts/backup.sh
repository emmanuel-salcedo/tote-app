#!/usr/bin/env bash
set -euo pipefail

# Backup Postgres and uploads. Requires Docker and a running db container.
# Usage: scripts/backup.sh /path/to/backup-dir

BACKUP_DIR=${1:-"./backups"}
TS=$(date +"%Y%m%d-%H%M%S")
mkdir -p "$BACKUP_DIR"

# Database dump (docker compose)
docker compose exec -T db pg_dump -U tote -d tote > "$BACKUP_DIR/db-$TS.sql"

# Uploads backup
if [ -d "./backend/uploads" ]; then
  tar -czf "$BACKUP_DIR/uploads-$TS.tgz" ./backend/uploads
fi

echo "Backup complete: $BACKUP_DIR"
