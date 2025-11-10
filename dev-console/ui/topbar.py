"""
Top Bar Component
Status bar showing server status, environment, and user info
"""

import customtkinter as ctk
from config import THEME, LAYOUT, ENVIRONMENTS
from typing import Optional


class TopBar(ctk.CTkFrame):
    """
    Top status bar component.
    Shows critical information at a glance.
    """
    
    def __init__(self, parent, user_name: str = "Admin", user_role: str = "admin"):
        super().__init__(
            parent,
            height=LAYOUT["topbar_height"],
            fg_color=THEME["card_bg"],
            corner_radius=0
        )
        
        self.user_name = user_name
        self.user_role = user_role
        self.current_environment = "dev"
        
        # Left side - Server status
        self.status_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.status_frame.pack(side="left", padx=20)
        
        self.server_status_label = ctk.CTkLabel(
            self.status_frame,
            text="● OFFLINE",
            font=THEME["font_body"],
            text_color=THEME["error"]
        )
        self.server_status_label.pack(side="left", padx=5)
        
        self.player_count_label = ctk.CTkLabel(
            self.status_frame,
            text="0 players",
            font=THEME["font_small"],
            text_color=THEME["text_secondary"]
        )
        self.player_count_label.pack(side="left", padx=10)
        
        # Center - Environment selector
        self.env_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.env_frame.pack(side="left", expand=True)
        
        ctk.CTkLabel(
            self.env_frame,
            text="Environment:",
            font=THEME["font_small"],
            text_color=THEME["text_secondary"]
        ).pack(side="left", padx=5)
        
        self.environment_menu = ctk.CTkOptionMenu(
            self.env_frame,
            values=["Development", "Staging", "Production"],
            command=self.on_environment_change,
            fg_color=THEME["accent"],
            button_color=THEME["accent"],
            button_hover_color=THEME["accent_hover"],
            font=THEME["font_body"]
        )
        self.environment_menu.set("Development")
        self.environment_menu.pack(side="left", padx=5)
        
        # Right side - User info
        self.user_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.user_frame.pack(side="right", padx=20)
        
        self.user_role_label = ctk.CTkLabel(
            self.user_frame,
            text=self.format_role(user_role),
            font=THEME["font_small"],
            text_color=THEME["text_secondary"]
        )
        self.user_role_label.pack(side="right", padx=5)
        
        self.user_name_label = ctk.CTkLabel(
            self.user_frame,
            text=f"👤 {user_name}",
            font=THEME["font_body"],
            text_color=THEME["text_primary"]
        )
        self.user_name_label.pack(side="right", padx=5)
    
    def format_role(self, role: str) -> str:
        """Format role name for display"""
        role_names = {
            "admin": "Administrator",
            "internal_dev": "Internal Dev",
            "external_dev": "External Dev"
        }
        return role_names.get(role, role)
    
    def update_server_status(self, online: bool, player_count: int = 0):
        """Update server status display"""
        if online:
            self.server_status_label.configure(
                text="● ONLINE",
                text_color=THEME["success"]
            )
            self.player_count_label.configure(
                text=f"{player_count} players"
            )
        else:
            self.server_status_label.configure(
                text="● OFFLINE",
                text_color=THEME["error"]
            )
            self.player_count_label.configure(
                text="0 players"
            )
    
    def on_environment_change(self, choice: str):
        """Handle environment change"""
        # Map display name to internal key
        env_map = {
            "Development": "dev",
            "Staging": "staging",
            "Production": "prod"
        }
        self.current_environment = env_map.get(choice, "dev")
        
        # Update environment indicator color
        env_color = ENVIRONMENTS[self.current_environment]["color"]
        self.environment_menu.configure(
            fg_color=env_color,
            button_color=env_color
        )
    
    def get_current_environment(self) -> str:
        """Get current selected environment"""
        return self.current_environment

