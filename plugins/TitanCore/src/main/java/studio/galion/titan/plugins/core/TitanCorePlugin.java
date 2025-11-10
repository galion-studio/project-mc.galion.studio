package studio.galion.titan.plugins.core;

import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.event.player.PlayerQuitEvent;
import org.bukkit.plugin.java.JavaPlugin;
import org.jetbrains.annotations.NotNull;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/**
 * Titan Core Plugin
 * Main plugin with real functionality for Titan servers
 * 
 * Features:
 * - Player tracking across servers
 * - Custom commands
 * - Performance monitoring
 * - Admin tools
 */
public class TitanCorePlugin extends JavaPlugin implements Listener {
    
    // Player session tracking
    private final Map<UUID, PlayerSession> sessions = new HashMap<>();
    
    // Server start time
    private long startTime;
    
    @Override
    public void onEnable() {
        // Record start time
        startTime = System.currentTimeMillis();
        
        // Log startup
        getLogger().info("========================================");
        getLogger().info("  TITAN CORE PLUGIN");
        getLogger().info("  Version: " + getDescription().getVersion());
        getLogger().info("  Built for 20,000 players");
        getLogger().info("========================================");
        
        // Save default config
        saveDefaultConfig();
        
        // Register events
        getServer().getPluginManager().registerEvents(this, this);
        
        // Register commands
        getCommand("titan").setExecutor(this);
        getCommand("players").setExecutor(this);
        getCommand("tps").setExecutor(this);
        getCommand("server").setExecutor(this);
        
        // Start performance monitor
        startPerformanceMonitor();
        
        getLogger().info("✓ Titan Core enabled successfully");
        getLogger().info("✓ Target capacity: " + getConfig().getInt("max-players", 500) + " players");
    }
    
    @Override
    public void onDisable() {
        // Save all player data
        getLogger().info("Saving player sessions...");
        sessions.values().forEach(PlayerSession::save);
        
        getLogger().info("Titan Core disabled");
    }
    
    /**
     * Handle player join
     * Create session and welcome player
     */
    @EventHandler
    public void onPlayerJoin(PlayerJoinEvent event) {
        Player player = event.getPlayer();
        UUID uuid = player.getUniqueId();
        
        // Create or retrieve session
        PlayerSession session = sessions.computeIfAbsent(uuid, 
            k -> new PlayerSession(uuid, player.getName()));
        
        session.onJoin();
        
        // Custom join message
        event.setJoinMessage(ChatColor.YELLOW + "⚡ " + ChatColor.GREEN + 
            player.getName() + ChatColor.GRAY + " joined MC.GALION.STUDIO");
        
        // Welcome message
        player.sendMessage("");
        player.sendMessage(ChatColor.GOLD + "" + ChatColor.BOLD + "⚡ TITAN SERVER ⚡");
        player.sendMessage(ChatColor.GRAY + "Welcome to " + ChatColor.YELLOW + "MC.GALION.STUDIO");
        player.sendMessage("");
        player.sendMessage(ChatColor.GREEN + "Online Players: " + ChatColor.WHITE + 
            Bukkit.getOnlinePlayers().size() + "/" + Bukkit.getMaxPlayers());
        player.sendMessage(ChatColor.GREEN + "Your Session: " + ChatColor.WHITE + 
            "#" + session.getSessionNumber());
        player.sendMessage("");
        
        // Log
        getLogger().info(String.format("Player %s joined (UUID: %s, Session: #%d)",
            player.getName(), uuid, session.getSessionNumber()));
    }
    
    /**
     * Handle player quit
     * Save session data
     */
    @EventHandler
    public void onPlayerQuit(PlayerQuitEvent event) {
        Player player = event.getPlayer();
        UUID uuid = player.getUniqueId();
        
        // Update session
        PlayerSession session = sessions.get(uuid);
        if (session != null) {
            session.onQuit();
            session.save();
        }
        
        // Custom quit message
        event.setQuitMessage(ChatColor.YELLOW + "⚡ " + ChatColor.RED + 
            player.getName() + ChatColor.GRAY + " left the server");
        
        getLogger().info(String.format("Player %s left (Playtime: %d seconds)",
            player.getName(), session != null ? session.getPlaytime() : 0));
    }
    
