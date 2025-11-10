"""
Debugger Component
Debugging tools with variable inspection and thread analysis
"""

import customtkinter as ctk
from typing import Optional, Dict
import socket

from config import THEME, LAYOUT, RCON_HOST, RCON_PORT, RCON_PASSWORD


class Debugger(ctk.CTkScrollableFrame):
    """
    Debugging tools for Minecraft mods.
    Inspect, analyze, troubleshoot.
    """
    
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color=THEME["bg_primary"],
            corner_radius=0
        )
        
        # Header
        header = ctk.CTkLabel(
            self,
            text="🐛 Debugger",
            font=THEME["font_header"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        header.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        # Quick debug commands
        self.create_commands_section()
        
        # Variable inspector
        self.create_inspector_section()
        
        # Thread dump
        self.create_thread_dump_section()
    
    def create_commands_section(self):
        """Create quick debug commands section"""
        commands_label = ctk.CTkLabel(
            self,
            text="Quick Debug Commands",
            font=THEME["font_subheader"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        commands_label.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        commands_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        commands_card.pack(fill="x", padx=LAYOUT["card_padding"], pady=10)
        
        # Command buttons in grid
        commands_frame = ctk.CTkFrame(commands_card, fg_color="transparent")
        commands_frame.pack(fill="x", padx=20, pady=20)
        
        # Row 1
        row1 = ctk.CTkFrame(commands_frame, fg_color="transparent")
        row1.pack(fill="x", pady=5)
        
        self.create_command_button(
            row1, "📊 Server TPS", "Display server TPS", 
            lambda: self.run_command("tps")
        ).pack(side="left", fill="x", expand=True, padx=5)
        
        self.create_command_button(
            row1, "💾 Memory Usage", "Check memory usage",
            lambda: self.run_command("forge gc")
        ).pack(side="left", fill="x", expand=True, padx=5)
        
        self.create_command_button(
            row1, "🔌 Plugin List", "List loaded plugins",
            lambda: self.run_command("plugins")
        ).pack(side="left", fill="x", expand=True, padx=5)
        
        # Row 2
        row2 = ctk.CTkFrame(commands_frame, fg_color="transparent")
        row2.pack(fill="x", pady=5)
        
        self.create_command_button(
            row2, "🌍 World Info", "World information",
            lambda: self.run_command("world info")
        ).pack(side="left", fill="x", expand=True, padx=5)
        
        self.create_command_button(
            row2, "👥 Players", "Online players",
            lambda: self.run_command("list")
        ).pack(side="left", fill="x", expand=True, padx=5)
        
        self.create_command_button(
            row2, "📝 Thread Dump", "Generate thread dump",
            lambda: self.generate_thread_dump()
        ).pack(side="left", fill="x", expand=True, padx=5)
        
        # Custom command
        custom_frame = ctk.CTkFrame(commands_card, fg_color="transparent")
        custom_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        ctk.CTkLabel(
            custom_frame,
            text="Custom Command:",
            font=THEME["font_body"],
            text_color=THEME["text_secondary"]
        ).pack(side="left", padx=(0, 10))
        
        self.custom_command_entry = ctk.CTkEntry(
            custom_frame,
            placeholder_text="Enter RCON command...",
            font=THEME["font_code"]
        )
        self.custom_command_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.custom_command_entry.bind("<Return>", lambda e: self.run_custom_command())
        
        ctk.CTkButton(
            custom_frame,
            text="Run",
            width=80,
            fg_color=THEME["accent"],
            command=self.run_custom_command
        ).pack(side="left")
        
        # Output
        self.command_output = ctk.CTkTextbox(
            commands_card,
            fg_color=THEME["bg_primary"],
            text_color=THEME["text_primary"],
            font=THEME["font_code"],
            height=150
        )
        self.command_output.pack(fill="x", padx=20, pady=(0, 20))
        self.command_output.insert("1.0", "Command output will appear here...\n")
        self.command_output.configure(state="disabled")
    
    def create_command_button(self, parent, title: str, description: str, command):
        """Create a command button"""
        btn = ctk.CTkButton(
            parent,
            text=title,
            font=THEME["font_body"],
            fg_color=THEME["card_hover"],
            hover_color=THEME["accent"],
            height=40,
            command=command
        )
        return btn
    
    def create_inspector_section(self):
        """Create variable inspector section"""
        inspector_label = ctk.CTkLabel(
            self,
            text="Variable Inspector",
            font=THEME["font_subheader"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        inspector_label.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        inspector_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        inspector_card.pack(fill="x", padx=LAYOUT["card_padding"], pady=10)
        
        # Variable lookup
        lookup_frame = ctk.CTkFrame(inspector_card, fg_color="transparent")
        lookup_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            lookup_frame,
            text="Inspect Variable:",
            font=THEME["font_body"],
            text_color=THEME["text_secondary"]
        ).pack(side="left", padx=(0, 10))
        
        self.variable_entry = ctk.CTkEntry(
            lookup_frame,
            placeholder_text="player.health, world.time, etc.",
            font=THEME["font_code"]
        )
        self.variable_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ctk.CTkButton(
            lookup_frame,
            text="Inspect",
            width=80,
            fg_color=THEME["accent"],
            command=self.inspect_variable
        ).pack(side="left")
        
        # Variable details
        self.variable_output = ctk.CTkTextbox(
            inspector_card,
            fg_color=THEME["bg_primary"],
            text_color=THEME["text_primary"],
            font=THEME["font_code"],
            height=100
        )
        self.variable_output.pack(fill="x", padx=20, pady=(0, 20))
        self.variable_output.insert("1.0", "Variable details will appear here...\n")
        self.variable_output.configure(state="disabled")
    
    def create_thread_dump_section(self):
        """Create thread dump section"""
        thread_label = ctk.CTkLabel(
            self,
            text="Thread Analysis",
            font=THEME["font_subheader"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        thread_label.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        thread_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        thread_card.pack(fill="both", expand=True, padx=LAYOUT["card_padding"], pady=10)
        
        # Thread dump output
        self.thread_output = ctk.CTkTextbox(
            thread_card,
            fg_color=THEME["bg_primary"],
            text_color=THEME["text_primary"],
            font=THEME["font_code"]
        )
        self.thread_output.pack(fill="both", expand=True, padx=20, pady=20)
        self.thread_output.insert("1.0", "Click 'Thread Dump' above to analyze threads...\n")
        self.thread_output.configure(state="disabled")
    
    def run_command(self, command: str):
        """Run RCON command"""
        self.log_command_output(f"\n> {command}\n")
        
        try:
            from mcrcon import MCRcon
            
            with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
                response = mcr.command(command)
                self.log_command_output(response + "\n")
        
        except Exception as e:
            self.log_command_output(f"[ERROR] {str(e)}\n")
            self.log_command_output("[!] Make sure RCON is enabled and configured correctly\n")
    
    def run_custom_command(self):
        """Run custom command"""
        command = self.custom_command_entry.get().strip()
        if command:
            self.run_command(command)
            self.custom_command_entry.delete(0, "end")
    
    def inspect_variable(self):
        """Inspect a variable"""
        variable = self.variable_entry.get().strip()
        if not variable:
            return
        
        self.log_variable_output(f"\nInspecting: {variable}\n")
        self.log_variable_output("="*40 + "\n")
        
        # This would require custom mod integration
        # For now, show placeholder
        self.log_variable_output("[!] Variable inspection requires custom mod integration\n")
        self.log_variable_output("[i] Add debugging endpoints to your mod to enable this feature\n")
    
    def generate_thread_dump(self):
        """Generate thread dump"""
        self.log_thread_output("\nGenerating thread dump...\n")
        self.log_thread_output("="*50 + "\n")
        
        # This would typically use JMX or a custom mod endpoint
        # For now, show placeholder
        self.log_thread_output("[!] Thread dump requires JMX connection or custom mod\n")
        self.log_thread_output("[i] To enable:\n")
        self.log_thread_output("    1. Start server with JMX enabled\n")
        self.log_thread_output("    2. Or add debugging endpoints to your mod\n")
        self.log_thread_output("    3. Or use /forge tps command for basic info\n")
        
        # Try to get basic server info via RCON
        try:
            self.run_command("forge tps")
        except:
            pass
    
    def log_command_output(self, text: str):
        """Log to command output"""
        self.command_output.configure(state="normal")
        self.command_output.insert("end", text)
        self.command_output.see("end")
        self.command_output.configure(state="disabled")
    
    def log_variable_output(self, text: str):
        """Log to variable output"""
        self.variable_output.configure(state="normal")
        self.variable_output.delete("1.0", "end")
        self.variable_output.insert("1.0", text)
        self.variable_output.configure(state="disabled")
    
    def log_thread_output(self, text: str):
        """Log to thread output"""
        self.thread_output.configure(state="normal")
        self.thread_output.insert("end", text)
        self.thread_output.see("end")
        self.thread_output.configure(state="disabled")

