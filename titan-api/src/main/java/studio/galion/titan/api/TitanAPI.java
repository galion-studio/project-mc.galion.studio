package studio.galion.titan.api;

import studio.galion.titan.common.player.PlayerData;

import java.util.UUID;
import java.util.concurrent.CompletableFuture;

/**
 * Titan API - Main entry point for plugin/mod developers
 * 
 * This API provides access to Titan's cross-server functionality:
 * - Player data management (shared across servers)
 * - Cross-server messaging
 * - Server registry
 * - Metrics and monitoring
 * 
 * Usage:
 * TitanAPI api = TitanAPI.getInstance();
 * PlayerData data = api.getPlayerData(uuid).join();
 */
public interface TitanAPI {
    
    /**
     * Get the singleton instance of TitanAPI
     * 
     * @return TitanAPI instance
     * @throws IllegalStateException if Titan is not initialized
     */
    static TitanAPI getInstance() {
        return TitanAPIProvider.getInstance();
    }
    
    /**
     * Get player data (async)
     * Fetches from cache or database
     * 
     * @param uuid Player UUID
     * @return CompletableFuture with PlayerData
     */
    CompletableFuture<PlayerData> getPlayerData(UUID uuid);
    
    /**
     * Save player data (async)
     * Updates cache and database
     * 
     * @param data PlayerData to save
     * @return CompletableFuture that completes when saved
     */
    CompletableFuture<Void> savePlayerData(PlayerData data);
    
    /**
     * Send player to another server
     * 
     * @param uuid Player UUID
     * @param serverName Target server name
     * @return CompletableFuture<Boolean> - true if transfer initiated
     */
    CompletableFuture<Boolean> transferPlayer(UUID uuid, String serverName);
    
    /**
     * Broadcast message to all servers
     * Uses Redis pub/sub for cross-server communication
     * 
     * @param channel Channel name
     * @param message Message to broadcast
     */
    void broadcastMessage(String channel, String message);
    
    /**
     * Get current server name
     * 
     * @return Server name (e.g., "hub-1", "survival-1")
     */
    String getServerName();
    
    /**
     * Get current server type
     * 
     * @return Server type (e.g., "hub", "survival")
     */
    String getServerType();
    
    /**
     * Check if server is in network mode
     * (connected to proxy and database)
     * 
     * @return true if networked
     */
    boolean isNetworkMode();
    
    /**
     * Get total online players across all servers
     * 
     * @return Total player count
     */
    int getTotalOnlinePlayers();
    
    /**
     * Get online players on specific server
     * 
     * @param serverName Server name
     * @return Player count on that server
     */
    int getOnlinePlayers(String serverName);
}

