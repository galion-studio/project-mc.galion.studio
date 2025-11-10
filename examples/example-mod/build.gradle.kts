// Example Titan Forge Mod
// Demonstrates how to create a Forge mod using Titan Mod API

plugins {
    java
    id("com.github.johnrengelman.shadow") version "8.1.1"
}

// Get versions from root project
val titanVersion: String by project.extra
val minecraftVersion: String by project.extra
val forgeVersion: String by project.extra

group = "studio.galion.titan.examples"
version = titanVersion

dependencies {
    // Forge API
    compileOnly("net.minecraftforge:forge:${forgeVersion}")
    
    // Titan Mod API - our simplified API
    implementation(project(":titan-mod-api"))
    
    // Titan Common utilities
    implementation(project(":titan-common"))
}

// Configure JAR
tasks.jar {
    archiveBaseName.set("TitanExampleMod")
    archiveVersion.set(titanVersion)
    
    manifest {
        attributes(
            "Specification-Title" to "Titan Example Mod",
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
    archiveBaseName.set("TitanExampleMod")
    
    // Include Titan Mod API
    configurations = listOf(project.configurations.runtimeClasspath.get())
    
    // Relocate to avoid conflicts
    relocate("studio.galion.titan.modapi", "studio.galion.titan.examples.mod.libs.modapi")
}

tasks.build {
    dependsOn(tasks.shadowJar)
}

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(21))
    }
}

tasks.withType<JavaCompile> {
    options.encoding = "UTF-8"
    options.release.set(21)
}

