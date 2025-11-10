package studio.galion.titan.database;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import lombok.extern.slf4j.Slf4j;
import org.flywaydb.core.Flyway;
import studio.galion.titan.common.config.TitanConfig;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

/**
 * Database Manager
 * Manages PostgreSQL connections using HikariCP
 * 
 * HikariCP is the fastest and most reliable connection pool.
 * This class provides the foundation for all database operations.
 */
@Slf4j
public class DatabaseManager {
    
    private final HikariDataSource dataSource;
    
    /**
     * Initialize database manager with configuration
     * 
     * @param config Titan configuration
     */
    public DatabaseManager(TitanConfig config) {
        TitanConfig.DatabaseConfig dbConfig = config.getDatabase();
        
        // Configure HikariCP
        HikariConfig hikariConfig = new HikariConfig();
        
        // JDBC URL
        String jdbcUrl = String.format(
            "jdbc:postgresql://%s:%d/%s",
            dbConfig.getHost(),
            dbConfig.getPort(),
            dbConfig.getDatabase()
        );
        hikariConfig.setJdbcUrl(jdbcUrl);
        
        // Credentials
        hikariConfig.setUsername(dbConfig.getUsername());
        hikariConfig.setPassword(dbConfig.getPassword());
        
        // Connection pool configuration
        hikariConfig.setMaximumPoolSize(dbConfig.getPoolSize());
        hikariConfig.setMinimumIdle(dbConfig.getPoolSize() / 2);
        hikariConfig.setConnectionTimeout(10000);     // 10 seconds
        hikariConfig.setIdleTimeout(300000);          // 5 minutes
        hikariConfig.setMaxLifetime(1800000);         // 30 minutes
        hikariConfig.setLeakDetectionThreshold(60000); // 1 minute
        
        // Performance tuning
        hikariConfig.addDataSourceProperty("cachePrepStmts", "true");
        hikariConfig.addDataSourceProperty("prepStmtCacheSize", "250");
        hikariConfig.addDataSourceProperty("prepStmtCacheSqlLimit", "2048");
        hikariConfig.addDataSourceProperty("useServerPrepStmts", "true");
        hikariConfig.addDataSourceProperty("useLocalSessionState", "true");
        hikariConfig.addDataSourceProperty("rewriteBatchedStatements", "true");
        hikariConfig.addDataSourceProperty("cacheResultSetMetadata", "true");
        hikariConfig.addDataSourceProperty("cacheServerConfiguration", "true");
        hikariConfig.addDataSourceProperty("elideSetAutoCommits", "true");
        hikariConfig.addDataSourceProperty("maintainTimeStats", "false");
        
        // Pool name for monitoring
        hikariConfig.setPoolName("TitanDB-Pool");
        
        // Create data source
        this.dataSource = new HikariDataSource(hikariConfig);
        
        log.info("Database connection pool initialized: {}", jdbcUrl);
        log.info("Pool size: {} connections", dbConfig.getPoolSize());
        
        // Run migrations
        runMigrations();
    }
    
    /**
     * Run database migrations using Flyway
     * Automatically updates schema to latest version
     */
    private void runMigrations() {
        try {
            log.info("Running database migrations...");
            
            Flyway flyway = Flyway.configure()
                .dataSource(dataSource)
                .locations("classpath:db/migration")
                .baselineOnMigrate(true)
                .load();
            
            int migrationsApplied = flyway.migrate().migrationsExecuted;
            
            if (migrationsApplied > 0) {
                log.info("Applied {} database migration(s)", migrationsApplied);
            } else {
                log.info("Database is up to date");
            }
            
        } catch (Exception e) {
            log.error("Database migration failed", e);
            throw new RuntimeException("Failed to migrate database", e);
        }
    }
    
    /**
     * Get a connection from the pool
     * IMPORTANT: Must be closed after use (use try-with-resources)
     * 
     * @return Database connection
     * @throws SQLException if connection cannot be obtained
     */
    public Connection getConnection() throws SQLException {
        return dataSource.getConnection();
    }
    
    /**
     * Get the underlying data source
     * 
     * @return HikariCP data source
     */
    public DataSource getDataSource() {
        return dataSource;
    }
    
    /**
     * Execute a query and process results
     * Automatically manages connection lifecycle
     * 
     * @param sql SQL query
     * @param handler Result handler
     * @param params Query parameters
     * @param <T> Return type
     * @return Result from handler
     */
    public <T> T executeQuery(String sql, ResultSetHandler<T> handler, Object... params) {
        try (Connection conn = getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            
            // Set parameters
            for (int i = 0; i < params.length; i++) {
                stmt.setObject(i + 1, params[i]);
            }
            
            // Execute and handle results
            try (ResultSet rs = stmt.executeQuery()) {
                return handler.handle(rs);
            }
            
        } catch (SQLException e) {
            log.error("Query failed: {}", sql, e);
            throw new RuntimeException("Database query failed", e);
        }
    }
    
    /**
     * Execute an update/insert/delete statement
     * 
     * @param sql SQL statement
     * @param params Statement parameters
     * @return Number of rows affected
     */
    public int executeUpdate(String sql, Object... params) {
        try (Connection conn = getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            
            // Set parameters
            for (int i = 0; i < params.length; i++) {
                stmt.setObject(i + 1, params[i]);
            }
            
            // Execute update
            return stmt.executeUpdate();
            
        } catch (SQLException e) {
            log.error("Update failed: {}", sql, e);
            throw new RuntimeException("Database update failed", e);
        }
    }
    
    /**
     * Execute a batch update
     * More efficient for multiple similar operations
     * 
     * @param sql SQL statement
     * @param paramsList List of parameter sets
     * @return Array of update counts
     */
    public int[] executeBatch(String sql, java.util.List<Object[]> paramsList) {
        try (Connection conn = getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {
            
            // Add all batches
            for (Object[] params : paramsList) {
                for (int i = 0; i < params.length; i++) {
                    stmt.setObject(i + 1, params[i]);
                }
                stmt.addBatch();
            }
            
            // Execute batch
            return stmt.executeBatch();
            
        } catch (SQLException e) {
            log.error("Batch update failed: {}", sql, e);
            throw new RuntimeException("Database batch update failed", e);
        }
    }
    
    /**
     * Test database connection
     * 
     * @return true if database is accessible
     */
    public boolean testConnection() {
        try (Connection conn = getConnection()) {
            return conn.isValid(5); // 5 second timeout
        } catch (SQLException e) {
            log.error("Database connection test failed", e);
            return false;
        }
    }
    
    /**
     * Get connection pool statistics
     * 
     * @return Statistics string
     */
    public String getPoolStats() {
        return String.format(
            "Active: %d, Idle: %d, Total: %d, Waiting: %d",
            dataSource.getHikariPoolMXBean().getActiveConnections(),
            dataSource.getHikariPoolMXBean().getIdleConnections(),
            dataSource.getHikariPoolMXBean().getTotalConnections(),
            dataSource.getHikariPoolMXBean().getThreadsAwaitingConnection()
        );
    }
    
    /**
     * Shutdown the connection pool
     * Should be called on server shutdown
     */
    public void shutdown() {
        if (dataSource != null && !dataSource.isClosed()) {
            log.info("Closing database connection pool");
            dataSource.close();
        }
    }
    
    /**
     * Functional interface for handling ResultSet
     * 
     * @param <T> Return type
     */
    @FunctionalInterface
    public interface ResultSetHandler<T> {
        T handle(ResultSet rs) throws SQLException;
    }
}

