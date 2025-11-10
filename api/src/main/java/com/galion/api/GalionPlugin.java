package com.galion.api;

import com.galion.api.database.Database;
import com.galion.api.database.RedisClient;
import com.galion.api.messaging.Messaging;
import com.galion.api.config.Configuration;

import java.util.logging.Logger;

/**
 * Base class for all Galion plugins.
 * Provides unified API for both Paper plugins and Forge mods.
 * 
 * Extend this class to create your plugin:
 * <pre>
 * public class MyPlugin extends GalionPlugin {
 *     @Override
 *     public void onEnable() {
 *         getLogger().info("MyPlugin enabled!");
 *     }
 * }
 * </pre>
 * 
 * @author Galion Studio
 * @version 1.0.0
 */
public abstract class GalionPlugin {
    
    // Injected by the adapter (Paper or Forge)
    private Server server;
    private Logger logger;
    private Database database;
    private RedisClient redis;
    private Messaging messaging;
    private Configuration config;
    
    /**
     * Called when the plugin is enabled.
     * Override this method to implement your plugin's startup logic.
     */
    public abstract void onEnable();
    
    /**
     * Called when the plugin is disabled.
     * Override this method to implement your plugin's shutdown logic.
     */
    public void onDisable() {
        // Default implementation (optional override)
    }
    
    /**
     * Get the server instance.
     * 
     * @return the server
     */
    public Server getServer() {
        return server;
    }
    
    /**
     * Get the plugin logger.
     * 
     * @return the logger
     */
    public Logger getLogger() {
        return logger;
    }
    
    /**
     * Get the database instance.
     * Provides access to PostgreSQL database.
     * 
     * @return the database client
     */
    public Database getDatabase() {
        return database;
    }
    
    /**
     * Get the Redis client.
     * Provides access to Redis cache.
     * 
     * @return the Redis client
     */
    public RedisClient getRedis() {
        return redis;
    }
    
    /**
     * Get the messaging system.
     * Provides cross-server communication.
     * 
     * @return the messaging system
     */
    public Messaging getMessaging() {
        return messaging;
    }
    
    /**
     * Get the plugin configuration.
     * 
     * @return the configuration
     */
    public Configuration getConfig() {
        return config;
    }
    
    // Setter methods (called by adapter, not by plugin developers)
    
    public void setServer(Server server) {
        this.server = server;
    }
    
    public void setLogger(Logger logger) {
        this.logger = logger;
    }
    
    public void setDatabase(Database database) {
        this.database = database;
    }
    
    public void setRedis(RedisClient redis) {
        this.redis = redis;
    }
    
    public void setMessaging(Messaging messaging) {
        this.messaging = messaging;
    }
    
    public void setConfig(Configuration config) {
        this.config = config;
    }
}

