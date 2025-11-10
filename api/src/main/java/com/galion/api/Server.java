package com.galion.api;

import com.galion.api.entity.Player;
import com.galion.api.world.World;

import java.util.Collection;
import java.util.UUID;

/**
 * Represents the Minecraft server.
 * Provides methods to interact with the server.
 * 
 * @author Galion Studio
 * @version 1.0.0
 */
public interface Server {
    
    /**
     * Get all online players.
     * 
     * @return collection of online players
     */
    Collection<Player> getOnlinePlayers();
    
    /**
     * Get a player by name.
     * 
     * @param name the player name
     * @return the player, or null if not found
     */
    Player getPlayer(String name);
    
    /**
     * Get a player by UUID.
     * 
     * @param uuid the player UUID
     * @return the player, or null if not found
     */
    Player getPlayer(UUID uuid);
    
    /**
     * Get all loaded worlds.
     * 
     * @return collection of worlds
     */
    Collection<World> getWorlds();
    
    /**
     * Get a world by name.
     * 
     * @param name the world name
     * @return the world, or null if not found
     */
    World getWorld(String name);
    
    /**
     * Broadcast a message to all players.
     * 
     * @param message the message to broadcast
     */
    void broadcast(String message);
    
    /**
     * Get the server name.
     * 
     * @return the server name
     */
    String getName();
    
    /**
     * Get the current TPS (ticks per second).
     * Target is 20.0 TPS.
     * 
     * @return the current TPS
     */
    double getTPS();
    
    /**
     * Get the MSPT (milliseconds per tick).
     * Target is under 50ms.
     * 
     * @return the MSPT
     */
    double getMSPT();
}

