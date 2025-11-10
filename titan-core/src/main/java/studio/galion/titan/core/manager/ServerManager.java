package studio.galion.titan.core.manager;

import com.google.gson.Gson;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import studio.galion.titan.common.config.TitanConfig;
import studio.galion.titan.redis.RedisManager;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;

/**
 * Server Manager
 * Manages server registration and heartbeat in the network
 * 
 * Each server registers itself in Redis so the proxy knows:
 * - What servers are available
 * - How many players on each
 * - Server health (TPS, CPU, etc.)
 */
@Slf4j
@RequiredArgsConstructor
public class ServerManager {
    
    private final TitanConfig config;
    private final RedisManager redis;
    private final Gson gson = new Gson();
    
    private static final String REGISTRY_KEY = "titan:servers";
    private static final int HEARTBEAT_TTL = 60; // 60 seconds
    
    /**
     * Register this server in the network
     * Called on startup
     */
    public void registerServer() {
        String serverKey = getServerKey();
        
        Map<String, Object> serverInfo = new HashMap<>();
        serverInfo.put("name", config.getServerName());
        serverInfo.put("type", config.getServerType());
        serverInfo.put("max_players", config.getMaxPlayers());
        serverInfo.put("online", true);
        serverInfo.put("startup_time", System.currentTimeMillis());
        
        // Add to server set
        redis.sAdd(REGISTRY_KEY, config.getServerName());
        
        // Store server info
        redis.setWithExpiry(serverKey, gson.toJson(serverInfo), HEARTBEAT_TTL);
        
        log.info("Registered server '{}' in network", config.getServerName());
    }
    
    /**
     * Unregister this server from network
     * Called on shutdown
     */
    public void unregisterServer() {
        String serverKey = getServerKey();
        
        // Remove from set
        redis.sRemove(REGISTRY_KEY, config.getServerName());
        
        // Delete server info
        redis.delete(serverKey);
        
        log.info("Unregistered server '{}' from network", config.getServerName());
    }
    
    /**
     * Send heartbeat
     * Updates server info and renews TTL
     * Called every 30 seconds
     */
    public void sendHeartbeat() {
        String serverKey = getServerKey();
        
        // Get current stats
        org.bukkit.Server bukkit = org.bukkit.Bukkit.getServer();
        
        Map<String, Object> serverInfo = new HashMap<>();
        serverInfo.put("name", config.getServerName());
        serverInfo.put("type", config.getServerType());
        serverInfo.put("max_players", config.getMaxPlayers());
        serverInfo.put("online_players", bukkit.getOnlinePlayers().size());
        serverInfo.put("tps", getAverageTPS());
        serverInfo.put("online", true);
        serverInfo.put("last_heartbeat", System.currentTimeMillis());
        
        // Update with TTL
        redis.setWithExpiry(serverKey, gson.toJson(serverInfo), HEARTBEAT_TTL);
    }
    
    /**
     * Get total players online across all servers
     * 
     * @return Total player count
     */
    public int getTotalOnlinePlayers() {
        Set<String> servers = redis.sMembers(REGISTRY_KEY);
        int total = 0;
        
        for (String serverName : servers) {
            total += getServerPlayerCount(serverName);
        }
        
        return total;
    }
    
    /**
     * Get player count for specific server
     * 
     * @param serverName Server name
     * @return Player count
     */
    public int getServerPlayerCount(String serverName) {
        String serverKey = "titan:server:" + serverName;
        String data = redis.get(serverKey);
        
        if (data == null) {
            return 0;
        }
        
        try {
            @SuppressWarnings("unchecked")
            Map<String, Object> info = gson.fromJson(data, Map.class);
            Object players = info.get("online_players");
            return players != null ? ((Number) players).intValue() : 0;
        } catch (Exception e) {
            log.error("Failed to parse server info for {}", serverName, e);
            return 0;
        }
    }
    
    /**
     * Get Redis key for this server
     * 
     * @return Server key
     */
    private String getServerKey() {
        return "titan:server:" + config.getServerName();
    }
    
    /**
     * Get average TPS (Ticks Per Second)
     * Paper provides this via reflection
     * 
     * @return Average TPS
     */
    private double getAverageTPS() {
        try {
            org.bukkit.Server server = org.bukkit.Bukkit.getServer();
            double[] tps = server.getTPS();
            return (tps[0] + tps[1] + tps[2]) / 3.0;
        } catch (Exception e) {
            return 20.0; // Assume nominal if we can't get it
        }
    }
}

