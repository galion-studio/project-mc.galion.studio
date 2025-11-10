package studio.galion.titan.common.player;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Player Location Model
 * Represents a player's position in the world
 * 
 * Used for cross-server teleportation and spawning
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class PlayerLocation {
    
    // World identifier
    private String world;
    
    // Position coordinates
    private double x;
    private double y;
    private double z;
    
    // Rotation (in degrees)
    private float yaw;
    private float pitch;
    
    /**
     * Create location from string format
     * Format: "world,x,y,z,yaw,pitch"
     * 
     * @param locationString String representation
     * @return PlayerLocation instance
     */
    public static PlayerLocation fromString(String locationString) {
        String[] parts = locationString.split(",");
        
        if (parts.length != 6) {
            throw new IllegalArgumentException("Invalid location string format");
        }
        
        return new PlayerLocation(
            parts[0],                    // world
            Double.parseDouble(parts[1]), // x
            Double.parseDouble(parts[2]), // y
            Double.parseDouble(parts[3]), // z
            Float.parseFloat(parts[4]),   // yaw
            Float.parseFloat(parts[5])    // pitch
        );
    }
    
    /**
     * Convert to string format
     * Format: "world,x,y,z,yaw,pitch"
     * 
     * @return String representation
     */
    @Override
    public String toString() {
        return String.format("%s,%.2f,%.2f,%.2f,%.2f,%.2f",
            world, x, y, z, yaw, pitch);
    }
    
    /**
     * Calculate distance to another location
     * Note: Only calculates if in same world
     * 
     * @param other Other location
     * @return Distance, or -1 if different worlds
     */
    public double distanceTo(PlayerLocation other) {
        if (!this.world.equals(other.world)) {
            return -1;
        }
        
        double dx = this.x - other.x;
        double dy = this.y - other.y;
        double dz = this.z - other.z;
        
        return Math.sqrt(dx * dx + dy * dy + dz * dz);
    }
    
    /**
     * Create a copy of this location
     * 
     * @return Cloned location
     */
    public PlayerLocation clone() {
        return new PlayerLocation(world, x, y, z, yaw, pitch);
    }
}

