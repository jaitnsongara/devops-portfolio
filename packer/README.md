# Packer Image Building

## Overview
Automated machine image creation with security hardening and pre-installed DevOps tools.

## Images Included

### Ubuntu Base Image
Hardened Ubuntu 22.04 AMI with:
- Docker and Docker Compose
- AWS CLI
- kubectl
- Terraform
- Security hardening (fail2ban, UFW)
- CloudWatch agent
- Essential DevOps tools

## Usage

```bash
# Initialize Packer
packer init ubuntu-base/ubuntu.pkr.hcl

# Validate template
packer validate ubuntu-base/ubuntu.pkr.hcl

# Build image
packer build ubuntu-base/ubuntu.pkr.hcl

# Build with variables
packer build -var 'aws_region=us-west-2' ubuntu-base/ubuntu.pkr.hcl
```

## Skills Demonstrated
- HCL2 template development
- Multi-region AMI distribution
- Provisioner usage (shell, file, ansible)
- Security hardening automation
- Image optimization
- Post-processor implementation
