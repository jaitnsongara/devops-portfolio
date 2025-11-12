# Terragrunt Configuration for Production
# Author: Jatin Songara
# Description: DRY Terraform configuration with Terragrunt

# Configure Terragrunt to automatically store tfstate files in S3
remote_state {
  backend = "s3"
  
  config = {
    encrypt        = true
    bucket         = "jatin-terraform-state-${get_aws_account_id()}"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    
    s3_bucket_tags = {
      Name        = "Terraform State Storage"
      Environment = "Production"
      ManagedBy   = "Terragrunt"
    }
    
    dynamodb_table_tags = {
      Name        = "Terraform Lock Table"
      Environment = "Production"
      ManagedBy   = "Terragrunt"
    }
  }
  
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
}

# Generate provider configuration
generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  
  contents = <<EOF
provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Environment = "Production"
      ManagedBy   = "Terragrunt"
      Owner       = "Jatin Songara"
      Terraform   = "true"
    }
  }
}
EOF
}

# Configure root level variables
inputs = {
  aws_region   = "us-east-1"
  environment  = "production"
  project_name = "jatin-demo"
  
  # Common tags
  common_tags = {
    Project     = "DevOps Portfolio"
    Owner       = "Jatin Songara"
    Environment = "Production"
    CostCenter  = "Engineering"
  }
}

# Terraform version constraint
terraform_version_constraint  = ">= 1.0"
terragrunt_version_constraint = ">= 0.45"
