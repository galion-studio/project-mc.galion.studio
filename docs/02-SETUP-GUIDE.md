# 🚀 SETUP GUIDE

**Last Updated**: 2025-11-09

---

## 📋 PREREQUISITES

### System Requirements

**Development Machine**:
- OS: Linux (Ubuntu 22.04+ recommended) or WSL2 on Windows
- RAM: 16GB minimum, 32GB recommended
- Disk: 100GB+ free space
- CPU: 8+ cores

**Production Cluster**:
- Kubernetes cluster (1.28+)
- Total resources: See Architecture doc for calculations
- Network: Low-latency, high-bandwidth

### Software Requirements

```bash
# Required tools
- Docker (24.0+)
- Kubernetes / kubectl (1.28+)
- Java 17 (OpenJDK)
- Git
- Python 3.10+ (for automation scripts)
- Redis CLI (for debugging)
- PostgreSQL client (for debugging)

# Optional but recommended
- k9s (Kubernetes terminal UI)
- Helm (package manager)
- Terraform (infrastructure as code)
- Ansible (configuration management)
```

---

## 🔧 INITIAL SETUP

### Step 1: Clone Repository

```bash
cd ~/projects
git clone https://github.com/galion-studio/project-mc-serv-mc.galion.studio
cd project-mc-serv-mc.galion.studio
```

### Step 2: Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Log out and back in for group changes

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install Java 17
sudo apt install -y openjdk-17-jdk openjdk-17-jre

# Install Python dependencies
pip3 install -r requirements.txt

# Install Redis CLI
sudo apt install -y redis-tools

# Install PostgreSQL client
sudo apt install -y postgresql-client
```

### Step 3: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit with your settings
nano .env
```

**.env example**:
```bash
# Minecraft Settings
MC_VERSION=1.20.4
MC_EULA=true
SERVER_PORT=25565
MAX_PLAYERS=100

# Database
POSTGRES_HOST=postgres.galion.svc.cluster.local
POSTGRES_PORT=5432
POSTGRES_DB=galion_mc
POSTGRES_USER=mcserver
POSTGRES_PASSWORD=CHANGE_ME_SECURE_PASSWORD

# Redis
REDIS_HOST=redis.galion.svc.cluster.local
REDIS_PORT=6379
REDIS_PASSWORD=CHANGE_ME_SECURE_PASSWORD

# Proxy
VELOCITY_SECRET=CHANGE_ME_RANDOM_STRING

# Monitoring
GRAFANA_ADMIN_PASSWORD=CHANGE_ME_SECURE_PASSWORD
```

---

## 🏗️ BUILD PROCESS

### Step 1: Build Hybrid Server Core

```bash
cd server-core

# Download base (Mohist)
./download-mohist.sh

# Apply custom patches
./apply-patches.sh

# Build custom server
./gradlew build

# Output: build/libs/galion-server-1.20.4.jar
```

### Step 2: Build Custom Plugins

```bash
cd ../plugins

# Build all custom plugins
./build-all.sh

# Outputs to: build/plugins/*.jar
```

### Step 3: Build Docker Images

```bash
cd ../infrastructure/docker

# Build all images
./build-all.sh

# Or build individually
docker build -t galion/velocity-proxy:latest -f Dockerfile.velocity .
docker build -t galion/hybrid-server:latest -f Dockerfile.server .
```

### Step 4: Push to Registry (Production)

```bash
# Tag for your registry
docker tag galion/velocity-proxy:latest registry.galion.studio/velocity-proxy:latest
docker tag galion/hybrid-server:latest registry.galion.studio/hybrid-server:latest

# Push
docker push registry.galion.studio/velocity-proxy:latest
docker push registry.galion.studio/hybrid-server:latest
```

---

## 🐳 LOCAL DEVELOPMENT SETUP

### Quick Start (Docker Compose)

```bash
cd infrastructure/docker

# Start minimal stack (1 proxy, 1 server, Redis, PostgreSQL)
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Connect to Minecraft
# IP: localhost:25565
```

### Stop & Clean

```bash
# Stop all containers
docker-compose down

# Remove volumes (CAUTION: deletes data)
docker-compose down -v
```

---

## ☸️ KUBERNETES DEPLOYMENT

### Step 1: Prepare Cluster

```bash
# Create namespaces
kubectl apply -f infrastructure/kubernetes/namespaces.yaml

# Create secrets
kubectl create secret generic db-credentials \
  --from-literal=username=mcserver \
  --from-literal=password=YOUR_SECURE_PASSWORD \
  -n galion-data

kubectl create secret generic redis-credentials \
  --from-literal=password=YOUR_SECURE_PASSWORD \
  -n galion-data
```

### Step 2: Deploy Data Layer

```bash
# Deploy PostgreSQL
kubectl apply -f infrastructure/kubernetes/postgresql/

# Deploy Redis
kubectl apply -f infrastructure/kubernetes/redis/

# Wait for ready
kubectl wait --for=condition=ready pod -l app=postgresql -n galion-data --timeout=300s
kubectl wait --for=condition=ready pod -l app=redis -n galion-data --timeout=300s
```

### Step 3: Initialize Database

```bash
# Run database migrations
kubectl apply -f infrastructure/kubernetes/jobs/db-init.yaml

# Check job status
kubectl get jobs -n galion-data
```

### Step 4: Deploy Proxy Layer

```bash
# Deploy Velocity proxies
kubectl apply -f infrastructure/kubernetes/velocity/

# Wait for ready
kubectl wait --for=condition=ready pod -l app=velocity -n galion-proxy --timeout=300s
```

