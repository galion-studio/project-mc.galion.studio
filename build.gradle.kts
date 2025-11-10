// Titan Server - Root build configuration
// This file configures the entire multi-module project

plugins {
    // Apply Java plugin to all subprojects
    java apply false
    
    // Kotlin support (for modern development)
    kotlin("jvm") version "1.9.20" apply false
    
    // Shadow plugin for fat JARs
    id("com.github.johnrengelman.shadow") version "8.1.1" apply false
}

// Configure all subprojects
subprojects {
    apply(plugin = "java")
    apply(plugin = "java-library")
    
    // Java version configuration
    configure<JavaPluginExtension> {
        toolchain {
            languageVersion.set(JavaLanguageVersion.of(17))
        }
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    
    // Common repositories for all modules
    repositories {
        mavenCentral()
        maven("https://repo.papermc.io/repository/maven-public/")
        maven("https://hub.spigotmc.org/nexus/content/repositories/snapshots/")
        maven("https://maven.minecraftforge.net/")
        maven("https://jitpack.io")
    }
    
    // Common dependencies for all modules
    dependencies {
        // Testing framework
        testImplementation("org.junit.jupiter:junit-jupiter:5.10.0")
        testImplementation("org.mockito:mockito-core:5.5.0")
        testImplementation("org.assertj:assertj-core:3.24.2")
        
        // Logging
        implementation("org.slf4j:slf4j-api:2.0.9")
        implementation("ch.qos.logback:logback-classic:1.4.11")
        
        // Annotations
        compileOnly("org.jetbrains:annotations:24.0.1")
    }
    
    // Configure test task
    tasks.test {
        useJUnitPlatform()
        
        testLogging {
            events("passed", "skipped", "failed")
            showStandardStreams = false
        }
    }
    
    // Set encoding
    tasks.withType<JavaCompile> {
        options.encoding = "UTF-8"
    }
}

// Root project tasks
tasks.register("buildAll") {
    group = "build"
    description = "Build all Titan modules"
    dependsOn(subprojects.map { it.tasks.named("build") })
}

tasks.register("cleanAll") {
    group = "build"
    description = "Clean all Titan modules"
    dependsOn(subprojects.map { it.tasks.named("clean") })
}

// Version management
val titanVersion = "1.0.0-ALPHA"
val minecraftVersion = "1.21.1"
val paperVersion = "1.21.1-R0.1-SNAPSHOT"
val forgeVersion = "1.21.1-52.0.17"

// Make versions available to all subprojects
subprojects {
    extra["titanVersion"] = titanVersion
    extra["minecraftVersion"] = minecraftVersion
    extra["paperVersion"] = paperVersion
    extra["forgeVersion"] = forgeVersion
}

// Print build information
println("""
    ╔═══════════════════════════════════════════╗
    ║   TITAN SERVER - Build Configuration      ║
    ╠═══════════════════════════════════════════╣
    ║   Version: $titanVersion              ║
    ║   Minecraft: $minecraftVersion                ║
    ║   Java: 21                                ║
    ║   Modules: ${subprojects.size}                            ║
    ╚═══════════════════════════════════════════╝
""".trimIndent())

