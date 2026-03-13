#!/bin/bash
# OpenClaw Daily Backup Script
# Runs every day at 4:00 AM
# Keeps 7 days of backups, pushes to GitHub

export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
export HOME=/root

BACKUP_DIR="/root/openclaw-backups"
GITHUB_REPO="/root/.openclaw/workspace/solution"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create backup directory if not exists
mkdir -p "$BACKUP_DIR"

echo "[$(date)] Starting OpenClaw backup..."

# Create backup
cd /root
BACKUP_FILE="${TIMESTAMP}-openclaw-backup.tar.gz"
openclaw backup create

# Find the created backup file
LATEST_BACKUP=$(ls -t /root/*-openclaw-backup.tar.gz 2>/dev/null | head -1)

if [ -f "$LATEST_BACKUP" ]; then
    # Move to backup directory
    mv "$LATEST_BACKUP" "$BACKUP_DIR/$BACKUP_FILE"
    echo "[$(date)] Backup created: $BACKUP_FILE"
    
    # Verify backup
    if openclaw backup verify "$BACKUP_DIR/$BACKUP_FILE"; then
        echo "[$(date)] Backup verified successfully"
        
        # Copy to GitHub repo
        mkdir -p "$GITHUB_REPO/backups"
        cp "$BACKUP_DIR/$BACKUP_FILE" "$GITHUB_REPO/backups/"
        
        # Push to GitHub
        cd "$GITHUB_REPO"
        git add backups/
        git commit -m "Auto-backup: $DATE"
        git push origin master
        echo "[$(date)] Backup pushed to GitHub"
    else
        echo "[$(date)] Backup verification failed!"
        rm -f "$BACKUP_DIR/$BACKUP_FILE"
    fi
else
    echo "[$(date)] Backup file not found!"
fi

# Clean up old backups (keep 7 days)
echo "[$(date)] Cleaning up old backups..."
find "$BACKUP_DIR" -name "*-openclaw-backup.tar.gz" -mtime +7 -delete
find "$GITHUB_REPO/backups" -name "*-openclaw-backup.tar.gz" -mtime +7 -delete

# Clean up old backup files in /root
find /root -name "*-openclaw-backup.tar.gz" -mtime +1 -delete 2>/dev/null

echo "[$(date)] Backup process complete!"
echo "---"
