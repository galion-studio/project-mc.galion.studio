package studio.galion.titan.core.listener;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.event.player.PlayerQuitEvent;
import studio.galion.titan.common.player.PlayerData;
import studio.galion.titan.common.player.PlayerLocation;
import studio.galion.titan.core.TitanPlugin;

import java.util.UUID;

/**
 * Player Connection Listener
 * Handles player join/quit events
 * 
 * First principles: Load data on join, save on quit.
 * Simple, reliable, works.
 */
@Slf4j
@RequiredArgsConstructor
public class PlayerConnectionListener implements Listener {
    
    private final TitanPlugin plugin;
    
    /**
     * Handle player join
     * Load player data from database/cache
     */
    @EventHandler(priority = EventPriority.HIGHEST)
    public void onPlayerJoin(PlayerJoinEvent event) {
        Player player = event.getPlayer();
        UUID uuid = player.getUniqueId();
        String username = player.getName();
        
        log.info("Player {} ({}) joining server", username, uuid);
        
        // Load or create player data
        PlayerData data = plugin.getPlayerDataManager().getPlayerData(uuid);
        
        if (data == null) {
            // New player!
            log.info("New player detected: {}", username);
            data = plugin.getPlayerDataManager().createPlayer(uuid, username);
            
            // Custom join message for first-time players
            event.setJoinMessage("§6§l[+] §7Welcome §a" + username + " §7to Titan! §e(First time)");
        } else {
            // Returning player
            data.updateLastJoin();
            
            // Update location
            org.bukkit.Location loc = player.getLocation();
            data.setCurrentWorld(loc.getWorld().getName());
            data.setLocation(new PlayerLocation(
                loc.getWorld().getName(),
                loc.getX(),
                loc.getY(),
                loc.getZ(),
                loc.getYaw(),
                loc.getPitch()
            ));
            
            plugin.getPlayerDataManager().savePlayerData(data);
            
            event.setJoinMessage("§6§l[+] §a" + username + " §7joined the server");
        }
        
        // Log to database
        logPlayerEvent(uuid, username, "join");
    }
    
    /**
     * Handle player quit
     * Save player data
     */
    @EventHandler(priority = EventPriority.MONITOR)
    public void onPlayerQuit(PlayerQuitEvent event) {
        Player player = event.getPlayer();
        UUID uuid = player.getUniqueId();
        String username = player.getName();
        
        log.info("Player {} ({}) leaving server", username, uuid);
        
        // Get player data
        PlayerData data = plugin.getPlayerDataManager().getPlayerData(uuid);
        
        if (data != null) {
            // Update location
            org.bukkit.Location loc = player.getLocation();
            data.setLocation(new PlayerLocation(
                loc.getWorld().getName(),
                loc.getX(),
                loc.getY(),
                loc.getZ(),
                loc.getYaw(),
                loc.getPitch()
            ));
            
            // Calculate session playtime (time since join)
            long sessionTime = (System.currentTimeMillis() - data.getLastJoin()) / 1000;
            data.addPlaytime(sessionTime);
            
            // Save and unload
            plugin.getPlayerDataManager().savePlayerData(data);
            plugin.getPlayerDataManager().unloadPlayer(uuid);
        }
        
        event.setQuitMessage("§6§l[-] §a" + username + " §7left the server");
        
        // Log to database
        logPlayerEvent(uuid, username, "quit");
    }
    
    /**
     * Log player event to database
     * 
     * @param uuid Player UUID
     * @param username Player username
     * @param eventType Event type (join/quit)
     */
    private void logPlayerEvent(UUID uuid, String username, String eventType) {
        String sql = """
            INSERT INTO server_events (server_name, event_type, player_uuid, player_username, severity)
            VALUES (?, ?, ?, ?, 'info')
            """;
        
        plugin.getDatabaseManager().executeUpdate(sql,
            plugin.getConfig().getServerName(),
            "player_" + eventType,
            uuid,
            username
        );
    }
}