### Step 5: Deploy Server Layer

```bash
# Deploy Minecraft servers
kubectl apply -f infrastructure/kubernetes/servers/

# Watch deployment
kubectl get pods -n galion-servers -w
```

### Step 6: Deploy Monitoring

```bash
# Deploy Prometheus
kubectl apply -f infrastructure/kubernetes/monitoring/prometheus/

# Deploy Grafana
kubectl apply -f infrastructure/kubernetes/monitoring/grafana/

# Get Grafana URL
kubectl get svc grafana -n galion-monitoring
```

### Step 7: Expose to Internet

```bash
# Deploy load balancer / ingress
kubectl apply -f infrastructure/kubernetes/ingress/

# Get external IP
kubectl get svc load-balancer -n galion-proxy
```

---

## 🔍 VERIFICATION

### Check All Components

```bash
# Run health check script
./scripts/health-check.sh
```

**Expected Output**:
```
✅ PostgreSQL: Healthy
✅ Redis: Healthy
✅ Velocity Proxy 1: Healthy
✅ Velocity Proxy 2: Healthy
✅ Server 1 (lobby): Healthy (TPS: 20.0)
✅ Server 2 (survival): Healthy (TPS: 20.0)
✅ Prometheus: Healthy
✅ Grafana: Healthy
```

### Test Player Connection

```bash
# Use test client
./scripts/test-connection.sh localhost 25565
```

### Check Logs

```bash
# Proxy logs
kubectl logs -f -l app=velocity -n galion-proxy

# Server logs
kubectl logs -f -l app=mc-server -n galion-servers

# Database logs
kubectl logs -f -l app=postgresql -n galion-data
```

---

## 🔧 COMMON ISSUES

### Issue 1: Server Won't Start

**Symptom**: Pod crashes or CrashLoopBackOff

**Check**:
```bash
kubectl describe pod <pod-name> -n galion-servers
kubectl logs <pod-name> -n galion-servers --previous
```

**Common Causes**:
- Insufficient memory (increase requests/limits)
- EULA not accepted (check environment variables)
- Missing dependencies (rebuild Docker image)

### Issue 2: Can't Connect

**Symptom**: Connection refused or timeout

**Check**:
```bash
# Check service
kubectl get svc -n galion-proxy

# Check firewall
sudo ufw status

# Test port
telnet <ip> 25565
```

**Common Causes**:
- Service not exposed
- Firewall blocking port 25565
- Proxy not routing correctly

### Issue 3: Lag / Low TPS

**Symptom**: TPS < 20, high MSPT

**Check**:
```bash
# Check server metrics
kubectl exec -it <server-pod> -n galion-servers -- rcon-cli tps
```

**Common Causes**:
- Too many entities (reduce spawn rates)
- View distance too high (reduce to 6-8)
- Insufficient CPU (increase limits or reduce player count)

---

## 📊 MONITORING ACCESS

### Grafana Dashboards

```bash
# Get Grafana URL
kubectl get ingress -n galion-monitoring

# Default credentials
Username: admin
Password: (from .env GRAFANA_ADMIN_PASSWORD)
```

**Default Dashboards**:
- Overview (player count, TPS, resource usage)
- Server Details (per-server metrics)
- Database Performance
- Network Traffic

### Prometheus Queries

Access: `http://<prometheus-url>:9090`

**Useful Queries**:
```promql
# Total player count
sum(minecraft_players_online)

# Average TPS
avg(minecraft_tps)

# CPU usage per server
rate(container_cpu_usage_seconds_total{namespace="galion-servers"}[5m])
```

---

## 🚀 SCALING OPERATIONS

### Manual Scaling

```bash
# Scale servers
kubectl scale deployment mc-server --replicas=20 -n galion-servers

# Scale proxies
kubectl scale deployment velocity-proxy --replicas=5 -n galion-proxy
```

### Auto-Scaling

Already configured via HPA (Horizontal Pod Autoscaler)

**Check auto-scaling**:
```bash
kubectl get hpa -n galion-servers
```

---

## 🔐 SECURITY HARDENING

### Production Checklist

- [ ] Change all default passwords
- [ ] Enable network policies (restrict inter-pod communication)
- [ ] Use TLS for database connections
- [ ] Enable DDoS protection (Cloudflare)
- [ ] Set up automated backups
- [ ] Configure log aggregation
- [ ] Enable audit logging
- [ ] Restrict kubectl access (RBAC)
- [ ] Use secrets management (Vault)
- [ ] Enable pod security policies

### Run Security Scan

```bash
# Scan Docker images
./scripts/security-scan.sh

# Check Kubernetes security
kubectl-scan --namespace galion-servers
```

---

## 📦 BACKUP & RESTORE

### Automated Backups

Configured via CronJob, runs daily at 3 AM UTC

**Check backup status**:
```bash
kubectl get cronjobs -n galion-data
kubectl get jobs -n galion-data
```

### Manual Backup

```bash
# Backup everything
./scripts/backup.sh

# Backup specific component
./scripts/backup.sh --database
./scripts/backup.sh --worlds
```

### Restore

```bash
# Restore from backup
./scripts/restore.sh --backup-file backups/2025-11-09-03-00.tar.gz
```

---

## 🎓 NEXT STEPS

1. Review architecture: `docs/01-ARCHITECTURE.md`
2. Develop custom plugins: `docs/03-API-DESIGN.md`
3. Optimize performance: `docs/05-OPTIMIZATION.md`
4. Run load tests: `tests/load-tests/README.md`

---

**Need help? Check progress log: `docs/00-PROGRESS.md`**

