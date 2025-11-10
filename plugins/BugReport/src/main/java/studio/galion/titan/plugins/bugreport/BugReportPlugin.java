package studio.galion.titan.plugins.bugreport;

import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.bukkit.plugin.java.JavaPlugin;
import org.jetbrains.annotations.NotNull;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * Bug Report Plugin
 * Allows players (especially admin galion.studio) to report bugs quickly
 * 
 * Usage: /bug <description>
 * 
 * Features:
 * - Saves to bugs.txt file
 * - Includes timestamp, player, location
 * - Notifies admin instantly
 * - Simple and fast
 */
public class BugReportPlugin extends JavaPlugin {
    
    private File bugFile;
    
    @Override
    public void onEnable() {
        // Create bugs file
        bugFile = new File(getDataFolder(), "bugs.txt");
        
        if (!getDataFolder().exists()) {
            getDataFolder().mkdirs();
        }
        
        if (!bugFile.exists()) {
            try {
                bugFile.createNewFile();
                getLogger().info("Created bugs.txt file");
            } catch (IOException e) {
                getLogger().severe("Failed to create bugs.txt: " + e.getMessage());
            }
        }
        
        // Register command
        getCommand("bug").setExecutor(this);
        
        getLogger().info("========================================");
        getLogger().info("  🐛 Bug Report Plugin Enabled");
        getLogger().info("  Quick bug reporting for admins");
        getLogger().info("========================================");
    }
    
    @Override
    public boolean onCommand(@NotNull CommandSender sender, @NotNull Command command, 
                             @NotNull String label, @NotNull String[] args) {
        
        if (command.getName().equalsIgnoreCase("bug")) {
            // Check if description provided
            if (args.length == 0) {
                sender.sendMessage(ChatColor.RED + "Usage: /bug <description>");
                sender.sendMessage(ChatColor.GRAY + "Example: /bug Server lag when 50+ players online");
                return true;
            }
            
            // Build bug description
            String description = String.join(" ", args);
            
            // Get player info
            String reporter = sender.getName();
            String location = "Console";
            
            if (sender instanceof Player) {
                Player player = (Player) sender;
                location = String.format("%s at X:%.0f Y:%.0f Z:%.0f",
                    player.getWorld().getName(),
                    player.getLocation().getX(),
                    player.getLocation().getY(),
                    player.getLocation().getZ()
                );
            }
            
            // Create bug report entry
            String timestamp = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date());
            String bugReport = String.format(
                "[%s] Reporter: %s | Location: %s\nDescription: %s\n" +
                "Online Players: %d | TPS: %.2f\n" +
                "----------------------------------------\n",
                timestamp,
                reporter,
                location,
                description,
                Bukkit.getOnlinePlayers().size(),
                getTPS()
            );
            
            // Save to file
            try (FileWriter writer = new FileWriter(bugFile, true)) {
                writer.write(bugReport);
                writer.flush();
                
                // Confirm to reporter
                sender.sendMessage("");
                sender.sendMessage(ChatColor.GOLD + "═══════════════════════════════════");
                sender.sendMessage(ChatColor.GREEN + "✓ Bug Report Submitted!");
                sender.sendMessage(ChatColor.GOLD + "═══════════════════════════════════");
                sender.sendMessage(ChatColor.YELLOW + "Description: " + ChatColor.WHITE + description);
                sender.sendMessage(ChatColor.YELLOW + "Time: " + ChatColor.WHITE + timestamp);
                sender.sendMessage(ChatColor.YELLOW + "Saved to: " + ChatColor.WHITE + "plugins/BugReport/bugs.txt");
                sender.sendMessage(ChatColor.GOLD + "═══════════════════════════════════");
                sender.sendMessage("");
                
                // Notify all admins/ops
                notifyAdmins(reporter, description);
                
                // Log to console
                getLogger().info(String.format("Bug reported by %s: %s", reporter, description));
                
                return true;
                
            } catch (IOException e) {
                sender.sendMessage(ChatColor.RED + "Error saving bug report: " + e.getMessage());
                getLogger().severe("Failed to save bug report: " + e.getMessage());
                return true;
            }
        }
        
        return false;
    }
    
    /**
     * Notify all online admins about new bug report
     */
    private void notifyAdmins(String reporter, String description) {
        String notification = ChatColor.RED + "[BUG ALERT] " + ChatColor.YELLOW + 
            reporter + ChatColor.GRAY + " reported: " + ChatColor.WHITE + description;
        
        // Notify OPs
        Bukkit.getOnlinePlayers().forEach(player -> {
            if (player.isOp() || player.hasPermission("bug.notify")) {
                player.sendMessage("");
                player.sendMessage(ChatColor.RED + "🐛 NEW BUG REPORT 🐛");
                player.sendMessage(notification);
                player.sendMessage("");
            }
        });
        
        // Also broadcast to console
        Bukkit.getConsoleSender().sendMessage(notification);
    }
    
    /**
     * Get server TPS
     */
    private double getTPS() {
        try {
            return Bukkit.getTPS()[0];
        } catch (Exception e) {
            return 20.0;
        }
    }
}

