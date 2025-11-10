// Titan AI Assistant Plugin
// In-game AI assistant powered by Claude Sonnet 4.5

plugins {
    `java-library`
    id("com.github.johnrengelman.shadow") version "8.1.1"
}

group = "studio.galion.titan.plugins"
version = "1.0.0"

repositories {
    mavenCentral()
    maven("https://repo.papermc.io/repository/maven-public/")
}

dependencies {
    // Paper API
    compileOnly("io.papermc.paper:paper-api:1.21.1-R0.1-SNAPSHOT")
    
    // HTTP client for Claude API
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
    
    // JSON parsing
    implementation("com.google.code.gson:gson:2.10.1")
    
    // Lombok
    compileOnly("org.projectlombok:lombok:1.18.30")
    annotationProcessor("org.projectlombok:lombok:1.18.30")
}

tasks {
    shadowJar {
        archiveBaseName.set("TitanAI")
        archiveClassifier.set("")
        
        // Relocate dependencies to avoid conflicts
        relocate("okhttp3", "studio.galion.titan.lib.okhttp3")
        relocate("okio", "studio.galion.titan.lib.okio")
    }
    
    processResources {
        filesMatching("plugin.yml") {
            expand("version" to project.version)
        }
    }
    
    build {
        dependsOn(shadowJar)
    }
}

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(21))
    }
}

