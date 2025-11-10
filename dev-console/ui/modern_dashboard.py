"""
Modern Dashboard with Perfect Grid Layout
Pristine, intuitive, professional design
"""

import customtkinter as ctk
from typing import Callable
from config import THEME, LAYOUT


class ModernDashboard(ctk.CTkFrame):
    """
    Professional dashboard with grid layout.
    Perfect spacing. Clean design. Intuitive UX.
    """
    
    def __init__(self, parent, on_action: Callable):
        super().__init__(
            parent,
            fg_color=THEME["bg_primary"],
            corner_radius=0
        )
        
        self.on_action = on_action
        
        # Configure grid
        self.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="col")
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=0)  # Stats
        self.grid_rowconfigure(2, weight=0)  # Actions
        self.grid_rowconfigure(3, weight=1)  # Activity
        
        # Header
        self.create_header()
        
        # Stats cards row
        self.create_stats_row()
        
        # Quick actions grid
        self.create_actions_grid()
        
        # Recent activity
        self.create_activity_section()
    
    def create_header(self):
        """Create header section"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent", height=80)
        header_frame.grid(row=0, column=0, columnspan=4, sticky="ew", padx=30, pady=(30, 20))
        header_frame.grid_propagate(False)
        
        # Title
        title = ctk.CTkLabel(
            header_frame,
            text="⚡ Development Dashboard",
            font=("Segoe UI", 32, "bold"),
            text_color=THEME["text_primary"]
        )
        title.pack(side="left", anchor="w")
        
        # Subtitle
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Galion.Studio Minecraft Server",
            font=("Segoe UI", 14),
            text_color=THEME["text_secondary"]
        )
        subtitle.pack(side="left", anchor="w", padx=(20, 0))
    
    def create_stats_row(self):
        """Create statistics cards row"""
        stats_data = [
            ("Active Mods", "0", "📦", THEME["info"]),
            ("Deployments Today", "0", "🚀", THEME["success"]),
            ("Server Status", "Online", "🖥️", THEME["success"]),
            ("Active Users", "1", "👥", THEME["accent"]),
        ]
        
        for idx, (label, value, icon, color) in enumerate(stats_data):
            card = self.create_stat_card(label, value, icon, color)
            card.grid(row=1, column=idx, sticky="ew", padx=15, pady=15)
    
    def create_stat_card(self, label: str, value: str, icon: str, color: str):
        """Create modern stat card"""
        card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=16,
            height=140
        )
        card.grid_propagate(False)
        
        # Icon at top
        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=("Segoe UI", 36),
            text_color=color
        )
        icon_label.pack(pady=(25, 10))
        
        # Value
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI", 28, "bold"),
            text_color=THEME["text_primary"]
        )
        value_label.pack(pady=(0, 5))
        
        # Label
        label_widget = ctk.CTkLabel(
            card,
            text=label,
            font=("Segoe UI", 12),
            text_color=THEME["text_secondary"]
        )
        label_widget.pack(pady=(0, 20))
        
        return card
    
    def create_actions_grid(self):
        """Create quick actions grid with perfect spacing"""
        # Section label
        actions_label = ctk.CTkLabel(
            self,
            text="⚡ Quick Actions",
            font=("Segoe UI", 22, "bold"),
            text_color=THEME["text_primary"]
        )
        actions_label.grid(row=2, column=0, columnspan=4, sticky="w", padx=30, pady=(30, 20))
        
        # Grid of action cards (2 rows x 4 columns = 8 actions)
        actions = [
            ("📦", "Upload Mod", "Upload new mod to server", "upload_mod"),
            ("🖥️", "Start Server", "Start Minecraft server", "start_server"),
            ("📜", "View Logs", "Real-time log viewer", "view_logs"),
            ("🎮", "Launch Client", "Start game client", "launch_client"),
            ("🤖", "AI Chat", "Chat with Grok 4 Fast", "ai_chat"),
            ("🔨", "Build Mod", "Compile with Gradle", "build_mod"),
            ("💬", "Console", "Execute RCON commands", "console"),
            ("📈", "Profiler", "Monitor performance", "profiler"),
        ]
        
        # Create cards in grid
        for idx, (icon, title, description, action) in enumerate(actions):
            row = 3 + (idx // 4)
            col = idx % 4
            
            card = self.create_action_card(icon, title, description, action)
            card.grid(row=row, column=col, sticky="nsew", padx=15, pady=15)
    
    def create_action_card(self, icon: str, title: str, description: str, action: str):
        """Create action card with perfect click area"""
        card = ctk.CTkButton(
            self,
            text="",
            fg_color=THEME["card_bg"],
            hover_color=THEME["accent"],
            corner_radius=16,
            height=160,
            command=lambda: self.on_action(action),
            cursor="hand2"
        )
        
        # Content frame
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.place(relx=0.5, rely=0.5, anchor="center")
        
        # Icon
        icon_label = ctk.CTkLabel(
            content,
            text=icon,
            font=("Segoe UI", 48),
            text_color=THEME["accent"]
        )
        icon_label.pack(pady=(0, 15))
        
        # Title
        title_label = ctk.CTkLabel(
            content,
            text=title,
            font=("Segoe UI", 16, "bold"),
            text_color=THEME["text_primary"]
        )
        title_label.pack(pady=(0, 8))
        
        # Description
        desc_label = ctk.CTkLabel(
            content,
            text=description,
            font=("Segoe UI", 11),
            text_color=THEME["text_secondary"],
            wraplength=200
        )
        desc_label.pack()
        
        return card
    
    def create_activity_section(self):
        """Create activity section at bottom"""
        # Section label
        activity_label = ctk.CTkLabel(
            self,
            text="📊 Recent Activity",
            font=("Segoe UI", 22, "bold"),
            text_color=THEME["text_primary"]
        )
        activity_label.grid(row=5, column=0, columnspan=4, sticky="w", padx=30, pady=(30, 20))
        
        # Activity card
        activity_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=16
        )
        activity_card.grid(row=6, column=0, columnspan=4, sticky="nsew", padx=30, pady=(0, 30))
        
        # Activity text
        activity_text = ctk.CTkTextbox(
            activity_card,
            fg_color=THEME["bg_primary"],
            text_color=THEME["text_secondary"],
            font=("Segoe UI", 12),
            height=120
        )
        activity_text.pack(fill="both", expand=True, padx=20, pady=20)
        activity_text.insert("1.0", "• Console started\n• Ready for development")
        activity_text.configure(state="disabled")
