package studio.galion.titan.common.config;

import lombok.Getter;
import org.yaml.snakeyaml.Yaml;

import java.io.InputStream;
import java.util.Map;

/**
 * Titan Configuration Manager
 * Loads and manages configuration from YAML files
 * 
 * This class provides centralized configuration management
 * for all Titan components.
 */
@Getter
public class TitanConfig {
    
    // Server configuration
    private final String serverName;
    private final String serverType;
    private final int maxPlayers;
    
    // Network configuration
    private final String bindAddress;
    private final int bindPort;
    
    // Database configuration
    private final DatabaseConfig database;
    
    // Redis configuration
    private final RedisConfig redis;
    
    // Performance configuration
    private final PerformanceConfig performance;
    
    /**
     * Load configuration from YAML file
     * 
     * @param configPath Path to configuration file
     * @return Loaded configuration object
     */
    public static TitanConfig load(String configPath) {
        Yaml yaml = new Yaml();
        
        try (InputStream input = TitanConfig.class.getClassLoader().getResourceAsStream(configPath)) {
            if (input == null) {
                throw new IllegalArgumentException("Configuration file not found: " + configPath);
            }
            
            Map<String, Object> config = yaml.load(input);
            return new TitanConfig(config);
            
        } catch (Exception e) {
            throw new RuntimeException("Failed to load configuration", e);
        }
    }
    
    /**
     * Constructor - Parse configuration from map
     * 
     * @param config Configuration map from YAML
     */
    @SuppressWarnings("unchecked")
    private TitanConfig(Map<String, Object> config) {
        // Parse server section
        Map<String, Object> serverSection = (Map<String, Object>) config.get("server");
        this.serverName = (String) serverSection.get("name");
        this.serverType = (String) serverSection.get("type");
        this.maxPlayers = (int) serverSection.get("max-players");
        
        // Parse network section
        Map<String, Object> networkSection = (Map<String, Object>) config.get("network");
        this.bindAddress = (String) networkSection.get("bind-address");
        this.bindPort = (int) networkSection.get("bind-port");
        
        // Parse database section
        Map<String, Object> dbSection = (Map<String, Object>) config.get("database");
        this.database = new DatabaseConfig(dbSection);
        
        // Parse Redis section
        Map<String, Object> redisSection = (Map<String, Object>) config.get("redis");
        this.redis = new RedisConfig(redisSection);
        
        // Parse performance section
        Map<String, Object> perfSection = (Map<String, Object>) config.get("performance");
        this.performance = new PerformanceConfig(perfSection);
    }
    
    /**
     * Database configuration holder
     */
    @Getter
    public static class DatabaseConfig {
        private final String host;
        private final int port;
        private final String database;
        private final String username;
        private final String password;
        private final int poolSize;
        
        DatabaseConfig(Map<String, Object> config) {
            this.host = (String) config.get("host");
            this.port = (int) config.get("port");
            this.database = (String) config.get("database");
            this.username = (String) config.get("username");
            this.password = (String) config.get("password");
            this.poolSize = config.containsKey("pool-size") 
                ? (int) config.get("pool-size") 
                : 10;
        }
    }
    
    /**
     * Redis configuration holder
     */
    @Getter
    public static class RedisConfig {
        private final String host;
        private final int port;
        private final String password;
        private final int database;
        
        RedisConfig(Map<String, Object> config) {
            this.host = (String) config.get("host");
            this.port = (int) config.get("port");
            this.password = config.containsKey("password") 
                ? (String) config.get("password") 
                : null;
            this.database = config.containsKey("database") 
                ? (int) config.get("database") 
                : 0;
        }
    }
    
    /**
     * Performance configuration holder
     */
    @Getter
    public static class PerformanceConfig {
        private final int viewDistance;
        private final int simulationDistance;
        private final boolean asyncChunks;
        private final int maxTickTime;
        
        PerformanceConfig(Map<String, Object> config) {
            this.viewDistance = (int) config.get("view-distance");
            this.simulationDistance = (int) config.get("simulation-distance");
            this.asyncChunks = (boolean) config.get("async-chunks");
            this.maxTickTime = (int) config.get("max-tick-time");
        }
    }
}

