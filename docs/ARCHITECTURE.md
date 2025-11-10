# 🏗️ TITAN Architecture - Deep Dive

> **Last Updated**: 2025-11-09  
> **Status**: Foundation Phase - Architecture Design

## Table of Contents
1. [First Principles Analysis](#first-principles-analysis)
2. [System Architecture](#system-architecture)
3. [Component Breakdown](#component-breakdown)
4. [Data Flow](#data-flow)
5. [Scaling Strategy](#scaling-strategy)
6. [Technical Decisions](#technical-decisions)

---

## First Principles Analysis

### The Core Problem
**Question**: Why can't Minecraft servers handle 20k players?

**Breaking it down**:
1. **Single-threaded world ticking** - Minecraft's main thread handles all entity updates, block updates, AI
2. **Network bottleneck** - Single server network stack can't handle 20k simultaneous connections
3. **Memory constraints** - Loading chunks for 20k players = massive RAM usage
4. **State synchronization** - Sending updates to all players = O(n²) complexity
5. **Plugin/Mod incompatibility** - Paper (plugins) and Forge (mods) are separate ecosystems

### The Solution from First Principles

**Principle 1**: Distribute the load horizontally
- Multiple game server instances, each handling a subset of players
- Each server: 100-500 players (manageable load)
- Total: 40-200 servers for 20k players

**Principle 2**: Separate concerns
- **Proxy Layer**: Handle connections, routing, authentication
- **Game Layer**: Run game logic, world simulation
- **Data Layer**: Store and sync player data, world state

**Principle 3**: Shared state management
- Redis for real-time data (online players, chat, cross-server sync)
- PostgreSQL for persistent data (player profiles, world data)
- No single point of failure

**Principle 4**: Build compatibility layer
- Create bridge between Paper and Forge APIs
- Translate plugin calls to mod system and vice versa
- Custom server core that understands both

---

## System Architecture

### High-Level Overview

```
                    Internet
                       │
                       ▼
        ┌──────────────────────────┐
        │   Load Balancer (L4)     │
        │   HAProxy / Nginx        │
        │   Port: 25565            │
        └──────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
┌───────────────┐            ┌───────────────┐
│ Titan Proxy 1 │            │ Titan Proxy 2 │
│  (Redundant)  │            │  (Redundant)  │
└───────────────┘            └───────────────┘
        │                             │
        └──────────────┬──────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
┌─────────────────┐          ┌─────────────────┐
│  Hub/Lobby      │          │  Game Servers   │
│  Servers (x5)   │          │  (Auto-scaled)  │
│  - World: Lobby │          │  - Survival     │
│  - Capacity:    │          │  - Creative     │
│    500 players  │          │  - Minigames    │
│    each         │          │  - Custom       │
└─────────────────┘          └─────────────────┘
        │                             │
        └──────────────┬──────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
┌─────────────────┐          ┌─────────────────┐
│  Redis Cluster  │          │   PostgreSQL    │
│  - Pub/Sub      │          │   Cluster       │
│  - Cache        │          │   - Player Data │
│  - Session      │          │   - World Data  │
│  - Real-time    │          │   - Logs        │
└─────────────────┘          └─────────────────┘
                       │
                       ▼
        ┌──────────────────────────┐
        │   Monitoring Stack       │
        │   Prometheus + Grafana   │
        │   ELK Stack              │
        └──────────────────────────┘
```

---

## Component Breakdown

### 1. Load Balancer (HAProxy)

**Purpose**: Distribute incoming connections across proxy instances

**Key Features**:
- Layer 4 (TCP) load balancing
- Health checks on proxy instances
- Automatic failover
- DDoS protection

**Configuration**:
```haproxy
frontend minecraft_frontend
    bind *:25565
    mode tcp
    default_backend titan_proxies

backend titan_proxies
    mode tcp
    balance leastconn
    option tcp-check
    server proxy1 10.0.1.10:25565 check
    server proxy2 10.0.1.11:25565 check
```

### 2. Titan Proxy Layer (Custom)

**Purpose**: Intelligent player routing and server orchestration

**Core Responsibilities**:
1. **Authentication** - Verify player sessions with Mojang
2. **Server Discovery** - Track available game servers and their load
3. **Player Routing** - Send players to appropriate servers
4. **Cross-Server Communication** - Enable chat, messaging between servers
5. **Load Balancing** - Distribute players evenly

**Technology**:
- Based on Velocity (modern, performant proxy)
- Custom plugins for routing logic
- Redis for server registry and player tracking

**Key Algorithms**:

```java
// Server Selection Algorithm
public Server selectServer(Player player, ServerType type) {
    // 1. Get all servers of requested type
    List<Server> candidates = getServersByType(type);
    
    // 2. Filter by capacity
    candidates = candidates.stream()
        .filter(s -> s.getCurrentPlayers() < s.getMaxPlayers())
        .collect(Collectors.toList());
    
    // 3. Prefer server with player's friends
    Server friendServer = findServerWithFriends(player, candidates);
    if (friendServer != null && friendServer.getLoad() < 0.8) {
        return friendServer;
    }
    
    // 4. Choose least loaded server
    return candidates.stream()
        .min(Comparator.comparingDouble(Server::getLoad))
        .orElse(null);
}
```

### 3. Titan Core (Hybrid Server)

**Purpose**: Custom Minecraft server supporting BOTH plugins AND mods

**The Challenge**: Paper and Forge are incompatible
- Paper: Bukkit/Spigot API for plugins
- Forge: Modding framework with different hooks

**Our Solution**: Build a compatibility bridge

```
┌─────────────────────────────────────────┐
│         Titan Server Core               │
├─────────────────────────────────────────┤
│  Plugin API Layer  │  Mod API Layer     │
│  (Bukkit/Spigot)   │  (Forge)           │
├─────────────────────────────────────────┤
│       Compatibility Bridge              │
│  - Event translation                    │
│  - Hook mapping                         │
│  - Conflict resolution                  │
├─────────────────────────────────────────┤
│      Minecraft Server Base              │
│  (Optimized Paper core)                 │
└─────────────────────────────────────────┘
```

**Implementation Strategy**:
1. Start with Paper (best performance, plugin ecosystem)
2. Add Forge mod loader as separate classloader
3. Create bridge layer that:
   - Translates Paper events to Forge events
   - Maps Bukkit API calls to Forge equivalents
   - Handles conflicts (mod vs plugin modifying same thing)

**Example Bridge Code**:
```java
// When a Paper plugin fires an event, also fire Forge equivalent
@EventHandler
public void onPlayerJoin(org.bukkit.event.player.PlayerJoinEvent bukkitEvent) {
    // Fire Forge event for mods
    Player forgePlayer = convertToForgePlayer(bukkitEvent.getPlayer());
    net.minecraftforge.event.entity.player.PlayerEvent.PlayerLoggedInEvent forgeEvent = 
        new PlayerLoggedInEvent(forgePlayer);
    MinecraftForge.EVENT_BUS.post(forgeEvent);
}
```

### 4. Data Layer

#### Redis Cluster (Real-time Data)

**Use Cases**:
- **Player Sessions** - Track which server each player is on
- **Cross-Server Chat** - Pub/Sub for global chat
- **Server Registry** - List of active servers and their status
- **Cache** - Frequently accessed data (player ranks, permissions)
- **Leaderboards** - Real-time player statistics

**Schema Example**:
```redis
# Player session
player:uuid:123 -> {server: "survival-1", world: "world", x: 100, y: 64, z: 200}

# Server registry
server:survival-1 -> {ip: "10.0.2.10", port: 25566, players: 342, max: 500, load: 0.68}

# Online players set
servers:survival-1:players -> [uuid1, uuid2, uuid3, ...]

# Cross-server messaging (Pub/Sub)
channel:global-chat -> messages
channel:staff-chat -> messages
```

#### PostgreSQL (Persistent Data)

**Schema Design**:

```sql
-- Players table
CREATE TABLE players (
    uuid UUID PRIMARY KEY,
    username VARCHAR(16) NOT NULL,
    first_join TIMESTAMP NOT NULL,
    last_join TIMESTAMP NOT NULL,
    playtime_seconds BIGINT DEFAULT 0,
    rank VARCHAR(32) DEFAULT 'player'
);

-- Player inventory (shared across servers)
CREATE TABLE player_inventory (
    uuid UUID REFERENCES players(uuid),
    slot INT NOT NULL,
    item_data JSONB NOT NULL,
    PRIMARY KEY (uuid, slot)
);

-- Player economy
CREATE TABLE player_balance (
    uuid UUID PRIMARY KEY REFERENCES players(uuid),
    balance DECIMAL(15, 2) DEFAULT 0.00
);

-- Server logs
CREATE TABLE server_events (
    id BIGSERIAL PRIMARY KEY,
    server_name VARCHAR(64),
    event_type VARCHAR(32),
    player_uuid UUID,
    timestamp TIMESTAMP DEFAULT NOW(),
    data JSONB
);
```

### 5. Monitoring Stack

**Components**:

1. **Prometheus** - Metrics collection
   - Server TPS (ticks per second)
   - Player count per server
   - Memory/CPU usage
   - Network throughput

2. **Grafana** - Visualization
   - Real-time dashboards
   - Alerts and notifications
   - Historical data analysis

3. **ELK Stack** - Logging
   - Elasticsearch: Log storage
   - Logstash: Log processing
   - Kibana: Log visualization

**Key Metrics**:
```yaml
# Server health
- minecraft_tps (target: 20.0)
- minecraft_players_online
- minecraft_chunks_loaded
- minecraft_entities_count

# Infrastructure
- jvm_memory_used_bytes
- jvm_gc_pause_seconds
- system_cpu_usage
- network_throughput_bytes

# Player experience
- player_join_time_seconds
- player_command_latency_seconds
- player_movement_lag_seconds
```

---

## Data Flow

### Player Join Flow

```
1. Player connects to Load Balancer (25565)
   │
2. Load Balancer routes to Titan Proxy (least connections)
   │
3. Proxy authenticates with Mojang API
   │
4. Proxy checks Redis for player data
   │   ├─ Exists: Load session
   │   └─ New: Create session in Redis
   │
5. Proxy queries PostgreSQL for player profile
   │
6. Proxy selects appropriate game server
   │   ├─ Check server capacity (Redis)
   │   ├─ Check server type (hub/game)
   │   └─ Apply routing algorithm
   │
7. Proxy connects player to selected server
   │
8. Game server loads player data
   │   ├─ Inventory from PostgreSQL
   │   ├─ Permissions from Redis cache
   │   └─ World position from last session
   │
9. Player spawns in world
   │
10. Server publishes "player_join" event to Redis
    │
11. Other servers receive notification (for friends list, etc.)
```

### Cross-Server Teleport Flow

```
1. Player executes /server survival-1
   │
2. Current server (hub-1) publishes intent to Redis
   │   {action: "transfer", player: uuid, from: "hub-1", to: "survival-1"}
   │
3. Target server (survival-1) receives notification
   │   └─ Prepares to receive player
   │
4. Proxy receives transfer request
   │
5. Current server saves player state to PostgreSQL
   │   ├─ Inventory
   │   ├─ Position
   │   └─ Status effects
   │
6. Proxy updates Redis player session
   │   player:uuid:123 -> {server: "survival-1", status: "transferring"}
   │
7. Proxy disconnects player from hub-1
   │
8. Proxy connects player to survival-1
   │
9. Survival-1 loads player data from PostgreSQL
   │
10. Player spawns in survival world
   │
11. Redis session updated: {server: "survival-1", status: "online"}
```

---

## Scaling Strategy

### Vertical Scaling (Per Server)

**Optimize each server to handle maximum players**

1. **JVM Tuning**:
```bash
# Recommended JVM flags for 16GB RAM server
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
  -jar titan-server.jar
```

2. **Server Configuration**:
```yaml
# server.properties optimized
view-distance: 8          # Reduce from default 10
simulation-distance: 6    # Reduce entity simulation
max-tick-time: 60000     # Prevent watchdog crashes
network-compression-threshold: 512  # Compress packets
```

3. **Paper/Spigot Configs**:
```yaml
# paper.yml
async-chunks: true        # Load chunks asynchronously
max-auto-save-chunks-per-tick: 8
optimize-explosions: true
treasure-maps-enabled: false  # Reduce server load
armor-stands-tick: false      # Don't tick armor stands
```

**Result**: Each server handles 400-500 players comfortably

### Horizontal Scaling (Add Servers)

**Auto-scaling based on player count**

```
Player Count  │  Hub Servers  │  Game Servers
──────────────┼───────────────┼──────────────
0 - 500       │  1            │  2
500 - 2,000   │  2            │  5
2,000 - 5,000 │  3            │  12
5,000 - 10,000│  5            │  25
10,000 - 20,000│ 8            │  50
```

**Auto-scaling Logic** (Kubernetes HPA):
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: titan-server-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: titan-game-server
  minReplicas: 5
  maxReplicas: 100
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
        averageValue: "400"
```

### Geographic Scaling

**Multi-region deployment for global player base**

```
Region          │  Primary Location  │  Player Capacity
────────────────┼────────────────────┼─────────────────
North America   │  US-East           │  8,000
Europe          │  EU-West           │  8,000
Asia-Pacific    │  Asia-Southeast    │  4,000
```

- Players auto-routed to nearest region (lowest latency)
- Cross-region data sync via Redis
- Shared PostgreSQL cluster with read replicas

---

## Technical Decisions

### Decision Log

#### 1. Why Paper over Spigot?
**Decision**: Use Paper as base server  
**Reasoning**:
- 30-40% better performance than Spigot
- Active development and modern features
- Better async chunk loading
- More configuration options
- Strong plugin ecosystem

#### 2. Why Redis over alternatives?
**Decision**: Use Redis for real-time data  
**Reasoning**:
- Extremely fast (in-memory)
- Pub/Sub for cross-server messaging
- Built-in cluster mode for scaling
- Wide language support
- Battle-tested in production

#### 3. Why PostgreSQL over MySQL?
**Decision**: Use PostgreSQL for persistent data  
**Reasoning**:
- Better JSON support (JSONB)
- Superior query optimization
- More reliable under high concurrency
- Better compliance with SQL standards
- Advanced indexing options

#### 4. Why Velocity over BungeeCord?
**Decision**: Use Velocity as proxy base  
**Reasoning**:
- Modern codebase (built for 1.7+)
- Better performance
- Native support for modern Minecraft features
- Cleaner API
- Active development

#### 5. Why Kubernetes over Docker Swarm?
**Decision**: Use Kubernetes for orchestration  
**Reasoning**:
- Industry standard
- Better auto-scaling
- More mature ecosystem
- Superior monitoring integration
- Easier multi-cloud deployment

#### 6. Hybrid Server Approach
**Decision**: Build Paper + Forge compatibility layer  
**Reasoning**:
- Existing solutions (Mohist, Magma) are unstable
- We need full control for 20k player optimization
- Can optimize specifically for our architecture
- Learning opportunity and future-proof

**Challenges**:
- Significant development effort
- Need to maintain compatibility with updates
- Complex debugging

**Mitigation**:
- Start with Paper core (stable foundation)
- Add Forge support incrementally
- Extensive testing at each phase
- Clear documentation of limitations

---

## Next Steps

1. ✅ Architecture design (this document)
2. ⏳ Implement basic Titan Proxy
3. ⏳ Set up Redis cluster
4. ⏳ Create Paper server with optimization
5. ⏳ Build monitoring stack
6. ⏳ Implement auto-scaling
7. ⏳ Begin Forge compatibility layer
8. ⏳ Load testing (1k, 5k, 10k, 20k players)

---

**Document Status**: Living document - updated as architecture evolves  
**Next Review**: After Phase 1 implementation

