-- Titan Database Schema - Version 1
-- Initial schema creation
-- This creates the foundational tables for the Titan server

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ========================================
-- Players Table
-- Stores core player information
-- ========================================
CREATE TABLE players (
    uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(16) NOT NULL UNIQUE,
    
    -- Timestamps
    first_join TIMESTAMP NOT NULL DEFAULT NOW(),
    last_join TIMESTAMP NOT NULL DEFAULT NOW(),
    last_seen TIMESTAMP NOT NULL DEFAULT NOW(),
    
    -- Playtime (in seconds)
    playtime BIGINT NOT NULL DEFAULT 0,
    
    -- Rank and permissions
    rank VARCHAR(32) NOT NULL DEFAULT 'player',
    
    -- Status
    is_online BOOLEAN NOT NULL DEFAULT false,
    current_server VARCHAR(64),
    
    -- Metadata
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Index for faster lookups
CREATE INDEX idx_players_username ON players(username);
CREATE INDEX idx_players_online ON players(is_online);
CREATE INDEX idx_players_rank ON players(rank);

-- ========================================
-- Player Data Table
-- Stores serialized player data (inventory, location, etc.)
-- Uses JSONB for flexible schema
-- ========================================
CREATE TABLE player_data (
    uuid UUID PRIMARY KEY REFERENCES players(uuid) ON DELETE CASCADE,
    
    -- Location data
    world VARCHAR(64),
    location_x DOUBLE PRECISION,
    location_y DOUBLE PRECISION,
    location_z DOUBLE PRECISION,
    location_yaw REAL,
    location_pitch REAL,
    
    -- Serialized data
    inventory JSONB,
    ender_chest JSONB,
    statistics JSONB,
    custom_data JSONB,
    
    -- Metadata
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ========================================
-- Player Economy Table
-- Stores player balances and transaction history
-- ========================================
CREATE TABLE player_economy (
    uuid UUID PRIMARY KEY REFERENCES players(uuid) ON DELETE CASCADE,
    balance DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    
    -- Metadata
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Ensure balance is never negative
ALTER TABLE player_economy ADD CONSTRAINT check_balance_positive CHECK (balance >= 0);

-- ========================================
-- Economy Transactions Table
-- Audit log for all economy transactions
-- ========================================
CREATE TABLE economy_transactions (
    id BIGSERIAL PRIMARY KEY,
    uuid UUID NOT NULL REFERENCES players(uuid) ON DELETE CASCADE,
    
    -- Transaction details
    transaction_type VARCHAR(32) NOT NULL, -- deposit, withdraw, transfer, etc.
    amount DECIMAL(15, 2) NOT NULL,
    balance_before DECIMAL(15, 2) NOT NULL,
    balance_after DECIMAL(15, 2) NOT NULL,
    
    -- Context
    reason VARCHAR(255),
    related_player UUID REFERENCES players(uuid),
    server_name VARCHAR(64),
    
    -- Timestamp
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Index for player transaction history
CREATE INDEX idx_transactions_uuid ON economy_transactions(uuid);
CREATE INDEX idx_transactions_created_at ON economy_transactions(created_at);

-- ========================================
-- Player Permissions Table
-- Stores individual player permissions
-- ========================================
CREATE TABLE player_permissions (
    id BIGSERIAL PRIMARY KEY,
    uuid UUID NOT NULL REFERENCES players(uuid) ON DELETE CASCADE,
    permission VARCHAR(255) NOT NULL,
    value BOOLEAN NOT NULL DEFAULT true,
    
    -- Expiration (for temporary permissions)
    expires_at TIMESTAMP,
    
    -- Metadata
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    
    -- Ensure no duplicate permissions per player
    UNIQUE(uuid, permission)
);

-- Index for faster permission lookups
CREATE INDEX idx_permissions_uuid ON player_permissions(uuid);
CREATE INDEX idx_permissions_expires ON player_permissions(expires_at);

-- ========================================
-- Server Registry Table
-- Tracks active game servers in the network
-- ========================================
CREATE TABLE server_registry (
    id BIGSERIAL PRIMARY KEY,
    server_name VARCHAR(64) NOT NULL UNIQUE,
    server_type VARCHAR(32) NOT NULL, -- hub, survival, creative, etc.
    
    -- Network info
    host VARCHAR(255) NOT NULL,
    port INTEGER NOT NULL,
    
    -- Status
    is_online BOOLEAN NOT NULL DEFAULT true,
    player_count INTEGER NOT NULL DEFAULT 0,
    max_players INTEGER NOT NULL DEFAULT 500,
    
    -- Performance metrics
    tps REAL,
    cpu_usage REAL,
    memory_used BIGINT,
    memory_max BIGINT,
    
    -- Timestamps
    last_heartbeat TIMESTAMP NOT NULL DEFAULT NOW(),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Index for server lookups
CREATE INDEX idx_servers_type ON server_registry(server_type);
CREATE INDEX idx_servers_online ON server_registry(is_online);

-- ========================================
-- Server Events Table
-- Logs important server events for analytics and debugging
-- ========================================
CREATE TABLE server_events (
    id BIGSERIAL PRIMARY KEY,
    server_name VARCHAR(64) NOT NULL,
    event_type VARCHAR(64) NOT NULL,
    
    -- Optional player context
    player_uuid UUID REFERENCES players(uuid) ON DELETE SET NULL,
    player_username VARCHAR(16),
    
    -- Event data (flexible JSON)
    event_data JSONB,
    
    -- Severity (info, warning, error)
    severity VARCHAR(16) NOT NULL DEFAULT 'info',
    
    -- Timestamp
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Index for event queries
CREATE INDEX idx_events_server ON server_events(server_name);
CREATE INDEX idx_events_type ON server_events(event_type);
CREATE INDEX idx_events_player ON server_events(player_uuid);
CREATE INDEX idx_events_created_at ON server_events(created_at);

-- ========================================
-- Chat Log Table
-- Stores chat messages for moderation and analytics
-- ========================================
CREATE TABLE chat_log (
    id BIGSERIAL PRIMARY KEY,
    uuid UUID NOT NULL REFERENCES players(uuid) ON DELETE CASCADE,
    username VARCHAR(16) NOT NULL,
    
    -- Message details
    message TEXT NOT NULL,
    chat_type VARCHAR(32) NOT NULL DEFAULT 'global', -- global, local, private, etc.
    server_name VARCHAR(64) NOT NULL,
    
    -- Moderation
    is_filtered BOOLEAN NOT NULL DEFAULT false,
    is_deleted BOOLEAN NOT NULL DEFAULT false,
    
    -- Timestamp
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Index for chat queries
CREATE INDEX idx_chat_uuid ON chat_log(uuid);
CREATE INDEX idx_chat_created_at ON chat_log(created_at);
CREATE INDEX idx_chat_server ON chat_log(server_name);

-- ========================================
-- Punishment Table
-- Stores bans, mutes, and warnings
-- ========================================
CREATE TABLE punishments (
    id BIGSERIAL PRIMARY KEY,
    uuid UUID NOT NULL REFERENCES players(uuid) ON DELETE CASCADE,
    
    -- Punishment details
    punishment_type VARCHAR(16) NOT NULL, -- ban, mute, warn, kick
    reason TEXT NOT NULL,
    
    -- Who issued the punishment
    issued_by_uuid UUID REFERENCES players(uuid) ON DELETE SET NULL,
    issued_by_username VARCHAR(16),
    
    -- Duration
    issued_at TIMESTAMP NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMP, -- NULL = permanent
    
    -- Status
    is_active BOOLEAN NOT NULL DEFAULT true,
    is_appealed BOOLEAN NOT NULL DEFAULT false,
    
    -- Revocation (if unbanned/unmuted)
    revoked_at TIMESTAMP,
    revoked_by_uuid UUID REFERENCES players(uuid) ON DELETE SET NULL,
    revoke_reason TEXT,
    
    -- Server context
    server_name VARCHAR(64)
);

-- Index for punishment lookups
CREATE INDEX idx_punishments_uuid ON punishments(uuid);
CREATE INDEX idx_punishments_active ON punishments(is_active);
CREATE INDEX idx_punishments_type ON punishments(punishment_type);
CREATE INDEX idx_punishments_expires ON punishments(expires_at);

-- ========================================
-- Trigger: Update updated_at on row modification
-- ========================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to tables with updated_at
CREATE TRIGGER update_players_updated_at BEFORE UPDATE ON players
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_player_data_updated_at BEFORE UPDATE ON player_data
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_economy_updated_at BEFORE UPDATE ON player_economy
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_server_registry_updated_at BEFORE UPDATE ON server_registry
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ========================================
-- Initial Data
-- ========================================

-- Insert default ranks (can be expanded with a ranks table later)
-- For now, ranks are just strings in the players table

-- Server health check view
CREATE OR REPLACE VIEW server_health AS
SELECT 
    server_name,
    server_type,
    is_online,
    player_count,
    max_players,
    ROUND((player_count::NUMERIC / max_players::NUMERIC) * 100, 2) as capacity_percent,
    tps,
    ROUND(cpu_usage, 2) as cpu_usage,
    ROUND((memory_used::NUMERIC / memory_max::NUMERIC) * 100, 2) as memory_percent,
    last_heartbeat,
    EXTRACT(EPOCH FROM (NOW() - last_heartbeat)) as seconds_since_heartbeat
FROM server_registry
ORDER BY is_online DESC, player_count DESC;

-- Player stats view
CREATE OR REPLACE VIEW player_stats AS
SELECT 
    COUNT(*) as total_players,
    COUNT(*) FILTER (WHERE is_online) as online_players,
    COUNT(*) FILTER (WHERE NOT is_online) as offline_players,
    ROUND(AVG(playtime) / 3600, 2) as avg_playtime_hours,
    MAX(playtime) as max_playtime
FROM players;

COMMENT ON TABLE players IS 'Core player information and metadata';
COMMENT ON TABLE player_data IS 'Player game state (inventory, location, etc.)';
COMMENT ON TABLE player_economy IS 'Player economy balances';
COMMENT ON TABLE economy_transactions IS 'Audit log for all economy operations';
COMMENT ON TABLE player_permissions IS 'Individual player permissions';
COMMENT ON TABLE server_registry IS 'Active server registry for network';
COMMENT ON TABLE server_events IS 'Server event log for analytics';
COMMENT ON TABLE chat_log IS 'Chat message history';
COMMENT ON TABLE punishments IS 'Player punishments (bans, mutes, etc.)';

