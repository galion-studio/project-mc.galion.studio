# 🚀 TITAN Deployment Guide

> **Philosophy**: Deploy fast, deploy often, deploy safely. Zero-downtime is the goal.

---

## Table of Contents
1. [Quick Start](#quick-start)
2. [Local Development](#local-development)
3. [Production Deployment](#production-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [CI/CD Pipeline](#cicd-pipeline)
6. [Monitoring Setup](#monitoring-setup)
7. [Backup & Recovery](#backup--recovery)
8. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Prerequisites
- Ubuntu 22.04 LTS (or similar Linux distribution)
- Docker 24.0+
- Docker Compose 2.0+
- 16GB+ RAM
- 4+ CPU cores
- 100GB+ storage

### One-Command Setup (Local Development)
```bash
# Clone repository
git clone https://github.com/yourusername/project-mc-serv-mc.galion.studio
cd project-mc-serv-mc.galion.studio

# Run bootstrap script
./automation/setup/bootstrap.sh

# Start development cluster
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f titan-proxy
```

**Result**: Local cluster running on `localhost:25565`

---

## Local Development

### Architecture
```
Your Computer
├── Docker Network (titan-network)
│   ├── titan-proxy:25577 → exposed as :25565
│   ├── titan-hub:25566
│   ├── titan-survival:25567
│   ├── redis:6379
│   ├── postgres:5432
│   ├── prometheus:9090
│   └── grafana:3000
```

### Docker Compose Configuration

**docker-compose.yml**:
```yaml
version: '3.9'

services:
  # Proxy server
  titan-proxy:
    build:
      context: ./titan-proxy
      dockerfile: ../docker/Dockerfile.proxy
    ports:
      - "25565:25577"  # Main Minecraft port
      - "8080:8080"    # Web dashboard
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    depends_on:
      - redis
      - titan-hub
    networks:
      - titan-network
    volumes:
      - ./titan-proxy/config:/app/config
      - proxy-data:/app/data

  # Hub/Lobby server
  titan-hub:
    build:
      context: ./titan-core
      dockerfile: ../docker/Dockerfile.server
    environment:
      - SERVER_TYPE=hub
      - SERVER_NAME=hub-1
      - REDIS_HOST=redis
      - DB_HOST=postgres
      - MAX_PLAYERS=1000
    depends_on:
      - redis
      - postgres
    networks:
      - titan-network
    volumes:
      - ./worlds/hub:/app/world
      - hub-data:/app/data

  # Game server (Survival)
  titan-survival:
    build:
      context: ./titan-core
      dockerfile: ../docker/Dockerfile.server
    environment:
      - SERVER_TYPE=survival
      - SERVER_NAME=survival-1
      - REDIS_HOST=redis
      - DB_HOST=postgres
      - MAX_PLAYERS=500
    depends_on:
      - redis
      - postgres
    networks:
      - titan-network
    volumes:
      - ./worlds/survival:/app/world
      - survival-data:/app/data

  # Redis (caching, pub/sub)
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - titan-network
    volumes:
      - redis-data:/data
    command: redis-server --appendonly yes

  # PostgreSQL (persistent data)
  postgres:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=titan
      - POSTGRES_USER=titan
      - POSTGRES_PASSWORD=changeme_in_production
    networks:
      - titan-network
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./database/schemas:/docker-entrypoint-initdb.d

  # Prometheus (metrics)
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    networks:
      - titan-network
    volumes:
      - ./monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus

  # Grafana (dashboards)
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    networks:
      - titan-network
    volumes:
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
      - grafana-data:/var/lib/grafana

networks:
  titan-network:
    driver: bridge

volumes:
  proxy-data:
  hub-data:
  survival-data:
  redis-data:
  postgres-data:
  prometheus-data:
  grafana-data:
```

### Development Commands

```bash
# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d titan-proxy

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f titan-survival

# Restart service
docker-compose restart titan-proxy

# Stop all services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v

# Build and restart after code changes
docker-compose up -d --build

# Scale game servers
docker-compose up -d --scale titan-survival=3

# Execute command in container
docker-compose exec titan-proxy bash

# View resource usage
docker stats
```

### Testing Your Setup

```bash
# Check if Minecraft server is responding
mcstatus localhost:25565 status

# Check if Redis is working
docker-compose exec redis redis-cli ping

# Check if PostgreSQL is accessible
docker-compose exec postgres psql -U titan -c "SELECT version();"

# View Prometheus targets
curl http://localhost:9090/api/v1/targets

# Access Grafana
open http://localhost:3000  # Default: admin/admin
```

---

## Production Deployment

### Server Requirements

#### Minimum Infrastructure (1,000 players)
- **Proxy**: 2 servers (2 vCPU, 4GB RAM each)
- **Game Servers**: 4 servers (4 vCPU, 16GB RAM each)
- **Redis**: 3 servers (2 vCPU, 4GB RAM each) - cluster
- **PostgreSQL**: 1 server (4 vCPU, 16GB RAM)
- **Monitoring**: 1 server (4 vCPU, 8GB RAM)

#### Recommended Cloud Providers
1. **DigitalOcean** - Simple, good for starting
2. **AWS** - Best scaling options
3. **Google Cloud** - Excellent networking
4. **Hetzner** - Best price/performance
5. **OVH** - Dedicated servers, DDoS protection

### Manual Deployment (Single Server)

**Step 1: Prepare Server**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose-plugin

# Create titan user
sudo useradd -m -s /bin/bash titan
sudo usermod -aG docker titan

# Switch to titan user
sudo su - titan
```

**Step 2: Clone & Configure**
```bash
# Clone repository
git clone https://github.com/yourusername/project-mc-serv-mc.galion.studio
cd project-mc-serv-mc.galion.studio

# Copy production config
cp .env.example .env

# Edit configuration
nano .env
```

**.env** (Production configuration):
```bash
# Environment
ENVIRONMENT=production

# Network
DOMAIN=mc.galion.studio
EXTERNAL_IP=YOUR_SERVER_IP

# Database
DB_HOST=postgres
DB_NAME=titan
DB_USER=titan
DB_PASSWORD=STRONG_PASSWORD_HERE

# Redis
REDIS_HOST=redis
REDIS_PASSWORD=ANOTHER_STRONG_PASSWORD

# Server Configuration
MAX_PLAYERS_PER_SERVER=500
VIEW_DISTANCE=8
SIMULATION_DISTANCE=6

# Java Options
JVM_MEMORY=14G
JVM_FLAGS=-XX:+UseG1GC -XX:MaxGCPauseMillis=200

# Monitoring
GRAFANA_ADMIN_PASSWORD=SECURE_PASSWORD
PROMETHEUS_RETENTION=30d

# Backups
BACKUP_ENABLED=true
BACKUP_INTERVAL=6h
BACKUP_RETENTION_DAYS=7
S3_BUCKET=titan-backups
AWS_ACCESS_KEY=YOUR_AWS_KEY
AWS_SECRET_KEY=YOUR_AWS_SECRET
```

**Step 3: Initialize Database**
```bash
# Start PostgreSQL first
docker-compose up -d postgres

# Wait for it to be ready
sleep 10

# Run migrations
docker-compose exec postgres psql -U titan -d titan -f /docker-entrypoint-initdb.d/01_schema.sql
```

**Step 4: Start Services**
```bash
# Start all services
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Test connection
mcstatus mc.galion.studio status
```

### Security Hardening

**Firewall Configuration** (UFW):
```bash
# Default: deny all incoming
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH (change port if needed)
sudo ufw allow 22/tcp

# Allow Minecraft
sudo ufw allow 25565/tcp

# Allow monitoring (restrict to your IP)
sudo ufw allow from YOUR_IP_ADDRESS to any port 3000  # Grafana
sudo ufw allow from YOUR_IP_ADDRESS to any port 9090  # Prometheus

# Enable firewall
sudo ufw enable
```

**Fail2ban** (DDoS protection):
```bash
# Install fail2ban
sudo apt install fail2ban -y

# Create Minecraft filter
sudo nano /etc/fail2ban/filter.d/minecraft.conf
```

**/etc/fail2ban/filter.d/minecraft.conf**:
```ini
[Definition]
failregex = ^.*\[Server thread/WARN\]: Failed to handle packet.*<HOST>.*$
            ^.*\[Server thread/INFO\]: Disconnecting.*<HOST>.*too many packets.*$
ignoreregex =
```

**Enable Minecraft jail**:
```bash
sudo nano /etc/fail2ban/jail.local
```

**/etc/fail2ban/jail.local**:
```ini
[minecraft]
enabled = true
port = 25565
filter = minecraft
logpath = /var/log/minecraft/*.log
maxretry = 10
bantime = 3600
```

---

## Kubernetes Deployment

### Prerequisites
- Kubernetes cluster (GKE, EKS, or self-hosted)
- kubectl configured
- Helm 3 installed

### Cluster Setup

**Create namespace**:
```bash
kubectl create namespace minecraft
kubectl config set-context --current --namespace=minecraft
```

**Install Helm charts** (dependencies):
```bash
# Redis cluster
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install redis bitnami/redis-cluster \
  --set cluster.nodes=6 \
  --set usePassword=true \
  --set password=YOUR_REDIS_PASSWORD \
  --namespace minecraft

# PostgreSQL
helm install postgres bitnami/postgresql \
  --set auth.database=titan \
  --set auth.username=titan \
  --set auth.password=YOUR_DB_PASSWORD \
  --set primary.persistence.size=100Gi \
  --namespace minecraft

# Prometheus + Grafana
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace minecraft
```

### Deploy Titan Components

**Apply Kubernetes manifests**:
```bash
# ConfigMaps and Secrets
kubectl apply -f kubernetes/config/

# Deployments
kubectl apply -f kubernetes/deployments/

# Services
kubectl apply -f kubernetes/services/

# HorizontalPodAutoscaler
kubectl apply -f kubernetes/autoscaling/

# Ingress (Load Balancer)
kubectl apply -f kubernetes/ingress/
```

**kubernetes/deployments/titan-proxy.yaml**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: titan-proxy
  namespace: minecraft
spec:
  replicas: 2
  selector:
    matchLabels:
      app: titan-proxy
  template:
    metadata:
      labels:
        app: titan-proxy
    spec:
      containers:
      - name: proxy
        image: your-registry/titan-proxy:latest
        ports:
        - containerPort: 25577
          name: minecraft
        - containerPort: 8080
          name: web
        env:
        - name: REDIS_HOST
          value: redis-cluster
        - name: DB_HOST
          value: postgres
        resources:
          requests:
            memory: "4Gi"
            cpu: "2"
          limits:
            memory: "8Gi"
            cpu: "4"
        livenessProbe:
          tcpSocket:
            port: 25577
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          tcpSocket:
            port: 25577
          initialDelaySeconds: 10
          periodSeconds: 5
```

**kubernetes/services/titan-proxy.yaml**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: titan-proxy
  namespace: minecraft
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"  # For AWS
spec:
  type: LoadBalancer
  selector:
    app: titan-proxy
  ports:
  - name: minecraft
    port: 25565
    targetPort: 25577
    protocol: TCP
  - name: web
    port: 8080
    targetPort: 8080
    protocol: TCP
```

### Monitoring Deployment

```bash
# Check all pods
kubectl get pods

# Check services
kubectl get svc

# Check HPA status
kubectl get hpa

# View pod logs
kubectl logs -f deployment/titan-proxy

# Describe pod (for troubleshooting)
kubectl describe pod <pod-name>

# Get external IP (for LoadBalancer)
kubectl get svc titan-proxy

# Port forward for local testing
kubectl port-forward svc/titan-proxy 25565:25565
```

---

## CI/CD Pipeline

### GitHub Actions Workflow

**.github/workflows/deploy.yml**:
```yaml
name: Build and Deploy

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_PREFIX: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up JDK 17
        uses: actions/setup-java@v3
        with:
          java-version: '17'
          distribution: 'temurin'
      
      - name: Build with Gradle
        run: ./gradlew build
      
      - name: Run tests
        run: ./gradlew test
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build-proxy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Log in to registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: ./titan-proxy
          push: true
          tags: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}/titan-proxy:latest
            ${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}/titan-proxy:${{ github.sha }}

  build-server:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build and push server image
        uses: docker/build-push-action@v4
        with:
          context: ./titan-core
          push: true
          tags: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}/titan-server:latest
            ${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}/titan-server:${{ github.sha }}

  deploy-staging:
    needs: [build-proxy, build-server]
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to staging
        run: |
          kubectl config use-context staging
          kubectl set image deployment/titan-proxy proxy=${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}/titan-proxy:${{ github.sha }}
          kubectl set image deployment/titan-server server=${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}/titan-server:${{ github.sha }}

  deploy-production:
    needs: [build-proxy, build-server]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to production
        run: |
          kubectl config use-context production
          kubectl set image deployment/titan-proxy proxy=${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}/titan-proxy:${{ github.sha }}
          kubectl rollout status deployment/titan-proxy
          kubectl set image deployment/titan-server server=${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}/titan-server:${{ github.sha }}
          kubectl rollout status deployment/titan-server
```

---

## Monitoring Setup

### Access Monitoring Dashboards

- **Grafana**: `http://your-server:3000` (admin/admin)
- **Prometheus**: `http://your-server:9090`
- **Kibana** (if ELK enabled): `http://your-server:5601`

### Import Titan Dashboards

Pre-built dashboards are in `monitoring/grafana/dashboards/`

1. Login to Grafana
2. Go to Dashboards → Import
3. Upload JSON files:
   - `minecraft-overview.json`
   - `server-performance.json`
   - `player-statistics.json`

---

## Backup & Recovery

### Automated Backups

**backup.sh** (runs every 6 hours):
```bash
#!/bin/bash
# automation/backup/backup.sh

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
S3_BUCKET="s3://titan-backups"

# Backup worlds
tar -czf "$BACKUP_DIR/worlds_$DATE.tar.gz" /app/worlds

# Backup database
docker-compose exec -T postgres pg_dump -U titan titan > "$BACKUP_DIR/db_$DATE.sql"

# Upload to S3
aws s3 cp "$BACKUP_DIR/worlds_$DATE.tar.gz" "$S3_BUCKET/worlds/"
aws s3 cp "$BACKUP_DIR/db_$DATE.sql" "$S3_BUCKET/database/"

# Clean old local backups (keep 3 days)
find "$BACKUP_DIR" -type f -mtime +3 -delete
```

### Disaster Recovery

**Restore from backup**:
```bash
# Stop services
docker-compose down

# Restore database
aws s3 cp s3://titan-backups/database/db_TIMESTAMP.sql /tmp/restore.sql
docker-compose up -d postgres
sleep 10
docker-compose exec -T postgres psql -U titan titan < /tmp/restore.sql

# Restore worlds
aws s3 cp s3://titan-backups/worlds/worlds_TIMESTAMP.tar.gz /tmp/worlds.tar.gz
tar -xzf /tmp/worlds.tar.gz -C /app/

# Start services
docker-compose up -d
```

---

## Troubleshooting

### Common Issues

#### Server won't start
```bash
# Check logs
docker-compose logs titan-survival

# Common causes:
# - Port already in use
# - Insufficient memory
# - Corrupt world data

# Fix: Check docker ps, increase memory, restore from backup
```

#### Players can't connect
```bash
# Test connectivity
mcstatus your-server:25565 ping

# Check firewall
sudo ufw status

# Check if port is listening
netstat -tlnp | grep 25565
```

#### Poor performance / Low TPS
```bash
# Check server resources
docker stats

# View Timings report
# In-game: /timings paste

# Common fixes:
# - Reduce view distance
# - Limit entities
# - Optimize plugins
# - Increase RAM
```

### Debug Mode

```bash
# Enable debug logging
docker-compose -f docker-compose.debug.yml up

# Attach debugger to Java process
docker-compose exec titan-survival jdb -attach 5005
```

---

**Document Status**: Complete  
**Last Updated**: 2025-11-09

