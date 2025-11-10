"""
Dashboard Component
Main dashboard showing overview and key metrics
"""

import customtkinter as ctk
from config import THEME, LAYOUT
from typing import Optional, Callable


class Dashboard(ctk.CTkScrollableFrame):
    """
    Main dashboard with cards showing key information.
    Clean, informative, actionable.
    """
    
    def __init__(self, parent, on_quick_action: Optional[Callable] = None):
        super().__init__(
            parent,
            fg_color=THEME["bg_primary"],
            corner_radius=0
        )
        
        self.on_quick_action = on_quick_action or (lambda x: None)
        
        # Header
        header = ctk.CTkLabel(
            self,
            text="Dashboard",
            font=THEME["font_header"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        header.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        # Quick stats row
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.pack(fill="x", padx=LAYOUT["card_padding"], pady=10)
        
        self.create_stat_card(
            self.stats_frame,
            "Active Mods",
            "0",
            THEME["info"]
        ).pack(side="left", fill="both", expand=True, padx=5)
        
        self.create_stat_card(
            self.stats_frame,
            "Deployments Today",
            "0",
            THEME["success"]
        ).pack(side="left", fill="both", expand=True, padx=5)
        
        self.create_stat_card(
            self.stats_frame,
            "Pending Approvals",
            "0",
            THEME["warning"]
        ).pack(side="left", fill="both", expand=True, padx=5)
        
        self.create_stat_card(
            self.stats_frame,
            "Active Users",
            "1",
            THEME["accent"]
        ).pack(side="left", fill="both", expand=True, padx=5)
        
        # Quick actions section
        actions_header = ctk.CTkLabel(
            self,
            text="Quick Actions",
            font=THEME["font_subheader"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        actions_header.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.pack(fill="x", padx=LAYOUT["card_padding"], pady=10)
        
        self.create_action_button(
            actions_frame,
            "📦 Upload Mod",
            "Upload a new mod to the server",
            lambda: self.on_quick_action("upload_mod")
        ).pack(side="left", fill="both", expand=True, padx=5)
        
        self.create_action_button(
            actions_frame,
            "🖥️ Start Server",
            "Start the development server",
            lambda: self.on_quick_action("start_server")
        ).pack(side="left", fill="both", expand=True, padx=5)
        
        self.create_action_button(
            actions_frame,
            "📜 View Logs",
            "Open real-time log viewer",
            lambda: self.on_quick_action("view_logs")
        ).pack(side="left", fill="both", expand=True, padx=5)
        
        # Recent activity section
        activity_header = ctk.CTkLabel(
            self,
            text="Recent Activity",
            font=THEME["font_subheader"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        activity_header.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        self.activity_card = self.create_card(self)
        self.activity_card.pack(fill="both", expand=True, padx=LAYOUT["card_padding"], pady=10)
        
        self.activity_list = ctk.CTkTextbox(
            self.activity_card,
            fg_color=THEME["bg_primary"],
            text_color=THEME["text_secondary"],
            font=THEME["font_small"],
            height=200
        )
        self.activity_list.pack(fill="both", expand=True, padx=15, pady=15)
        self.activity_list.insert("1.0", "No recent activity")
        self.activity_list.configure(state="disabled")
        
        # Server info section
        info_header = ctk.CTkLabel(
            self,
            text="Server Information",
            font=THEME["font_subheader"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        info_header.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        self.server_info_card = self.create_card(self)
        self.server_info_card.pack(fill="both", padx=LAYOUT["card_padding"], pady=10)
        
        self.server_info_text = ctk.CTkTextbox(
            self.server_info_card,
            fg_color=THEME["bg_primary"],
            text_color=THEME["text_secondary"],
            font=THEME["font_code"],
            height=150
        )
        self.server_info_text.pack(fill="both", expand=True, padx=15, pady=15)
        self.server_info_text.insert("1.0", 
            "Server: Offline\n"
            "Version: Minecraft 1.21.1\n"
            "Port: 25565\n"
            "TPS: --\n"
            "Memory: -- / --"
        )
        self.server_info_text.configure(state="disabled")
    
    def create_card(self, parent) -> ctk.CTkFrame:
        """Create a card frame"""
        return ctk.CTkFrame(
            parent,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
    
    def create_stat_card(self, parent, label: str, value: str, color: str) -> ctk.CTkFrame:
        """Create a statistics card"""
        card = self.create_card(parent)
        
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI", 32, "bold"),
            text_color=color
        )
        value_label.pack(pady=(20, 5))
        
        label_widget = ctk.CTkLabel(
            card,
            text=label,
            font=THEME["font_small"],
            text_color=THEME["text_secondary"]
        )
        label_widget.pack(pady=(0, 20))
        
        return card
    
    def create_action_button(self, parent, title: str, description: str,
                            command: Callable) -> ctk.CTkFrame:
        """Create an action button card"""
        card = self.create_card(parent)
        
        button = ctk.CTkButton(
            card,
            text=title,
            font=THEME["font_body"],
            fg_color=THEME["accent"],
            hover_color=THEME["accent_hover"],
            height=40,
            command=command
        )
        button.pack(pady=(20, 5), padx=20, fill="x")
        
        desc_label = ctk.CTkLabel(
            card,
            text=description,
            font=THEME["font_small"],
            text_color=THEME["text_secondary"],
            wraplength=150
        )
        desc_label.pack(pady=(0, 20), padx=10)
        
        return card
    
    def update_stats(self, active_mods: int, deployments: int,
                    pending_approvals: int, active_users: int):
        """Update dashboard statistics"""
        # This would update the stat cards
        # For now, we'll implement this when we connect to real data
        pass
    
    def add_activity(self, activity: str):
        """Add activity to recent activity list"""
        self.activity_list.configure(state="normal")
        current = self.activity_list.get("1.0", "end-1c")
        if current == "No recent activity":
            self.activity_list.delete("1.0", "end")
        self.activity_list.insert("1.0", f"• {activity}\n")
        self.activity_list.configure(state="disabled")
    
    def update_server_info(self, status: str, tps: Optional[float] = None,
                          memory_used: Optional[int] = None,
                          memory_max: Optional[int] = None):
        """Update server information display"""
        info = f"Server: {status}\n"
        info += "Version: Minecraft 1.21.1\n"
        info += "Port: 25565\n"
        info += f"TPS: {tps if tps else '--'}\n"
        
        if memory_used and memory_max:
            info += f"Memory: {memory_used}MB / {memory_max}MB"
        else:
            info += "Memory: -- / --"
        
        self.server_info_text.configure(state="normal")
        self.server_info_text.delete("1.0", "end")
        self.server_info_text.insert("1.0", info)
        self.server_info_text.configure(state="disabled")

