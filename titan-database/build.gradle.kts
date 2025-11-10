// Titan Database - PostgreSQL integration layer
// Provides database connectivity and ORM

plugins {
    `java-library`
}

description = "Titan Database - PostgreSQL integration and data access layer"

dependencies {
    // Common utilities
    api(project(":titan-common"))
    
    // PostgreSQL driver
    implementation("org.postgresql:postgresql:42.6.0")
    
    // Connection pooling (HikariCP - fastest connection pool)
    api("com.zaxxer:HikariCP:5.0.1")
    
    // Database migrations (Flyway)
    implementation("org.flywaydb:flyway-core:9.22.3")
    
    // Lombok
    compileOnly("org.projectlombok:lombok:1.18.30")
    annotationProcessor("org.projectlombok:lombok:1.18.30")
}

tasks.jar {
    archiveBaseName.set("titan-database")
}

