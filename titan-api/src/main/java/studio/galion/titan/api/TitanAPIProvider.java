package studio.galion.titan.api;

/**
 * Provider for TitanAPI singleton
 * Internal class - plugins should use TitanAPI.getInstance()
 */
class TitanAPIProvider {
    
    private static TitanAPI instance;
    
    /**
     * Set the API implementation
     * Called by Titan core on startup
     * 
     * @param api API implementation
     */
    public static void setInstance(TitanAPI api) {
        if (instance != null) {
            throw new IllegalStateException("TitanAPI already initialized");
        }
        instance = api;
    }
    
    /**
     * Get the API instance
     * 
     * @return TitanAPI instance
     * @throws IllegalStateException if not initialized
     */
    public static TitanAPI getInstance() {
        if (instance == null) {
            throw new IllegalStateException("TitanAPI not initialized - is Titan loaded?");
        }
        return instance;
    }
}

