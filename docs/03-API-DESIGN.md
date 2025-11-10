# 🔌 UNIFIED PLUGIN/MOD API DESIGN

**Version**: 1.0  
**Last Updated**: 2025-11-09

---

## 🎯 GOAL

Create a **unified API** that works for both:
- **Plugins** (Paper/Spigot/Bukkit API)
- **Mods** (Forge API)

**Why?** Developers write code once, works in both environments.

---

## 🧠 FIRST PRINCIPLES APPROACH

### The Problem

**Current State**:
- Plugin: Uses Bukkit/Spigot/Paper API (server-side only)
- Mod: Uses Forge API (client + server)
- **Incompatible**: Different event systems, different lifecycles, different APIs

### The Solution

Create **abstraction layer** that:
1. Translates unified API → Paper API (for plugins)
2. Translates unified API → Forge API (for mods)
3. Provides common interfaces for both

**Architecture**:
```
┌─────────────────────────────────────┐
│   Developer Code (Unified API)      │
└──────────────┬──────────────────────┘
               │
    ┌──────────▼──────────┐
    │  Galion API Layer   │
    │   (Abstraction)     │
    └──────────┬──────────┘
               │
       ┌───────┴───────┐
       │               │
   ┌───▼────┐     ┌────▼────┐
   │ Paper  │     │  Forge  │
   │Adapter │     │ Adapter │
   └───┬────┘     └────┬────┘
       │               │
   ┌───▼────┐     ┌────▼────┐
   │ Paper  │     │  Forge  │
   │  API   │     │   API   │
   └────────┘     └─────────┘
```

---

## 📦 API STRUCTURE

### Package Layout

```
com.galion.api/
├── core/
│   ├── GalionPlugin.java          # Base plugin class
│   ├── Server.java                # Server interface
│   └── Player.java                # Player interface
├── event/
│   ├── Event.java                 # Base event
│   ├── EventHandler.java          # Event handler annotation
│   ├── EventPriority.java         # Priority enum
│   └── events/
│       ├── PlayerJoinEvent.java
│       ├── PlayerQuitEvent.java
│       └── ...
├── command/
│   ├── Command.java               # Command interface
│   ├── CommandExecutor.java       # Executor interface
│   └── CommandSender.java         # Sender interface
├── world/
│   ├── World.java                 # World interface
│   ├── Location.java              # Location class
│   ├── Block.java                 # Block interface
│   └── Chunk.java                 # Chunk interface
├── entity/
│   ├── Entity.java                # Entity interface
│   ├── Player.java                # Player interface
│   └── LivingEntity.java          # Living entity
├── inventory/
│   ├── Inventory.java             # Inventory interface
│   ├── ItemStack.java             # Item stack class
│   └── Material.java              # Material enum
├── config/
│   ├── Configuration.java         # Config interface
│   └── YamlConfiguration.java     # YAML impl
└── database/
    ├── Database.java              # Database wrapper
    └── RedisClient.java           # Redis wrapper
```

---

## 💻 CODE EXAMPLES

### Example 1: Simple Plugin

```java
package com.example.myplugin;

import com.galion.api.core.GalionPlugin;
import com.galion.api.event.EventHandler;
import com.galion.api.event.events.PlayerJoinEvent;

public class MyPlugin extends GalionPlugin {
    
    @Override
    public void onEnable() {
        // Plugin startup logic
        getLogger().info("MyPlugin enabled!");
        
        // Register events
        registerEvents(this);
        
        // Register commands
        registerCommand("hello", new HelloCommand());
    }
    
    @Override
    public void onDisable() {
        // Plugin shutdown logic
        getLogger().info("MyPlugin disabled!");
    }
    
    // Event handler
    @EventHandler
    public void onPlayerJoin(PlayerJoinEvent event) {
        Player player = event.getPlayer();
        player.sendMessage("Welcome to Galion Server, " + player.getName() + "!");
    }
}
```