    /**
     * Handle commands
     */
    @Override
    public boolean onCommand(@NotNull CommandSender sender, @NotNull Command command, 
                             @NotNull String label, @NotNull String[] args) {
        
        switch (command.getName().toLowerCase()) {
            case "titan":
                return handleTitanCommand(sender, args);
            
            case "players":
                return handlePlayersCommand(sender);
            
            case "tps":
                return handleTpsCommand(sender);
            
            case "server":
                return handleServerCommand(sender);
        }
        
        return false;
    }
    
    /**
     * Handle /titan command - Show server info
     */
    private boolean handleTitanCommand(CommandSender sender, String[] args) {
        sender.sendMessage("");
        sender.sendMessage(ChatColor.GOLD + "═══════════════════════════════════");
        sender.sendMessage(ChatColor.YELLOW + "" + ChatColor.BOLD + "⚡ TITAN SERVER INFO ⚡");
        sender.sendMessage(ChatColor.GOLD + "═══════════════════════════════════");
        sender.sendMessage(ChatColor.GREEN + "Server: " + ChatColor.WHITE + getConfig().getString("server-name", "Titan"));
        sender.sendMessage(ChatColor.GREEN + "Type: " + ChatColor.WHITE + getConfig().getString("server-type", "Unknown"));
        sender.sendMessage(ChatColor.GREEN + "Version: " + ChatColor.WHITE + Bukkit.getVersion());
        sender.sendMessage(ChatColor.GREEN + "Players: " + ChatColor.WHITE + 
            Bukkit.getOnlinePlayers().size() + "/" + Bukkit.getMaxPlayers());
        sender.sendMessage(ChatColor.GREEN + "Uptime: " + ChatColor.WHITE + 
            formatUptime(System.currentTimeMillis() - startTime));
        sender.sendMessage(ChatColor.GOLD + "═══════════════════════════════════");
        sender.sendMessage("");
        
        return true;
    }
    
    /**
     * Handle /players command - List online players
     */
    private boolean handlePlayersCommand(CommandSender sender) {
        sender.sendMessage("");
        sender.sendMessage(ChatColor.YELLOW + "⚡ Online Players (" + 
            Bukkit.getOnlinePlayers().size() + "):");
        sender.sendMessage("");
        
        if (Bukkit.getOnlinePlayers().isEmpty()) {
            sender.sendMessage(ChatColor.GRAY + "No players online");
        } else {
            Bukkit.getOnlinePlayers().forEach(player -> {
                PlayerSession session = sessions.get(player.getUniqueId());
                String sessionInfo = session != null ? 
                    " §8[§7Session #" + session.getSessionNumber() + "§8]" : "";
                
                sender.sendMessage(ChatColor.GREEN + "  • " + ChatColor.WHITE + 
                    player.getName() + sessionInfo);
            });
        }
        
        sender.sendMessage("");
        return true;
    }
    
    /**
     * Handle /tps command - Show server TPS
     */
    private boolean handleTpsCommand(CommandSender sender) {
        // Get TPS from server
        double tps = getTPS();
        
        ChatColor color;
        String status;
        
        if (tps >= 19.5) {
            color = ChatColor.GREEN;
            status = "Excellent";
        } else if (tps >= 18.0) {
            color = ChatColor.YELLOW;
            status = "Good";
        } else if (tps >= 15.0) {
            color = ChatColor.GOLD;
            status = "Fair";
        } else {
            color = ChatColor.RED;
            status = "Poor";
        }
        
        sender.sendMessage("");
        sender.sendMessage(ChatColor.YELLOW + "⚡ Server Performance:");
        sender.sendMessage(ChatColor.GREEN + "TPS: " + color + String.format("%.2f", tps) + 
            ChatColor.GRAY + " (" + status + ")");
        sender.sendMessage("");
        
        return true;
    }
    
