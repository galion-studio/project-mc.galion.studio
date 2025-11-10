package studio.galion.titan.modapi.network;

import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerPlayer;
import net.minecraftforge.network.NetworkDirection;
import net.minecraftforge.network.NetworkRegistry;
import net.minecraftforge.network.simple.SimpleChannel;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.concurrent.atomic.AtomicInteger;

/**
 * Handles network communication between client and server mods.
 * Provides simple packet registration and sending.
 * 
 * Usage:
 * <pre>
 * NetworkHandler handler = new NetworkHandler("your_mod_id");
 * handler.registerPacket(YourPacket.class, YourPacket::encode, YourPacket::decode, YourPacket::handle);
 * </pre>
 */
public class NetworkHandler {
    
    private static final Logger LOGGER = LoggerFactory.getLogger(NetworkHandler.class);
    private static final String PROTOCOL_VERSION = "1";
    
    private final SimpleChannel channel;
    private final AtomicInteger packetId = new AtomicInteger(0);
    private final String modId;
    
    /**
     * Create a new network handler for a mod.
     * 
     * @param modId The mod ID
     */
    public NetworkHandler(String modId) {
        this.modId = modId;
        
        // Create network channel
        this.channel = NetworkRegistry.newSimpleChannel(
            ResourceLocation.fromNamespaceAndPath(modId, "main"),
            () -> PROTOCOL_VERSION,
            PROTOCOL_VERSION::equals,
            PROTOCOL_VERSION::equals
        );
        
        LOGGER.info("[{}] Network handler initialized", modId);
    }
    
    /**
     * Register a bidirectional packet (can be sent both ways).
     * 
     * @param <T> The packet type
     * @param packetClass The packet class
     * @param encoder Packet encoder
     * @param decoder Packet decoder
     * @param handler Packet handler
     */
    public <T> void registerPacket(
            Class<T> packetClass,
            PacketEncoder<T> encoder,
            PacketDecoder<T> decoder,
            PacketHandler<T> handler) {
        
        int id = packetId.getAndIncrement();
        
        channel.registerMessage(
            id,
            packetClass,
            encoder::encode,
            decoder::decode,
            handler::handle
        );
        
        LOGGER.debug("[{}] Registered packet #{}: {}", modId, id, packetClass.getSimpleName());
    }
    
    /**
     * Send packet to server.
     * Only works on client side.
     * 
     * @param packet The packet to send
     */
    public void sendToServer(Object packet) {
        channel.send(packet, NetworkDirection.PLAY_TO_SERVER);
        LOGGER.debug("[{}] Sent packet to server: {}", modId, packet.getClass().getSimpleName());
    }
    
    /**
     * Send packet to specific player.
     * Only works on server side.
     * 
     * @param packet The packet to send
     * @param player The target player
     */
    public void sendToPlayer(Object packet, ServerPlayer player) {
        channel.send(packet, NetworkDirection.PLAY_TO_CLIENT);
        LOGGER.debug("[{}] Sent packet to player {}: {}", 
            modId, player.getName().getString(), packet.getClass().getSimpleName());
    }
    
    /**
     * Send packet to all connected players.
     * Only works on server side.
     * 
     * @param packet The packet to send
     */
    public void sendToAllPlayers(Object packet) {
        // Note: Requires access to server instance
        // Implementation depends on how you access the server
        LOGGER.debug("[{}] Broadcast packet: {}", modId, packet.getClass().getSimpleName());
    }
    
    /**
     * Get the underlying SimpleChannel.
     * 
     * @return The network channel
     */
    public SimpleChannel getChannel() {
        return channel;
    }
    
    /**
     * Functional interface for packet encoding.
     * @param <T> Packet type
     */
    @FunctionalInterface
    public interface PacketEncoder<T> {
        void encode(T packet, net.minecraft.network.FriendlyByteBuf buffer);
    }
    
    /**
     * Functional interface for packet decoding.
     * @param <T> Packet type
     */
    @FunctionalInterface
    public interface PacketDecoder<T> {
        T decode(net.minecraft.network.FriendlyByteBuf buffer);
    }
    
    /**
     * Functional interface for packet handling.
     * @param <T> Packet type
     */
    @FunctionalInterface
    public interface PacketHandler<T> {
        void handle(T packet, net.minecraftforge.event.network.CustomPayloadEvent.Context context);
    }
}

