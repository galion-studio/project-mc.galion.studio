package studio.galion.titan.common.server;

import com.google.gson.Gson;
import lombok.Data;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

/**
 * Server Information Model
 * Represents a game server in the Titan network
 * 
 * Real functionality: Server discovery, load balancing, player routing
 */
@Data
public class ServerInfo {
    
    private static final Gson GSON = new Gson();
    
    // Server identity
    private String name;                // Unique server name
    private String type;                // hub, survival, creative, minigame
    private String host;                // IP address or hostname
    private int port;                   // Server port
    
    // Server status
    private ServerStatus status;        // Server status enum
    private long lastHeartbeat;         // Last heartbeat timestamp
    private long startTime;             // When server started
    
    // Player data
    private int currentPlayers;         // Current player count
    private int maxPlayers;             // Maximum players
    private List<UUID> playerList;     // List of online players
    
    // Performance metrics
    private double tps;                 // Ticks per second (20 = ideal)
    private double cpuUsage;            // CPU usage percentage
    private long memoryUsed;            // Memory used (bytes)
    private long memoryMax;             // Max memory (bytes)
    
    // Metadata
    private String minecraftVersion;    // Minecraft version
    private String serverSoftware;      // Paper, Forge, etc
    private boolean acceptingPlayers;   // Can players join?
    
    /**
     * Server status enum
     */
    public enum ServerStatus {
        STARTING,       // Server is starting up
        ONLINE,         // Server is online and accepting players
        FULL,           // Server is full (at max capacity)
        STOPPING,       // Server is shutting down
        OFFLINE,        // Server is offline
        MAINTENANCE     // Server in maintenance mode
    }
    
    /**
     * Create new server info
     * 
     * @param name Server name
     * @param type Server type
     * @param host Server host
     * @param port Server port
     * @return New ServerInfo instance
     */
    public static ServerInfo create(String name, String type, String host, int port) {
        ServerInfo info = new ServerInfo();
        info.name = name;
        info.type = type;
        info.host = host;
        info.port = port;
        info.status = ServerStatus.STARTING;
        info.startTime = System.currentTimeMillis();
        info.lastHeartbeat = System.currentTimeMillis();
        info.currentPlayers = 0;
        info.maxPlayers = 500;
        info.playerList = new ArrayList<>();
        info.acceptingPlayers = true;
        info.tps = 20.0;
        return info;
    }
    
    /**
     * Update heartbeat timestamp
     * Called every 30 seconds to indicate server is alive
     */
    public void updateHeartbeat() {
        this.lastHeartbeat = System.currentTimeMillis();
    }
    
    /**
     * Check if server is alive
     * 
     * @param timeoutMs Timeout in milliseconds
     * @return true if server responded recently
     */
    public boolean isAlive(long timeoutMs) {
        return (System.currentTimeMillis() - lastHeartbeat) < timeoutMs;
    }
    
    /**
     * Calculate server load (0.0 to 1.0)
     * 
     * @return Load percentage (0.0 = empty, 1.0 = full)
     */
    public double getLoad() {
        if (maxPlayers == 0) {
            return 0.0;
        }
        return (double) currentPlayers / (double) maxPlayers;
    }
    
    /**
     * Check if server has capacity for more players
     * 
     * @return true if server can accept more players
     */
    public boolean hasCapacity() {
        return currentPlayers < maxPlayers && acceptingPlayers;
    }
    
    /**
     * Get server uptime in seconds
     * 
     * @return Uptime in seconds
     */
    public long getUptimeSeconds() {
        if (startTime == 0) {
            return 0;
        }
        return (System.currentTimeMillis() - startTime) / 1000;
    }
    
    /**
     * Add player to server
     * 
     * @param playerUuid Player UUID
     * @return true if player was added
     */
    public boolean addPlayer(UUID playerUuid) {
        if (!hasCapacity()) {
            return false;
        }
        
        if (!playerList.contains(playerUuid)) {
            playerList.add(playerUuid);
            currentPlayers = playerList.size();
            
            // Update status if full
            if (currentPlayers >= maxPlayers) {
                status = ServerStatus.FULL;
                acceptingPlayers = false;
            }
            
            return true;
        }
        
        return false;
    }
    
    /**
     * Remove player from server
     * 
     * @param playerUuid Player UUID
     */
    public void removePlayer(UUID playerUuid) {
        if (playerList.remove(playerUuid)) {
            currentPlayers = playerList.size();
            
            // Update status if no longer full
            if (status == ServerStatus.FULL && currentPlayers < maxPlayers) {
                status = ServerStatus.ONLINE;
                acceptingPlayers = true;
            }
        }
    }
    
    /**
     * Serialize to JSON for Redis
     * 
     * @return JSON string
     */
    public String toJson() {
        return GSON.toJson(this);
    }
    
    /**
     * Deserialize from JSON
     * 
     * @param json JSON string
     * @return ServerInfo instance
     */
    public static ServerInfo fromJson(String json) {
        return GSON.fromJson(json, ServerInfo.class);
    }
    
    /**
     * Get human-readable status string
     * 
     * @return Status description
     */
    public String getStatusString() {
        return String.format("%s [%d/%d players] [%.1f TPS] [Load: %.1f%%]",
            status.name(),
            currentPlayers,
            maxPlayers,
            tps,
            getLoad() * 100
        );
    }
}

