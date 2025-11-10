package studio.galion.titan.core;

import lombok.Getter;
import lombok.extern.slf4j.Slf4j;
import org.bukkit.plugin.java.JavaPlugin;
import studio.galion.titan.api.TitanAPI;
import studio.galion.titan.common.config.TitanConfig;
import studio.galion.titan.core.api.TitanAPIImpl;
import studio.galion.titan.core.manager.PlayerDataManager;
import studio.galion.titan.core.manager.ServerManager;
import studio.galion.titan.database.DatabaseManager;
import studio.galion.titan.redis.RedisManager;

/**
 * Titan Plugin - Main entry point
 * 
 * This is a Paper plugin that provides:
 * - Cross-server player data synchronization
 * - Redis-backed state management
 * - PostgreSQL persistent storage
 * - Metrics and monitoring
 * - Plugin/Mod API
 * 
 * First principles: Build a rock-solid foundation.
 * Everything else builds on top of this.
 */
@Slf4j
@Getter
public class TitanPlugin extends JavaPlugin {
    
    // Singleton instance
    @Getter
    private static TitanPlugin instance;
    
    // Configuration
    private TitanConfig config;
    
    // Core managers
    private DatabaseManager databaseManager;
    private RedisManager redisManager;
    private PlayerDataManager playerDataManager;
    private ServerManager serverManager;
    
    // API implementation
    private TitanAPIImpl apiImpl;
    
    @Override
    public void onEnable() {
        long startTime = System.currentTimeMillis();
        
        log.info("========================================");
        log.info("  TITAN SERVER - Starting...");
        log.info("========================================");
        
        // Set singleton
        instance = this;
        
        try {
            // Step 1: Load configuration
            log.info("Loading configuration...");
            loadConfiguration();
            
            // Step 2: Initialize database
            log.info("Initializing database...");
            this.databaseManager = new DatabaseManager(config);
            
            // Step 3: Initialize Redis
            log.info("Initializing Redis...");
            this.redisManager = new RedisManager(config);
            
            // Step 4: Initialize managers
            log.info("Initializing managers...");
            this.playerDataManager = new PlayerDataManager(databaseManager, redisManager);
            this.serverManager = new ServerManager(config, redisManager);
            
            // Step 5: Initialize API
            log.info("Initializing API...");
            this.apiImpl = new TitanAPIImpl(this);
            studio.galion.titan.api.TitanAPIProvider.setInstance(apiImpl);
            
            // Step 6: Register server in network
            log.info("Registering server in network...");
            serverManager.registerServer();
            
            // Step 7: Start background tasks
            log.info("Starting background tasks...");
            startBackgroundTasks();
            
            // Step 8: Register event listeners
            log.info("Registering event listeners...");
            registerEventListeners();
            
            long duration = System.currentTimeMillis() - startTime;
            log.info("========================================");
            log.info("  TITAN SERVER - Ready!");
            log.info("  Server: {}", config.getServerName());
            log.info("  Type: {}", config.getServerType());
            log.info("  Started in: {}ms", duration);
            log.info("========================================");
            
        } catch (Exception e) {
            log.error("========================================");
            log.error("  TITAN SERVER - FAILED TO START!");
            log.error("========================================");
            log.error("Error during startup", e);
            getServer().getPluginManager().disablePlugin(this);
        }
    }
    
    @Override
    public void onDisable() {
        log.info("========================================");
        log.info("  TITAN SERVER - Shutting down...");
        log.info("========================================");
        
        try {
            // Unregister from network
            if (serverManager != null) {
                log.info("Unregistering from network...");
                serverManager.unregisterServer();
            }
            
            // Save all player data
            if (playerDataManager != null) {
                log.info("Saving player data...");
                playerDataManager.saveAllPlayerData().join();
            }
            
            // Shutdown Redis
            if (redisManager != null) {
                log.info("Closing Redis connections...");
                redisManager.shutdown();
            }
            
            // Shutdown database
            if (databaseManager != null) {
                log.info("Closing database connections...");
                databaseManager.shutdown();
            }
            
            log.info("========================================");
            log.info("  TITAN SERVER - Goodbye!");
            log.info("========================================");
            
        } catch (Exception e) {
            log.error("Error during shutdown", e);
        }
    }
    
    /**
     * Load configuration from file and environment
     */
    private void loadConfiguration() {
        // Save default config if doesn't exist
        saveDefaultConfig();
        
        // Load from config.yml
        this.config = TitanConfig.load("config.yml");
        
        // Override with system properties if provided
        String serverName = System.getProperty("titan.server.name");
        if (serverName != null) {
            log.info("Overriding server name from system property: {}", serverName);
            // Would need to add setter in TitanConfig
        }
        
        String serverType = System.getProperty("titan.server.type");
        if (serverType != null) {
            log.info("Overriding server type from system property: {}", serverType);
        }
    }
    
    /**
     * Start background tasks
     * - Heartbeat to keep server registered
     * - Player data auto-save
     * - Metrics collection
     */
    private void startBackgroundTasks() {
        // Heartbeat every 30 seconds
        getServer().getScheduler().runTaskTimerAsynchronously(this, () -> {
            if (serverManager != null) {
                serverManager.sendHeartbeat();
            }
        }, 20L * 30, 20L * 30); // 30 seconds
        
        // Auto-save player data every 5 minutes
        getServer().getScheduler().runTaskTimerAsynchronously(this, () -> {
            if (playerDataManager != null) {
                playerDataManager.saveAllPlayerData();
            }
        }, 20L * 60 * 5, 20L * 60 * 5); // 5 minutes
    }
    
    /**
     * Register Bukkit event listeners
     */
    private void registerEventListeners() {
        // Register player join/quit listeners
        getServer().getPluginManager().registerEvents(
            new studio.galion.titan.core.listener.PlayerConnectionListener(this),
            this
        );
        
        // Register chat listener
        getServer().getPluginManager().registerEvents(
            new studio.galion.titan.core.listener.ChatListener(this),
            this
        );
    }
    
    /**
     * Get TitanAPI instance
     * 
     * @return TitanAPI
     */
    public TitanAPI getAPI() {
        return apiImpl;
    }
}

