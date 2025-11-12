# Ansible Configuration Management

## Overview
Production-ready Ansible playbooks for automated server configuration, application deployment, and infrastructure management.

## Playbooks Included

### Web Server Setup
Complete web server configuration with:
- Nginx installation and configuration
- SSL/TLS with Let's Encrypt
- Firewall configuration (UFW)
- Security hardening (fail2ban, SSH hardening)
- Node.js and PM2 setup
- Log rotation

### Database Setup
PostgreSQL/MySQL configuration with:
- Installation and initialization
- Replication setup
- Backup automation
- Performance tuning

### Monitoring Stack
Prometheus and Grafana deployment

## Usage

```bash
# Test connectivity
ansible all -i inventory.ini -m ping

# Run web server setup
ansible-playbook -i inventory.ini web-server-setup/playbook.yml

# Run with specific tags
ansible-playbook -i inventory.ini web-server-setup/playbook.yml --tags security

# Dry run
ansible-playbook -i inventory.ini web-server-setup/playbook.yml --check
```

## Skills Demonstrated
- Playbook development
- Role-based organization
- Variable management
- Template usage (Jinja2)
- Handler implementation
- Idempotent operations
- Security hardening
