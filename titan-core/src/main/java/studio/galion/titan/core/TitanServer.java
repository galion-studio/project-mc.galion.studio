package studio.galion.titan.core;

import lombok.Getter;
import lombok.extern.slf4j.Slf4j;
import studio.galion.titan.common.config.TitanConfig;
import studio.galion.titan.database.DatabaseManager;
import studio.galion.titan.redis.RedisManager;

/**
 * Titan Server - Main server class
 * This is the core of the Titan hybrid server system
 * 
 * DESIGN PHILOSOPHY (Elon Musk principles):
 * 1. Make it work first
 * 2. Make it good
 * 3. Make it fast
 * 
 * We're building a server that can handle 20,000 players.
 * Start simple, iterate rapidly, optimize ruthlessly.
 */
@Slf4j
@Getter
public class TitanServer {
    
    // Configuration
    private final TitanConfig config;
    
    // Data layer managers
    private final DatabaseManager databaseManager;
    private final RedisManager redisManager;
    
    // Server state
    private boolean running;
    private long startTime;
    
    /**
     * Initialize Titan Server
     * 
     * This sets up the core infrastructure:
     * - Load configuration
     * - Connect to database
     * - Connect to Redis
     * - Initialize monitoring
     * 
     * @param configPath Path to configuration file
     */
    public TitanServer(String configPath) {
        log.info("Initializing Titan Server...");
        log.info("First principles: Build it. Ship it. Improve it.");
        
        // Load configuration
        log.info("Loading configuration from: {}", configPath);
        this.config = TitanConfig.load(configPath);
        log.info("Configuration loaded: {}", config.getServerName());
        
        // Initialize database connection
        log.info("Connecting to database...");
        this.databaseManager = new DatabaseManager(config);
        
        // Test database connection
        if (databaseManager.testConnection()) {
            log.info("✓ Database connection established");
            log.info("  Pool stats: {}", databaseManager.getPoolStats());
        } else {
            log.error("✗ Database connection failed!");
            throw new RuntimeException("Cannot start without database");
        }
        
        // Initialize Redis connection
        log.info("Connecting to Redis...");
        this.redisManager = new RedisManager(config);
        
        // Test Redis connection
        if (redisManager.ping()) {
            log.info("✓ Redis connection established");
            log.info("  Pool stats: {}", redisManager.getPoolStats());
        } else {
            log.error("✗ Redis connection failed!");
            throw new RuntimeException("Cannot start without Redis");
        }
        
        // Register server in registry
        registerServer();
        
        log.info("✓ Titan Server initialized successfully");
    }
    
    /**
     * Start the Titan server
     * 
     * This starts all server components and begins accepting players
     */
    public void start() {
        log.info("========================================");
        log.info("  TITAN SERVER STARTING");
        log.info("========================================");
        log.info("Server: {}", config.getServerName());
        log.info("Type: {}", config.getServerType());
        log.info("Max Players: {}", config.getMaxPlayers());
        log.info("========================================");
        
        this.running = true;
        this.startTime = System.currentTimeMillis();
        
        // Start monitoring heartbeat
        startHeartbeat();
        
        log.info("✓ Server is now RUNNING");
        log.info("Ready to accept players!");
    }
    
    /**
     * Stop the Titan server
     * 
     * Graceful shutdown:
     * 1. Stop accepting new players
     * 2. Save all player data
     * 3. Close database connections
     * 4. Close Redis connections
     * 5. Unregister from server registry
     */
    public void stop() {
        log.info("Stopping Titan Server...");
        
        this.running = false;
        
        // Unregister from server registry
        unregisterServer();
        
        // Close database connections
        if (databaseManager != null) {
            databaseManager.shutdown();
            log.info("✓ Database connections closed");
        }
        
        // Close Redis connections
        if (redisManager != null) {
            redisManager.shutdown();
            log.info("✓ Redis connections closed");
        }
        
        log.info("✓ Titan Server stopped gracefully");
    }
    
    /**
     * Register this server in the server registry (Redis)
     * This allows the proxy to discover and route players to this server
     */
    private void registerServer() {
        log.info("Registering server in network registry...");
        
        String serverKey = "server:" + config.getServerName();
        String serverData = String.format(
            "{\"name\":\"%s\",\"type\":\"%s\",\"host\":\"%s\",\"port\":%d,\"maxPlayers\":%d,\"status\":\"starting\"}",
            config.getServerName(),
            config.getServerType(),
            config.getBindAddress(),
            config.getBindPort(),
            config.getMaxPlayers()
        );
        
        redisManager.setWithExpiry(serverKey, serverData, 60); // 60 second TTL
        
        // Add to server list
        redisManager.sAdd("servers:all", config.getServerName());
        redisManager.sAdd("servers:" + config.getServerType(), config.getServerName());
        
        log.info("✓ Server registered in network");
    }
    
    /**
     * Unregister this server from the registry
     */
    private void unregisterServer() {
        log.info("Unregistering server from network registry...");
        
        String serverKey = "server:" + config.getServerName();
        redisManager.delete(serverKey);
        
        redisManager.sRemove("servers:all", config.getServerName());
        redisManager.sRemove("servers:" + config.getServerType(), config.getServerName());
        
        log.info("✓ Server unregistered from network");
    }
    
    /**
     * Start heartbeat thread
     * Updates server status in Redis every 30 seconds
     */
    private void startHeartbeat() {
        Thread heartbeatThread = new Thread(() -> {
            while (running) {
                try {
                    // Update server status
                    String serverKey = "server:" + config.getServerName();
                    String serverData = String.format(
                        "{\"name\":\"%s\",\"type\":\"%s\",\"host\":\"%s\",\"port\":%d,\"maxPlayers\":%d,\"status\":\"online\",\"uptime\":%d}",
                        config.getServerName(),
                        config.getServerType(),
                        config.getBindAddress(),
                        config.getBindPort(),
                        config.getMaxPlayers(),
                        (System.currentTimeMillis() - startTime) / 1000
                    );
                    
                    redisManager.setWithExpiry(serverKey, serverData, 60);
                    
                    // Sleep for 30 seconds
                    Thread.sleep(30000);
                    
                } catch (InterruptedException e) {
                    log.debug("Heartbeat thread interrupted");
                    break;
                } catch (Exception e) {
                    log.error("Heartbeat failed", e);
                }
            }
        }, "Titan-Heartbeat");
        
        heartbeatThread.setDaemon(true);
        heartbeatThread.start();
        
        log.info("✓ Heartbeat started");
    }
    
    /**
     * Get uptime in seconds
     * 
     * @return Server uptime in seconds
     */
    public long getUptimeSeconds() {
        if (!running || startTime == 0) {
            return 0;
        }
        return (System.currentTimeMillis() - startTime) / 1000;
    }
    
    /**
     * Main method for standalone testing
     */
    public static void main(String[] args) {
        log.info("========================================");
        log.info("  TITAN SERVER");
        log.info("  Next-generation Minecraft server");
        log.info("  Target: 20,000 concurrent players");
        log.info("========================================");
        
        // Load config path from system property or use default
        String configPath = System.getProperty("titan.config", "config/server.yml");
        
        // Create and start server
        TitanServer server = new TitanServer(configPath);
        
        // Add shutdown hook for graceful shutdown
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            log.info("Shutdown signal received");
            server.stop();
        }, "Shutdown-Hook"));
        
        // Start server
        server.start();
        
        // Keep main thread alive
        try {
            Thread.currentThread().join();
        } catch (InterruptedException e) {
            log.info("Main thread interrupted");
        }
    }
}

