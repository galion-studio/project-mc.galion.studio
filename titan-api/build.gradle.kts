// Titan API - Public API for plugin/mod developers

plugins {
    `java-library`
}

description = "Titan API - Public API for plugins and mods"

dependencies {
    // Common utilities
    api(project(":titan-common"))
    
    // Paper API (for plugin development)
    compileOnly("io.papermc.paper:paper-api:1.20.4-R0.1-SNAPSHOT")
}

tasks.jar {
    archiveBaseName.set("titan-api")
}

