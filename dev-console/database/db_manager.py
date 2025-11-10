"""
Database Manager for Development Console
Handles all database operations with SQLite
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
import hashlib

from config import DATABASE_PATH


class DatabaseManager:
    """
    Manages database connections and operations.
    Simple, fast, effective - Elon Musk style.
    """
    
    def __init__(self, db_path: Path = DATABASE_PATH):
        self.db_path = db_path
        self.connection = None
        self.initialize_database()
    
    def initialize_database(self):
        """
        Initialize database with schema.
        Creates tables if they don't exist.
        """
        # Read schema file
        schema_path = Path(__file__).parent / "schema.sql"
        with open(schema_path, 'r') as f:
            schema = f.read()
        
        # Execute schema
        conn = self.get_connection()
        conn.executescript(schema)
        conn.commit()
    
    def get_connection(self) -> sqlite3.Connection:
        """
        Get database connection.
        Creates connection if it doesn't exist.
        """
        if self.connection is None:
            self.connection = sqlite3.connect(
                str(self.db_path),
                check_same_thread=False
            )
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    # === User Management ===
    
    def create_user(self, username: str, password_hash: str, role: str) -> int:
        """Create new user"""
        conn = self.get_connection()
        cursor = conn.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role)
        )
        conn.commit()
        return cursor.lastrowid
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        conn = self.get_connection()
        cursor = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        conn = self.get_connection()
        cursor = conn.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def update_user_token(self, user_id: int, token: str):
        """Update user token"""
        conn = self.get_connection()
        conn.execute(
            "UPDATE users SET token = ?, last_login = ? WHERE id = ?",
            (token, datetime.now(), user_id)
        )
        conn.commit()
    
    def get_all_users(self) -> List[Dict]:
        """Get all users"""
        conn = self.get_connection()
        cursor = conn.execute("SELECT * FROM users")
        return [dict(row) for row in cursor.fetchall()]
    
    # === Mod Management ===
    
    def create_mod(self, **kwargs) -> int:
        """
        Create new mod entry.
        
        Required kwargs:
        - name, version, file_name, file_path, file_size,
        - checksum, author_id, environment
        """
        conn = self.get_connection()
        
        # Convert dependencies to JSON if it's a list
        if 'dependencies' in kwargs and isinstance(kwargs['dependencies'], list):
            kwargs['dependencies'] = json.dumps(kwargs['dependencies'])
        
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join('?' * len(kwargs))
        
        cursor = conn.execute(
            f"INSERT INTO mods ({columns}) VALUES ({placeholders})",
            tuple(kwargs.values())
        )
        conn.commit()
        return cursor.lastrowid
    
    def get_mod_by_id(self, mod_id: int) -> Optional[Dict]:
        """Get mod by ID"""
        conn = self.get_connection()
        cursor = conn.execute("SELECT * FROM mods WHERE id = ?", (mod_id,))
        row = cursor.fetchone()
        if row:
            mod = dict(row)
            # Parse dependencies JSON
            if mod.get('dependencies'):
                mod['dependencies'] = json.loads(mod['dependencies'])
            return mod
        return None
    
    def get_mods_by_environment(self, environment: str) -> List[Dict]:
        """Get all mods for an environment"""
        conn = self.get_connection()
        cursor = conn.execute(
            "SELECT * FROM mods WHERE environment = ? ORDER BY created_at DESC",
            (environment,)
        )
        return [dict(row) for row in cursor.fetchall()]
    
    def get_all_mods(self) -> List[Dict]:
        """Get all mods"""
        conn = self.get_connection()
        cursor = conn.execute("SELECT * FROM mods ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]
    
    def update_mod_status(self, mod_id: int, status: str):
        """Update mod status"""
        conn = self.get_connection()
        conn.execute(
            "UPDATE mods SET status = ?, updated_at = ? WHERE id = ?",
            (status, datetime.now(), mod_id)
        )
        conn.commit()
    
    def delete_mod(self, mod_id: int):
        """Delete mod"""
        conn = self.get_connection()
        conn.execute("DELETE FROM mods WHERE id = ?", (mod_id,))
        conn.commit()
    
    # === Deployment Tracking ===
    
    def create_deployment(self, mod_id: int, environment: str, user_id: int,
                         status: str, deployment_type: str,
                         error_message: Optional[str] = None) -> int:
        """Create deployment record"""
        conn = self.get_connection()
        cursor = conn.execute(
            """INSERT INTO deployments 
            (mod_id, environment, user_id, status, deployment_type, error_message)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (mod_id, environment, user_id, status, deployment_type, error_message)
        )
        conn.commit()
        return cursor.lastrowid
    
    def get_recent_deployments(self, limit: int = 50) -> List[Dict]:
        """Get recent deployments"""
        conn = self.get_connection()
        cursor = conn.execute(
            """SELECT d.*, m.name as mod_name, u.username 
            FROM deployments d
            JOIN mods m ON d.mod_id = m.id
            JOIN users u ON d.user_id = u.id
            ORDER BY d.deployed_at DESC
            LIMIT ?""",
            (limit,)
        )
        return [dict(row) for row in cursor.fetchall()]
    
    def get_deployments_by_environment(self, environment: str, limit: int = 50) -> List[Dict]:
        """Get deployments for specific environment"""
        conn = self.get_connection()
        cursor = conn.execute(
            """SELECT d.*, m.name as mod_name, u.username 
            FROM deployments d
            JOIN mods m ON d.mod_id = m.id
            JOIN users u ON d.user_id = u.id
            WHERE d.environment = ?
            ORDER BY d.deployed_at DESC
            LIMIT ?""",
            (environment, limit)
        )
        return [dict(row) for row in cursor.fetchall()]
    
    # === Activity Logging ===
    
    def log_activity(self, user_id: Optional[int], action: str,
                    details: Optional[Dict] = None, ip_address: Optional[str] = None):
        """Log user activity"""
        conn = self.get_connection()
        
        # Convert details to JSON
        details_json = json.dumps(details) if details else None
        
        conn.execute(
            "INSERT INTO activity_logs (user_id, action, details, ip_address) VALUES (?, ?, ?, ?)",
            (user_id, action, details_json, ip_address)
        )
        conn.commit()
    
    def get_recent_activity(self, limit: int = 100) -> List[Dict]:
        """Get recent activity logs"""
        conn = self.get_connection()
        cursor = conn.execute(
            """SELECT a.*, u.username 
            FROM activity_logs a
            LEFT JOIN users u ON a.user_id = u.id
            ORDER BY a.timestamp DESC
            LIMIT ?""",
            (limit,)
        )
        logs = []
        for row in cursor.fetchall():
            log = dict(row)
            # Parse details JSON
            if log.get('details'):
                log['details'] = json.loads(log['details'])
            logs.append(log)
        return logs
    
    def get_user_activity(self, user_id: int, limit: int = 50) -> List[Dict]:
        """Get activity for specific user"""
        conn = self.get_connection()
        cursor = conn.execute(
            """SELECT * FROM activity_logs 
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?""",
            (user_id, limit)
        )
        return [dict(row) for row in cursor.fetchall()]
    
    # === Server Status ===
    
    def record_server_status(self, environment: str, status: str,
                            player_count: int = 0, tps: Optional[float] = None,
                            memory_used: Optional[int] = None,
                            memory_max: Optional[int] = None,
                            uptime: Optional[int] = None):
        """Record server status snapshot"""
        conn = self.get_connection()
        conn.execute(
            """INSERT INTO server_status 
            (environment, status, player_count, tps, memory_used, memory_max, uptime)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (environment, status, player_count, tps, memory_used, memory_max, uptime)
        )
        conn.commit()
    
    def get_latest_server_status(self, environment: str) -> Optional[Dict]:
        """Get latest server status for environment"""
        conn = self.get_connection()
        cursor = conn.execute(
            """SELECT * FROM server_status 
            WHERE environment = ?
            ORDER BY recorded_at DESC
            LIMIT 1""",
            (environment,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None
    
    # === Mod Approvals ===
    
    def create_approval_request(self, mod_id: int, submitted_by: int) -> int:
        """Create mod approval request"""
        conn = self.get_connection()
        cursor = conn.execute(
            "INSERT INTO mod_approvals (mod_id, submitted_by) VALUES (?, ?)",
            (mod_id, submitted_by)
        )
        conn.commit()
        return cursor.lastrowid
    
    def get_pending_approvals(self) -> List[Dict]:
        """Get pending approval requests"""
        conn = self.get_connection()
        cursor = conn.execute(
            """SELECT ma.*, m.name as mod_name, u.username as submitter
            FROM mod_approvals ma
            JOIN mods m ON ma.mod_id = m.id
            JOIN users u ON ma.submitted_by = u.id
            WHERE ma.status = 'pending'
            ORDER BY ma.submitted_at DESC"""
        )
        return [dict(row) for row in cursor.fetchall()]
    
    def update_approval_status(self, approval_id: int, reviewed_by: int,
                              status: str, review_notes: Optional[str] = None):
        """Update approval request status"""
        conn = self.get_connection()
        conn.execute(
            """UPDATE mod_approvals 
            SET reviewed_by = ?, status = ?, review_notes = ?, reviewed_at = ?
            WHERE id = ?""",
            (reviewed_by, status, review_notes, datetime.now(), approval_id)
        )
        conn.commit()
    
    # === Git Commits ===
    
    def create_git_commit(self, mod_id: int, commit_hash: str,
                         commit_message: str, author_id: int) -> int:
        """Record git commit for mod"""
        conn = self.get_connection()
        cursor = conn.execute(
            """INSERT INTO git_commits (mod_id, commit_hash, commit_message, author_id)
            VALUES (?, ?, ?, ?)""",
            (mod_id, commit_hash, commit_message, author_id)
        )
        conn.commit()
        return cursor.lastrowid
    
    def get_mod_commits(self, mod_id: int) -> List[Dict]:
        """Get commit history for mod"""
        conn = self.get_connection()
        cursor = conn.execute(
            """SELECT gc.*, u.username as author
            FROM git_commits gc
            JOIN users u ON gc.author_id = u.id
            WHERE gc.mod_id = ?
            ORDER BY gc.committed_at DESC""",
            (mod_id,)
        )
        return [dict(row) for row in cursor.fetchall()]


# Singleton instance
_db_instance = None


def get_db() -> DatabaseManager:
    """Get database manager singleton"""
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseManager()
    return _db_instance

