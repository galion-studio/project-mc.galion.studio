package studio.galion.titan.examples;

import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.entity.Player;

/**
 * Example Event Listener
 * 
 * Shows how to listen to Minecraft events
 */
public class ExampleListener implements Listener {
    
    /**
     * Handle player join event
     * Send a welcome message
     */
    @EventHandler
    public void onPlayerJoin(PlayerJoinEvent event) {
        Player player = event.getPlayer();
        
        // Send welcome message
        player.sendMessage("§6§l[TITAN]§r §7Welcome to the server!");
        player.sendMessage("§7Running on Titan Platform - Built for 20k players!");
        
        // Log to console
        System.out.println("[ExamplePlugin] " + player.getName() + " joined the server");
    }
}

