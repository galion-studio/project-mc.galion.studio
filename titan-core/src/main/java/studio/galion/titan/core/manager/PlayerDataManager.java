package studio.galion.titan.core.manager;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import studio.galion.titan.common.player.PlayerData;
import studio.galion.titan.database.DatabaseManager;
import studio.galion.titan.redis.RedisManager;

import java.sql.ResultSet;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Player Data Manager
 * Manages player data with Redis caching and PostgreSQL persistence
 * 
 * First principles: Cache for speed, database for durability.
 * Read from cache, write through to database.
 */
@Slf4j
@RequiredArgsConstructor
public class PlayerDataManager {
    
    private final DatabaseManager database;
    private final RedisManager redis;
    
    // In-memory cache for currently online players
    private final Map<UUID, PlayerData> onlinePlayerCache = new ConcurrentHashMap<>();
    
    private static final int REDIS_CACHE_TTL = 3600; // 1 hour
    
    /**
     * Get player data
     * Priority: Memory -> Redis -> Database
     * 
     * @param uuid Player UUID
     * @return PlayerData or null if not found
     */
    public PlayerData getPlayerData(UUID uuid) {
        // Check memory cache first (fastest)
        PlayerData data = onlinePlayerCache.get(uuid);
        if (data != null) {
            return data;
        }
        
        // Check Redis cache (fast)
        String cacheKey = "player:" + uuid;
        String cached = redis.get(cacheKey);
        if (cached != null) {
            data = PlayerData.fromJson(cached);
            return data;
        }
        
        // Fallback to database (slow but authoritative)
        data = loadFromDatabase(uuid);
        
        // Cache in Redis if found
        if (data != null) {
            redis.setWithExpiry(cacheKey, data.toJson(), REDIS_CACHE_TTL);
        }
        
        return data;
    }
    
    /**
     * Save player data
     * Writes to both cache and database
     * 
     * @param data PlayerData to save
     */
    public void savePlayerData(PlayerData data) {
        if (data == null) {
            return;
        }
        
        // Update memory cache
        onlinePlayerCache.put(data.getUuid(), data);
        
        // Update Redis cache (async)
        CompletableFuture.runAsync(() -> {
            String cacheKey = "player:" + data.getUuid();
            redis.setWithExpiry(cacheKey, data.toJson(), REDIS_CACHE_TTL);
        });
        
        // Update database (async)
        CompletableFuture.runAsync(() -> {
            saveToDatabase(data);
        });
    }
    
    /**
     * Load player data from database
     * 
     * @param uuid Player UUID
     * @return PlayerData or null
     */
    private PlayerData loadFromDatabase(UUID uuid) {
        String sql = "SELECT * FROM players WHERE uuid = ?";
        
        return database.executeQuery(sql, rs -> {
            if (rs.next()) {
                return mapResultSetToPlayerData(rs);
            }
            return null;
        }, uuid);
    }
    
    /**
     * Save player data to database
     * 
     * @param data PlayerData to save
     */
    private void saveToDatabase(PlayerData data) {
        // Upsert player record
        String sql = """
            INSERT INTO players (uuid, username, first_join, last_join, playtime, rank, is_online)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (uuid) DO UPDATE SET
                username = EXCLUDED.username,
                last_join = EXCLUDED.last_join,
                playtime = EXCLUDED.playtime,
                rank = EXCLUDED.rank,
                is_online = EXCLUDED.is_online,
                updated_at = NOW()
            """;
        
        database.executeUpdate(sql,
            data.getUuid(),
            data.getUsername(),
            new java.sql.Timestamp(data.getFirstJoin()),
            new java.sql.Timestamp(data.getLastJoin()),
            data.getPlaytime(),
            data.getRank(),
            true
        );
        
        // Save player data (location, inventory, etc.)
        String dataSql = """
            INSERT INTO player_data (uuid, world, location_x, location_y, location_z,
                location_yaw, location_pitch, statistics, custom_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?::jsonb, ?::jsonb)
            ON CONFLICT (uuid) DO UPDATE SET
                world = EXCLUDED.world,
                location_x = EXCLUDED.location_x,
                location_y = EXCLUDED.location_y,
                location_z = EXCLUDED.location_z,
                location_yaw = EXCLUDED.location_yaw,
                location_pitch = EXCLUDED.location_pitch,
                statistics = EXCLUDED.statistics,
                custom_data = EXCLUDED.custom_data,
                updated_at = NOW()
            """;
        
        if (data.getLocation() != null) {
            database.executeUpdate(dataSql,
                data.getUuid(),
                data.getLocation().getWorld(),
                data.getLocation().getX(),
                data.getLocation().getY(),
                data.getLocation().getZ(),
                data.getLocation().getYaw(),
                data.getLocation().getPitch(),
                new com.google.gson.Gson().toJson(data.getStatistics()),
                new com.google.gson.Gson().toJson(data.getCustomData())
            );
        }
    }
    
    /**
     * Create new player
     * 
     * @param uuid Player UUID
     * @param username Player username
     * @return New PlayerData
     */
    public PlayerData createPlayer(UUID uuid, String username) {
        PlayerData data = PlayerData.create(uuid, username);
        savePlayerData(data);
        return data;
    }
    
    /**
     * Remove player from online cache
     * Called when player disconnects
     * 
     * @param uuid Player UUID
     */
    public void unloadPlayer(UUID uuid) {
        PlayerData data = onlinePlayerCache.remove(uuid);
        if (data != null) {
            // Final save
            savePlayerData(data);
        }
    }
    
    /**
     * Save all online players' data
     * Called periodically and on shutdown
     * 
     * @return CompletableFuture that completes when all saved
     */
    public CompletableFuture<Void> saveAllPlayerData() {
        return CompletableFuture.runAsync(() -> {
            log.info("Saving data for {} online players...", onlinePlayerCache.size());
            
            for (PlayerData data : onlinePlayerCache.values()) {
                try {
                    saveToDatabase(data);
                } catch (Exception e) {
                    log.error("Failed to save player data for {}", data.getUuid(), e);
                }
            }
            
            log.info("Player data saved successfully");
        });
    }
    
    /**
     * Map database ResultSet to PlayerData
     * 
     * @param rs ResultSet from query
     * @return PlayerData
     */
    private PlayerData mapResultSetToPlayerData(ResultSet rs) throws java.sql.SQLException {
        PlayerData data = new PlayerData();
        data.setUuid((UUID) rs.getObject("uuid"));
        data.setUsername(rs.getString("username"));
        data.setFirstJoin(rs.getTimestamp("first_join").getTime());
        data.setLastJoin(rs.getTimestamp("last_join").getTime());
        data.setPlaytime(rs.getLong("playtime"));
        data.setRank(rs.getString("rank"));
        return data;
    }
}

