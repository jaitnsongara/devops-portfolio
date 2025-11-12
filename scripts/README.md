# Automation Scripts

## Overview
Production-ready automation scripts for infrastructure management, monitoring, and deployment tasks.

## Bash Scripts

### aws-backup.sh
Automated EBS volume backup with retention policy
- Creates snapshots of tagged volumes
- Implements retention policy
- Logging and error handling
- Email notifications (optional)

**Usage:**
```bash
export AWS_REGION=us-east-1
export RETENTION_DAYS=7
./aws-backup.sh
```

## Python Scripts

### k8s-health-check.py
Comprehensive Kubernetes cluster health monitoring
- Node status verification
- Pod health checks
- Deployment status
- Storage (PVC) validation
- Detailed reporting

**Usage:**
```bash
python3 k8s-health-check.py --namespace production
```

## Skills Demonstrated
- Error handling and logging
- AWS API integration
- Kubernetes API interaction
- Automation best practices
- Production-ready code quality
