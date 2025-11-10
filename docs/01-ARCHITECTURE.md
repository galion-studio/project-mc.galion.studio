# 🏗️ SYSTEM ARCHITECTURE

**Version**: 1.0  
**Last Updated**: 2025-11-09

---

## 🧠 FIRST PRINCIPLES ANALYSIS

### The Core Challenge

**Problem**: Support 20,000 concurrent players with plugins AND mods

**Fundamental Constraints**:
1. **Single Server Limit**: A Minecraft server instance maxes out at ~100-200 players
   - CPU bound: Tick processing (20 TPS target)
   - Network bound: Packet sending/receiving
   - Memory bound: Entity tracking, chunk loading
   
2. **Plugin vs Mod Conflict**: 
   - Plugins use Bukkit/Spigot/Paper API
   - Mods use Forge API
   - These are typically incompatible

3. **State Synchronization**:
   - Players need shared data across servers
   - Economy, inventory, permissions must sync
   - Chat, friends list, cross-server features

### The Solution Path

```
20,000 players ÷ 100 players/server = 200 server instances minimum
```

**Required Components**:
1. **Proxy Layer**: Route players to appropriate server
2. **Hybrid Server**: Support both plugins and mods
3. **Shared State**: Cross-server data synchronization
4. **Load Balancer**: Distribute players efficiently
5. **Auto-Scaler**: Spin up/down servers based on load
6. **Monitoring**: Real-time metrics and alerting

---

## 🌐 HIGH-LEVEL ARCHITECTURE

```
                        ┌─────────────────────┐
                        │   EXTERNAL WORLD    │
                        │  (20,000 Players)   │
                        └──────────┬──────────┘
                                   │
                                   │ TCP 25565
                                   │
                        ┌──────────▼──────────┐
                        │   LOAD BALANCER     │
                        │  (HAProxy/Nginx)    │
                        └──────────┬──────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
         ┌──────────▼─────┐  ┌────▼─────┐  ┌────▼─────┐
         │  Velocity #1   │  │Velocity#2│  │Velocity#3│
         │  (Proxy)       │  │ (Proxy)  │  │ (Proxy)  │
         └──────┬─────────┘  └────┬─────┘  └────┬─────┘
                │                 │             │
                └─────────────────┼─────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
    ┌───▼────┐              ┌─────▼─────┐           ┌─────▼─────┐
    │Server 1│              │  Server N │           │ Server 200│
    │ (Lobby)│              │ (Survival)│           │  (PvP)    │
    │        │              │           │           │           │
    │Hybrid  │              │  Hybrid   │           │  Hybrid   │
    │Core    │              │  Core     │           │  Core     │
    └───┬────┘              └─────┬─────┘           └─────┬─────┘
        │                         │                       │
        └─────────────────────────┼───────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
            ┌───────▼────────┐         ┌────────▼────────┐
            │ REDIS CLUSTER  │         │  POSTGRESQL     │
            │                │         │   CLUSTER       │
            │ - Sessions     │         │                 │
            │ - Cache        │         │ - Players       │
            │ - Pub/Sub      │         │ - Economy       │
            │ - Hot Data     │         │ - Inventory     │
            └────────────────┘         │ - Permissions   │
                                       │ - World Data    │
                                       └─────────────────┘
```

---

## 🔧 COMPONENT BREAKDOWN

### 1. Load Balancer Layer

**Technology**: HAProxy or Nginx Stream

**Purpose**: 
- Distribute incoming connections across proxy servers
- Health checking
- DDoS protection

**Configuration**:
```
Players → Load Balancer (TCP 25565) → Velocity Proxy 1/2/3
```

**Scale**: 2-3 instances for redundancy

---

### 2. Velocity Proxy Layer

**Technology**: Velocity (modern, high-performance proxy)

**Purpose**:
- Accept player connections
- Route to appropriate backend server
- Handle cross-server messaging
- Manage player state transitions

**Why Velocity over BungeeCord?**
- Modern codebase (written from scratch)
- Better performance (async, modern Java)
- Security features built-in
- Active development
- Clean plugin API

**Scale**: 3-10 instances (each handles ~2,000-5,000 players)

**Plugins Needed**:
- Custom routing plugin (route to least-loaded server)
- Cross-server chat
- Friend system
- Economy sync

---

### 3. Hybrid Server Core

**Technology**: Custom Hybrid (Based on Mohist or Arclight)

**Options Analysis**:

