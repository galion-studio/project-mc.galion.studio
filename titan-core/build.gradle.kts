// Titan Core - Main server implementation
// Hybrid Paper + Forge compatibility

plugins {
    `java-library`
    id("com.github.johnrengelman.shadow") version "8.1.1"
}

description = "Titan Core - Hybrid Minecraft server implementation"

dependencies {
    // Titan modules
    api(project(":titan-common"))
    api(project(":titan-database"))
    api(project(":titan-redis"))
    
    // Paper API
    compileOnly("io.papermc.paper:paper-api:1.20.4-R0.1-SNAPSHOT")
    
    // Lombok
    compileOnly("org.projectlombok:lombok:1.18.30")
    annotationProcessor("org.projectlombok:lombok:1.18.30")
}

tasks {
    shadowJar {
        archiveBaseName.set("titan-core")
        archiveClassifier.set("")
        
        // Include dependencies
        configurations = listOf(project.configurations.runtimeClasspath.get())
        
        // Relocate to avoid conflicts
        relocate("redis.clients.jedis", "studio.galion.titan.lib.jedis")
        relocate("com.zaxxer.hikari", "studio.galion.titan.lib.hikari")
        relocate("org.postgresql", "studio.galion.titan.lib.postgresql")
        
        manifest {
            attributes(
                "Main-Class" to "studio.galion.titan.core.TitanServer",
                "Implementation-Title" to "Titan Core",
                "Implementation-Version" to project.version
            )
        }
    }
    
    build {
        dependsOn(shadowJar)
    }
}
