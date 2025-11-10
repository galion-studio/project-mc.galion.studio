package studio.galion.titan.core.api;

import lombok.RequiredArgsConstructor;
import studio.galion.titan.api.TitanAPI;
import studio.galion.titan.common.player.PlayerData;
import studio.galion.titan.core.TitanPlugin;

import java.util.UUID;
import java.util.concurrent.CompletableFuture;

/**
 * Implementation of TitanAPI
 * Provides plugin/mod developers access to Titan functionality
 */
@RequiredArgsConstructor
public class TitanAPIImpl implements TitanAPI {
    
    private final TitanPlugin plugin;
    
    @Override
    public CompletableFuture<PlayerData> getPlayerData(UUID uuid) {
        return CompletableFuture.supplyAsync(() -> 
            plugin.getPlayerDataManager().getPlayerData(uuid)
        );
    }
    
    @Override
    public CompletableFuture<Void> savePlayerData(PlayerData data) {
        return CompletableFuture.runAsync(() -> 
            plugin.getPlayerDataManager().savePlayerData(data)
        );
    }
    
    @Override
    public CompletableFuture<Boolean> transferPlayer(UUID uuid, String serverName) {
        return CompletableFuture.supplyAsync(() -> {
            // TODO: Implement player transfer via proxy
            // This requires proxy communication
            plugin.getRedisManager().publish(
                "titan:transfer",
                String.format("{\"uuid\":\"%s\",\"target\":\"%s\"}", uuid, serverName)
            );
            return true;
        });
    }
    
    @Override
    public void broadcastMessage(String channel, String message) {
        plugin.getRedisManager().publish("titan:broadcast:" + channel, message);
    }
    
    @Override
    public String getServerName() {
        return plugin.getConfig().getServerName();
    }
    
    @Override
    public String getServerType() {
        return plugin.getConfig().getServerType();
    }
    
    @Override
    public boolean isNetworkMode() {
        return plugin.getRedisManager() != null && 
               plugin.getDatabaseManager() != null;
    }
    
    @Override
    public int getTotalOnlinePlayers() {
        // Sum players from all servers in registry
        return plugin.getServerManager().getTotalOnlinePlayers();
    }
    
    @Override
    public int getOnlinePlayers(String serverName) {
        return plugin.getServerManager().getServerPlayerCount(serverName);
    }
}

