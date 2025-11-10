// Titan Server - Multi-module Gradle configuration
// Root project build configuration

rootProject.name = "titan-server"

// Include all subprojects
include(
    // Core server modules
    "titan-core",           // Hybrid Paper + Forge server
    "titan-proxy",          // Velocity-based proxy
    "titan-api",            // Common API for plugins/mods
    
    // Plugin/Mod development
    "titan-plugin-api",     // Plugin API (Bukkit-compatible)
    "titan-mod-api",        // Mod API (Forge-compatible)
    "titan-bridge",         // Paper-Forge compatibility bridge
    
    // Utilities
    "titan-common",         // Shared utilities
    "titan-database",       // Database access layer
    "titan-redis",          // Redis integration
    
    // Monitoring
    "titan-metrics",        // Metrics collection and export
    
    // Plugins
    "plugins:TitanCore",
    "plugins:TitanAI",
    
    // Examples
    "examples:example-plugin",
    "examples:example-mod"
)

// Configure plugin management
pluginManagement {
    repositories {
        gradlePluginPortal()
        maven("https://repo.papermc.io/repository/maven-public/")
        maven("https://maven.minecraftforge.net/")
    }
}

// Configure dependency resolution
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.PREFER_PROJECT)
    repositories {
        mavenCentral()
        maven("https://repo.papermc.io/repository/maven-public/")
        maven("https://hub.spigotmc.org/nexus/content/repositories/snapshots/")
        maven("https://oss.sonatype.org/content/repositories/snapshots/")
        maven("https://oss.sonatype.org/content/repositories/central/")
        maven("https://libraries.minecraft.net/")
        maven("https://maven.minecraftforge.net/")
        maven("https://jitpack.io")
    }
}