### Example 2: Custom Command

```java
package com.example.myplugin;

import com.galion.api.command.Command;
import com.galion.api.command.CommandSender;
import com.galion.api.entity.Player;

public class HelloCommand implements Command {
    
    @Override
    public boolean execute(CommandSender sender, String[] args) {
        if (!(sender instanceof Player)) {
            sender.sendMessage("This command is for players only!");
            return false;
        }
        
        Player player = (Player) sender;
        player.sendMessage("Hello, " + player.getName() + "!");
        
        return true;
    }
    
    @Override
    public String getUsage() {
        return "/hello";
    }
    
    @Override
    public String getDescription() {
        return "Says hello to the player";
    }
}
```

### Example 3: Database Integration

```java
package com.example.myplugin;

import com.galion.api.core.GalionPlugin;
import com.galion.api.database.Database;
import com.galion.api.database.RedisClient;
import com.galion.api.entity.Player;

public class EconomyPlugin extends GalionPlugin {
    
    private Database database;
    private RedisClient redis;
    
    @Override
    public void onEnable() {
        // Get shared database instance
        this.database = getDatabase();
        this.redis = getRedis();
    }
    
    public int getPlayerMoney(Player player) {
        // Try cache first (Redis)
        String cached = redis.get("money:" + player.getUUID());
        if (cached != null) {
            return Integer.parseInt(cached);
        }
        
        // Cache miss, load from database
        int money = database.query(
            "SELECT money FROM players WHERE uuid = ?",
            player.getUUID()
        ).getInt("money");
        
        // Store in cache
        redis.set("money:" + player.getUUID(), String.valueOf(money));
        
        return money;
    }
    
    public void setPlayerMoney(Player player, int amount) {
        // Update both cache and database
        redis.set("money:" + player.getUUID(), String.valueOf(amount));
        
        database.executeAsync(
            "UPDATE players SET money = ? WHERE uuid = ?",
            amount, player.getUUID()
        );
    }
}
```

### Example 4: Cross-Server Messaging

```java
package com.example.myplugin;

import com.galion.api.core.GalionPlugin;
import com.galion.api.messaging.MessageChannel;
import com.galion.api.messaging.MessageListener;

public class ChatPlugin extends GalionPlugin {
    
    private MessageChannel globalChat;
    
    @Override
    public void onEnable() {
        // Subscribe to global chat channel
        globalChat = getMessaging().getChannel("global-chat");
        
        globalChat.subscribe(new MessageListener() {
            @Override
            public void onMessage(String message) {
                // Broadcast to all players on this server
                getServer().broadcast(message);
            }
        });
    }
    
    public void sendGlobalMessage(String message) {
        // Publish to all servers
        globalChat.publish(message);
    }
}
```

---

## 🔧 IMPLEMENTATION DETAILS

### Paper Adapter (Plugin Side)

**File**: `api/adapters/paper/PaperAdapter.java`

```java
package com.galion.api.adapters.paper;

import com.galion.api.core.GalionPlugin;
import org.bukkit.plugin.java.JavaPlugin;

public class PaperAdapter extends JavaPlugin {
    
    private GalionPlugin galionPlugin;
    
    @Override
    public void onEnable() {
        // Load the actual plugin
        try {
            Class<?> pluginClass = Class.forName(getDescription().getMain());
            galionPlugin = (GalionPlugin) pluginClass.getDeclaredConstructor().newInstance();
            
            // Inject dependencies
            galionPlugin.setServer(new PaperServerWrapper(getServer()));
            galionPlugin.setLogger(getLogger());
            galionPlugin.setDatabase(DatabaseManager.getInstance());
            galionPlugin.setRedis(RedisManager.getInstance());
            
            // Call plugin's onEnable
            galionPlugin.onEnable();
            
        } catch (Exception e) {
            getLogger().severe("Failed to load plugin: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    @Override
    public void onDisable() {
        if (galionPlugin != null) {
            galionPlugin.onDisable();
        }
    }
}
```

