# Monitoring & Observability Stack

## Overview
Complete monitoring solution with Prometheus, Grafana, and alerting for infrastructure and applications.

## Components

### Prometheus
- Metrics collection and storage
- Service discovery (Kubernetes, Consul)
- Multi-target scraping
- Alert rule evaluation

### Grafana
- Visualization dashboards
- Multi-datasource support
- Alert management
- User authentication

### Alertmanager
- Alert routing and grouping
- Notification channels (Slack, Email, PagerDuty)
- Silence management

### Exporters
- Node Exporter (system metrics)
- Postgres Exporter (database metrics)
- Redis Exporter (cache metrics)
- Nginx Exporter (web server metrics)
- Blackbox Exporter (endpoint monitoring)

## Deployment

```bash
# Deploy with Docker Compose
docker-compose -f monitoring/docker-compose.yml up -d

# Deploy to Kubernetes
kubectl apply -f monitoring/kubernetes/

# Access Grafana
http://localhost:3000
# Default credentials: admin/admin
```

## Dashboards Included
- Kubernetes Cluster Overview
- Node Metrics
- Application Performance
- Database Performance
- Network Traffic

## Skills Demonstrated
- Metrics collection and aggregation
- Dashboard creation
- Alert rule configuration
- Service discovery
- Multi-environment monitoring
- SLO/SLI tracking
