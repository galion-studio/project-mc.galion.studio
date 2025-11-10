# 🚢 DEPLOYMENT GUIDE

**Last Updated**: 2025-11-09

---

## 🎯 DEPLOYMENT STRATEGIES

### Strategy 1: Development (Local)
- **Use Case**: Testing, plugin development
- **Infrastructure**: Docker Compose
- **Scale**: 1-3 servers
- **Cost**: Free (local resources)

### Strategy 2: Staging (Small Cluster)
- **Use Case**: Integration testing, load testing
- **Infrastructure**: Kubernetes (3-5 nodes)
- **Scale**: 10-20 servers (500-1000 players)
- **Cost**: ~$500-1000/month

### Strategy 3: Production (Full Scale)
- **Use Case**: Live 20k player server
- **Infrastructure**: Kubernetes (50-100 nodes)
- **Scale**: 200+ servers
- **Cost**: ~$8,000-12,000/month (optimized)

---

## 📦 PRE-DEPLOYMENT CHECKLIST

### Infrastructure
- [ ] Kubernetes cluster provisioned
- [ ] kubectl configured and tested
- [ ] Docker registry set up
- [ ] DNS configured
- [ ] SSL certificates obtained
- [ ] Firewall rules configured

### Configuration
- [ ] Environment variables set
- [ ] Secrets created
- [ ] Database initialized
- [ ] Redis cluster ready
- [ ] Backups configured

### Code
- [ ] All images built
- [ ] Images pushed to registry
- [ ] Config files validated
- [ ] Database migrations ready

### Monitoring
- [ ] Prometheus deployed
- [ ] Grafana dashboards imported
- [ ] Alerting configured
- [ ] Logging configured

---

## 🐳 DOCKER DEPLOYMENT

### Build All Images

```bash
cd infrastructure/docker

# Build Velocity proxy
docker build -t galion/velocity-proxy:1.0.0 \
  -f Dockerfile.velocity .

# Build hybrid server
docker build -t galion/hybrid-server:1.0.0 \
  -f Dockerfile.server .

# Build monitoring tools
docker build -t galion/monitoring:1.0.0 \
  -f Dockerfile.monitoring .
```

### Push to Registry

```bash
# Tag for registry
docker tag galion/velocity-proxy:1.0.0 registry.galion.studio/velocity-proxy:1.0.0
docker tag galion/hybrid-server:1.0.0 registry.galion.studio/hybrid-server:1.0.0

# Push
docker push registry.galion.studio/velocity-proxy:1.0.0
docker push registry.galion.studio/hybrid-server:1.0.0
```

### Local Development

```bash
# Start everything
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f velocity
docker-compose logs -f server-lobby
```

---

## ☸️ KUBERNETES DEPLOYMENT

### Step-by-Step Production Deployment

#### 1. Create Namespaces

```bash
kubectl apply -f - <<EOF
apiVersion: v1
kind: Namespace
metadata:
  name: galion-proxy
---
apiVersion: v1
kind: Namespace
metadata:
  name: galion-servers
---
apiVersion: v1
kind: Namespace
metadata:
  name: galion-data
---
apiVersion: v1
kind: Namespace
metadata:
  name: galion-monitoring
EOF
```

#### 2. Create Secrets

```bash
# Database credentials
kubectl create secret generic db-credentials \
  --from-literal=username=mcserver \
  --from-literal=password='YOUR_SECURE_PASSWORD_HERE' \
  -n galion-data

# Redis password
kubectl create secret generic redis-credentials \
  --from-literal=password='YOUR_SECURE_PASSWORD_HERE' \
  -n galion-data

# Velocity forwarding secret
kubectl create secret generic velocity-secret \
  --from-literal=secret='CHANGE_THIS_RANDOM_STRING' \
  -n galion-proxy

# Docker registry credentials
kubectl create secret docker-registry regcred \
  --docker-server=registry.galion.studio \
  --docker-username=admin \
  --docker-password='YOUR_REGISTRY_PASSWORD' \
  -n galion-proxy

kubectl create secret docker-registry regcred \
  --docker-server=registry.galion.studio \
  --docker-username=admin \
  --docker-password='YOUR_REGISTRY_PASSWORD' \
  -n galion-servers
```

