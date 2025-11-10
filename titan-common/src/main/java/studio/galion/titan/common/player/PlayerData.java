package studio.galion.titan.common.player;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import lombok.Data;

import java.util.UUID;
import java.util.HashMap;
import java.util.Map;

/**
 * Player Data Model
 * Represents a player's persistent data across servers
 * 
 * This data is shared between all Titan servers via Redis/PostgreSQL
 */
@Data
public class PlayerData {
    
    private static final Gson GSON = new GsonBuilder().setPrettyPrinting().create();
    
    // Identity
    private UUID uuid;
    private String username;
    
    // Session data
    private String currentServer;
    private String currentWorld;
    private PlayerLocation location;
    
    // Timestamps
    private long firstJoin;
    private long lastJoin;
    private long playtime; // in seconds
    
    // Rank and permissions
    private String rank;
    private Map<String, Boolean> permissions;
    
    // Economy
    private double balance;
    
    // Statistics
    private Map<String, Integer> statistics;
    
    // Custom data (for plugins/mods)
    private Map<String, Object> customData;
    
    /**
     * Create new player data with defaults
     * 
     * @param uuid Player UUID
     * @param username Player username
     * @return New PlayerData instance
     */
    public static PlayerData create(UUID uuid, String username) {
        PlayerData data = new PlayerData();
        data.uuid = uuid;
        data.username = username;
        data.firstJoin = System.currentTimeMillis();
        data.lastJoin = System.currentTimeMillis();
        data.playtime = 0;
        data.rank = "player";
        data.balance = 0.0;
        data.permissions = new HashMap<>();
        data.statistics = new HashMap<>();
        data.customData = new HashMap<>();
        return data;
    }
    
    /**
     * Serialize to JSON
     * 
     * @return JSON representation
     */
    public String toJson() {
        return GSON.toJson(this);
    }
    
    /**
     * Deserialize from JSON
     * 
     * @param json JSON string
     * @return PlayerData instance
     */
    public static PlayerData fromJson(String json) {
        return GSON.fromJson(json, PlayerData.class);
    }
    
    /**
     * Update last join timestamp
     */
    public void updateLastJoin() {
        this.lastJoin = System.currentTimeMillis();
    }
    
    /**
     * Add playtime
     * 
     * @param seconds Seconds to add
     */
    public void addPlaytime(long seconds) {
        this.playtime += seconds;
    }
    
    /**
     * Check if player has permission
     * 
     * @param permission Permission node
     * @return true if player has permission
     */
    public boolean hasPermission(String permission) {
        // Check explicit permissions first
        if (permissions.containsKey(permission)) {
            return permissions.get(permission);
        }
        
        // Check wildcard permissions
        String[] parts = permission.split("\\.");
        StringBuilder builder = new StringBuilder();
        
        for (int i = 0; i < parts.length; i++) {
            if (i > 0) builder.append(".");
            builder.append(parts[i]);
            String node = builder.toString() + ".*";
            
            if (permissions.containsKey(node)) {
                return permissions.get(node);
            }
        }
        
        // Check root wildcard
        return permissions.getOrDefault("*", false);
    }
    
    /**
     * Set permission
     * 
     * @param permission Permission node
     * @param value Permission value
     */
    public void setPermission(String permission, boolean value) {
        permissions.put(permission, value);
    }
    
    /**
     * Get statistic value
     * 
     * @param statistic Statistic name
     * @return Statistic value, or 0 if not found
     */
    public int getStatistic(String statistic) {
        return statistics.getOrDefault(statistic, 0);
    }
    
    /**
     * Increment statistic
     * 
     * @param statistic Statistic name
     * @param amount Amount to increment by
     */
    public void incrementStatistic(String statistic, int amount) {
        statistics.put(statistic, getStatistic(statistic) + amount);
    }
    
    /**
     * Get custom data value
     * 
     * @param key Data key
     * @return Data value, or null if not found
     */
    public Object getCustomData(String key) {
        return customData.get(key);
    }
    
    /**
     * Set custom data value
     * 
     * @param key Data key
     * @param value Data value
     */
    public void setCustomData(String key, Object value) {
        customData.put(key, value);
    }
}

