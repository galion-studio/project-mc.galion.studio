"""
Activity Feed Component
Team collaboration and activity tracking
"""

import customtkinter as ctk
from datetime import datetime
from typing import Optional

from config import THEME, LAYOUT
from database.db_manager import DatabaseManager


class ActivityFeed(ctk.CTkScrollableFrame):
    """
    Activity feed for team collaboration.
    Real-time activity tracking and mod approvals.
    """
    
    def __init__(self, parent, db: DatabaseManager):
        super().__init__(
            parent,
            fg_color=THEME["bg_primary"],
            corner_radius=0
        )
        
        self.db = db
        
        # Header
        header = ctk.CTkLabel(
            self,
            text="👥 Team Activity",
            font=THEME["font_header"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        header.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        # Tabs for different views
        self.create_tabs()
        
        # Load initial data
        self.load_activity()
    
    def create_tabs(self):
        """Create tabbed interface"""
        tab_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        tab_frame.pack(fill="x", padx=LAYOUT["card_padding"], pady=10)
        
        self.activity_btn = ctk.CTkButton(
            tab_frame,
            text="Recent Activity",
            width=150,
            fg_color=THEME["accent"],
            command=lambda: self.switch_tab("activity")
        )
        self.activity_btn.pack(side="left", padx=5)
        
        self.approvals_btn = ctk.CTkButton(
            tab_frame,
            text="Pending Approvals",
            width=150,
            fg_color=THEME["card_bg"],
            command=lambda: self.switch_tab("approvals")
        )
        self.approvals_btn.pack(side="left", padx=5)
        
        self.users_btn = ctk.CTkButton(
            tab_frame,
            text="Team Members",
            width=150,
            fg_color=THEME["card_bg"],
            command=lambda: self.switch_tab("users")
        )
        self.users_btn.pack(side="left", padx=5)
        
        # Content card
        self.content_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        self.content_card.pack(fill="both", expand=True, padx=LAYOUT["card_padding"], pady=10)
        
        # Content frame (will be replaced on tab switch)
        self.content_frame = ctk.CTkScrollableFrame(
            self.content_card,
            fg_color="transparent"
        )
        self.content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.current_tab = "activity"
    
    def switch_tab(self, tab: str):
        """Switch between tabs"""
        # Update button colors
        self.activity_btn.configure(
            fg_color=THEME["accent"] if tab == "activity" else THEME["card_bg"]
        )
        self.approvals_btn.configure(
            fg_color=THEME["accent"] if tab == "approvals" else THEME["card_bg"]
        )
        self.users_btn.configure(
            fg_color=THEME["accent"] if tab == "users" else THEME["card_bg"]
        )
        
        self.current_tab = tab
        
        # Load appropriate content
        if tab == "activity":
            self.load_activity()
        elif tab == "approvals":
            self.load_approvals()
        elif tab == "users":
            self.load_users()
    
    def load_activity(self):
        """Load recent activity"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Get recent activity
        activities = self.db.get_recent_activity(50)
        
        if not activities:
            ctk.CTkLabel(
                self.content_frame,
                text="No recent activity",
                font=THEME["font_body"],
                text_color=THEME["text_secondary"]
            ).pack(pady=20)
            return
        
        # Display activities
        for activity in activities:
            self.create_activity_item(activity)
    
    def create_activity_item(self, activity: dict):
        """Create activity item"""
        item_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=THEME["bg_primary"],
            corner_radius=8
        )
        item_frame.pack(fill="x", pady=5)
        
        # Icon based on action
        action_icons = {
            "login": "🔐",
            "logout": "🚪",
            "upload_mod": "📦",
            "delete_mod": "🗑️",
            "deploy_mod": "🚀",
            "reload_mod": "🔄",
            "user_registered": "👤",
            "change_user_role": "⚙️",
        }
        icon = action_icons.get(activity['action'], "ℹ️")
        
        # Format action text
        action_text = self.format_action_text(activity)
        
        # Username and action
        text = f"{icon} {activity.get('username', 'System')}: {action_text}"
        
        ctk.CTkLabel(
            item_frame,
            text=text,
            font=THEME["font_body"],
            text_color=THEME["text_primary"],
            anchor="w"
        ).pack(side="left", padx=15, pady=10, fill="x", expand=True)
        
        # Timestamp
        timestamp = activity.get('timestamp', '')
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp)
                time_str = dt.strftime("%H:%M")
            except:
                time_str = timestamp
        else:
            time_str = ""
        
        ctk.CTkLabel(
            item_frame,
            text=time_str,
            font=THEME["font_small"],
            text_color=THEME["text_dim"]
        ).pack(side="right", padx=15, pady=10)
    
    def format_action_text(self, activity: dict) -> str:
        """Format activity action text"""
        action = activity['action']
        details = activity.get('details', {})
        
        if isinstance(details, str):
            import json
            try:
                details = json.loads(details)
            except:
                details = {}
        
        if action == "upload_mod":
            mod_name = details.get('mod_name', 'unknown')
            return f"uploaded mod {mod_name}"
        elif action == "delete_mod":
            mod_name = details.get('mod_name', 'unknown')
            return f"deleted mod {mod_name}"
        elif action == "login":
            return "logged in"
        elif action == "logout":
            return "logged out"
        elif action == "user_registered":
            username = details.get('username', 'unknown')
            return f"registered user {username}"
        elif action == "change_user_role":
            username = details.get('username', 'unknown')
            new_role = details.get('new_role', 'unknown')
            return f"changed {username}'s role to {new_role}"
        else:
            return action.replace('_', ' ')
    
    def load_approvals(self):
        """Load pending approvals"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Get pending approvals
        approvals = self.db.get_pending_approvals()
        
        if not approvals:
            ctk.CTkLabel(
                self.content_frame,
                text="No pending approvals",
                font=THEME["font_body"],
                text_color=THEME["text_secondary"]
            ).pack(pady=20)
            return
        
        # Display approvals
        for approval in approvals:
            self.create_approval_item(approval)
    
    def create_approval_item(self, approval: dict):
        """Create approval request item"""
        item_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=THEME["bg_primary"],
            corner_radius=8
        )
        item_frame.pack(fill="x", pady=5)
        
        # Info section
        info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)
        
        # Mod name
        ctk.CTkLabel(
            info_frame,
            text=f"📦 {approval['mod_name']}",
            font=("Segoe UI", 14, "bold"),
            text_color=THEME["text_primary"],
            anchor="w"
        ).pack(anchor="w")
        
        # Submitter
        ctk.CTkLabel(
            info_frame,
            text=f"Submitted by: {approval['submitter']}",
            font=THEME["font_small"],
            text_color=THEME["text_secondary"],
            anchor="w"
        ).pack(anchor="w")
        
        # Action buttons
        actions_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        actions_frame.pack(side="right", padx=10, pady=10)
        
        ctk.CTkButton(
            actions_frame,
            text="✓ Approve",
            width=100,
            fg_color=THEME["success"],
            hover_color="#00c993",
            command=lambda: self.approve_mod(approval['id'])
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            actions_frame,
            text="✗ Reject",
            width=100,
            fg_color=THEME["error"],
            hover_color="#cc4444",
            command=lambda: self.reject_mod(approval['id'])
        ).pack(side="left", padx=2)
    
    def load_users(self):
        """Load team members"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Get all users
        users = self.db.get_all_users()
        
        if not users:
            ctk.CTkLabel(
                self.content_frame,
                text="No users found",
                font=THEME["font_body"],
                text_color=THEME["text_secondary"]
            ).pack(pady=20)
            return
        
        # Display users
        for user in users:
            self.create_user_item(user)
    
    def create_user_item(self, user: dict):
        """Create user item"""
        item_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color=THEME["bg_primary"],
            corner_radius=8
        )
        item_frame.pack(fill="x", pady=5)
        
        # User info
        info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)
        
        # Username
        ctk.CTkLabel(
            info_frame,
            text=f"👤 {user['username']}",
            font=("Segoe UI", 14, "bold"),
            text_color=THEME["text_primary"],
            anchor="w"
        ).pack(anchor="w")
        
        # Role
        role_colors = {
            "admin": THEME["error"],
            "internal_dev": THEME["accent"],
            "external_dev": THEME["warning"]
        }
        role_color = role_colors.get(user['role'], THEME["text_secondary"])
        
        ctk.CTkLabel(
            info_frame,
            text=user['role'].replace('_', ' ').title(),
            font=THEME["font_small"],
            text_color=role_color,
            anchor="w"
        ).pack(anchor="w")
        
        # Last login
        last_login = user.get('last_login', 'Never')
        if last_login and last_login != 'Never':
            try:
                dt = datetime.fromisoformat(last_login)
                last_login = dt.strftime("%Y-%m-%d %H:%M")
            except:
                pass
        
        ctk.CTkLabel(
            info_frame,
            text=f"Last login: {last_login}",
            font=THEME["font_small"],
            text_color=THEME["text_dim"],
            anchor="w"
        ).pack(anchor="w")
    
    def approve_mod(self, approval_id: int):
        """Approve mod"""
        # Update approval status
        self.db.update_approval_status(
            approval_id,
            reviewed_by=1,  # TODO: Use actual user ID
            status="approved",
            review_notes="Approved via console"
        )
        
        # Reload approvals
        self.load_approvals()
        
        # Show message
        self.show_message("Mod approved", THEME["success"])
    
    def reject_mod(self, approval_id: int):
        """Reject mod"""
        # Update approval status
        self.db.update_approval_status(
            approval_id,
            reviewed_by=1,  # TODO: Use actual user ID
            status="rejected",
            review_notes="Rejected via console"
        )
        
        # Reload approvals
        self.load_approvals()
        
        # Show message
        self.show_message("Mod rejected", THEME["error"])
    
    def show_message(self, message: str, color: str):
        """Show temporary message"""
        msg_label = ctk.CTkLabel(
            self,
            text=message,
            font=THEME["font_body"],
            text_color=color
        )
        msg_label.place(relx=0.5, rely=0.95, anchor="center")
        self.after(3000, msg_label.destroy)