#### 3. Deploy PostgreSQL

```bash
kubectl apply -f infrastructure/kubernetes/postgresql/statefulset.yaml
kubectl apply -f infrastructure/kubernetes/postgresql/service.yaml

# Wait for ready
kubectl wait --for=condition=ready pod/postgresql-0 \
  -n galion-data --timeout=300s

# Initialize database
kubectl apply -f infrastructure/kubernetes/postgresql/init-job.yaml
```

#### 4. Deploy Redis Cluster

```bash
kubectl apply -f infrastructure/kubernetes/redis/statefulset.yaml
kubectl apply -f infrastructure/kubernetes/redis/service.yaml

# Wait for ready
kubectl wait --for=condition=ready pod -l app=redis \
  -n galion-data --timeout=300s

# Initialize cluster
kubectl exec -it redis-0 -n galion-data -- \
  redis-cli --cluster create \
  redis-0.redis:6379 \
  redis-1.redis:6379 \
  redis-2.redis:6379 \
  redis-3.redis:6379 \
  redis-4.redis:6379 \
  redis-5.redis:6379 \
  --cluster-replicas 1
```

#### 5. Deploy Velocity Proxies

```bash
kubectl apply -f infrastructure/kubernetes/velocity/deployment.yaml
kubectl apply -f infrastructure/kubernetes/velocity/service.yaml
kubectl apply -f infrastructure/kubernetes/velocity/hpa.yaml

# Wait for ready
kubectl wait --for=condition=ready pod -l app=velocity \
  -n galion-proxy --timeout=300s
```

#### 6. Deploy Minecraft Servers

```bash
# Deploy lobby servers
kubectl apply -f infrastructure/kubernetes/servers/lobby/

# Deploy survival servers
kubectl apply -f infrastructure/kubernetes/servers/survival/

# Deploy creative servers
kubectl apply -f infrastructure/kubernetes/servers/creative/

# Wait for ready
kubectl get pods -n galion-servers -w
```

#### 7. Deploy Load Balancer

```bash
kubectl apply -f infrastructure/kubernetes/ingress/loadbalancer.yaml

# Get external IP
kubectl get svc load-balancer -n galion-proxy
```

#### 8. Deploy Monitoring Stack

```bash
# Prometheus
kubectl apply -f infrastructure/kubernetes/monitoring/prometheus/

# Grafana
kubectl apply -f infrastructure/kubernetes/monitoring/grafana/

# Alertmanager
kubectl apply -f infrastructure/kubernetes/monitoring/alertmanager/

# Get Grafana URL
kubectl get ingress -n galion-monitoring
```

---

## 🔄 ROLLING UPDATES

### Zero-Downtime Update Strategy

```bash
# Build new image
docker build -t galion/hybrid-server:1.0.1 .
docker push registry.galion.studio/hybrid-server:1.0.1

# Update deployment
kubectl set image deployment/mc-server \
  server=registry.galion.studio/hybrid-server:1.0.1 \
  -n galion-servers

# Watch rollout
kubectl rollout status deployment/mc-server -n galion-servers

# Rollback if needed
kubectl rollout undo deployment/mc-server -n galion-servers
```

### Blue-Green Deployment

```bash
# Deploy green (new version)
kubectl apply -f infrastructure/kubernetes/servers/survival/deployment-green.yaml

# Wait for healthy
kubectl wait --for=condition=ready pod -l version=green -n galion-servers

# Switch traffic (update service selector)
kubectl patch service mc-server -n galion-servers \
  -p '{"spec":{"selector":{"version":"green"}}}'

# Remove blue (old version) after verification
kubectl delete deployment mc-server-blue -n galion-servers
```

---

## 📊 AUTO-SCALING CONFIGURATION

