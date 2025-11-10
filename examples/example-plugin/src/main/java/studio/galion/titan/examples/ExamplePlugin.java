package studio.galion.titan.examples;

import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.command.Command;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.jetbrains.annotations.NotNull;

/**
 * Example Titan Plugin
 * 
 * This is a template/example plugin showing how to create
 * plugins for the Titan server platform.
 * 
 * SIMPLE. CLEAN. DOCUMENTED.
 */
public class ExamplePlugin extends JavaPlugin {
    
    @Override
    public void onEnable() {
        // Plugin startup logic
        getLogger().info("========================================");
        getLogger().info("  Example Plugin Enabled!");
        getLogger().info("  Building on Titan Platform");
        getLogger().info("========================================");
        
        // Save default config
        saveDefaultConfig();
        
        // Register events
        getServer().getPluginManager().registerEvents(new ExampleListener(), this);
        
        getLogger().info("✓ Example Plugin loaded successfully");
    }
    
    @Override
    public void onDisable() {
        // Plugin shutdown logic
        getLogger().info("Example Plugin disabled");
    }
    
    @Override
    public boolean onCommand(@NotNull CommandSender sender, @NotNull Command command, 
                             @NotNull String label, @NotNull String[] args) {
        
        // Handle /example command
        if (command.getName().equalsIgnoreCase("example")) {
            if (sender instanceof Player) {
                Player player = (Player) sender;
                player.sendMessage("§6[Example] §7Hello from Titan Plugin!");
                player.sendMessage("§7This is an example command.");
                return true;
            } else {
                sender.sendMessage("This command can only be used by players!");
                return true;
            }
        }
        
        return false;
    }
}
