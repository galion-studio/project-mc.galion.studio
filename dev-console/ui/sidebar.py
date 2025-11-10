"""
Modern Sidebar Navigation Component
Clean, minimal, elegant navigation with icons
"""

import customtkinter as ctk
from config import THEME, LAYOUT


class Sidebar(ctk.CTkFrame):
    """
    Modern sidebar navigation.
    Ultra-clean design with smooth animations.
    """
    
    def __init__(self, parent, on_navigate):
        super().__init__(
            parent,
            width=LAYOUT["sidebar_width"],
            fg_color=THEME["bg_secondary"],
            corner_radius=0
        )
        
        self.on_navigate = on_navigate
        self.active_button = None
        
        # Logo section with modern design
        logo_frame = ctk.CTkFrame(self, fg_color="transparent", height=80)
        logo_frame.pack(fill="x", pady=(20, 30))
        logo_frame.pack_propagate(False)
        
        logo_icon = ctk.CTkLabel(
            logo_frame,
            text="⚡",
            font=("Segoe UI", 32),
            text_color=THEME["accent"]
        )
        logo_icon.pack(pady=(10, 5))
        
        logo_text = ctk.CTkLabel(
            logo_frame,
            text="GALION",
            font=("Segoe UI", 14, "bold"),
            text_color=THEME["text_primary"]
        )
        logo_text.pack()
        
        # Separator
        separator = ctk.CTkFrame(self, fg_color=THEME["border"], height=1)
        separator.pack(fill="x", padx=15, pady=(0, 20))
        
        # Navigation sections
        self.nav_buttons = {}
        
        # Main section
        self.create_section_label("MAIN")
        self.create_nav_button("dashboard", "📊", "Dashboard", True)
        self.create_nav_button("client_console", "💬", "Console")
        
        # Development section
        self.create_section_label("DEVELOPMENT")
        self.create_nav_button("mods", "📦", "Mods")
        self.create_nav_button("server", "🖥️", "Server")
        self.create_nav_button("logs", "📜", "Logs")
        self.create_nav_button("builder", "🔨", "Builder")
        
        # Tools section
        self.create_section_label("TOOLS")
        self.create_nav_button("ai_chat", "🤖", "AI Chat")
        self.create_nav_button("snippets", "💡", "Snippets")
        self.create_nav_button("profiler", "📈", "Profiler")
        
        # Advanced section
        self.create_section_label("ADVANCED")
        self.create_nav_button("repository", "🗄️", "Repository")
        self.create_nav_button("environments", "🌍", "Environments")
        self.create_nav_button("team", "👥", "Team")
        
        # Spacer
        spacer = ctk.CTkFrame(self, fg_color="transparent")
        spacer.pack(expand=True, fill="both")
        
        # Bottom separator
        separator2 = ctk.CTkFrame(self, fg_color=THEME["border"], height=1)
        separator2.pack(fill="x", padx=15, pady=(0, 15))
        
        # Settings button at bottom with special styling
        self.settings_btn = self.create_special_button("⚙️", "Settings")
        self.settings_btn.pack(fill="x", padx=10, pady=(0, 20))
    
    def create_section_label(self, text: str):
        """Create section label"""
        label = ctk.CTkLabel(
            self,
            text=text,
            font=("Segoe UI", 10, "bold"),
            text_color=THEME["text_dim"],
            anchor="w"
        )
        label.pack(fill="x", padx=20, pady=(15, 8))
    
    def create_nav_button(self, key: str, icon: str, label: str, active: bool = False):
        """Create modern navigation button with icon and label"""
        # Button container
        btn_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        btn_frame.pack(fill="x", padx=10, pady=1)
        
        btn = ctk.CTkButton(
            btn_frame,
            text="",
            fg_color=THEME["accent"] if active else "transparent",
            hover_color=THEME["accent"] if not active else THEME["accent_hover"],
            corner_radius=8,
            height=42,
            width=180,
            command=lambda: self.navigate_to(key),
            anchor="w"
        )
        btn.pack(fill="x")
        
        # Custom content with icon and text
        content_frame = ctk.CTkFrame(btn, fg_color="transparent")
        content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Icon
        icon_label = ctk.CTkLabel(
            content_frame,
            text=icon,
            font=("Segoe UI", 16),
            text_color=THEME["text_primary"]
        )
        icon_label.pack(side="left", padx=(10, 10))
        
        # Label text
        text_label = ctk.CTkLabel(
            content_frame,
            text=label,
            font=("Segoe UI", 13),
            text_color=THEME["text_primary"] if active else THEME["text_secondary"]
        )
        text_label.pack(side="left")
        
        # Store references
        self.nav_buttons[key] = {
            "button": btn,
            "icon": icon_label,
            "text": text_label
        }
        
        if active:
            self.active_button = key
    
    def create_special_button(self, icon: str, label: str):
        """Create special button (for settings)"""
        btn = ctk.CTkButton(
            self,
            text="",
            fg_color=THEME["card_bg"],
            hover_color=THEME["card_hover"],
            corner_radius=8,
            height=50,
            command=lambda: self.navigate_to("settings"),
            anchor="w"
        )
        
        # Custom content
        content_frame = ctk.CTkFrame(btn, fg_color="transparent")
        content_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        icon_label = ctk.CTkLabel(
            content_frame,
            text=icon,
            font=("Segoe UI", 18),
            text_color=THEME["accent"]
        )
        icon_label.pack(side="left", padx=(10, 10))
        
        text_label = ctk.CTkLabel(
            content_frame,
            text=label,
            font=("Segoe UI", 13, "bold"),
            text_color=THEME["text_primary"]
        )
        text_label.pack(side="left")
        
        return btn
    
    def navigate_to(self, key: str):
        """Navigate to section with smooth state updates"""
        # Update previous active button
        if self.active_button and self.active_button in self.nav_buttons:
            prev_btn_data = self.nav_buttons[self.active_button]
            prev_btn_data["button"].configure(fg_color="transparent")
            prev_btn_data["text"].configure(text_color=THEME["text_secondary"])
        
        # Update new active button
        if key in self.nav_buttons:
            btn_data = self.nav_buttons[key]
            btn_data["button"].configure(fg_color=THEME["accent"])
            btn_data["text"].configure(text_color=THEME["text_primary"])
            self.active_button = key
        
        # Call navigation callback
        self.on_navigate(key)