### Horizontal Pod Autoscaler (HPA)

**For Minecraft Servers**:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: mc-server-hpa
  namespace: galion-servers
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: mc-server
  minReplicas: 10
  maxReplicas: 200
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: minecraft_players_online
      target:
        type: AverageValue
        averageValue: "80"  # 80 players per server
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Pods
        value: 5
        periodSeconds: 60
```

### Cluster Autoscaler

```yaml
# For cloud providers (AWS, GCP, Azure)
# Automatically adds/removes nodes based on pod requirements

# AWS example (using eksctl)
eksctl create cluster \
  --name galion-prod \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type m5.2xlarge \
  --nodes 10 \
  --nodes-min 10 \
  --nodes-max 100 \
  --asg-access
```

---

## 🌍 MULTI-REGION DEPLOYMENT

### Global Architecture

```
           ┌─────────────────────────────┐
           │   Global Load Balancer      │
           │   (GeoDNS / Cloudflare)     │
           └──────────┬──────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
   ┌────▼────┐   ┌────▼────┐   ┌───▼─────┐
   │ US-East │   │ EU-West │   │ AP-SE   │
   │ Cluster │   │ Cluster │   │ Cluster │
   └─────────┘   └─────────┘   └─────────┘
```

### Cross-Region Data Replication

**PostgreSQL**:
- Primary in US-East
- Read replicas in EU-West, AP-SE
- Streaming replication (async)

**Redis**:
- Active-Active with Redis Enterprise
- Or: Regional clusters with cross-region pub/sub

---

## 🔐 SECURITY HARDENING

### Network Policies

```yaml
# Restrict server to data layer communication
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: mc-server-policy
  namespace: galion-servers
spec:
  podSelector:
    matchLabels:
      app: mc-server
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: galion-proxy
    ports:
    - protocol: TCP
      port: 25565
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: galion-data
    ports:
    - protocol: TCP
      port: 5432  # PostgreSQL
    - protocol: TCP
      port: 6379  # Redis
```

### Pod Security Standards

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: galion-servers
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

### RBAC

```bash
# Create service account
kubectl create serviceaccount mc-server-sa -n galion-servers

# Create role
kubectl apply -f - <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: mc-server-role
  namespace: galion-servers
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["get", "list"]
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get"]
EOF

# Bind role to service account
kubectl create rolebinding mc-server-binding \
  --role=mc-server-role \
  --serviceaccount=galion-servers:mc-server-sa \
  -n galion-servers
```

---

## 📦 BACKUP & DISASTER RECOVERY

### Automated Backups

**CronJob for daily backups**:
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: backup-cron
  namespace: galion-data
spec:
  schedule: "0 3 * * *"  # 3 AM UTC daily
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: galion/backup:latest
            env:
            - name: BACKUP_TARGET
              value: "s3://galion-backups/"
            volumeMounts:
            - name: data
              mountPath: /data
          restartPolicy: OnFailure
          volumes:
          - name: data
            persistentVolumeClaim:
              claimName: server-data
```

### Disaster Recovery Plan

**RTO (Recovery Time Objective)**: 30 minutes  
**RPO (Recovery Point Objective)**: 1 hour

**Steps**:
1. Detect failure (automatic alerts)
2. Spin up new cluster (Terraform)
3. Restore database from latest backup
4. Deploy applications
5. Update DNS
6. Verify functionality

**Automation script**:
```bash
./scripts/disaster-recovery.sh \
  --backup-id 2025-11-09-03-00 \
  --region us-west-2
```

---

## 🔍 POST-DEPLOYMENT VERIFICATION

### Health Check Script