| Solution | Pros | Cons | Decision |
|----------|------|------|----------|
| **Mohist** | Supports Forge + Paper, maintained | Stability issues, version lag | ✅ Start here |
| **Arclight** | Supports Forge + Bukkit, newer | Less mature, smaller community | 🔄 Fallback |
| **Custom Fork** | Full control, optimized | Massive development effort | 🎯 Future goal |

**Initial Decision**: Start with Mohist, monitor stability, prepare to fork if needed

**Core Features**:
- Forge mod support (client-side and server-side mods)
- Paper plugin support (Bukkit/Spigot API)
- Custom optimizations for high player count
- Cross-server communication hooks

**Scale**: 100-200+ instances (auto-scaled)

---

### 4. Redis Cluster

**Technology**: Redis Cluster (sharded, replicated)

**Purpose**: Ultra-fast data access for hot data

**Data Stored**:
- Player sessions (who's online, where they are)
- Cache (frequently accessed data)
- Pub/Sub channels (cross-server events)
- Leaderboards (sorted sets)
- Temporary data (TTL-based)

**Why Redis?**
- Sub-millisecond latency
- Atomic operations
- Pub/Sub for real-time events
- Built-in data structures (sets, sorted sets, hashes)

**Scale**: 6-12 nodes (3-6 shards, 2x replication)

**Access Pattern**:
```
Server Instance → Redis → Get/Set player state (< 1ms)
```

---

### 5. PostgreSQL Cluster

**Technology**: PostgreSQL with TimescaleDB extension

**Purpose**: Persistent, reliable data storage

**Data Stored**:
- Player profiles
- Economy (money, transactions)
- Inventory (persistent items)
- Permissions (roles, permissions)
- World data
- Statistics (TimescaleDB for time-series)
- Audit logs

**Why PostgreSQL?**
- ACID compliance (data integrity)
- Rich query capabilities (JOIN, complex queries)
- JSON support (flexible schemas)
- Proven at scale
- Excellent backup/recovery tools

**Scale**: Primary + 2-3 read replicas

**Access Pattern**:
```
Server Instance → PostgreSQL → Load/Save on join/quit
Server Instance → Redis (cache) → PostgreSQL (on miss)
```

---

### 6. Message Queue (Optional, Future)

**Technology**: RabbitMQ or Kafka

**Purpose**: Asynchronous event processing

**Use Cases**:
- Async database writes (queue → worker → DB)
- Event processing (player actions → analytics)
- Cross-server commands
- Webhook integrations

**Status**: Phase 2 addition if needed

---

## 🔄 DATA FLOW EXAMPLES

### Player Login Flow

```
1. Player connects → Load Balancer
2. Load Balancer → Velocity Proxy (least loaded)
3. Velocity authenticates player (Mojang API)
4. Velocity checks Redis for player data
5. If not in Redis, load from PostgreSQL
6. Velocity selects target server (lobby)
7. Velocity sends player to Server 1 (lobby)
8. Server 1 loads player data from Redis
9. Player spawns in lobby
```

### Cross-Server Teleport

```
1. Player on Server 5 uses /server survival
2. Server 5 → Redis: Update player location state
3. Server 5 → Velocity: Request transfer
4. Velocity → Server 12 (survival): Prepare player arrival
5. Server 12 → Redis: Get player data
6. Velocity transfers connection
7. Server 12 spawns player
8. Server 5 cleans up player resources
```

### Economy Transaction

```
1. Player A (/pay PlayerB 100) on Server 3
2. Server 3 → Redis: DECRBY playerA:money 100
3. Server 3 → Redis: INCRBY playerB:money 100
4. Server 3 → Redis: Publish event to playerB's server
5. Player B's server (Server 7) receives event → Update display
6. Server 3 → PostgreSQL (async): Log transaction
```

---

## 🐳 CONTAINERIZATION & ORCHESTRATION

### Docker Strategy

**Each Component = Container**:
- `galion/velocity-proxy:latest`
- `galion/hybrid-server:latest`
- `redis:7-alpine`
- `postgres:16-alpine`
- `haproxy:latest`

**Benefits**:
- Consistent environments
- Easy scaling
- Version control
- Rollback capability

### Kubernetes Deployment

**Cluster Structure**:
```
├── Namespace: galion-proxy (Velocity proxies)
├── Namespace: galion-servers (Minecraft servers)
├── Namespace: galion-data (Redis, PostgreSQL)
└── Namespace: galion-monitoring (Prometheus, Grafana)
```

**Auto-Scaling**:
- Horizontal Pod Autoscaler (HPA) for server instances
- Scale based on player count metric
- Min: 10 servers, Max: 200 servers

**Resource Allocation** (per server pod):
```yaml
resources:
  requests:
    memory: "4Gi"
    cpu: "2"
  limits:
    memory: "8Gi"
    cpu: "4"
```

---

## 🔥 PERFORMANCE OPTIMIZATIONS

### Network Level
- Use TCP BBR congestion control
- Enable TCP Fast Open
- Optimize kernel network buffers
- Use dedicated network for inter-server communication

### JVM Level (per server)
```bash
java -Xms4G -Xmx4G \
  -XX:+UseG1GC \
  -XX:G1HeapRegionSize=4M \
  -XX:+UnlockExperimentalVMOptions \
  -XX:+ParallelRefProcEnabled \
  -XX:+AlwaysPreTouch \
  -XX:MaxInlineLevel=15 \
  -jar server.jar
```

### Minecraft Server Level
- View distance: 6-8 chunks (not 10+)
- Entity activation range: Reduced
- Tick rate optimizations
- Async chunk loading
- Mob spawn limits tuned

### Database Level
- Connection pooling (HikariCP)
- Query optimization (indexes, explain analyze)
- Read replicas for read-heavy queries
- Prepared statements (prevent SQL injection + faster)

### Redis Level
- Pipelining for bulk operations
- Key expiration for temporary data
- Lua scripts for atomic multi-operations

---

## 📊 MONITORING & OBSERVABILITY

### Metrics to Track

**Server Level**:
- TPS (ticks per second) - target: 20
- MSPT (milliseconds per tick) - target: < 50ms
- Player count
- CPU/Memory usage
- Chunk count loaded

**Network Level**:
- Packets per second
- Bandwidth usage
- Connection count
- Latency (player ping)

**Database Level**:
- Query time (p50, p95, p99)
- Connection pool usage
- Cache hit rate

**System Level**:
- Disk I/O
- Network I/O
- CPU usage
- Memory usage

### Monitoring Stack

**Prometheus**: Metrics collection
**Grafana**: Visualization dashboards
**Alertmanager**: Alert routing
**Loki**: Log aggregation
**Jaeger**: Distributed tracing (future)

---

## 🔒 SECURITY CONSIDERATIONS

1. **DDoS Protection**: Cloudflare + rate limiting
2. **Authentication**: Online mode only (Mojang verification)
3. **Database Security**: Encrypted connections, principle of least privilege
4. **Container Security**: Non-root users, minimal base images
5. **Network Segmentation**: Separate networks for data/proxy/servers
6. **Secrets Management**: Kubernetes secrets, encrypted at rest

---

## 🚀 SCALING STRATEGY

### Vertical Scaling (Per Server)
- Start: 4GB RAM, 2 CPU cores
- Max: 8GB RAM, 4 CPU cores
- Beyond: Add more instances, not bigger

### Horizontal Scaling (Add Servers)
- Automatic based on metrics
- Scale out: Player count > 80% capacity per server
- Scale in: Player count < 30% capacity, consolidate

### Geographic Scaling (Future)
- Multi-region deployment
- Players route to nearest data center
- Cross-region data replication

---

## 📈 CAPACITY PLANNING

**Target**: 20,000 concurrent players

**Math**:
```
20,000 players ÷ 100 players/server = 200 servers
Buffer factor: 1.3x = 260 servers provisioned
```

**Infrastructure Needs**:
- 260 server pods (4GB RAM, 2 CPU each) = 1040GB RAM, 520 CPU cores
- 10 proxy pods (2GB RAM, 1 CPU each) = 20GB RAM, 10 CPU cores
- 12 Redis nodes (4GB RAM, 2 CPU each) = 48GB RAM, 24 CPU cores
- 3 PostgreSQL nodes (16GB RAM, 4 CPU each) = 48GB RAM, 12 CPU cores

**Total**: ~1156GB RAM, ~566 CPU cores

**Cost Estimate** (AWS):
- Instance type: m5.2xlarge (8 vCPU, 32GB RAM) = ~$0.40/hour
- Instances needed: ~72 instances
- Monthly cost: 72 × $0.40 × 24 × 30 = ~$20,736/month

**Cost Optimization**:
- Reserved instances: -40% = ~$12,442/month
- Spot instances for non-critical: -60% = ~$8,294/month

---

## 🎯 NEXT STEPS

1. Set up development environment
2. Deploy minimal viable setup (1 proxy + 1 server)
3. Test hybrid server core
4. Implement shared state (Redis + PostgreSQL)
5. Scale to 3 servers + cross-server features
6. Load testing (simulate 500 → 1000 → 5000 players)
7. Optimize based on metrics
8. Production hardening

---

**Built from first principles. Scaled with precision. 🚀**

