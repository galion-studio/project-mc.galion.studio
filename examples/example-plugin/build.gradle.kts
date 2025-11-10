// Example Titan Plugin - Build Configuration
// Template for creating Titan plugins

plugins {
    `java-library`
    id("com.github.johnrengelman.shadow") version "8.1.1"
}

group = "studio.galion.titan.examples"
version = "1.0.0"

dependencies {
    // Titan API
    compileOnly(project(":titan-common"))
    
    // Paper API
    compileOnly("io.papermc.paper:paper-api:1.20.4-R0.1-SNAPSHOT")
}

tasks {
    shadowJar {
        archiveBaseName.set("ExamplePlugin")
        archiveClassifier.set("")
    }
    
    processResources {
        filesMatching("plugin.yml") {
            expand("version" to project.version)
        }
    }
}
