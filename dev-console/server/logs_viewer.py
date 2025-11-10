"""
Logs Viewer Component
Real-time log streaming with search and filtering
"""

import customtkinter as ctk
import threading
import time
from pathlib import Path
from typing import Optional
import re

from config import THEME, LAYOUT, LOGS_DIR


class LogsViewer(ctk.CTkFrame):
    """
    Real-time logs viewer.
    Fast, searchable, color-coded.
    """
    
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color=THEME["bg_primary"],
            corner_radius=0
        )
        
        self.log_file_path = LOGS_DIR / "latest.log"
        self.following = True
        self.search_term = ""
        self.filter_level = "ALL"
        self.last_position = 0
        
        # Create UI
        self.create_header()
        self.create_controls()
        self.create_log_display()
        
        # Start log following
        self.start_following_logs()
    
    def create_header(self):
        """Create header"""
        header = ctk.CTkLabel(
            self,
            text="📜 Server Logs",
            font=THEME["font_header"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        header.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
    
    def create_controls(self):
        """Create control buttons and filters"""
        controls_frame = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        controls_frame.pack(fill="x", padx=LAYOUT["card_padding"], pady=10)
        
        # Top row - Auto-scroll and clear
        top_row = ctk.CTkFrame(controls_frame, fg_color="transparent")
        top_row.pack(fill="x", padx=15, pady=(15, 5))
        
        # Auto-scroll toggle
        self.autoscroll_var = ctk.BooleanVar(value=True)
        self.autoscroll_checkbox = ctk.CTkCheckBox(
            top_row,
            text="Auto-scroll",
            variable=self.autoscroll_var,
            font=THEME["font_body"],
            text_color=THEME["text_primary"],
            fg_color=THEME["accent"],
            hover_color=THEME["accent_hover"]
        )
        self.autoscroll_checkbox.pack(side="left", padx=5)
        
        # Clear button
        clear_btn = ctk.CTkButton(
            top_row,
            text="Clear",
            width=80,
            font=THEME["font_body"],
            fg_color=THEME["error"],
            hover_color="#cc4444",
            command=self.clear_logs
        )
        clear_btn.pack(side="right", padx=5)
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            top_row,
            text="Refresh",
            width=80,
            font=THEME["font_body"],
            fg_color=THEME["accent"],
            hover_color=THEME["accent_hover"],
            command=self.refresh_logs
        )
        refresh_btn.pack(side="right", padx=5)
        
        # Bottom row - Search and filter
        bottom_row = ctk.CTkFrame(controls_frame, fg_color="transparent")
        bottom_row.pack(fill="x", padx=15, pady=(5, 15))
        
        # Search
        ctk.CTkLabel(
            bottom_row,
            text="Search:",
            font=THEME["font_body"],
            text_color=THEME["text_secondary"]
        ).pack(side="left", padx=5)
        
        self.search_entry = ctk.CTkEntry(
            bottom_row,
            placeholder_text="Search logs...",
            width=200,
            font=THEME["font_body"]
        )
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", lambda e: self.apply_filters())
        
        # Log level filter
        ctk.CTkLabel(
            bottom_row,
            text="Level:",
            font=THEME["font_body"],
            text_color=THEME["text_secondary"]
        ).pack(side="left", padx=(20, 5))
        
        self.level_menu = ctk.CTkOptionMenu(
            bottom_row,
            values=["ALL", "INFO", "WARN", "ERROR", "DEBUG"],
            command=self.on_level_filter_change,
            width=100,
            font=THEME["font_body"],
            fg_color=THEME["accent"],
            button_color=THEME["accent"],
            button_hover_color=THEME["accent_hover"]
        )
        self.level_menu.set("ALL")
        self.level_menu.pack(side="left", padx=5)
    
    def create_log_display(self):
        """Create log display area"""
        log_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        log_card.pack(fill="both", expand=True, padx=LAYOUT["card_padding"], pady=10)
        
        # Log text widget
        self.log_text = ctk.CTkTextbox(
            log_card,
            fg_color="#0a0a0a",  # Dark terminal-like background
            text_color="#e0e0e0",
            font=THEME["font_code"],
            wrap="word"
        )
        self.log_text.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Configure tags for color coding
        # Note: CTkTextbox doesn't support tags like Tkinter Text
        # We'll keep it simple for now
    
    def start_following_logs(self):
        """Start following logs in background thread"""
        self.following = True
        thread = threading.Thread(target=self._follow_logs_thread, daemon=True)
        thread.start()
    
    def _follow_logs_thread(self):
        """Background thread to follow logs"""
        while self.following:
            try:
                if self.log_file_path.exists():
                    with open(self.log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        # Seek to last position
                        f.seek(self.last_position)
                        
                        # Read new lines
                        new_lines = f.readlines()
                        
                        # Update position
                        self.last_position = f.tell()
                        
                        # Add new lines to display
                        if new_lines:
                            self.add_log_lines(new_lines)
                
                # Sleep before next check
                time.sleep(0.5)
            
            except Exception as e:
                # If error reading log, wait and try again
                time.sleep(1)
    
    def add_log_lines(self, lines: list):
        """Add log lines to display"""
        if not lines:
            return
        
        # Filter lines based on current filters
        filtered_lines = []
        search_term = self.search_entry.get().lower()
        
        for line in lines:
            # Apply search filter
            if search_term and search_term not in line.lower():
                continue
            
            # Apply level filter
            if self.filter_level != "ALL":
                if self.filter_level not in line:
                    continue
            
            filtered_lines.append(line)
        
        if not filtered_lines:
            return
        
        # Add to text widget
        self.after(0, lambda: self._append_lines(filtered_lines))
    
    def _append_lines(self, lines: list):
        """Append lines to text widget (must run in main thread)"""
        for line in lines:
            # Color code based on log level
            colored_line = self.colorize_log_line(line)
            self.log_text.insert("end", colored_line)
        
        # Auto-scroll if enabled
        if self.autoscroll_var.get():
            self.log_text.see("end")
    
    def colorize_log_line(self, line: str) -> str:
        """Add simple color indicators to log lines"""
        # Since CTkTextbox doesn't support rich text,
        # we'll add emoji indicators for different log levels
        
        if "[ERROR]" in line or "ERROR" in line:
            return f"❌ {line}"
        elif "[WARN]" in line or "WARN" in line:
            return f"⚠️ {line}"
        elif "[INFO]" in line or "INFO" in line:
            return f"ℹ️ {line}"
        elif "[DEBUG]" in line or "DEBUG" in line:
            return f"🔍 {line}"
        else:
            return line
    
    def apply_filters(self):
        """Apply search and filter to current logs"""
        # For now, filters only apply to new logs
        # Full filtering would require re-reading the entire log file
        pass
    
    def on_level_filter_change(self, value: str):
        """Handle log level filter change"""
        self.filter_level = value
        self.refresh_logs()
    
    def clear_logs(self):
        """Clear log display"""
        self.log_text.delete("1.0", "end")
    
    def refresh_logs(self):
        """Refresh logs from file"""
        self.clear_logs()
        self.last_position = 0
        
        # Read entire log file with filters
        if self.log_file_path.exists():
            try:
                with open(self.log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    
                    # Apply filters
                    search_term = self.search_entry.get().lower()
                    filtered_lines = []
                    
                    for line in lines:
                        # Apply search filter
                        if search_term and search_term not in line.lower():
                            continue
                        
                        # Apply level filter
                        if self.filter_level != "ALL":
                            if self.filter_level not in line:
                                continue
                        
                        filtered_lines.append(line)
                    
                    # Display filtered lines
                    for line in filtered_lines:
                        colored_line = self.colorize_log_line(line)
                        self.log_text.insert("end", colored_line)
                    
                    # Update position
                    self.last_position = f.tell()
                    
                    # Scroll to end
                    if self.autoscroll_var.get():
                        self.log_text.see("end")
            
            except Exception as e:
                self.log_text.insert("1.0", f"Error reading log file: {str(e)}\n")
        else:
            self.log_text.insert("1.0", f"Log file not found: {self.log_file_path}\n")
            self.log_text.insert("end", "Waiting for server to start...\n")
    
    def destroy(self):
        """Clean up when widget is destroyed"""
        self.following = False
        super().destroy()

