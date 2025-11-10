package studio.galion.titan.plugins.ai;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import okhttp3.*;
import org.bukkit.plugin.Plugin;

import java.io.IOException;
import java.util.concurrent.TimeUnit;

/**
 * Claude API Integration
 * Connects to Anthropic's Claude API (Sonnet 4.5)
 * 
 * This allows in-game chat with Claude AI for:
 * - Code help
 * - Plugin development
 * - Server management
 * - Debugging assistance
 */
public class ClaudeAPI {
    
    private static final String API_URL = "https://api.anthropic.com/v1/messages";
    private static final String MODEL = "claude-sonnet-4-20250514"; // Latest Sonnet 4.5
    private static final int MAX_TOKENS = 1024;  // Response length
    
    private final String apiKey;
    private final Plugin plugin;
    private final OkHttpClient client;
    private final Gson gson;
    
    /**
     * Initialize Claude API client
     * 
     * @param apiKey Anthropic API key
     * @param plugin Plugin instance
     */
    public ClaudeAPI(String apiKey, Plugin plugin) {
        this.apiKey = apiKey;
        this.plugin = plugin;
        this.gson = new Gson();
        
        // Create HTTP client with timeout
        this.client = new OkHttpClient.Builder()
            .connectTimeout(10, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .writeTimeout(10, TimeUnit.SECONDS)
            .build();
    }
    
    /**
     * Check if API is properly configured
     * 
     * @return true if API key is set
     */
    public boolean isConfigured() {
        return apiKey != null && !apiKey.isEmpty() && !apiKey.equals("YOUR_API_KEY_HERE");
    }
    
    /**
     * Ask Claude a question
     * 
     * @param question User's question
     * @param playerName Player who asked
     * @return Claude's response
     * @throws IOException if API call fails
     */
    public String ask(String question, String playerName) throws IOException {
        if (!isConfigured()) {
            return "AI not configured. Admin needs to set API key in config.yml";
        }
        
        // Build request payload
        JsonObject requestBody = new JsonObject();
        requestBody.addProperty("model", MODEL);
        requestBody.addProperty("max_tokens", MAX_TOKENS);
        
        // Add system message (gives context to Claude)
        requestBody.addProperty("system", 
            "You are an AI assistant embedded in a Minecraft server called Titan. " +
            "You help players with code, plugins, server management, and Minecraft questions. " +
            "Keep responses SHORT (under 200 chars) - Minecraft chat is limited. " +
            "Be helpful, friendly, and concise. " +
            "You're talking to player: " + playerName);
        
        // Add user message
        JsonArray messages = new JsonArray();
        JsonObject userMessage = new JsonObject();
        userMessage.addProperty("role", "user");
        userMessage.addProperty("content", question);
        messages.add(userMessage);
        requestBody.add("messages", messages);
        
        // Create HTTP request
        RequestBody body = RequestBody.create(
            gson.toJson(requestBody),
            MediaType.parse("application/json")
        );
        
        Request request = new Request.Builder()
            .url(API_URL)
            .addHeader("x-api-key", apiKey)
            .addHeader("anthropic-version", "2023-06-01")
            .addHeader("content-type", "application/json")
            .post(body)
            .build();
        
        // Execute request
        try (Response response = client.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                plugin.getLogger().warning("Claude API error: " + response.code());
                return "Error: API returned status " + response.code();
            }
            
            // Parse response
            String responseBody = response.body().string();
            JsonObject jsonResponse = gson.fromJson(responseBody, JsonObject.class);
            
            // Extract text from response
            JsonArray content = jsonResponse.getAsJsonArray("content");
            if (content.size() > 0) {
                JsonObject firstContent = content.get(0).getAsJsonObject();
                String text = firstContent.get("text").getAsString();
                
                // Log for debugging
                plugin.getLogger().info("AI Response: " + text);
                
                return text;
            }
            
            return "No response from AI";
        }
    }
}

