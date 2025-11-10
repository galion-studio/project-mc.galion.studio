"""
Sidebar Navigation Component
Modern sidebar with icons and navigation
"""

import customtkinter as ctk
from config import THEME, LAYOUT


class Sidebar(ctk.CTkFrame):
    """
    Sidebar navigation component.
    Simple, clean, effective.
    """
    
    def __init__(self, parent, on_navigate):
        super().__init__(
            parent,
            width=LAYOUT["sidebar_width"],
            fg_color=THEME["card_bg"],
            corner_radius=0
        )
        
        self.on_navigate = on_navigate
        self.active_button = None
        
        # Logo/Title section
        self.title_label = ctk.CTkLabel(
            self,
            text="DEV CONSOLE",
            font=("Segoe UI", 16, "bold"),
            text_color=THEME["accent"]
        )
        self.title_label.pack(pady=30)
        
        # Navigation buttons
        self.nav_buttons = {}
        
        self.create_nav_button("dashboard", "📊 Dashboard", True)
        self.create_nav_button("client_console", "💬 Client Console")
        self.create_nav_button("mods", "📦 Mods")
        self.create_nav_button("server", "🖥️ Server")
        self.create_nav_button("logs", "📜 Logs")
        self.create_nav_button("repository", "🗄️ Repository")
        self.create_nav_button("environments", "🌍 Environments")
        self.create_nav_button("team", "👥 Team")
        self.create_nav_button("snippets", "💡 Snippets")
        self.create_nav_button("builder", "🔨 Builder")
        self.create_nav_button("profiler", "📈 Profiler")
        self.create_nav_button("ai_chat", "🤖 AI Chat")
        
        # Settings button at bottom
        self.spacer = ctk.CTkFrame(self, fg_color="transparent")
        self.spacer.pack(expand=True, fill="both")
        
        self.settings_btn = ctk.CTkButton(
            self,
            text="⚙️ Settings",
            fg_color="transparent",
            text_color=THEME["text_secondary"],
            hover_color=THEME["card_hover"],
            font=THEME["font_body"],
            anchor="w",
            command=lambda: self.on_navigate("settings")
        )
        self.settings_btn.pack(side="bottom", fill="x", padx=10, pady=20)
    
    def create_nav_button(self, key: str, text: str, active: bool = False):
        """Create navigation button"""
        btn = ctk.CTkButton(
            self,
            text=text,
            fg_color=THEME["accent"] if active else "transparent",
            text_color=THEME["text_primary"] if active else THEME["text_secondary"],
            hover_color=THEME["card_hover"],
            font=THEME["font_body"],
            anchor="w",
            height=40,
            command=lambda: self.navigate_to(key)
        )
        btn.pack(fill="x", padx=10, pady=2)
        
        self.nav_buttons[key] = btn
        
        if active:
            self.active_button = btn
    
    def navigate_to(self, key: str):
        """Navigate to section"""
        # Update button states
        if self.active_button:
            self.active_button.configure(
                fg_color="transparent",
                text_color=THEME["text_secondary"]
            )
        
        new_button = self.nav_buttons.get(key)
        if new_button:
            new_button.configure(
                fg_color=THEME["accent"],
                text_color=THEME["text_primary"]
            )
            self.active_button = new_button
        
        # Call navigation callback
        self.on_navigate(key)

