// Titan Common - Shared utilities and classes
// Used across all Titan modules

plugins {
    `java-library`
}

description = "Titan Common - Shared utilities and core classes"

dependencies {
    // JSON processing
    api("com.google.code.gson:gson:2.10.1")
    
    // Utilities
    api("com.google.guava:guava:32.1.3-jre")
    
    // Configuration
    api("org.yaml:snakeyaml:2.2")
    
    // Lombok (reduce boilerplate)
    compileOnly("org.projectlombok:lombok:1.18.30")
    annotationProcessor("org.projectlombok:lombok:1.18.30")
}

tasks.jar {
    archiveBaseName.set("titan-common")
    manifest {
        attributes(
            "Implementation-Title" to "Titan Common",
            "Implementation-Version" to project.version
        )
    }
}

