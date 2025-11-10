// Titan Redis - Redis integration layer
// Provides Redis connectivity and helper utilities

plugins {
    `java-library`
}

description = "Titan Redis - Redis integration and caching layer"

dependencies {
    // Common utilities
    api(project(":titan-common"))
    
    // Jed is - Redis client
    api("redis.clients:jedis:5.0.2")
    
    // Connection pooling
    implementation("org.apache.commons:commons-pool2:2.12.0")
    
    // Lombok
    compileOnly("org.projectlombok:lombok:1.18.30")
    annotationProcessor("org.projectlombok:lombok:1.18.30")
}

tasks.jar {
    archiveBaseName.set("titan-redis")
}

