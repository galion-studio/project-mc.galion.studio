# 📈 TITAN Scaling Strategy

> **Goal**: Scale from 0 to 20,000 concurrent players with optimal performance and cost efficiency

---

## Table of Contents
1. [Scaling Philosophy](#scaling-philosophy)
2. [Capacity Planning](#capacity-planning)
3. [Horizontal Scaling](#horizontal-scaling)
4. [Vertical Scaling](#vertical-scaling)
5. [Auto-Scaling Logic](#auto-scaling-logic)
6. [Performance Targets](#performance-targets)
7. [Cost Analysis](#cost-analysis)

---

## Scaling Philosophy

### First Principles
**Question**: How do we serve 20,000 players simultaneously?

**Answer**: Distribute the load across many servers, each running optimally

### Key Principles
1. **Think in clusters, not single servers**
2. **Scale horizontally first** (add servers) before vertically (bigger servers)
3. **Automate everything** - humans can't react fast enough
4. **Monitor aggressively** - you can't optimize what you don't measure
5. **Over-provision slightly** - better than crashes during spikes

---

## Capacity Planning

### Server Capacity Per Instance

#### Game Server (Optimized Paper)
- **Hardware**: 4 vCPU, 16GB RAM
- **Comfortable Load**: 400 players
- **Maximum Load**: 500 players (80% threshold)
- **Target TPS**: 19.5+ (Minecraft ideal: 20)

**Reasoning**:
- 16GB allows 14GB for JVM (generous heap)
- 4 vCPU handles async tasks efficiently
- 400 players = ~2,000 entities (players + mobs)
- Chunk loading: ~40 chunks per player = 16,000 chunks
- Network: ~400 * 50KB/s = 20MB/s bandwidth

#### Hub/Lobby Server
- **Hardware**: 4 vCPU, 8GB RAM
- **Comfortable Load**: 800 players
- **Maximum Load**: 1,000 players
- **Target TPS**: 19.8+

**Reasoning**:
- No complex world simulation (flat lobby)
- Minimal entities
- Players just chatting/navigating menus
- Can handle 2x density of game servers

#### Proxy Server (Titan Proxy)
- **Hardware**: 8 vCPU, 16GB RAM
- **Capacity**: 5,000 concurrent connections
- **Throughput**: 500 connections/second

**Reasoning**:
- Proxy is lightweight (just routing packets)
- Main bottleneck is network I/O
- Need burst capacity for login storms

### Total Infrastructure

| Player Count | Hub Servers | Game Servers | Proxy Servers | Total Servers |
|--------------|-------------|--------------|---------------|---------------|
| 500          | 1           | 2            | 1             | 4             |
| 1,000        | 1           | 3            | 1             | 5             |
| 2,000        | 2           | 5            | 1             | 8             |
| 5,000        | 3           | 12           | 2             | 17            |
| 10,000       | 5           | 25           | 3             | 33            |
| 15,000       | 7           | 38           | 4             | 49            |
| 20,000       | 10          | 50           | 5             | 65            |

**Supporting Infrastructure** (constant):
- Redis Cluster: 3 nodes (HA)
- PostgreSQL: 1 primary + 2 read replicas
- Load Balancer: 2 nodes (HA)
- Monitoring: 3 nodes (Prometheus, Grafana, ELK)

**Total at 20k players**: ~75 servers

---

## Horizontal Scaling

### Auto-Scaling Triggers

#### Scale UP (Add Server) When:
1. **Average CPU > 70%** across all servers of that type
2. **Average Player Count > 80%** of capacity
3. **TPS < 19.0** for more than 2 minutes
4. **Queue length > 50** players waiting to join

#### Scale DOWN (Remove Server) When:
1. **Average CPU < 30%** for 10+ minutes
2. **Average Player Count < 40%** of capacity
3. **Excess capacity** (more than 2 empty servers)

**Cooldown Period**: 
- Scale up: 2 minutes (fast response to load)
- Scale down: 15 minutes (prevent flapping)

### Scaling Strategy by Phase

#### Phase 1: Manual Scaling (0-1,000 players)
**Goal**: Prove the architecture, gather metrics

**Infrastructure**:
- 1 proxy
- 1 hub server
- 3 game servers (survival, creative, minigame)
- 3 Redis nodes
- 1 PostgreSQL

**Cost**: ~$300/month

**Duration**: First month, onboarding initial players

#### Phase 2: Semi-Auto Scaling (1,000-5,000 players)
**Goal**: Implement auto-scaling, optimize costs

**Infrastructure**:
- 2 proxies (HA)
- 3 hub servers
- 12 game servers (auto-scale 5-20)
- 3 Redis nodes (cluster)
- 1 PostgreSQL + 1 read replica

**Cost**: ~$1,200/month

**Features**:
- Kubernetes HPA (Horizontal Pod Autoscaler)
- Automated server provisioning
- Basic predictive scaling (time of day)

#### Phase 3: Full Auto Scaling (5,000-20,000 players)
**Goal**: Handle massive scale automatically

**Infrastructure**:
- 5 proxies (geo-distributed)
- 10 hub servers (auto-scale 5-15)
- 50 game servers (auto-scale 20-80)
- 5 Redis nodes (cluster)
- 1 PostgreSQL + 3 read replicas

**Cost**: ~$5,000-8,000/month

**Features**:
- Multi-region deployment
- ML-based predictive scaling
- Spot instance utilization for cost savings
- Advanced load balancing

---

## Vertical Scaling

### Per-Server Optimization

#### JVM Tuning

**Base Configuration** (16GB server):
```bash
java -Xms14G -Xmx14G \
  -XX:+UseG1GC \
  -XX:+ParallelRefProcEnabled \
  -XX:MaxGCPauseMillis=200 \
  -XX:+UnlockExperimentalVMOptions \
  -XX:+DisableExplicitGC \
  -XX:+AlwaysPreTouch \
  -XX:G1NewSizePercent=30 \
  -XX:G1MaxNewSizePercent=40 \
  -XX:G1HeapRegionSize=8M \
  -XX:G1ReservePercent=20 \
  -XX:G1HeapWastePercent=5 \
  -XX:G1MixedGCCountTarget=4 \
  -XX:InitiatingHeapOccupancyPercent=15 \
  -XX:G1MixedGCLiveThresholdPercent=90 \
  -XX:G1RSetUpdatingPauseTimePercent=5 \
  -XX:SurvivorRatio=32 \
  -XX:+PerfDisableSharedMem \
  -XX:MaxTenuringThreshold=1 \
  -Dusing.aikars.flags=https://mcflags.emc.gs \
  -Daikars.new.flags=true \
  -jar titan-server.jar nogui
```

**Why These Flags?**
- `-Xms14G -Xmx14G`: Fixed heap (prevents resizing overhead)
- `-XX:+UseG1GC`: Best GC for large heaps
- `-XX:MaxGCPauseMillis=200`: Limit pause times (reduces lag spikes)
- `-XX:+AlwaysPreTouch`: Pre-allocate memory (faster startup)
- G1 tuning: Optimize for low pause times

#### Server Configuration

**server.properties**:
```properties
# Network optimization
network-compression-threshold=256
max-tick-time=60000

# Performance
view-distance=8
simulation-distance=6
spawn-protection=0

# Chunk management
max-chained-neighbor-updates=1000000

# Entity limits
spawn-limits.monster=50
spawn-limits.creature=15
spawn-limits.ambient=15
spawn-limits.water-creature=7
spawn-limits.water-ambient=10
```

**paper-world-defaults.yml**:
```yaml
entities:
  armor-stands:
    tick: false
  spawning:
    per-player-mob-spawns: true
    alt-item-despawn-rate:
      enabled: true
      
chunks:
  auto-save-interval: 6000  # 5 minutes instead of 6000 ticks
  delay-chunk-unloads-by: 10s
  entity-per-chunk-save-limit:
    arrow: 16
    
misc:
  fix-climbing-bypassing-cramming-rule: true
  light-queue-size: 20
  max-leash-distance: 10.0
```

**Expected Performance**:
- TPS: 19.5-20.0 (optimal)
- RAM Usage: 10-12GB (out of 14GB allocated)
- CPU Usage: 60-80% under load
- Chunk Load Time: <50ms
- Player Join Time: <2 seconds

#### Network Optimization

**Linux Kernel Tuning** (`/etc/sysctl.conf`):
```bash
# Increase network buffers
net.core.rmem_max=134217728
net.core.wmem_max=134217728
net.ipv4.tcp_rmem=4096 87380 67108864
net.ipv4.tcp_wmem=4096 65536 67108864

# TCP optimization
net.ipv4.tcp_congestion_control=bbr
net.core.default_qdisc=fq
net.ipv4.tcp_slow_start_after_idle=0
net.ipv4.tcp_tw_reuse=1

# Connection limits
net.core.somaxconn=8192
net.ipv4.tcp_max_syn_backlog=8192
net.core.netdev_max_backlog=5000

# File descriptor limits
fs.file-max=2097152
```

---

## Auto-Scaling Logic

### Kubernetes Configuration

**HorizontalPodAutoscaler** (Game Servers):
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: titan-game-server-hpa
  namespace: minecraft
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: titan-game-server
  minReplicas: 5
  maxReplicas: 80
  metrics:
  # CPU-based scaling
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  # Custom metric: Player count
  - type: Pods
    pods:
      metric:
        name: minecraft_players_online
      target:
        type: AverageValue
        averageValue: "400"  # Target 400 players per server
  # Custom metric: TPS
  - type: Pods
    pods:
      metric:
        name: minecraft_tps
      target:
        type: AverageValue
        averageValue: "19.5"  # Scale if TPS drops below 19.5
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50  # Increase by 50% of current pods
        periodSeconds: 60
      - type: Pods
        value: 2   # Or add 2 pods, whichever is higher
        periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300  # Wait 5 minutes before scaling down
      policies:
      - type: Percent
        value: 25  # Decrease by 25% at a time
        periodSeconds: 60
```

### Custom Scaling Logic

**Predictive Scaling** (Python script):
```python
# automation/scaling/predictive_scaler.py

import datetime
from kubernetes import client, config

def predict_player_count(current_hour, day_of_week):
    """
    Predict player count based on historical data
    Returns expected player count for next hour
    """
    # Historical patterns (example data)
    patterns = {
        'weekday': {
            6: 500,    # 6 AM
            12: 2000,  # Noon
            18: 8000,  # 6 PM (peak)
            22: 5000,  # 10 PM
        },
        'weekend': {
            6: 1000,
            12: 10000,  # Weekend peak
            18: 15000,  # Weekend evening peak
            22: 12000,
        }
    }
    
    schedule = 'weekend' if day_of_week >= 5 else 'weekday'
    return patterns[schedule].get(current_hour, 1000)

def calculate_required_servers(predicted_players):
    """
    Calculate how many servers needed for predicted load
    """
    PLAYERS_PER_SERVER = 400
    BUFFER_MULTIPLIER = 1.2  # 20% buffer
    
    required = (predicted_players / PLAYERS_PER_SERVER) * BUFFER_MULTIPLIER
    return int(required) + 1  # Always round up

def scale_preemptively():
    """
    Scale infrastructure before expected load increase
    """
    now = datetime.datetime.now()
    next_hour = (now + datetime.timedelta(hours=1)).hour
    day_of_week = now.weekday()
    
    predicted_players = predict_player_count(next_hour, day_of_week)
    required_servers = calculate_required_servers(predicted_players)
    
    # Get current server count from Kubernetes
    config.load_incluster_config()
    apps_v1 = client.AppsV1Api()
    deployment = apps_v1.read_namespaced_deployment(
        name="titan-game-server",
        namespace="minecraft"
    )
    
    current_replicas = deployment.spec.replicas
    
    # Scale if difference is significant
    if abs(required_servers - current_replicas) >= 2:
        deployment.spec.replicas = required_servers
        apps_v1.patch_namespaced_deployment(
            name="titan-game-server",
            namespace="minecraft",
            body=deployment
        )
        print(f"Scaled to {required_servers} servers (predicted {predicted_players} players)")

# Run every 30 minutes
if __name__ == "__main__":
    scale_preemptively()
```

---

## Performance Targets

### Key Metrics

| Metric | Target | Acceptable | Critical |
|--------|--------|------------|----------|
| TPS (Ticks Per Second) | 20.0 | 19.5+ | <18.0 |
| Player Join Time | <2s | <5s | >10s |
| Cross-Server Transfer | <1s | <3s | >5s |
| CPU Usage (per server) | 60-70% | <85% | >90% |
| RAM Usage | 70-80% | <90% | >95% |
| Network Latency | <50ms | <100ms | >200ms |
| Database Query Time | <10ms | <50ms | >100ms |
| Redis Response Time | <1ms | <5ms | >10ms |

### Monitoring & Alerts

**Critical Alerts** (Immediate action):
- TPS < 18.0 for 1 minute
- Any server CPU > 90% for 2 minutes
- Any server RAM > 95%
- Database connection pool exhausted
- Proxy disconnects > 10/minute

**Warning Alerts** (Investigate soon):
- TPS < 19.5 for 5 minutes
- Average CPU > 80% across cluster
- Slow database queries (>50ms average)
- Chunk load time > 100ms

---

## Cost Analysis

### Infrastructure Costs (Monthly)

#### Small Scale (1,000 players)
```
2x Proxy (4 vCPU, 8GB):    $60
4x Game Server (4 vCPU, 16GB): $240
3x Redis (2 vCPU, 4GB):    $45
1x PostgreSQL (4 vCPU, 16GB): $80
1x Monitoring (8 vCPU, 16GB): $80
1x Load Balancer:           $20
---------------------------------
Total:                      $525/month
Per player:                 $0.53/month
```

#### Medium Scale (5,000 players)
```
3x Proxy:                   $90
15x Game Server:            $900
5x Redis (cluster):         $100
2x PostgreSQL (primary + replica): $180
1x Monitoring:              $80
2x Load Balancer (HA):      $40
---------------------------------
Total:                      $1,390/month
Per player:                 $0.28/month
```

#### Large Scale (20,000 players)
```
5x Proxy:                   $150
60x Game Server:            $3,600
7x Redis (large cluster):   $210
4x PostgreSQL (1 primary + 3 replicas): $360
2x Monitoring (HA):         $160
3x Load Balancer (geo):     $60
---------------------------------
Total:                      $4,540/month
Per player:                 $0.23/month
```

**Cost Optimization Strategies**:
1. **Spot Instances**: Use for game servers (save 60-70%)
2. **Reserved Instances**: For stable infrastructure (save 30-40%)
3. **Auto-scaling**: Scale down during off-peak (save 20-30%)
4. **Regional Pricing**: Host in cheaper regions when possible

**With Optimization** (20k players):
- Spot instances for game servers: -$2,160
- Reserved instances for stable: -$200
- **Optimized Total**: ~$2,180/month (~$0.11/player)

---

## Testing & Benchmarking

### Load Testing Plan

#### Test 1: Baseline (100 players)
- Goal: Verify single server performance
- Duration: 30 minutes
- Metrics: TPS, CPU, RAM, latency

#### Test 2: Scale Test (1,000 players)
- Goal: Test proxy routing and multi-server
- Duration: 1 hour
- Scenarios: Login storm, cross-server transfer

#### Test 3: Stress Test (5,000 players)
- Goal: Test auto-scaling logic
- Duration: 2 hours
- Scenarios: Gradual ramp-up, sudden spike

#### Test 4: Endurance Test (10,000 players)
- Goal: Test system stability under sustained load
- Duration: 24 hours
- Monitor: Memory leaks, performance degradation

#### Test 5: Peak Load (20,000 players)
- Goal: Prove we can handle target capacity
- Duration: 4 hours
- Scenarios: All game modes simultaneously

### Bot Framework for Testing

```python
# tests/load-tests/player_bot.py

import asyncio
from mcstatus import JavaServer

class PlayerBot:
    """Simulates a Minecraft player for load testing"""
    
    async def connect(self, server_address):
        # Connect to server
        await self.perform_handshake()
        await self.login()
        
    async def simulate_player_behavior(self):
        # Random walk around
        # Send chat messages
        # Break/place blocks
        # Simulate realistic player activity
        pass

# Spawn 1000 bots
async def load_test():
    bots = [PlayerBot() for _ in range(1000)]
    await asyncio.gather(*[bot.connect("mc.galion.studio") for bot in bots])
```

---

## Next Steps

1. ✅ Document scaling strategy (this file)
2. ⏳ Implement basic auto-scaling
3. ⏳ Create load testing framework
4. ⏳ Test with 100 → 1,000 → 5,000 players
5. ⏳ Optimize based on results
6. ⏳ Scale to 20,000 players

---

**Document Status**: Complete  
**Last Updated**: 2025-11-09  
**Next Review**: After first load test

