# Terragrunt - DRY Terraform

## Overview
Terragrunt configurations demonstrating DRY (Don't Repeat Yourself) principles for Terraform code.

## Features

- Remote state management with S3 and DynamoDB
- Automatic backend configuration
- Provider generation
- Environment-specific configurations
- Dependency management between modules

## Structure

```
terragrunt/
├── live/
│   ├── prod/
│   │   ├── terragrunt.hcl
│   │   ├── vpc/
│   │   ├── eks/
│   │   └── rds/
│   └── staging/
│       └── terragrunt.hcl
└── modules/
    ├── vpc/
    ├── eks/
    └── rds/
```

## Usage

```bash
# Initialize
cd live/prod/vpc
terragrunt init

# Plan
terragrunt plan

# Apply
terragrunt apply

# Apply all modules
terragrunt run-all apply
```

## Skills Demonstrated
- DRY Terraform configurations
- Remote state management
- Multi-environment setup
- Module dependencies
- Automated backend configuration
