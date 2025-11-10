package studio.galion.titan.common.messaging;

import com.google.gson.Gson;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.UUID;

/**
 * Cross-Server Message Model
 * Used for communication between Titan servers via Redis Pub/Sub
 * 
 * Real functionality: Enables chat, teleports, and data sync across servers
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Message {
    
    private static final Gson GSON = new Gson();
    
    // Message metadata
    private String id;                  // Unique message ID
    private MessageType type;           // Type of message
    private String sourceServer;        // Server that sent the message
    private String targetServer;        // Target server (null = broadcast)
    private long timestamp;             // When message was sent
    
    // Message payload
    private UUID playerUuid;            // Related player (if any)
    private String channel;             // Message channel (chat, admin, etc)
    private String content;             // Message content
    private String data;                // Additional data (JSON)
    
    /**
     * Message types for different cross-server operations
     */
    public enum MessageType {
        CHAT,               // Global chat message
        PLAYER_JOIN,        // Player joined network
        PLAYER_QUIT,        // Player left network
        PLAYER_SWITCH,      // Player switching servers
        TELEPORT,           // Cross-server teleport
        COMMAND,            // Execute command on other server
        DATA_SYNC,          // Sync player data
        BROADCAST,          // Server broadcast
        STAFF_MESSAGE       // Staff-only message
    }
    
    /**
     * Create a new message
     * 
     * @param type Message type
     * @param sourceServer Source server name
     * @return New message instance
     */
    public static Message create(MessageType type, String sourceServer) {
        Message message = new Message();
        message.id = UUID.randomUUID().toString();
        message.type = type;
        message.sourceServer = sourceServer;
        message.timestamp = System.currentTimeMillis();
        return message;
    }
    
    /**
     * Create chat message
     * 
     * @param sourceServer Server name
     * @param playerUuid Player UUID
     * @param channel Chat channel
     * @param content Message content
     * @return Chat message
     */
    public static Message createChatMessage(String sourceServer, UUID playerUuid, 
                                          String channel, String content) {
        Message message = create(MessageType.CHAT, sourceServer);
        message.playerUuid = playerUuid;
        message.channel = channel;
        message.content = content;
        return message;
    }
    
    /**
     * Create teleport request
     * 
     * @param sourceServer Source server
     * @param targetServer Target server
     * @param playerUuid Player to teleport
     * @return Teleport message
     */
    public static Message createTeleportRequest(String sourceServer, String targetServer, 
                                               UUID playerUuid) {
        Message message = create(MessageType.TELEPORT, sourceServer);
        message.targetServer = targetServer;
        message.playerUuid = playerUuid;
        return message;
    }
    
    /**
     * Serialize to JSON for Redis
     * 
     * @return JSON string
     */
    public String toJson() {
        return GSON.toJson(this);
    }
    
    /**
     * Deserialize from JSON
     * 
     * @param json JSON string
     * @return Message instance
     */
    public static Message fromJson(String json) {
        return GSON.fromJson(json, Message.class);
    }
    
    /**
     * Check if message is for this server
     * 
     * @param serverName This server's name
     * @return true if message is targeted at this server or is broadcast
     */
    public boolean isForServer(String serverName) {
        // Broadcast messages (targetServer is null)
        if (targetServer == null) {
            return true;
        }
        
        // Targeted message
        return targetServer.equals(serverName);
    }
    
    /**
     * Check if message is expired
     * 
     * @param maxAgeMs Maximum age in milliseconds
     * @return true if message is too old
     */
    public boolean isExpired(long maxAgeMs) {
        return (System.currentTimeMillis() - timestamp) > maxAgeMs;
    }
}

