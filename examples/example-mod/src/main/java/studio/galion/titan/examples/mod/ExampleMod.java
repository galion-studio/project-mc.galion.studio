package studio.galion.titan.examples.mod;

import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.event.entity.player.PlayerEvent;
import net.minecraftforge.event.server.ServerStartingEvent;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.ModContainer;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.event.lifecycle.*;
import studio.galion.titan.modapi.core.TitanMod;
import studio.galion.titan.modapi.event.TitanEventHandler;

/**
 * Example Titan Forge Mod
 * 
 * This demonstrates how to create a Forge mod using the Titan Mod API.
 * The mod adds simple functionality like welcoming players and logging events.
 * 
 * Key features:
 * - Extends TitanMod for simplified lifecycle management
 * - Uses TitanEventHandler for easy event registration
 * - Demonstrates both server and client-side code
 * - Shows network communication patterns
 */
@Mod(ExampleMod.MOD_ID)
public class ExampleMod extends TitanMod {
    
    // Mod constants
    public static final String MOD_ID = "titanexample";
    public static final String MOD_NAME = "Titan Example Mod";
    public static final String VERSION = "1.0.0";
    
    // Event handler
    private TitanEventHandler events;
    
    /**
     * Mod constructor.
     * Called by Forge when loading the mod.
     */
    public ExampleMod(IEventBus modEventBus, ModContainer modContainer) {
        super(modEventBus, modContainer);
        
        logger.info("===========================================");
        logger.info("  {} v{}", MOD_NAME, VERSION);
        logger.info("  by Galion Studio");
        logger.info("===========================================");
        
        // Initialize event handler
        this.events = new TitanEventHandler(MOD_ID);
        
        // Register game events
        registerGameEvents();
    }
    
    /**
     * Common setup - runs on both client and server.
     * This is where you initialize things that work on both sides.
     */
    @Override
    protected void commonSetup(FMLCommonSetupEvent event) {
        logger.info("[{}] Running common setup...", MOD_ID);
        
        // Example: Register items, blocks, etc.
        // registerItems();
        // registerBlocks();
        
        logger.info("[{}] Common setup complete!", MOD_ID);
    }
    
    /**
     * Client setup - runs only on client side.
     * This is where you initialize client-only features.
     */
    @Override
    protected void clientSetup(FMLClientSetupEvent event) {
        logger.info("[{}] Running client setup...", MOD_ID);
        
        // Example: Register renderers, keybinds, etc.
        // registerRenderers();
        // registerKeybinds();
        
        logger.info("[{}] Client setup complete!", MOD_ID);
    }
    
    /**
     * Server setup - runs only on dedicated server.
     * This is where you initialize server-only features.
     */
    @Override
    protected void serverSetup(FMLDedicatedServerSetupEvent event) {
        logger.info("[{}] Running server setup...", MOD_ID);
        
        // Example: Register server commands, schedulers, etc.
        // registerCommands();
        // startBackgroundTasks();
        
        logger.info("[{}] Server setup complete!", MOD_ID);
    }
    
    /**
     * Load complete - all mods have finished loading.
     * This is where you can interact with other mods safely.
     */
    @Override
    protected void loadComplete(FMLLoadCompleteEvent event) {
        logger.info("[{}] Finalizing mod initialization...", MOD_ID);
        
        // Example: Interact with other mods
        // setupModIntegrations();
        
        logger.info("===========================================");
        logger.info("  {} is ready!", MOD_NAME);
        logger.info("===========================================");
    }
    
    /**
     * Register game events (events that happen during gameplay).
     * These are separate from mod lifecycle events.
     */
    private void registerGameEvents() {
        logger.debug("[{}] Registering game events...", MOD_ID);
        
        // Example: Player login event
        events.on(PlayerEvent.PlayerLoggedInEvent.class, this::onPlayerLogin);
        
        // Example: Player logout event
        events.on(PlayerEvent.PlayerLoggedOutEvent.class, this::onPlayerLogout);
        
        // Example: Server starting event
        MinecraftForge.EVENT_BUS.addListener(this::onServerStarting);
        
        logger.debug("[{}] Game events registered", MOD_ID);
    }
    
    /**
     * Called when a player logs in.
     */
    private void onPlayerLogin(PlayerEvent.PlayerLoggedInEvent event) {
        String playerName = event.getEntity().getName().getString();
        logger.info("[{}] Player joined: {}", MOD_ID, playerName);
        
        // Example: Send welcome message
        // event.getEntity().sendSystemMessage(
        //     Component.literal("§b[Titan] §fWelcome to the server, " + playerName + "!")
        // );
    }
    
    /**
     * Called when a player logs out.
     */
    private void onPlayerLogout(PlayerEvent.PlayerLoggedOutEvent event) {
        String playerName = event.getEntity().getName().getString();
        logger.info("[{}] Player left: {}", MOD_ID, playerName);
    }
    
    /**
     * Called when server is starting.
     */
    private void onServerStarting(ServerStartingEvent event) {
        logger.info("[{}] Server is starting...", MOD_ID);
        
        // Example: Register commands
        // Commands.register(event.getServer().getCommands().getDispatcher());
    }
}

