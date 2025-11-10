-- Development Console Database Schema
-- SQLite database for metadata and activity tracking

-- Users table
-- Stores user accounts and their roles
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin', 'internal_dev', 'external_dev')),
    token TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Mods table
-- Stores mod metadata and versions
CREATE TABLE IF NOT EXISTS mods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    version TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_size INTEGER NOT NULL,
    checksum TEXT NOT NULL,
    mc_version TEXT,
    author_id INTEGER,
    environment TEXT NOT NULL CHECK(environment IN ('dev', 'staging', 'prod')),
    status TEXT DEFAULT 'active' CHECK(status IN ('active', 'inactive', 'pending_approval', 'rejected')),
    description TEXT,
    dependencies TEXT,  -- JSON array of mod dependencies
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users(id),
    UNIQUE(name, version, environment)
);

-- Deployments table
-- Tracks deployment history
CREATE TABLE IF NOT EXISTS deployments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mod_id INTEGER NOT NULL,
    environment TEXT NOT NULL CHECK(environment IN ('dev', 'staging', 'prod')),
    user_id INTEGER NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('pending', 'success', 'failed', 'rolled_back')),
    deployment_type TEXT CHECK(deployment_type IN ('upload', 'hot_reload', 'rollback')),
    error_message TEXT,
    deployed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (mod_id) REFERENCES mods(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Activity logs table
-- Comprehensive activity tracking for auditing
CREATE TABLE IF NOT EXISTS activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT NOT NULL,
    details TEXT,  -- JSON object with additional details
    ip_address TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Server status table
-- Tracks server health and uptime
CREATE TABLE IF NOT EXISTS server_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    environment TEXT NOT NULL CHECK(environment IN ('dev', 'staging', 'prod')),
    status TEXT NOT NULL CHECK(status IN ('online', 'offline', 'starting', 'stopping')),
    player_count INTEGER DEFAULT 0,
    tps REAL,
    memory_used INTEGER,
    memory_max INTEGER,
    uptime INTEGER,  -- seconds
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Mod approvals table
-- For external developer mod approval workflow
CREATE TABLE IF NOT EXISTS mod_approvals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mod_id INTEGER NOT NULL,
    submitted_by INTEGER NOT NULL,
    reviewed_by INTEGER,
    status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'approved', 'rejected')),
    review_notes TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP,
    FOREIGN KEY (mod_id) REFERENCES mods(id),
    FOREIGN KEY (submitted_by) REFERENCES users(id),
    FOREIGN KEY (reviewed_by) REFERENCES users(id)
);

-- Git commits table
-- Track version control commits for mods
CREATE TABLE IF NOT EXISTS git_commits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mod_id INTEGER NOT NULL,
    commit_hash TEXT NOT NULL,
    commit_message TEXT,
    author_id INTEGER,
    committed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (mod_id) REFERENCES mods(id),
    FOREIGN KEY (author_id) REFERENCES users(id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_mods_environment ON mods(environment);
CREATE INDEX IF NOT EXISTS idx_mods_status ON mods(status);
CREATE INDEX IF NOT EXISTS idx_deployments_environment ON deployments(environment);
CREATE INDEX IF NOT EXISTS idx_deployments_status ON deployments(status);
CREATE INDEX IF NOT EXISTS idx_activity_logs_timestamp ON activity_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_activity_logs_user ON activity_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_server_status_environment ON server_status(environment);
CREATE INDEX IF NOT EXISTS idx_mod_approvals_status ON mod_approvals(status);

-- Create default admin user (password: admin123 - CHANGE THIS!)
-- Password hash is bcrypt of 'admin123'
INSERT OR IGNORE INTO users (username, password_hash, role) 
VALUES ('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYfJ3pSvH8S', 'admin');