### Forge Adapter (Mod Side)

**File**: `api/adapters/forge/ForgeAdapter.java`

```java
package com.galion.api.adapters.forge;

import com.galion.api.core.GalionPlugin;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.event.lifecycle.FMLCommonSetupEvent;

@Mod("galion_plugin_loader")
public class ForgeAdapter {
    
    private GalionPlugin galionPlugin;
    
    public ForgeAdapter() {
        // Register setup event
        FMLJavaModLoadingContext.get().getModEventBus()
            .addListener(this::setup);
    }
    
    private void setup(FMLCommonSetupEvent event) {
        // Load the actual plugin
        try {
            // Similar to Paper adapter...
            galionPlugin.onEnable();
            
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

---

## 🎨 EVENT SYSTEM

### Event Registration

Both plugins and mods use same event system:

```java
@EventHandler
public void onEvent(SomeEvent event) {
    // Handle event
}
```

**Behind the scenes**:
- **Paper**: Translates to Bukkit event system
- **Forge**: Translates to Forge event bus

### Event Priority

```java
@EventHandler(priority = EventPriority.HIGH)
public void onPlayerJoin(PlayerJoinEvent event) {
    // Runs before lower priority handlers
}
```

**Priorities** (highest to lowest):
1. `MONITOR` (read-only, for logging)
2. `HIGHEST`
3. `HIGH`
4. `NORMAL` (default)
5. `LOW`
6. `LOWEST`

### Cancellable Events

```java
@EventHandler
public void onPlayerDamage(PlayerDamageEvent event) {
    if (event.getPlayer().isInvulnerable()) {
        event.setCancelled(true); // Prevent damage
    }
}
```

---

## 🗄️ DATA PERSISTENCE

### Configuration Files

```java
// Load config
Configuration config = getConfig();

// Get values
String serverName = config.getString("server-name", "Default");
int maxLevel = config.getInt("max-level", 100);
List<String> allowedWorlds = config.getStringList("allowed-worlds");

// Save config
config.set("last-restart", System.currentTimeMillis());
config.save();
```

**Config format** (YAML):
```yaml
server-name: "Galion Survival"
max-level: 100
allowed-worlds:
  - world
  - world_nether
  - world_the_end
```

### Database Access

**PostgreSQL** (for persistent data):
```java
Database db = getDatabase();

// Query
ResultSet rs = db.query(
    "SELECT * FROM players WHERE uuid = ?",
    player.getUUID()
);

if (rs.next()) {
    String name = rs.getString("name");
    int level = rs.getInt("level");
}

// Update
db.execute(
    "UPDATE players SET level = ? WHERE uuid = ?",
    newLevel, player.getUUID()
);

// Async (recommended)
db.executeAsync(
    "INSERT INTO logs (player, action, timestamp) VALUES (?, ?, ?)",
    player.getName(), "login", System.currentTimeMillis()
);
```

**Redis** (for fast cache):
```java
RedisClient redis = getRedis();

// Set value (with TTL)
redis.set("session:" + player.getUUID(), sessionData, 3600); // 1 hour

// Get value
String data = redis.get("session:" + player.getUUID());

// Delete
redis.del("session:" + player.getUUID());

// Increment (atomic)
long newValue = redis.incr("player:" + player.getUUID() + ":kills");
```

---

## 🌐 CROSS-SERVER FEATURES

### Messaging Between Servers

```java
MessageChannel channel = getMessaging().getChannel("my-channel");

// Send message
channel.publish("Hello from server 1!");

// Receive messages
channel.subscribe(message -> {
    getLogger().info("Received: " + message);
});
```

### Teleport Player to Another Server

```java
Player player = ...;

// Teleport to another server
getProxy().teleport(player, "survival-2");

