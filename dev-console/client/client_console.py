"""
Client Console
Real-time console for interacting with Minecraft server
"""

import customtkinter as ctk
from typing import Optional
import threading
import time

from config import THEME, LAYOUT, RCON_HOST, RCON_PORT, RCON_PASSWORD


class ClientConsole(ctk.CTkFrame):
    """
    Interactive Minecraft server console.
    Send commands, view responses, control server.
    """
    
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color=THEME["bg_primary"],
            corner_radius=0
        )
        
        self.command_history = []
        self.history_index = -1
        
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        header = ctk.CTkLabel(
            header_frame,
            text="💬 Server Console",
            font=THEME["font_header"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        header.pack(side="left")
        
        # Connection status
        self.status_indicator = ctk.CTkLabel(
            header_frame,
            text="● Checking...",
            font=THEME["font_body"],
            text_color=THEME["warning"]
        )
        self.status_indicator.pack(side="right", padx=10)
        
        # Quick commands bar
        self.create_quick_commands()
        
        # Console output
        self.create_console_output()
        
        # Command input
        self.create_command_input()
        
        # Check connection
        self.check_connection()
    
    def create_quick_commands(self):
        """Create quick command buttons"""
        quick_frame = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        quick_frame.pack(fill="x", padx=LAYOUT["card_padding"], pady=(0, 10))
        
        label = ctk.CTkLabel(
            quick_frame,
            text="Quick Commands:",
            font=THEME["font_body"],
            text_color=THEME["text_secondary"]
        )
        label.pack(side="left", padx=(20, 10), pady=15)
        
        commands = [
            ("📊 TPS", "tps"),
            ("👥 Players", "list"),
            ("💾 Save", "save-all"),
            ("☀️ Day", "time set day"),
            ("🌙 Night", "time set night"),
            ("☁️ Clear", "weather clear"),
        ]
        
        for label_text, command in commands:
            btn = ctk.CTkButton(
                quick_frame,
                text=label_text,
                width=90,
                height=35,
                fg_color=THEME["accent"],
                hover_color=THEME["accent_hover"],
                font=("Segoe UI", 11),
                command=lambda c=command: self.send_quick_command(c)
            )
            btn.pack(side="left", padx=3, pady=15)
    
    def create_console_output(self):
        """Create console output area"""
        output_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        output_card.pack(fill="both", expand=True, padx=LAYOUT["card_padding"], pady=(0, 10))
        
        # Console text
        self.console_text = ctk.CTkTextbox(
            output_card,
            fg_color="#000000",
            text_color="#00ff00",
            font=("Consolas", 12),
            wrap="word"
        )
        self.console_text.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Welcome message
        self.log_console(
            "╔════════════════════════════════════════════════════╗\n"
            "║   GALION MINECRAFT SERVER CONSOLE                 ║\n"
            "║   Ready to execute commands                       ║\n"
            "╚════════════════════════════════════════════════════╝\n\n"
        )
    
    def create_command_input(self):
        """Create command input area"""
        input_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"],
            height=80
        )
        input_card.pack(fill="x", padx=LAYOUT["card_padding"], pady=(0, 10))
        input_card.pack_propagate(False)
        
        input_frame = ctk.CTkFrame(input_card, fg_color="transparent")
        input_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Prompt label
        prompt = ctk.CTkLabel(
            input_frame,
            text=">",
            font=("Consolas", 16, "bold"),
            text_color=THEME["accent"]
        )
        prompt.pack(side="left", padx=(0, 10))
        
        # Command entry
        self.command_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter server command...",
            font=("Consolas", 13),
            height=45
        )
        self.command_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.command_entry.bind("<Return>", lambda e: self.send_command())
        self.command_entry.bind("<Up>", self.history_up)
        self.command_entry.bind("<Down>", self.history_down)
        
        # Send button
        self.send_btn = ctk.CTkButton(
            input_frame,
            text="Execute",
            width=100,
            height=45,
            fg_color=THEME["success"],
            hover_color="#00c993",
            font=("Segoe UI", 12, "bold"),
            command=self.send_command
        )
        self.send_btn.pack(side="left")
    
    def check_connection(self):
        """Check RCON connection"""
        thread = threading.Thread(target=self._check_connection_thread, daemon=True)
        thread.start()
    
    def _check_connection_thread(self):
        """Check connection in background"""
        try:
            from mcrcon import MCRcon
            
            with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT, timeout=2) as mcr:
                response = mcr.command("list")
                
                # Success
                self.after(0, lambda: self.status_indicator.configure(
                    text="● Connected",
                    text_color=THEME["success"]
                ))
                self.after(0, lambda: self.log_console(f"[SYSTEM] Connected to server\n"))
        
        except Exception as e:
            self.after(0, lambda: self.status_indicator.configure(
                text="● Disconnected",
                text_color=THEME["error"]
            ))
            self.after(0, lambda: self.log_console(
                f"[ERROR] Connection failed: {str(e)}\n"
                "[INFO] Enable RCON in server.properties to use console\n\n"
            ))
    
    def send_command(self):
        """Send command to server"""
        command = self.command_entry.get().strip()
        
        if not command:
            return
        
        # Add to history
        self.command_history.append(command)
        self.history_index = -1
        
        # Clear input
        self.command_entry.delete(0, "end")
        
        # Log command
        self.log_console(f"> {command}\n", color="#ffff00")
        
        # Send to server
        thread = threading.Thread(target=self._send_command_thread, args=(command,), daemon=True)
        thread.start()
    
    def send_quick_command(self, command: str):
        """Send quick command"""
        self.command_entry.delete(0, "end")
        self.command_entry.insert(0, command)
        self.send_command()
    
    def _send_command_thread(self, command: str):
        """Send command in background"""
        try:
            from mcrcon import MCRcon
            
            with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT, timeout=5) as mcr:
                response = mcr.command(command)
                
                # Log response
                if response:
                    self.after(0, lambda: self.log_console(f"{response}\n\n"))
                else:
                    self.after(0, lambda: self.log_console("[OK] Command executed\n\n"))
        
        except Exception as e:
            self.after(0, lambda: self.log_console(
                f"[ERROR] Failed to execute: {str(e)}\n\n",
                color="#ff0000"
            ))
    
    def history_up(self, event):
        """Navigate command history up"""
        if not self.command_history:
            return
        
        if self.history_index == -1:
            self.history_index = len(self.command_history) - 1
        elif self.history_index > 0:
            self.history_index -= 1
        
        self.command_entry.delete(0, "end")
        self.command_entry.insert(0, self.command_history[self.history_index])
    
    def history_down(self, event):
        """Navigate command history down"""
        if not self.command_history or self.history_index == -1:
            return
        
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.command_entry.delete(0, "end")
            self.command_entry.insert(0, self.command_history[self.history_index])
        else:
            self.history_index = -1
            self.command_entry.delete(0, "end")
    
    def log_console(self, text: str, color: Optional[str] = None):
        """Log text to console"""
        self.console_text.insert("end", text)
        self.console_text.see("end")