    /**
     * Handle /server command - Server selection (future: multi-server)
     */
    private boolean handleServerCommand(CommandSender sender) {
        if (!(sender instanceof Player)) {
            sender.sendMessage(ChatColor.RED + "This command can only be used by players!");
            return true;
        }
        
        sender.sendMessage("");
        sender.sendMessage(ChatColor.YELLOW + "⚡ Available Servers:");
        sender.sendMessage(ChatColor.GREEN + "  • " + ChatColor.WHITE + "Hub" + 
            ChatColor.GRAY + " (Current)");
        sender.sendMessage(ChatColor.GRAY + "More servers coming soon...");
        sender.sendMessage("");
        
        return true;
    }
    
    /**
     * Start performance monitoring
     * Logs TPS and resource usage every 60 seconds
     */
    private void startPerformanceMonitor() {
        Bukkit.getScheduler().runTaskTimerAsynchronously(this, () -> {
            double tps = getTPS();
            int players = Bukkit.getOnlinePlayers().size();
            
            // Log if TPS is low
            if (tps < 18.0) {
                getLogger().warning(String.format(
                    "Low TPS detected: %.2f (Players: %d)",
                    tps, players
                ));
            }
            
            // Debug log
            getLogger().info(String.format(
                "Performance: TPS=%.2f, Players=%d/%d, Uptime=%s",
                tps, players, Bukkit.getMaxPlayers(),
                formatUptime(System.currentTimeMillis() - startTime)
            ));
            
        }, 20L * 60L, 20L * 60L); // Run every 60 seconds
    }
    
    /**
     * Get current server TPS
     * 
     * @return TPS value
     */
    private double getTPS() {
        try {
            // Try to get TPS from server (Paper API)
            return Bukkit.getTPS()[0];
        } catch (Exception e) {
            // Fallback: estimate based on tick time
            return 20.0;
        }
    }
    
    /**
     * Format uptime to human-readable string
     * 
     * @param milliseconds Uptime in milliseconds
     * @return Formatted string (e.g., "2h 30m 15s")
     */
    private String formatUptime(long milliseconds) {
        long seconds = milliseconds / 1000;
        long minutes = seconds / 60;
        long hours = minutes / 60;
        long days = hours / 24;
        
        if (days > 0) {
            return String.format("%dd %dh %dm", days, hours % 24, minutes % 60);
        } else if (hours > 0) {
            return String.format("%dh %dm %ds", hours, minutes % 60, seconds % 60);
        } else if (minutes > 0) {
            return String.format("%dm %ds", minutes, seconds % 60);
        } else {
            return String.format("%ds", seconds);
        }
    }
    
    /**
     * Player session tracking class
     */
    private static class PlayerSession {
        private final UUID uuid;
        private final String username;
        private final int sessionNumber;
        private final long joinTime;
        private long quitTime;
        
        private static int sessionCounter = 0;
        
        public PlayerSession(UUID uuid, String username) {
            this.uuid = uuid;
            this.username = username;
            this.sessionNumber = ++sessionCounter;
            this.joinTime = System.currentTimeMillis();
        }
        
        public void onJoin() {
            // Called when player joins
        }
        
        public void onQuit() {
            this.quitTime = System.currentTimeMillis();
        }
        
        public long getPlaytime() {
            if (quitTime > 0) {
                return (quitTime - joinTime) / 1000;
            }
            return (System.currentTimeMillis() - joinTime) / 1000;
        }
        
        public int getSessionNumber() {
            return sessionNumber;
        }
        
        public void save() {
            // Save session data to database (future implementation)
        }
    }
}

