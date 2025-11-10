package studio.galion.titan.plugins.ai;

import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.AsyncPlayerChatEvent;
import org.bukkit.plugin.java.JavaPlugin;

/**
 * Titan AI Assistant Plugin
 * Connects Minecraft chat to Claude Sonnet 4.5 AI
 * 
 * Usage:
 * - Type "@ai <question>" in chat to talk to the AI
 * - AI responds as [Console] in chat
 * - Perfect for in-game development assistance!
 * 
 * Features:
 * - Real-time AI responses in Minecraft
 * - Code help and debugging
 * - Server management assistance
 * - Multi-player support
 */
public class TitanAIPlugin extends JavaPlugin implements Listener {
    
    private ClaudeAPI claudeAPI;
    private String commandPrefix = "@ai";  // Trigger for AI chat
    
    @Override
    public void onEnable() {
        // Log startup
        getLogger().info("========================================");
        getLogger().info("  🤖 TITAN AI ASSISTANT");
        getLogger().info("  Powered by Claude Sonnet 4.5");
        getLogger().info("========================================");
        
        // Save default config
        saveDefaultConfig();
        
        // Initialize Claude API
        String apiKey = getConfig().getString("claude-api-key", "");
        if (apiKey.isEmpty()) {
            getLogger().warning("⚠️  No API key configured!");
            getLogger().warning("⚠️  Set 'claude-api-key' in config.yml");
            getLogger().warning("⚠️  Get API key from: https://console.anthropic.com/");
        } else {
            claudeAPI = new ClaudeAPI(apiKey, this);
            getLogger().info("✓ Claude API initialized");
        }
        
        // Register event listener
        getServer().getPluginManager().registerEvents(this, this);
        
        // Send welcome message to console
        getLogger().info("✓ AI Assistant enabled");
        getLogger().info("✓ Players can use: " + commandPrefix + " <question>");
        getLogger().info("✓ Example: @ai how do I create a plugin?");
    }
    
    @Override
    public void onDisable() {
        getLogger().info("🤖 AI Assistant disabled");
    }
    
    /**
     * Listen for player chat messages
     * Intercept messages starting with @ai
     */
    @EventHandler
    public void onPlayerChat(AsyncPlayerChatEvent event) {
        String message = event.getMessage();
        Player player = event.getPlayer();
        
        // Check if message is for AI
        if (message.startsWith(commandPrefix + " ")) {
            // Cancel normal chat (don't broadcast the @ai command)
            event.setCancelled(true);
            
            // Extract question (remove @ai prefix)
            String question = message.substring(commandPrefix.length() + 1).trim();
            
            if (question.isEmpty()) {
                player.sendMessage(ChatColor.RED + "[Console] Usage: @ai <your question>");
                return;
            }
            
            // Show "thinking" message
            broadcastMessage(ChatColor.GRAY + "[" + player.getName() + "] " + 
                ChatColor.WHITE + "@ai " + question);
            broadcastMessage(ChatColor.YELLOW + "[Console] 🤔 Thinking...");
            
            // Check if API is configured
            if (claudeAPI == null || !claudeAPI.isConfigured()) {
                player.sendMessage(ChatColor.RED + "[Console] ⚠️  AI not configured!");
                player.sendMessage(ChatColor.GRAY + "[Console] Admin needs to set API key in config.yml");
                return;
            }
            
            // Query Claude API asynchronously (don't block server)
            Bukkit.getScheduler().runTaskAsynchronously(this, () -> {
                try {
                    String response = claudeAPI.ask(question, player.getName());
                    
                    // Send response back in main thread
                    Bukkit.getScheduler().runTask(this, () -> {
                        sendAIResponse(response);
                    });
                    
                } catch (Exception e) {
                    getLogger().warning("AI request failed: " + e.getMessage());
                    
                    Bukkit.getScheduler().runTask(this, () -> {
                        player.sendMessage(ChatColor.RED + "[Console] ⚠️  Error: " + e.getMessage());
                    });
                }
            });
        }
    }
    
    /**
     * Send AI response to all players
     * Breaks long messages into multiple chat lines
     */
    private void sendAIResponse(String response) {
        // Split response into chat-sized chunks (max ~100 chars per line)
        String[] lines = wrapText(response, 80);
        
        for (String line : lines) {
            broadcastMessage(ChatColor.AQUA + "[Console] " + ChatColor.WHITE + line);
        }
    }
    
    /**
     * Broadcast message to all players
     */
    private void broadcastMessage(String message) {
        Bukkit.getOnlinePlayers().forEach(p -> p.sendMessage(message));
        getLogger().info(ChatColor.stripColor(message));  // Also log to console
    }
    
    /**
     * Wrap text to fit in Minecraft chat
     * Minecraft chat is ~100 characters wide
     */
    private String[] wrapText(String text, int lineLength) {
        String[] words = text.split(" ");
        java.util.List<String> lines = new java.util.ArrayList<>();
        StringBuilder currentLine = new StringBuilder();
        
        for (String word : words) {
            if (currentLine.length() + word.length() + 1 > lineLength) {
                if (currentLine.length() > 0) {
                    lines.add(currentLine.toString());
                    currentLine = new StringBuilder();
                }
            }
            
            if (currentLine.length() > 0) {
                currentLine.append(" ");
            }
            currentLine.append(word);
        }
        
        if (currentLine.length() > 0) {
            lines.add(currentLine.toString());
        }
        
        return lines.toArray(new String[0]);
    }
}

