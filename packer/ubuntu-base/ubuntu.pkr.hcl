# Packer Template for Ubuntu Base Image
# Author: Jatin Songara
# Description: Hardened Ubuntu AMI with pre-installed tools

packer {
  required_plugins {
    amazon = {
      version = ">= 1.2.0"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

# Variables
variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "ami_name_prefix" {
  type    = string
  default = "jatin-ubuntu-base"
}

variable "ssh_username" {
  type    = string
  default = "ubuntu"
}

# Data source for latest Ubuntu AMI
data "amazon-ami" "ubuntu" {
  filters = {
    name                = "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"
    root-device-type    = "ebs"
    virtualization-type = "hvm"
  }
  most_recent = true
  owners      = ["099720109477"] # Canonical
  region      = var.aws_region
}

# Source configuration
source "amazon-ebs" "ubuntu" {
  ami_name      = "${var.ami_name_prefix}-${formatdate("YYYY-MM-DD-hhmm", timestamp())}"
  instance_type = var.instance_type
  region        = var.aws_region
  source_ami    = data.amazon-ami.ubuntu.id
  ssh_username  = var.ssh_username
  
  # AMI configuration
  ami_description = "Hardened Ubuntu 22.04 base image with DevOps tools"
  
  ami_regions = [
    "us-east-1",
    "us-west-2"
  ]
  
  # Tags
  tags = {
    Name        = "${var.ami_name_prefix}"
    OS          = "Ubuntu 22.04"
    BuildDate   = "${formatdate("YYYY-MM-DD", timestamp())}"
    BuildBy     = "Packer"
    Owner       = "Jatin Songara"
    Environment = "Base"
  }
  
  # Snapshot tags
  snapshot_tags = {
    Name      = "${var.ami_name_prefix}-snapshot"
    BuildDate = "${formatdate("YYYY-MM-DD", timestamp())}"
  }
  
  # Launch configuration
  launch_block_device_mappings {
    device_name = "/dev/sda1"
    volume_size = 20
    volume_type = "gp3"
    iops        = 3000
    throughput  = 125
    encrypted   = true
    delete_on_termination = true
  }
}

# Build configuration
build {
  name    = "ubuntu-base"
  sources = ["source.amazon-ebs.ubuntu"]
  
  # Wait for cloud-init to complete
  provisioner "shell" {
    inline = [
      "echo 'Waiting for cloud-init to complete...'",
      "cloud-init status --wait"
    ]
  }
  
  # System updates
  provisioner "shell" {
    inline = [
      "echo '=== Updating system packages ==='",
      "sudo apt-get update",
      "sudo DEBIAN_FRONTEND=noninteractive apt-get upgrade -y",
      "sudo apt-get autoremove -y",
      "sudo apt-get clean"
    ]
  }
  
  # Install essential tools
  provisioner "shell" {
    inline = [
      "echo '=== Installing essential tools ==='",
      "sudo apt-get install -y \\",
      "  curl wget git vim htop \\",
      "  build-essential software-properties-common \\",
      "  apt-transport-https ca-certificates \\",
      "  gnupg lsb-release unzip jq \\",
      "  python3 python3-pip \\",
      "  fail2ban ufw"
    ]
  }
  
  # Install Docker
  provisioner "shell" {
    script = "scripts/install-docker.sh"
  }
  
  # Install AWS CLI
  provisioner "shell" {
    inline = [
      "echo '=== Installing AWS CLI ==='",
      "curl 'https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip' -o 'awscliv2.zip'",
      "unzip awscliv2.zip",
      "sudo ./aws/install",
      "rm -rf aws awscliv2.zip",
      "aws --version"
    ]
  }
  
  # Install kubectl
  provisioner "shell" {
    inline = [
      "echo '=== Installing kubectl ==='",
      "curl -LO 'https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl'",
      "sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl",
      "rm kubectl",
      "kubectl version --client"
    ]
  }
  
  # Install Terraform
  provisioner "shell" {
    inline = [
      "echo '=== Installing Terraform ==='",
      "wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg",
      "echo 'deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main' | sudo tee /etc/apt/sources.list.d/hashicorp.list",
      "sudo apt-get update",
      "sudo apt-get install -y terraform",
      "terraform version"
    ]
  }
  
  # Security hardening
  provisioner "shell" {
    script = "scripts/security-hardening.sh"
  }
  
  # Configure monitoring agent
  provisioner "shell" {
    inline = [
      "echo '=== Installing CloudWatch agent ==='",
      "wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb",
      "sudo dpkg -i -E ./amazon-cloudwatch-agent.deb",
      "rm amazon-cloudwatch-agent.deb"
    ]
  }
  
  # Cleanup
  provisioner "shell" {
    inline = [
      "echo '=== Cleaning up ==='",
      "sudo apt-get autoremove -y",
      "sudo apt-get clean",
      "sudo rm -rf /tmp/*",
      "sudo rm -rf /var/tmp/*",
      "history -c"
    ]
  }
  
  # Post-processor for manifest
  post-processor "manifest" {
    output     = "manifest.json"
    strip_path = true
  }
}
