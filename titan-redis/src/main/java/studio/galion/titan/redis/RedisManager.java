package studio.galion.titan.redis;

import lombok.extern.slf4j.Slf4j;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;
import studio.galion.titan.common.config.TitanConfig;

import java.util.Set;
import java.util.function.Function;

/**
 * Redis Manager
 * Manages Redis connections and provides helper methods
 * 
 * This is the central point for all Redis operations in Titan.
 * Uses connection pooling for optimal performance.
 */
@Slf4j
public class RedisManager {
    
    private final JedisPool jedisPool;
    
    /**
     * Initialize Redis manager with configuration
     * 
     * @param config Titan configuration
     */
    public RedisManager(TitanConfig config) {
        TitanConfig.RedisConfig redisConfig = config.getRedis();
        
        // Configure connection pool
        JedisPoolConfig poolConfig = new JedisPoolConfig();
        poolConfig.setMaxTotal(128);          // Max connections
        poolConfig.setMaxIdle(64);            // Max idle connections
        poolConfig.setMinIdle(16);            // Min idle connections
        poolConfig.setTestOnBorrow(true);     // Test connection before use
        poolConfig.setTestOnReturn(true);     // Test when returning to pool
        poolConfig.setTestWhileIdle(true);    // Test idle connections
        poolConfig.setBlockWhenExhausted(true);  // Block when no connections available
        
        // Create Jedis pool
        if (redisConfig.getPassword() != null && !redisConfig.getPassword().isEmpty()) {
            this.jedisPool = new JedisPool(
                poolConfig,
                redisConfig.getHost(),
                redisConfig.getPort(),
                3000,  // Timeout: 3 seconds
                redisConfig.getPassword(),
                redisConfig.getDatabase()
            );
        } else {
            this.jedisPool = new JedisPool(
                poolConfig,
                redisConfig.getHost(),
                redisConfig.getPort(),
                3000,
                null,
                redisConfig.getDatabase()
            );
        }
        
        log.info("Redis connection pool initialized: {}:{}", 
            redisConfig.getHost(), redisConfig.getPort());
    }
    
    /**
     * Execute a Redis operation with automatic resource management
     * 
     * @param function Function to execute with Jedis connection
     * @param <T> Return type
     * @return Result of the operation
     */
    public <T> T execute(Function<Jedis, T> function) {
        try (Jedis jedis = jedisPool.getResource()) {
            return function.apply(jedis);
        } catch (Exception e) {
            log.error("Redis operation failed", e);
            throw new RuntimeException("Redis operation failed", e);
        }
    }
    
    /**
     * Execute a Redis operation without return value
     * 
     * @param consumer Consumer to execute with Jedis connection
     */
    public void executeVoid(java.util.function.Consumer<Jedis> consumer) {
        try (Jedis jedis = jedisPool.getResource()) {
            consumer.accept(jedis);
        } catch (Exception e) {
            log.error("Redis operation failed", e);
            throw new RuntimeException("Redis operation failed", e);
        }
    }
    
    // ========================================
    // Common Operations (Convenience Methods)
    // ========================================
    
    /**
     * Set a key-value pair with expiration
     * 
     * @param key Key
     * @param value Value
     * @param ttlSeconds Time to live in seconds
     */
    public void setWithExpiry(String key, String value, int ttlSeconds) {
        executeVoid(jedis -> jedis.setex(key, ttlSeconds, value));
    }
    
    /**
     * Get value for key
     * 
     * @param key Key
     * @return Value, or null if not found
     */
    public String get(String key) {
        return execute(jedis -> jedis.get(key));
    }
    
    /**
     * Delete key(s)
     * 
     * @param keys Keys to delete
     * @return Number of keys deleted
     */
    public long delete(String... keys) {
        return execute(jedis -> jedis.del(keys));
    }
    
    /**
     * Check if key exists
     * 
     * @param key Key
     * @return true if key exists
     */
    public boolean exists(String key) {
        return execute(jedis -> jedis.exists(key));
    }
    
    /**
     * Set expiration on key
     * 
     * @param key Key
     * @param seconds Seconds until expiration
     * @return true if expiration was set
     */
    public boolean expire(String key, int seconds) {
        return execute(jedis -> jedis.expire(key, seconds) == 1);
    }
    
    /**
     * Add member to set
     * 
     * @param key Set key
     * @param members Members to add
     * @return Number of members added
     */
    public long sAdd(String key, String... members) {
        return execute(jedis -> jedis.sadd(key, members));
    }
    
    /**
     * Remove member from set
     * 
     * @param key Set key
     * @param members Members to remove
     * @return Number of members removed
     */
    public long sRemove(String key, String... members) {
        return execute(jedis -> jedis.srem(key, members));
    }
    
    /**
     * Get all members of set
     * 
     * @param key Set key
     * @return Set of members
     */
    public Set<String> sMembers(String key) {
        return execute(jedis -> jedis.smembers(key));
    }
    
    /**
     * Check if member is in set
     * 
     * @param key Set key
     * @param member Member to check
     * @return true if member exists in set
     */
    public boolean sIsMember(String key, String member) {
        return execute(jedis -> jedis.sismember(key, member));
    }
    
    /**
     * Publish message to channel
     * 
     * @param channel Channel name
     * @param message Message to publish
     * @return Number of subscribers that received the message
     */
    public long publish(String channel, String message) {
        return execute(jedis -> jedis.publish(channel, message));
    }
    
    /**
     * Get Redis pool statistics
     * 
     * @return Pool statistics string
     */
    public String getPoolStats() {
        return String.format(
            "Active: %d, Idle: %d, Waiting: %d",
            jedisPool.getNumActive(),
            jedisPool.getNumIdle(),
            jedisPool.getNumWaiters()
        );
    }
    
    /**
     * Ping Redis to check connection
     * 
     * @return true if connection is alive
     */
    public boolean ping() {
        try {
            return execute(jedis -> "PONG".equals(jedis.ping()));
        } catch (Exception e) {
            log.error("Redis ping failed", e);
            return false;
        }
    }
    
    /**
     * Close Redis connection pool
     * Should be called on shutdown
     */
    public void shutdown() {
        if (jedisPool != null && !jedisPool.isClosed()) {
            log.info("Closing Redis connection pool");
            jedisPool.close();
        }
    }
}

