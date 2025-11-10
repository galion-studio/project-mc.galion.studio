"""
AI Control Center
Complete AI integration: Admin chat + Minecraft monitoring + Auto-responses
"""

import customtkinter as ctk
import asyncio
import threading
from typing import Optional
from datetime import datetime

from config import THEME, LAYOUT, PROJECT_ROOT
from ai.grok_chat import GrokChatPanel
from ai.minecraft_chat_bridge import MinecraftChatBridge


class AIControlCenter(ctk.CTkFrame):
    """
    Complete AI control center.
    Admin chat + Minecraft bridge in one interface.
    """
    
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color=THEME["bg_primary"],
            corner_radius=0
        )
        
        self.bridge = None
        self.bridge_thread = None
        self.bridge_running = False
        
        # Header
        header = ctk.CTkLabel(
            self,
            text="🤖 AI Control Center - Grok 4 Fast",
            font=THEME["font_header"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        header.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        # Create split view
        self.create_split_view()
    
    def create_split_view(self):
        """Create split view with admin chat and MC monitor"""
        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=LAYOUT["card_padding"], pady=10)
        
        # Left side - Admin Chat
        left_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        admin_label = ctk.CTkLabel(
            left_frame,
            text="💬 Admin Chat",
            font=THEME["font_subheader"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        admin_label.pack(fill="x", pady=(0, 10))
        
        self.admin_chat = GrokChatPanel(left_frame)
        self.admin_chat.pack(fill="both", expand=True)
        
        # Right side - Minecraft Monitor
        right_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        right_frame.pack(side="left", fill="both", expand=True, padx=(10, 0))
        
        mc_label = ctk.CTkLabel(
            right_frame,
            text="🎮 Minecraft AI Monitor",
            font=THEME["font_subheader"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        mc_label.pack(fill="x", pady=(0, 10))
        
        self.create_mc_monitor(right_frame)
    
    def create_mc_monitor(self, parent):
        """Create Minecraft monitoring section"""
        # Control card
        control_card = ctk.CTkFrame(
            parent,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        control_card.pack(fill="x", pady=(0, 10))
        
        control_frame = ctk.CTkFrame(control_card, fg_color="transparent")
        control_frame.pack(fill="x", padx=20, pady=15)
        
        # Status
        self.mc_status_label = ctk.CTkLabel(
            control_frame,
            text="● Stopped",
            font=THEME["font_body"],
            text_color=THEME["error"]
        )
        self.mc_status_label.pack(side="left")
        
        # Trigger word
        ctk.CTkLabel(
            control_frame,
            text="Trigger:",
            font=THEME["font_small"],
            text_color=THEME["text_secondary"]
        ).pack(side="left", padx=(20, 5))
        
        self.trigger_entry = ctk.CTkEntry(
            control_frame,
            width=100,
            font=THEME["font_code"]
        )
        self.trigger_entry.insert(0, "ai")
        self.trigger_entry.pack(side="left", padx=(0, 20))
        
        # Start/Stop button
        self.bridge_btn = ctk.CTkButton(
            control_frame,
            text="▶️ Start Bridge",
            width=120,
            fg_color=THEME["success"],
            hover_color="#00c993",
            command=self.toggle_bridge
        )
        self.bridge_btn.pack(side="right")
        
        # Activity log
        log_card = ctk.CTkFrame(
            parent,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        log_card.pack(fill="both", expand=True)
        
        self.mc_log = ctk.CTkTextbox(
            log_card,
            fg_color=THEME["bg_primary"],
            text_color=THEME["text_primary"],
            font=THEME["font_code"]
        )
        self.mc_log.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.mc_log.insert("1.0",
            "Minecraft AI Bridge\n"
            "===================\n\n"
            "Click 'Start Bridge' to monitor Minecraft chat.\n\n"
            "Players can trigger AI by typing:\n"
            "  ai <question>\n\n"
            "Example:\n"
            "  ai what is redstone?\n"
            "  ai how do I make a piston?\n\n"
            "The AI will respond in Minecraft chat automatically!\n"
        )
        self.mc_log.configure(state="disabled")
    
    def toggle_bridge(self):
        """Start or stop the bridge"""
        if self.bridge_running:
            self.stop_bridge()
        else:
            self.start_bridge()
    
    def start_bridge(self):
        """Start Minecraft chat bridge"""
        # Check if admin chat has Grok connected
        if not self.admin_chat.grok_client:
            self.log_mc("[ERROR] Connect to Grok first in Admin Chat!\n")
            return
        
        trigger = self.trigger_entry.get().strip()
        if not trigger:
            trigger = "ai"
        
        self.log_mc(f"[STARTING] Bridge with trigger '{trigger}'...\n")
        
        # Create bridge
        self.bridge = MinecraftChatBridge(
            self.admin_chat.grok_client,
            trigger_word=trigger
        )
        
        # Set callback for activity logging
        self.bridge.set_message_callback(self.log_mc)
        
        # Start bridge in thread
        self.bridge_running = True
        self.bridge_thread = threading.Thread(
            target=self._run_bridge,
            daemon=True
        )
        self.bridge_thread.start()
        
        # Update UI
        self.mc_status_label.configure(
            text=f"● Running (trigger: {trigger})",
            text_color=THEME["success"]
        )
        self.bridge_btn.configure(
            text="⏹️ Stop Bridge",
            fg_color=THEME["error"]
        )
        
        self.log_mc(f"[OK] Bridge started! Players can type: {trigger} <question>\n")
    
    def stop_bridge(self):
        """Stop Minecraft chat bridge"""
        if self.bridge:
            self.bridge.stop()
        
        self.bridge_running = False
        
        # Update UI
        self.mc_status_label.configure(
            text="● Stopped",
            text_color=THEME["error"]
        )
        self.bridge_btn.configure(
            text="▶️ Start Bridge",
            fg_color=THEME["success"]
        )
        
        self.log_mc("[STOPPED] Bridge stopped\n")
    
    def _run_bridge(self):
        """Run bridge in thread"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(self.bridge.start())
        except Exception as e:
            self.log_mc(f"[ERROR] Bridge error: {e}\n")
        finally:
            loop.close()
    
    def log_mc(self, message: str):
        """Log message to Minecraft monitor"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        def update():
            self.mc_log.configure(state="normal")
            self.mc_log.insert("end", f"[{timestamp}] {message}\n")
            self.mc_log.see("end")
            self.mc_log.configure(state="disabled")
        
        self.after(0, update)