// Callback when complete
getProxy().teleport(player, "survival-2", success -> {
    if (success) {
        getLogger().info("Player teleported successfully");
    }
});
```

---

## 🛠️ DEVELOPMENT WORKFLOW

### Step 1: Create Plugin Project

```bash
# Use Maven archetype
mvn archetype:generate \
  -DgroupId=com.example \
  -DartifactId=my-plugin \
  -DarchetypeArtifactId=galion-plugin-archetype \
  -DinteractiveMode=false

cd my-plugin
```

### Step 2: Add Dependencies

**pom.xml**:
```xml
<dependencies>
    <!-- Galion API -->
    <dependency>
        <groupId>com.galion</groupId>
        <artifactId>galion-api</artifactId>
        <version>1.0.0</version>
        <scope>provided</scope>
    </dependency>
</dependencies>
```

### Step 3: Write Plugin

```java
// src/main/java/com/example/myplugin/MyPlugin.java
public class MyPlugin extends GalionPlugin {
    @Override
    public void onEnable() {
        getLogger().info("Plugin enabled!");
    }
}
```

### Step 4: Build

```bash
mvn clean package

# Output: target/my-plugin-1.0.0.jar
```

### Step 5: Install

```bash
# Copy to plugins folder
cp target/my-plugin-1.0.0.jar ~/server/plugins/

# Restart server
~/server/restart.sh
```

---

## 📚 API REFERENCE

### Core Classes

| Class | Description |
|-------|-------------|
| `GalionPlugin` | Base class for all plugins |
| `Server` | Server interface (get players, worlds, etc) |
| `Player` | Player interface |
| `World` | World interface |
| `Location` | 3D position (x, y, z, world) |
| `ItemStack` | Item stack (type, amount, metadata) |
| `Configuration` | Config file interface |

### Event Classes

| Event | Description | Cancellable |
|-------|-------------|-------------|
| `PlayerJoinEvent` | Player joins server | No |
| `PlayerQuitEvent` | Player leaves server | No |
| `PlayerChatEvent` | Player sends chat message | Yes |
| `PlayerMoveEvent` | Player moves | Yes |
| `BlockBreakEvent` | Player breaks block | Yes |
| `BlockPlaceEvent` | Player places block | Yes |
| `EntityDamageEvent` | Entity takes damage | Yes |

### Utility Classes

| Class | Description |
|-------|-------------|
| `Scheduler` | Run tasks async or delayed |
| `Permissions` | Check player permissions |
| `Economy` | Economy API (money, transactions) |
| `Messaging` | Cross-server messaging |
| `Database` | SQL database wrapper |
| `RedisClient` | Redis cache wrapper |

---

## 🚀 ADVANCED TOPICS

### Performance Optimization

```java
// BAD: Sync database call on main thread
public void onPlayerJoin(PlayerJoinEvent event) {
    int money = database.query("SELECT money FROM players WHERE uuid = ?", 
        event.getPlayer().getUUID()).getInt("money");
}

// GOOD: Async database call
public void onPlayerJoin(PlayerJoinEvent event) {
    database.queryAsync("SELECT money FROM players WHERE uuid = ?", 
        event.getPlayer().getUUID()).thenAccept(rs -> {
            int money = rs.getInt("money");
            // Update player asynchronously
        });
}
```

### Batch Operations

```java
// BAD: Multiple Redis calls
for (Player player : players) {
    redis.set("online:" + player.getUUID(), "true");
}

// GOOD: Pipeline
redis.pipeline(pipeline -> {
    for (Player player : players) {
        pipeline.set("online:" + player.getUUID(), "true");
    }
});
```

---

## 📖 NEXT STEPS

1. Read example plugins in `plugins/examples/`
2. Check API documentation: `docs/api/javadoc/`
3. Join development Discord for support
4. Review best practices: `docs/BEST-PRACTICES.md`

---

**Build amazing plugins. Scale to 20k players. 🚀**

