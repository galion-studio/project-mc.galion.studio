package studio.galion.titan.core.listener;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.player.AsyncPlayerChatEvent;
import studio.galion.titan.core.TitanPlugin;

import java.util.UUID;

/**
 * Chat Listener
 * Handles chat messages
 * - Logs to database for moderation
 * - Broadcasts across servers via Redis (future)
 * - Filters profanity (future)
 */
@Slf4j
@RequiredArgsConstructor
public class ChatListener implements Listener {
    
    private final TitanPlugin plugin;
    
    /**
     * Handle player chat
     */
    @EventHandler(priority = EventPriority.MONITOR, ignoreCancelled = true)
    public void onPlayerChat(AsyncPlayerChatEvent event) {
        Player player = event.getPlayer();
        UUID uuid = player.getUniqueId();
        String message = event.getMessage();
        
        // Log chat to database (async, already on async thread)
        logChatMessage(uuid, player.getName(), message);
        
        // TODO: Broadcast to other servers via Redis pub/sub
        // TODO: Profanity filter
        // TODO: Anti-spam
    }
    
    /**
     * Log chat message to database
     * 
     * @param uuid Player UUID
     * @param username Player username
     * @param message Chat message
     */
    private void logChatMessage(UUID uuid, String username, String message) {
        try {
            String sql = """
                INSERT INTO chat_log (uuid, username, message, chat_type, server_name)
                VALUES (?, ?, ?, 'global', ?)
                """;
            
            plugin.getDatabaseManager().executeUpdate(sql,
                uuid,
                username,
                message,
                plugin.getConfig().getServerName()
            );
        } catch (Exception e) {
            log.error("Failed to log chat message", e);
        }
    }
}

