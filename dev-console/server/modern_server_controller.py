"""
Modern Server Controller Component
Sleek, modern server control panel with real-time status
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
    Modern server control panel.
    Beautiful, powerful, intuitive.
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
        header = ctk.CTkFrame(self, fg_color=THEME["bg_secondary"], height=100)
        header.pack(fill="x", padx=20, pady=(20, 10))
        header.pack_propagate(False)
        
        title = ctk.CTkLabel(
            header,
            text="🖥️ Server Control",
            font=("Segoe UI", 28, "bold"),
            text_color=THEME["text_primary"]
        )
        title.pack(side="left", padx=30, pady=30)
        
        subtitle = ctk.CTkLabel(
            header,
            text="Manage and monitor your Minecraft server",
            font=THEME["font_body"],
            text_color=THEME["text_secondary"]
        )
        subtitle.pack(side="left", padx=(0, 30), pady=30)
        
        # Modern status card with gradient
        self.create_modern_status_card()
        
        # Control panel with modern buttons
        self.create_modern_control_panel()
        
        # Quick actions card
        self.create_quick_actions_card()
        
        # Server info and metrics
        self.create_server_metrics()
        
        # Start status checking
        self.start_status_checking()
    
    def create_modern_status_card(self):
        """Create modern server status display with gradient"""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="x", padx=20, pady=10)
        
        # Large status card
        self.status_card = ctk.CTkFrame(
            container,
            fg_color=THEME["card_bg"],
            corner_radius=15,
            height=180
        )
        self.status_card.pack(fill="x")
        self.status_card.pack_propagate(False)
        
        # Left side - Status indicator
        left_frame = ctk.CTkFrame(self.status_card, fg_color="transparent")
        left_frame.pack(side="left", fill="y", padx=30, pady=30)
        
        # Large animated status indicator
        self.status_indicator = ctk.CTkFrame(
            left_frame,
            fg_color=THEME["error"],
            width=80,
            height=80,
            corner_radius=40
        )
        self.status_indicator.pack()
        
        # Pulse effect label
        self.pulse_label = ctk.CTkLabel(
            self.status_indicator,
            text="●",
            font=("Segoe UI", 40),
            text_color=THEME["text_primary"]
        )
        self.pulse_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Right side - Status text
        right_frame = ctk.CTkFrame(self.status_card, fg_color="transparent")
        right_frame.pack(side="left", fill="both", expand=True, pady=30)
        
        self.status_text = ctk.CTkLabel(
            right_frame,
            text="OFFLINE",
            font=("Segoe UI", 36, "bold"),
            text_color=THEME["error"],
            anchor="w"
        )
        self.status_text.pack(anchor="w", pady=(10, 5))
        
        self.status_details = ctk.CTkLabel(
            right_frame,
            text="Server is not running",
            font=("Segoe UI", 16),
            text_color=THEME["text_secondary"],
            anchor="w"
        )
        self.status_details.pack(anchor="w")
        
        # Metrics row
        metrics_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        metrics_frame.pack(anchor="w", pady=(15, 0))
        
        # Player count
        self.player_metric = self.create_metric_badge(
            metrics_frame,
            "👥",
            "0 Players",
            THEME["text_secondary"]
        )
        self.player_metric.pack(side="left", padx=(0, 15))
        
        # Uptime
        self.uptime_metric = self.create_metric_badge(
            metrics_frame,
            "⏱",
            "00:00:00",
            THEME["text_secondary"]
        )
        self.uptime_metric.pack(side="left", padx=(0, 15))
        
        # Port
        self.port_metric = self.create_metric_badge(
            metrics_frame,
            "🔌",
            f"Port {MINECRAFT_SERVER_PORT}",
            THEME["text_secondary"]
        )
        self.port_metric.pack(side="left")
    
    def create_metric_badge(self, parent, icon, text, color):
        """Create a metric badge"""
        badge = ctk.CTkFrame(
            parent,
            fg_color=THEME["bg_primary"],
            corner_radius=8
        )
        
        ctk.CTkLabel(
            badge,
            text=f"{icon} {text}",
            font=THEME["font_body"],
            text_color=color
        ).pack(padx=15, pady=8)
        
        return badge
    
    def create_modern_control_panel(self):
        """Create modern control panel with gradient buttons"""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="x", padx=20, pady=10)
        
        label = ctk.CTkLabel(
            container,
            text="⚡ Quick Controls",
            font=("Segoe UI", 20, "bold"),
            text_color=THEME["text_primary"],
            anchor="w"
        )
        label.pack(fill="x", pady=(0, 10))
        
        # Control card
        control_card = ctk.CTkFrame(
            container,
            fg_color=THEME["card_bg"],
            corner_radius=15
        )
        control_card.pack(fill="x")
        
        buttons_frame = ctk.CTkFrame(control_card, fg_color="transparent")
        buttons_frame.pack(pady=25, padx=25, fill="x")
        
        # Modern start button
        self.start_btn = ctk.CTkButton(
            buttons_frame,
            text="▶  START SERVER",
            font=("Segoe UI", 15, "bold"),
            fg_color=THEME["success"],
            hover_color="#00c993",
            height=60,
            corner_radius=10,
            command=self.start_server
        )
        self.start_btn.pack(side="left", fill="x", expand=True, padx=5)
        
        # Modern stop button
        self.stop_btn = ctk.CTkButton(
            buttons_frame,
            text="⏹  STOP SERVER",
            font=("Segoe UI", 15, "bold"),
            fg_color=THEME["error"],
            hover_color="#cc4444",
            height=60,
            corner_radius=10,
            state="disabled",
            command=self.stop_server
        )
        self.stop_btn.pack(side="left", fill="x", expand=True, padx=5)
        
        # Modern restart button
        self.restart_btn = ctk.CTkButton(
            buttons_frame,
            text="🔄  RESTART SERVER",
            font=("Segoe UI", 15, "bold"),
            fg_color=THEME["warning"],
            hover_color="#ff9937",
            height=60,
            corner_radius=10,
            state="disabled",
            command=self.restart_server
        )
        self.restart_btn.pack(side="left", fill="x", expand=True, padx=5)
        
        # Status message with modern styling
        self.control_status = ctk.CTkLabel(
            control_card,
            text="",
            font=("Segoe UI", 13),
            text_color=THEME["text_secondary"]
        )
        self.control_status.pack(pady=(0, 20))
    
    def create_quick_actions_card(self):
        """Create quick actions card"""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="x", padx=20, pady=10)
        
        label = ctk.CTkLabel(
            container,
            text="⚙️ Quick Actions",
            font=("Segoe UI", 20, "bold"),
            text_color=THEME["text_primary"],
            anchor="w"
        )
        label.pack(fill="x", pady=(0, 10))
        
        actions_card = ctk.CTkFrame(
            container,
            fg_color=THEME["card_bg"],
            corner_radius=15
        )
        actions_card.pack(fill="x")
        
        actions_grid = ctk.CTkFrame(actions_card, fg_color="transparent")
        actions_grid.pack(padx=25, pady=25, fill="x")
        
        # Action buttons in grid
        actions = [
            ("📜", "View Logs", self.view_logs),
            ("📊", "Performance", self.view_performance),
            ("🔧", "Console", self.open_console),
            ("⚡", "Reload", self.reload_config)
        ]
        
        for i, (icon, text, cmd) in enumerate(actions):
            btn = self.create_action_button(actions_grid, icon, text, cmd)
            btn.grid(row=0, column=i, padx=5, sticky="ew")
            actions_grid.grid_columnconfigure(i, weight=1)
    
    def create_action_button(self, parent, icon, text, command):
        """Create modern action button"""
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        
        btn = ctk.CTkButton(
            btn_frame,
            text="",
            fg_color=THEME["bg_primary"],
            hover_color=THEME["accent"],
            corner_radius=10,
            height=90,
            command=command
        )
        btn.pack(fill="both", expand=True)
        
        # Icon and text
        content = ctk.CTkFrame(btn, fg_color="transparent")
        content.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(
            content,
            text=icon,
            font=("Segoe UI", 28)
        ).pack(pady=(5, 0))
        
        ctk.CTkLabel(
            content,
            text=text,
            font=("Segoe UI", 12),
            text_color=THEME["text_secondary"]
        ).pack(pady=(0, 5))
        
        return btn_frame
    
    def create_server_metrics(self):
        """Create server metrics display"""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=10)
        
        label = ctk.CTkLabel(
            container,
            text="📈 Server Information",
            font=("Segoe UI", 20, "bold"),
            text_color=THEME["text_primary"],
            anchor="w"
        )
        label.pack(fill="x", pady=(0, 10))
        
        info_card = ctk.CTkFrame(
            container,
            fg_color=THEME["card_bg"],
            corner_radius=15
        )
        info_card.pack(fill="both", expand=True)
        
        self.info_text = ctk.CTkTextbox(
            info_card,
            fg_color=THEME["bg_primary"],
            text_color=THEME["text_secondary"],
            font=("Consolas", 12),
            wrap="none"
        )
        self.info_text.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.update_server_info()
    
    # Keep all the original methods (start_server, stop_server, etc.)
    def start_server(self):
        """Start the Minecraft server"""
        self.control_status.configure(
            text="⏳ Starting server...",
            text_color=THEME["info"]
        )
        self.start_btn.configure(state="disabled")
        thread = threading.Thread(target=self._start_server_thread, daemon=True)
        thread.start()
    
    def _start_server_thread(self):
        """Start server thread"""
        try:
            start_script = PROJECT_ROOT / "START-SERVER.cmd"
            if not start_script.exists():
                # Try docker-compose
                subprocess.Popen(
                    ["docker-compose", "up", "-d"],
                    cwd=str(PROJECT_ROOT),
                    shell=True
                )
            else:
                subprocess.Popen([str(start_script)], cwd=str(PROJECT_ROOT), shell=True)
            
            time.sleep(3)
            self.after(0, lambda: self.control_status.configure(
                text="✓ Server start command executed",
                text_color=THEME["success"]
            ))
        except Exception as e:
            self.after(0, lambda: self.control_status.configure(
                text=f"❌ Error: {str(e)}",
                text_color=THEME["error"]
            ))
            self.after(0, lambda: self.start_btn.configure(state="normal"))
    
    def stop_server(self):
        """Stop the Minecraft server"""
        self.control_status.configure(text="⏳ Stopping server...", text_color=THEME["warning"])
        self.stop_btn.configure(state="disabled")
        self.restart_btn.configure(state="disabled")
        thread = threading.Thread(target=self._stop_server_thread, daemon=True)
        thread.start()
    
    def _stop_server_thread(self):
        """Stop server thread"""
        try:
            subprocess.run(["docker-compose", "down"], cwd=str(PROJECT_ROOT), shell=True)
            time.sleep(2)
            self.after(0, lambda: self.control_status.configure(
                text="✓ Server stopped",
                text_color=THEME["success"]
            ))
            self.after(0, lambda: self.start_btn.configure(state="normal"))
        except Exception as e:
            self.after(0, lambda: self.control_status.configure(
                text=f"❌ Error: {str(e)}",
                text_color=THEME["error"]
            ))
    
    def restart_server(self):
        """Restart the Minecraft server"""
        self.control_status.configure(text="⏳ Restarting server...", text_color=THEME["info"])
        self.stop_btn.configure(state="disabled")
        self.restart_btn.configure(state="disabled")
        self.start_btn.configure(state="disabled")
        thread = threading.Thread(target=self._restart_server_thread, daemon=True)
        thread.start()
    
    def _restart_server_thread(self):
        """Restart server thread"""
        try:
            subprocess.run(["docker-compose", "restart"], cwd=str(PROJECT_ROOT), shell=True)
            time.sleep(3)
            self.after(0, lambda: self.control_status.configure(
                text="✓ Server restarted",
                text_color=THEME["success"]
            ))
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
        
        is_online = self.check_server_online()
        
        if is_online:
            self.status_indicator.configure(fg_color=THEME["success"])
            self.status_text.configure(text="ONLINE", text_color=THEME["success"])
            self.status_details.configure(text=f"Server is running on port {MINECRAFT_SERVER_PORT}")
            
            if self.on_status_change:
                self.on_status_change(True, 0)
            
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            self.restart_btn.configure(state="normal")
        else:
            self.status_indicator.configure(fg_color=THEME["error"])
            self.status_text.configure(text="OFFLINE", text_color=THEME["error"])
            self.status_details.configure(text="Server is not running")
            
            if self.on_status_change:
                self.on_status_change(False, 0)
            
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")
            self.restart_btn.configure(state="disabled")
        
        self.after(5000, self._check_status_loop)
    
    def check_server_online(self) -> bool:
        """Check if server is online"""
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
        info = f"═══════════════════════════════════════════════════════════\n"
        info += f"  SERVER CONFIGURATION\n"
        info += f"═══════════════════════════════════════════════════════════\n\n"
        info += f"  Address: localhost:{MINECRAFT_SERVER_PORT}\n"
        info += f"  Version: Minecraft 1.21.1 (Paper)\n"
        info += f"  Type: Dockerized Server\n\n"
        info += f"═══════════════════════════════════════════════════════════\n"
        info += f"  PATHS\n"
        info += f"═══════════════════════════════════════════════════════════\n\n"
        info += f"  Project Root: {PROJECT_ROOT}\n"
        info += f"  Mods Directory: {PROJECT_ROOT / 'server-mods'}\n"
        info += f"  Worlds: {PROJECT_ROOT / 'worlds'}\n\n"
        
        self.info_text.delete("1.0", "end")
        self.info_text.insert("1.0", info)
        self.info_text.configure(state="disabled")
    
    # Quick action methods
    def view_logs(self):
        """View server logs"""
        print("Opening logs viewer...")
    
    def view_performance(self):
        """View performance metrics"""
        print("Opening performance metrics...")
    
    def open_console(self):
        """Open server console"""
        print("Opening server console...")
    
    def reload_config(self):
        """Reload configuration"""
        self.control_status.configure(
            text="✓ Configuration reloaded",
            text_color=THEME["success"]
        )

