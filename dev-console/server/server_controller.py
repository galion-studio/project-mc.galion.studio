"""
Server Controller Component
Start, stop, restart, and monitor server status
"""

import customtkinter as ctk
import subprocess
import threading
import socket
from pathlib import Path
from typing import Optional, Callable
import time

from config import THEME, LAYOUT, MINECRAFT_SERVER_PORT, PROJECT_ROOT
from database.db_manager import DatabaseManager


class ServerController(ctk.CTkScrollableFrame):
    """
    Server control panel.
    Simple, powerful, intuitive.
    """
    
    def __init__(self, parent, db: DatabaseManager, on_status_change: Optional[Callable] = None):
        super().__init__(
            parent,
            fg_color=THEME["bg_primary"],
            corner_radius=0
        )
        
        self.db = db
        self.on_status_change = on_status_change
        self.server_process = None
        self.status_checking = False
        
        # Header
        header = ctk.CTkLabel(
            self,
            text="🖥️ Server Control",
            font=THEME["font_header"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        header.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        # Server status card
        self.create_status_card()
        
        # Control buttons card
        self.create_control_card()
        
        # Server info card
        self.create_info_card()
        
        # Start status checking
        self.start_status_checking()
    
    def create_status_card(self):
        """Create server status display"""
        status_label = ctk.CTkLabel(
            self,
            text="Server Status",
            font=THEME["font_subheader"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        status_label.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        self.status_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        self.status_card.pack(fill="x", padx=LAYOUT["card_padding"], pady=10)
        
        # Status indicator
        self.status_indicator = ctk.CTkFrame(
            self.status_card,
            fg_color=THEME["error"],
            width=20,
            height=20,
            corner_radius=10
        )
        self.status_indicator.pack(side="left", padx=20, pady=20)
        
        # Status text
        status_text_frame = ctk.CTkFrame(self.status_card, fg_color="transparent")
        status_text_frame.pack(side="left", fill="both", expand=True, pady=20)
        
        self.status_text = ctk.CTkLabel(
            status_text_frame,
            text="OFFLINE",
            font=("Segoe UI", 24, "bold"),
            text_color=THEME["error"],
            anchor="w"
        )
        self.status_text.pack(anchor="w")
        
        self.status_details = ctk.CTkLabel(
            status_text_frame,
            text="Server is not running",
            font=THEME["font_body"],
            text_color=THEME["text_secondary"],
            anchor="w"
        )
        self.status_details.pack(anchor="w")
    
    def create_control_card(self):
        """Create control buttons"""
        control_label = ctk.CTkLabel(
            self,
            text="Controls",
            font=THEME["font_subheader"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        control_label.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        self.control_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        self.control_card.pack(fill="x", padx=LAYOUT["card_padding"], pady=10)
        
        buttons_frame = ctk.CTkFrame(self.control_card, fg_color="transparent")
        buttons_frame.pack(pady=20, padx=20, fill="x")
        
        # Start button
        self.start_btn = ctk.CTkButton(
            buttons_frame,
            text="▶️ START SERVER",
            font=THEME["font_body"],
            fg_color=THEME["success"],
            hover_color="#00c993",
            height=50,
            command=self.start_server
        )
        self.start_btn.pack(side="left", fill="x", expand=True, padx=5)
        
        # Stop button
        self.stop_btn = ctk.CTkButton(
            buttons_frame,
            text="⏹️ STOP SERVER",
            font=THEME["font_body"],
            fg_color=THEME["error"],
            hover_color="#cc4444",
            height=50,
            state="disabled",
            command=self.stop_server
        )
        self.stop_btn.pack(side="left", fill="x", expand=True, padx=5)
        
        # Restart button
        self.restart_btn = ctk.CTkButton(
            buttons_frame,
            text="🔄 RESTART SERVER",
            font=THEME["font_body"],
            fg_color=THEME["warning"],
            hover_color="#ff9937",
            height=50,
            state="disabled",
            command=self.restart_server
        )
        self.restart_btn.pack(side="left", fill="x", expand=True, padx=5)
        
        # Status message
        self.control_status = ctk.CTkLabel(
            self.control_card,
            text="",
            font=THEME["font_small"],
            text_color=THEME["text_secondary"]
        )
        self.control_status.pack(pady=(0, 20))
    
    def create_info_card(self):
        """Create server info display"""
        info_label = ctk.CTkLabel(
            self,
            text="Server Information",
            font=THEME["font_subheader"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        info_label.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        self.info_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        self.info_card.pack(fill="both", expand=True, padx=LAYOUT["card_padding"], pady=10)
        
        self.info_text = ctk.CTkTextbox(
            self.info_card,
            fg_color=THEME["bg_primary"],
            text_color=THEME["text_secondary"],
            font=THEME["font_code"],
            height=200
        )
        self.info_text.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.update_server_info()
    
    def start_server(self):
        """Start the Minecraft server"""
        self.control_status.configure(
            text="Starting server...",
            text_color=THEME["info"]
        )
        
        # Disable start button
        self.start_btn.configure(state="disabled")
        
        # Start server in thread
        thread = threading.Thread(target=self._start_server_thread, daemon=True)
        thread.start()
    
    def _start_server_thread(self):
        """Start server thread"""
        try:
            # Look for start script
            start_script = PROJECT_ROOT / "START-SERVER.cmd"
            
            if not start_script.exists():
                # Fallback - try to start directly
                self.after(0, lambda: self.control_status.configure(
                    text="❌ START-SERVER.cmd not found",
                    text_color=THEME["error"]
                ))
                self.after(0, lambda: self.start_btn.configure(state="normal"))
                return
            
            # Execute start script
            # Note: This won't block, just launches the script
            subprocess.Popen(
                [str(start_script)],
                cwd=str(PROJECT_ROOT),
                shell=True
            )
            
            # Wait a bit for server to start
            time.sleep(3)
            
            self.after(0, lambda: self.control_status.configure(
                text="✓ Server start command executed",
                text_color=THEME["success"]
            ))
            
            # Enable stop and restart buttons
            self.after(0, lambda: self.stop_btn.configure(state="normal"))
            self.after(0, lambda: self.restart_btn.configure(state="normal"))
            
        except Exception as e:
            self.after(0, lambda: self.control_status.configure(
                text=f"❌ Error: {str(e)}",
                text_color=THEME["error"]
            ))
            self.after(0, lambda: self.start_btn.configure(state="normal"))
    
    def stop_server(self):
        """Stop the Minecraft server"""
        self.control_status.configure(
            text="Stopping server...",
            text_color=THEME["warning"]
        )
        
        # Disable stop button
        self.stop_btn.configure(state="disabled")
        self.restart_btn.configure(state="disabled")
        
        # Stop server in thread
        thread = threading.Thread(target=self._stop_server_thread, daemon=True)
        thread.start()
    
    def _stop_server_thread(self):
        """Stop server thread"""
        try:
            # Look for stop script
            stop_script = PROJECT_ROOT / "STOP-SERVER.cmd"
            
            if stop_script.exists():
                subprocess.run(
                    [str(stop_script)],
                    cwd=str(PROJECT_ROOT),
                    shell=True
                )
            
            # Wait for server to stop
            time.sleep(2)
            
            self.after(0, lambda: self.control_status.configure(
                text="✓ Server stopped",
                text_color=THEME["success"]
            ))
            
            # Enable start button
            self.after(0, lambda: self.start_btn.configure(state="normal"))
            
        except Exception as e:
            self.after(0, lambda: self.control_status.configure(
                text=f"❌ Error: {str(e)}",
                text_color=THEME["error"]
            ))
    
    def restart_server(self):
        """Restart the Minecraft server"""
        self.control_status.configure(
            text="Restarting server...",
            text_color=THEME["info"]
        )
        
        # Disable buttons
        self.stop_btn.configure(state="disabled")
        self.restart_btn.configure(state="disabled")
        self.start_btn.configure(state="disabled")
        
        # Restart in thread
        thread = threading.Thread(target=self._restart_server_thread, daemon=True)
        thread.start()
    
    def _restart_server_thread(self):
        """Restart server thread"""
        try:
            # Stop server
            stop_script = PROJECT_ROOT / "STOP-SERVER.cmd"
            if stop_script.exists():
                subprocess.run([str(stop_script)], cwd=str(PROJECT_ROOT), shell=True)
            
            time.sleep(3)
            
            # Start server
            start_script = PROJECT_ROOT / "START-SERVER.cmd"
            if start_script.exists():
                subprocess.Popen([str(start_script)], cwd=str(PROJECT_ROOT), shell=True)
            
            time.sleep(3)
            
            self.after(0, lambda: self.control_status.configure(
                text="✓ Server restarted",
                text_color=THEME["success"]
            ))
            
            # Enable buttons
            self.after(0, lambda: self.stop_btn.configure(state="normal"))
            self.after(0, lambda: self.restart_btn.configure(state="normal"))
            
        except Exception as e:
            self.after(0, lambda: self.control_status.configure(
                text=f"❌ Error: {str(e)}",
                text_color=THEME["error"]
            ))
            self.after(0, lambda: self.start_btn.configure(state="normal"))
    
    def start_status_checking(self):
        """Start background status checking"""
        if not self.status_checking:
            self.status_checking = True
            self._check_status_loop()
    
    def _check_status_loop(self):
        """Status checking loop"""
        if not self.status_checking:
            return
        
        # Check server status
        is_online = self.check_server_online()
        
        # Update UI
        if is_online:
            self.status_indicator.configure(fg_color=THEME["success"])
            self.status_text.configure(
                text="ONLINE",
                text_color=THEME["success"]
            )
            self.status_details.configure(
                text=f"Server is running on port {MINECRAFT_SERVER_PORT}"
            )
            
            # Update topbar if callback provided
            if self.on_status_change:
                self.on_status_change(True, 0)  # TODO: Get actual player count
            
            # Enable stop/restart, disable start
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            self.restart_btn.configure(state="normal")
        else:
            self.status_indicator.configure(fg_color=THEME["error"])
            self.status_text.configure(
                text="OFFLINE",
                text_color=THEME["error"]
            )
            self.status_details.configure(
                text="Server is not running"
            )
            
            # Update topbar if callback provided
            if self.on_status_change:
                self.on_status_change(False, 0)
            
            # Enable start, disable stop/restart
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")
            self.restart_btn.configure(state="disabled")
        
        # Check again in 5 seconds
        self.after(5000, self._check_status_loop)
    
    def check_server_online(self) -> bool:
        """Check if server is online by trying to connect to port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', MINECRAFT_SERVER_PORT))
            sock.close()
            return result == 0
        except:
            return False
    
    def update_server_info(self):
        """Update server information display"""
        info = f"Server Address: localhost:{MINECRAFT_SERVER_PORT}\n"
        info += f"Version: Minecraft 1.21.1 (Paper)\n"
        info += f"Project Root: {PROJECT_ROOT}\n"
        info += f"Mods Directory: {PROJECT_ROOT / 'server-mods'}\n"
        info += f"\nAvailable Scripts:\n"
        
        # Check for scripts
        scripts = [
            "START-SERVER.cmd",
            "STOP-SERVER.cmd",
            "RESTART-SERVER.cmd",
            "VIEW-LOGS.cmd"
        ]
        
        for script in scripts:
            script_path = PROJECT_ROOT / script
            status = "✓" if script_path.exists() else "✗"
            info += f"  {status} {script}\n"
        
        self.info_text.delete("1.0", "end")
        self.info_text.insert("1.0", info)
        self.info_text.configure(state="disabled")

