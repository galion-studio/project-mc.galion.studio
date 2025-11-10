package studio.galion.titan.modapi.event;

import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.eventbus.api.Event;
import net.minecraftforge.eventbus.api.EventPriority;
import net.minecraftforge.eventbus.api.IEventBus;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.function.Consumer;

/**
 * Simplified event handler for Titan mods.
 * Provides easy event registration and handling.
 * 
 * Usage:
 * <pre>
 * TitanEventHandler events = new TitanEventHandler("your_mod_id");
 * events.on(PlayerEvent.PlayerLoggedInEvent.class, this::onPlayerLogin);
 * </pre>
 */
public class TitanEventHandler {
    
    private static final Logger LOGGER = LoggerFactory.getLogger(TitanEventHandler.class);
    private final String modId;
    private final IEventBus gameEventBus;
    
    /**
     * Create event handler.
     * 
     * @param modId The mod ID for logging
     */
    public TitanEventHandler(String modId) {
        this.modId = modId;
        this.gameEventBus = MinecraftForge.EVENT_BUS;
        LOGGER.debug("[{}] Event handler initialized", modId);
    }
    
    /**
     * Register event handler with normal priority.
     * 
     * @param <T> Event type
     * @param eventClass The event class
     * @param handler The handler function
     */
    public <T extends Event> void on(Class<T> eventClass, Consumer<T> handler) {
        on(eventClass, handler, EventPriority.NORMAL);
    }
    
    /**
     * Register event handler with custom priority.
     * 
     * @param <T> Event type
     * @param eventClass The event class
     * @param handler The handler function
     * @param priority Event priority
     */
    public <T extends Event> void on(Class<T> eventClass, Consumer<T> handler, EventPriority priority) {
        gameEventBus.addListener(priority, false, eventClass, event -> {
            try {
                handler.accept(event);
            } catch (Exception e) {
                LOGGER.error("[{}] Error handling event: {}", modId, eventClass.getSimpleName(), e);
            }
        });
        
        LOGGER.debug("[{}] Registered handler for: {} (priority: {})", 
            modId, eventClass.getSimpleName(), priority);
    }
    
    /**
     * Register a cancelable event handler.
     * The handler can return true to cancel the event.
     * 
     * @param <T> Event type
     * @param eventClass The event class
     * @param handler Handler that returns true to cancel
     */
    public <T extends Event> void onCancelable(Class<T> eventClass, CancelableHandler<T> handler) {
        gameEventBus.addListener(EventPriority.NORMAL, false, eventClass, event -> {
            try {
                if (handler.handle(event)) {
                    if (event.isCancelable()) {
                        event.setCanceled(true);
                    }
                }
            } catch (Exception e) {
                LOGGER.error("[{}] Error handling cancelable event: {}", 
                    modId, eventClass.getSimpleName(), e);
            }
        });
        
        LOGGER.debug("[{}] Registered cancelable handler for: {}", 
            modId, eventClass.getSimpleName());
    }
    
    /**
     * Post an event to the event bus.
     * 
     * @param event The event to post
     * @return true if event was canceled
     */
    public boolean post(Event event) {
        return gameEventBus.post(event);
    }
    
    /**
     * Get the game event bus.
     * @return The Forge event bus
     */
    public IEventBus getEventBus() {
        return gameEventBus;
    }
    
    /**
     * Functional interface for cancelable event handlers.
     * @param <T> Event type
     */
    @FunctionalInterface
    public interface CancelableHandler<T extends Event> {
        /**
         * Handle the event.
         * @param event The event
         * @return true to cancel the event
         */
        boolean handle(T event);
    }
}

