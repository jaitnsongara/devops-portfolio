#!/bin/bash
# AWS EC2 Snapshot Backup Script
# Author: Jatin Songara
# Description: Automated EBS volume backup with retention policy

set -euo pipefail

# Configuration
REGION="${AWS_REGION:-us-east-1}"
RETENTION_DAYS="${RETENTION_DAYS:-7}"
TAG_KEY="AutoBackup"
TAG_VALUE="true"
LOG_FILE="/var/log/aws-backup.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${NC} $*" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $*" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $*" | tee -a "$LOG_FILE"
}

# Check AWS CLI installation
check_prerequisites() {
    if ! command -v aws &> /dev/null; then
        error "AWS CLI is not installed"
        exit 1
    fi
    
    if ! aws sts get-caller-identity &> /dev/null; then
        error "AWS credentials not configured"
        exit 1
    fi
    
    success "Prerequisites check passed"
}

# Get volumes to backup
get_volumes() {
    log "Fetching volumes with tag ${TAG_KEY}=${TAG_VALUE}"
    
    aws ec2 describe-volumes \
        --region "$REGION" \
        --filters "Name=tag:${TAG_KEY},Values=${TAG_VALUE}" \
        --query 'Volumes[*].VolumeId' \
        --output text
}

# Create snapshot
create_snapshot() {
    local volume_id=$1
    local description="Automated backup of ${volume_id} on $(date +'%Y-%m-%d %H:%M:%S')"
    
    log "Creating snapshot for volume: ${volume_id}"
    
    snapshot_id=$(aws ec2 create-snapshot \
        --region "$REGION" \
        --volume-id "$volume_id" \
        --description "$description" \
        --tag-specifications "ResourceType=snapshot,Tags=[{Key=Name,Value=Backup-${volume_id}},{Key=CreatedBy,Value=AutoBackup},{Key=VolumeId,Value=${volume_id}}]" \
        --query 'SnapshotId' \
        --output text)
    
    if [ -n "$snapshot_id" ]; then
        success "Snapshot created: ${snapshot_id}"
        return 0
    else
        error "Failed to create snapshot for ${volume_id}"
        return 1
    fi
}

# Delete old snapshots
cleanup_old_snapshots() {
    log "Cleaning up snapshots older than ${RETENTION_DAYS} days"
    
    cutoff_date=$(date -u -d "${RETENTION_DAYS} days ago" +%Y-%m-%d)
    
    old_snapshots=$(aws ec2 describe-snapshots \
        --region "$REGION" \
        --owner-ids self \
        --filters "Name=tag:CreatedBy,Values=AutoBackup" \
        --query "Snapshots[?StartTime<='${cutoff_date}'].SnapshotId" \
        --output text)
    
    if [ -z "$old_snapshots" ]; then
        log "No old snapshots to delete"
        return 0
    fi
    
    for snapshot_id in $old_snapshots; do
        log "Deleting old snapshot: ${snapshot_id}"
        if aws ec2 delete-snapshot --region "$REGION" --snapshot-id "$snapshot_id"; then
            success "Deleted snapshot: ${snapshot_id}"
        else
            error "Failed to delete snapshot: ${snapshot_id}"
        fi
    done
}

# Main execution
main() {
    log "=== Starting AWS Backup Process ==="
    
    check_prerequisites
    
    volumes=$(get_volumes)
    
    if [ -z "$volumes" ]; then
        warning "No volumes found with tag ${TAG_KEY}=${TAG_VALUE}"
        exit 0
    fi
    
    backup_count=0
    failed_count=0
    
    for volume_id in $volumes; do
        if create_snapshot "$volume_id"; then
            ((backup_count++))
        else
            ((failed_count++))
        fi
    done
    
    cleanup_old_snapshots
    
    log "=== Backup Process Complete ==="
    log "Successful backups: ${backup_count}"
    log "Failed backups: ${failed_count}"
    
    if [ "$failed_count" -gt 0 ]; then
        exit 1
    fi
}

# Run main function
main "$@"
