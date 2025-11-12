# DevSecOps Demonstrations

## Overview
Security automation and compliance tools integrated into the DevOps pipeline.

## Tools & Scripts Included

### Security Scanning
- **Trivy Scanner**: Comprehensive vulnerability scanning
  - Container image scanning
  - Filesystem scanning
  - IaC misconfiguration detection
  - Secret detection

### Compliance Automation
- **Policy as Code**: OPA (Open Policy Admission) policies
- **Security Benchmarks**: CIS compliance checks
- **SAST Integration**: Static code analysis

### Secret Management
- **Vault Integration**: HashiCorp Vault setup
- **Secret Rotation**: Automated credential rotation
- **Encryption**: Data encryption at rest and in transit

## Usage

### Run Security Scan
```bash
# Scan filesystem and IaC
./trivy-scan.sh

# Scan specific Docker images
DOCKER_IMAGES="nginx:latest,node:18" ./trivy-scan.sh

# Custom severity levels
SEVERITY="MEDIUM,HIGH,CRITICAL" ./trivy-scan.sh
```

### Policy Enforcement
```bash
# Validate Kubernetes manifests
conftest test kubernetes/ --policy opa-policies/

# Check Terraform compliance
tfsec terraform/
```

## Skills Demonstrated
- Vulnerability scanning automation
- Security policy enforcement
- Compliance as Code
- Secret management
- Container security
- Infrastructure security
- SAST/DAST integration
- Security monitoring and alerting