```bash
#!/bin/bash
# scripts/health-check.sh

echo "=== Galion Server Health Check ==="

# Check PostgreSQL
echo -n "PostgreSQL: "
kubectl exec -it postgresql-0 -n galion-data -- \
  psql -U mcserver -c "SELECT 1" > /dev/null 2>&1
[ $? -eq 0 ] && echo "✅ Healthy" || echo "❌ Failed"

# Check Redis
echo -n "Redis: "
kubectl exec -it redis-0 -n galion-data -- \
  redis-cli ping > /dev/null 2>&1
[ $? -eq 0 ] && echo "✅ Healthy" || echo "❌ Failed"

# Check Velocity
echo -n "Velocity Proxy: "
kubectl get pods -n galion-proxy -l app=velocity \
  --field-selector=status.phase=Running --no-headers | wc -l
echo "✅ $(kubectl get pods -n galion-proxy -l app=velocity --field-selector=status.phase=Running --no-headers | wc -l) instances running"

# Check Servers
echo -n "Minecraft Servers: "
kubectl get pods -n galion-servers -l app=mc-server \
  --field-selector=status.phase=Running --no-headers | wc -l
echo "✅ $(kubectl get pods -n galion-servers -l app=mc-server --field-selector=status.phase=Running --no-headers | wc -l) instances running"

echo ""
echo "=== Detailed Status ==="
kubectl top nodes
kubectl top pods -n galion-servers | head -10
```

### Load Testing

```bash
# Simulate player connections
cd tests/load-tests

# Test 100 players
./load-test.sh --players 100 --duration 300

# Test 1000 players
./load-test.sh --players 1000 --duration 600

# Test 5000 players (requires approval)
./load-test.sh --players 5000 --duration 900
```

---

## 📈 MONITORING DASHBOARDS

### Grafana Dashboard URLs

After deployment, access dashboards:

- **Overview**: `https://grafana.galion.studio/d/overview`
- **Server Details**: `https://grafana.galion.studio/d/server-details`
- **Database Performance**: `https://grafana.galion.studio/d/database`
- **Network Traffic**: `https://grafana.galion.studio/d/network`

### Key Metrics to Monitor

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| TPS | 20.0 | < 18.0 |
| MSPT | < 50ms | > 80ms |
| Player Count | - | - |
| CPU Usage | < 70% | > 85% |
| Memory Usage | < 80% | > 90% |
| Disk I/O | < 80% | > 90% |
| Network Latency | < 50ms | > 100ms |
| Database Query Time (p95) | < 10ms | > 50ms |
| Redis Latency (p95) | < 1ms | > 5ms |

---

## 🚨 TROUBLESHOOTING

### Issue: Pods Not Starting

```bash
# Check pod status
kubectl describe pod <pod-name> -n galion-servers

# Check logs
kubectl logs <pod-name> -n galion-servers

# Common causes:
# - Image pull error: Check registry credentials
# - Resource limits: Check node capacity
# - Mount failures: Check PVC status
```

### Issue: High Latency

```bash
# Check network latency
kubectl exec -it <pod-name> -n galion-servers -- ping redis.galion-data.svc.cluster.local

# Check database connections
kubectl exec -it postgresql-0 -n galion-data -- \
  psql -U mcserver -c "SELECT count(*) FROM pg_stat_activity;"

# Check resource usage
kubectl top pods -n galion-servers
```

### Issue: Database Connection Pool Exhausted

```bash
# Increase pool size in config
# Or scale database read replicas
kubectl scale deployment postgresql-replica --replicas=5 -n galion-data
```

---

## 📝 DEPLOYMENT CHECKLIST

### Pre-Launch
- [ ] All components deployed
- [ ] Health checks passing
- [ ] Load testing completed
- [ ] Monitoring dashboards configured
- [ ] Alerts set up
- [ ] Backups verified
- [ ] Security scan passed
- [ ] Performance tuning applied

### Launch
- [ ] DNS updated
- [ ] Traffic routed to new cluster
- [ ] Players can connect
- [ ] No errors in logs
- [ ] Metrics looking healthy

### Post-Launch
- [ ] Monitor for 24 hours
- [ ] Address any issues
- [ ] Document learnings
- [ ] Update runbooks

---

**Deploy with confidence. Scale with precision. 🚀**

