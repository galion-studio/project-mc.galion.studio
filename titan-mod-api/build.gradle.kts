// Titan Mod API - Forge mod development API
// Provides unified interface for creating Forge mods

plugins {
    java
    id("com.github.johnrengelman.shadow") version "8.1.1"
}

// Get version from root project
val titanVersion: String by project.extra
val minecraftVersion: String by project.extra
val forgeVersion: String by project.extra

// Project configuration
group = "studio.galion.titan"
version = titanVersion

dependencies {
    // Forge API - use MinecraftForge dependency
    compileOnly("net.minecraftforge:forge:${forgeVersion}")
    
    // Titan Common - shared utilities across all modules
    implementation(project(":titan-common"))
    
    // Networking
    implementation("com.google.code.gson:gson:2.10.1")
    
    // Annotations for safety
    compileOnly("org.jetbrains:annotations:24.0.1")
}

// Configure JAR task
tasks.jar {
    archiveBaseName.set("TitanModAPI")
    archiveVersion.set(titanVersion)
    
    manifest {
        attributes(
            "Specification-Title" to "Titan Mod API",
            "Specification-Vendor" to "Galion Studio",
            "Specification-Version" to "1",
            "Implementation-Title" to project.name,
            "Implementation-Version" to titanVersion,
            "Implementation-Vendor" to "Galion Studio"
        )
    }
}

// Shadow JAR for distribution
tasks.shadowJar {
    archiveClassifier.set("")
    archiveBaseName.set("TitanModAPI")
    
    // Don't include Forge itself
    configurations = listOf(project.configurations.runtimeClasspath.get())
    
    // Relocate dependencies to avoid conflicts
    relocate("com.google.gson", "studio.galion.titan.libs.gson")
}

// Build task
tasks.build {
    dependsOn(tasks.shadowJar)
}

// Configure Java compilation
java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(21))
    }
    withSourcesJar()
    withJavadocJar()
}

// Compiler options
tasks.withType<JavaCompile> {
    options.encoding = "UTF-8"
    options.release.set(21)
}

