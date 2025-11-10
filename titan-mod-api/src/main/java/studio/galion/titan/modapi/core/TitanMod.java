package studio.galion.titan.modapi.core;

import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.ModContainer;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.event.lifecycle.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Base class for all Titan Forge mods.
 * Provides unified lifecycle management and common functionality.
 * 
 * Usage:
 * <pre>
 * @Mod("your_mod_id")
 * public class YourMod extends TitanMod {
 *     public YourMod(IEventBus modEventBus, ModContainer modContainer) {
 *         super(modEventBus, modContainer);
 *     }
 *     
 *     @Override
 *     protected void commonSetup(FMLCommonSetupEvent event) {
 *         // Your common setup code
 *     }
 * }
 * </pre>
 */
public abstract class TitanMod {
    
    // Logger for this mod
    protected final Logger logger;
    
    // Mod information
    private final String modId;
    private final ModContainer container;
    private final IEventBus modEventBus;
    
    // Lifecycle state
    private boolean isInitialized = false;
    
    /**
     * Constructor for Titan mods.
     * 
     * @param modEventBus The mod-specific event bus
     * @param modContainer The mod container
     */
    public TitanMod(IEventBus modEventBus, ModContainer modContainer) {
        this.container = modContainer;
        this.modId = modContainer.getModId();
        this.modEventBus = modEventBus;
        this.logger = LoggerFactory.getLogger(getClass());
        
        // Register lifecycle events
        registerLifecycleEvents();
        
        logger.info("Initializing Titan Mod: {}", modId);
    }
    
    /**
     * Register all lifecycle event handlers.
     * Automatically called by constructor.
     */
    private void registerLifecycleEvents() {
        // Common setup (both client and server)
        modEventBus.addListener(this::onCommonSetup);
        
        // Client setup
        modEventBus.addListener(this::onClientSetup);
        
        // Server setup
        modEventBus.addListener(this::onServerSetup);
        
        // Load complete
        modEventBus.addListener(this::onLoadComplete);
        
        // Allow subclasses to register additional events
        registerEvents(modEventBus);
    }
    
    /**
     * Called during common setup phase.
     * Override this to add your common initialization logic.
     */
    protected void commonSetup(FMLCommonSetupEvent event) {
        // Default implementation - override in subclasses
    }
    
    /**
     * Called during client setup phase.
     * Override this to add client-specific initialization.
     */
    protected void clientSetup(FMLClientSetupEvent event) {
        // Default implementation - override in subclasses
    }
    
    /**
     * Called during server setup phase.
     * Override this to add server-specific initialization.
     */
    protected void serverSetup(FMLDedicatedServerSetupEvent event) {
        // Default implementation - override in subclasses
    }
    
    /**
     * Called when all mods have finished loading.
     * Override this for post-load initialization.
     */
    protected void loadComplete(FMLLoadCompleteEvent event) {
        // Default implementation - override in subclasses
    }
    
    /**
     * Register additional event handlers.
     * Override this to register custom events.
     * 
     * @param eventBus The mod event bus
     */
    protected void registerEvents(IEventBus eventBus) {
        // Default implementation - override in subclasses
    }
    
    // Internal event handlers that call protected methods
    
    private void onCommonSetup(FMLCommonSetupEvent event) {
        logger.info("[{}] Running common setup...", modId);
        event.enqueueWork(() -> {
            try {
                commonSetup(event);
                logger.info("[{}] Common setup complete", modId);
            } catch (Exception e) {
                logger.error("[{}] Error during common setup", modId, e);
            }
        });
    }
    
    private void onClientSetup(FMLClientSetupEvent event) {
        logger.info("[{}] Running client setup...", modId);
        event.enqueueWork(() -> {
            try {
                clientSetup(event);
                logger.info("[{}] Client setup complete", modId);
            } catch (Exception e) {
                logger.error("[{}] Error during client setup", modId, e);
            }
        });
    }
    
    private void onServerSetup(FMLDedicatedServerSetupEvent event) {
        logger.info("[{}] Running server setup...", modId);
        event.enqueueWork(() -> {
            try {
                serverSetup(event);
                isInitialized = true;
                logger.info("[{}] Server setup complete", modId);
            } catch (Exception e) {
                logger.error("[{}] Error during server setup", modId, e);
            }
        });
    }
    
    private void onLoadComplete(FMLLoadCompleteEvent event) {
        logger.info("[{}] Finalizing initialization...", modId);
        event.enqueueWork(() -> {
            try {
                loadComplete(event);
                isInitialized = true;
                logger.info("[{}] ✓ Mod fully loaded and ready!", modId);
            } catch (Exception e) {
                logger.error("[{}] Error during load complete", modId, e);
            }
        });
    }
    
    // Getters
    
    /**
     * Get the mod ID.
     * @return The mod ID
     */
    public String getModId() {
        return modId;
    }
    
    /**
     * Get the mod container.
     * @return The mod container
     */
    public ModContainer getContainer() {
        return container;
    }
    
    /**
     * Get the mod event bus.
     * @return The mod event bus
     */
    public IEventBus getModEventBus() {
        return modEventBus;
    }
    
    /**
     * Get the logger.
     * @return The logger instance
     */
    public Logger getLogger() {
        return logger;
    }
    
    /**
     * Check if mod is fully initialized.
     * @return True if initialized
     */
    public boolean isInitialized() {
        return isInitialized;
    }
}

