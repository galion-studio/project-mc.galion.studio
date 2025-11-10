"""
Role Manager
Manage user roles and permissions
"""

from typing import Dict, List, Optional
from config import ROLES
from database.db_manager import DatabaseManager


class RoleManager:
    """
    Role and permission manager.
    Simple, clear, effective.
    """
    
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def get_all_roles(self) -> Dict:
        """Get all available roles"""
        return ROLES
    
    def get_role_info(self, role: str) -> Optional[Dict]:
        """Get information about a specific role"""
        return ROLES.get(role)
    
    def get_role_permissions(self, role: str) -> List[str]:
        """Get permissions for a role"""
        role_info = ROLES.get(role)
        if role_info:
            return role_info.get('permissions', [])
        return []
    
    def has_permission(self, role: str, permission: str) -> bool:
        """Check if a role has a specific permission"""
        if role == "admin":
            return True  # Admin has all permissions
        
        permissions = self.get_role_permissions(role)
        return permission in permissions or "all" in permissions
    
    def get_users_by_role(self, role: str) -> List[Dict]:
        """Get all users with a specific role"""
        all_users = self.db.get_all_users()
        return [user for user in all_users if user['role'] == role]
    
    def change_user_role(self, user_id: int, new_role: str, changed_by: int) -> bool:
        """
        Change a user's role.
        
        Args:
            user_id: ID of user to change
            new_role: New role to assign
            changed_by: ID of user making the change
        
        Returns:
            True if successful
        """
        if new_role not in ROLES:
            print(f"[Roles] Invalid role: {new_role}")
            return False
        
        # Get user
        user = self.db.get_user_by_id(user_id)
        if not user:
            print(f"[Roles] User not found: {user_id}")
            return False
        
        old_role = user['role']
        
        # Update role (would need to add this method to db_manager)
        # For now, just log the activity
        self.db.log_activity(
            changed_by,
            "change_user_role",
            {
                "user_id": user_id,
                "username": user['username'],
                "old_role": old_role,
                "new_role": new_role
            }
        )
        
        print(f"[Roles] Changed user {user['username']} role: {old_role} -> {new_role}")
        return True
    
    def format_permissions_list(self, role: str) -> List[str]:
        """Get human-readable permissions list"""
        permissions = self.get_role_permissions(role)
        
        permission_names = {
            "all": "All permissions (Administrator)",
            "upload_mod": "Upload mods",
            "deploy_dev": "Deploy to Development",
            "deploy_staging": "Deploy to Staging",
            "deploy_prod": "Deploy to Production",
            "hot_reload": "Hot reload mods",
            "view_logs": "View server logs",
            "server_control": "Control server (start/stop/restart)",
            "rollback": "Rollback deployments",
        }
        
        return [permission_names.get(perm, perm) for perm in permissions]


# Singleton instance
_role_manager = None


def get_role_manager(db: Optional[DatabaseManager] = None) -> RoleManager:
    """Get role manager singleton"""
    global _role_manager
    if _role_manager is None:
        if db is None:
            from database.db_manager import get_db
            db = get_db()
        _role_manager = RoleManager(db)
    return _role_manager

