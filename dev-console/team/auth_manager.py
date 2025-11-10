"""
Authentication Manager
User authentication and session management
"""

import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Dict
from pathlib import Path

from config import ROLES
from database.db_manager import DatabaseManager


class AuthManager:
    """
    Authentication manager.
    Simple, secure, effective.
    """
    
    # Secret key for JWT tokens (should be in environment variable in production)
    SECRET_KEY = "dev_console_secret_key_change_in_production"
    TOKEN_EXPIRY_DAYS = 7
    
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password
        
        Returns:
            Hashed password
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """
        Verify a password against a hash.
        
        Args:
            password: Plain text password
            hashed: Hashed password
        
        Returns:
            True if password matches
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def generate_token(self, user_id: int, username: str, role: str) -> str:
        """
        Generate JWT token for user.
        
        Args:
            user_id: User ID
            username: Username
            role: User role
        
        Returns:
            JWT token string
        """
        payload = {
            "user_id": user_id,
            "username": username,
            "role": role,
            "exp": datetime.utcnow() + timedelta(days=self.TOKEN_EXPIRY_DAYS)
        }
        
        token = jwt.encode(payload, self.SECRET_KEY, algorithm="HS256")
        return token
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """
        Verify and decode JWT token.
        
        Args:
            token: JWT token string
        
        Returns:
            Decoded payload if valid, None otherwise
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            print("[Auth] Token expired")
            return None
        except jwt.InvalidTokenError:
            print("[Auth] Invalid token")
            return None
    
    def login(self, username: str, password: str) -> Optional[Dict]:
        """
        Authenticate user and generate token.
        
        Args:
            username: Username
            password: Plain text password
        
        Returns:
            User info with token if successful, None otherwise
        """
        # Get user from database
        user = self.db.get_user_by_username(username)
        
        if not user:
            print(f"[Auth] User not found: {username}")
            return None
        
        # Verify password
        if not self.verify_password(password, user['password_hash']):
            print(f"[Auth] Invalid password for user: {username}")
            return None
        
        # Generate token
        token = self.generate_token(user['id'], user['username'], user['role'])
        
        # Update user token in database
        self.db.update_user_token(user['id'], token)
        
        # Log activity
        self.db.log_activity(
            user['id'],
            "login",
            {"username": username}
        )
        
        print(f"[Auth] Login successful: {username} ({user['role']})")
        
        return {
            "id": user['id'],
            "username": user['username'],
            "role": user['role'],
            "token": token
        }
    
    def logout(self, user_id: int):
        """
        Logout user by clearing token.
        
        Args:
            user_id: User ID
        """
        self.db.update_user_token(user_id, None)
        
        # Log activity
        self.db.log_activity(
            user_id,
            "logout",
            {}
        )
        
        print(f"[Auth] User logged out: {user_id}")
    
    def register_user(self, username: str, password: str, role: str = "external_dev") -> Optional[int]:
        """
        Register a new user.
        
        Args:
            username: Username
            password: Plain text password
            role: User role (default: external_dev)
        
        Returns:
            User ID if successful, None otherwise
        """
        # Validate role
        if role not in ROLES:
            print(f"[Auth] Invalid role: {role}")
            return None
        
        # Check if username already exists
        existing_user = self.db.get_user_by_username(username)
        if existing_user:
            print(f"[Auth] Username already exists: {username}")
            return None
        
        # Hash password
        password_hash = self.hash_password(password)
        
        # Create user
        user_id = self.db.create_user(username, password_hash, role)
        
        # Log activity
        self.db.log_activity(
            user_id,
            "user_registered",
            {"username": username, "role": role}
        )
        
        print(f"[Auth] User registered: {username} ({role})")
        
        return user_id
    
    def check_permission(self, user: Dict, permission: str) -> bool:
        """
        Check if user has a specific permission.
        
        Args:
            user: User dictionary with 'role' key
            permission: Permission to check
        
        Returns:
            True if user has permission
        """
        role = user.get('role')
        
        if not role or role not in ROLES:
            return False
        
        # Admin has all permissions
        if role == "admin":
            return True
        
        # Check role permissions
        role_permissions = ROLES[role].get('permissions', [])
        
        return permission in role_permissions or "all" in role_permissions
    
    def require_permission(self, permission: str):
        """
        Decorator to require permission for a function.
        
        Args:
            permission: Required permission
        
        Returns:
            Decorator function
        """
        def decorator(func):
            def wrapper(user: Dict, *args, **kwargs):
                if not self.check_permission(user, permission):
                    raise PermissionError(f"User lacks permission: {permission}")
                return func(user, *args, **kwargs)
            return wrapper
        return decorator


# Singleton instance
_auth_manager = None


def get_auth_manager(db: Optional[DatabaseManager] = None) -> AuthManager:
    """Get authentication manager singleton"""
    global _auth_manager
    if _auth_manager is None:
        if db is None:
            from database.db_manager import get_db
            db = get_db()
        _auth_manager = AuthManager(db)
    return _auth_manager


# Test function
if __name__ == "__main__":
    from database.db_manager import get_db
    
    print("="*50)
    print("  AUTHENTICATION MANAGER TEST")
    print("="*50)
    print()
    
    db = get_db()
    auth = get_auth_manager(db)
    
    # Test login with default admin account
    print("Testing login with admin account...")
    result = auth.login("admin", "admin123")
    
    if result:
        print("[OK] Login successful!")
        print(f"  User ID: {result['id']}")
        print(f"  Username: {result['username']}")
        print(f"  Role: {result['role']}")
        print(f"  Token: {result['token'][:50]}...")
        print()
        
        # Test token verification
        print("Testing token verification...")
        payload = auth.verify_token(result['token'])
        if payload:
            print("[OK] Token valid!")
            print(f"  User ID: {payload['user_id']}")
            print(f"  Username: {payload['username']}")
            print(f"  Role: {payload['role']}")
        else:
            print("[ERROR] Token invalid!")
        print()
        
        # Test permissions
        print("Testing permissions...")
        perms_to_test = ["upload_mod", "deploy_prod", "view_logs", "invalid_perm"]
        for perm in perms_to_test:
            has_perm = auth.check_permission(result, perm)
            print(f"  {perm}: {'✓' if has_perm else '✗'}")
    else:
        print("[ERROR] Login failed!")
        print("  Make sure the default admin account exists")
        print("  Username: admin")
        print("  Password: admin123")
    
    print("\nDone!")

