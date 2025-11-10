"""
Client Console Integration for Dev Console
Interactive chat interface with AI, RCON, and project control

Features:
- Grok-4 Fast AI integration
- Minecraft RCON commands
- Project control operations
- Color-coded output
- Command history
- Real-time responses
"""

import customtkinter as ctk
import asyncio
import os
import sys
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from datetime import datetime

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import console functionality
try:
    from grok_client import GrokClient
    from rcon_client import RconClient
    from project_controller import ProjectController
except ImportError:
    GrokClient = None
    RconClient = None
    ProjectController = None

# Import dev-console config
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import THEME


class ClientConsole(ctk.CTkFrame):
    """
    Client Console view for Dev Console.
    Combines AI chat, RCON control, and project management.
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=THEME["bg_primary"], **kwargs)
        
        # Load environment variables
        load_dotenv(".env.grok")
        
        # Configuration
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "")
        self.rcon_host = os.getenv("MINECRAFT_RCON_HOST", "localhost")
        self.rcon_port = int(os.getenv("MINECRAFT_RCON_PORT", 25575))
        self.rcon_password = os.getenv("MINECRAFT_RCON_PASSWORD", "titan123")
        self.docker_container = os.getenv("MINECRAFT_DOCKER_CONTAINER", "titan-hub")
        
        # Initialize clients (lazy loading)
        self.grok: Optional[GrokClient] = None
        self.rcon: Optional[RconClient] = None
        self.project: Optional[ProjectController] = None
        
        # Command history
        self.command_history = []
        self.history_index = -1
        
        # Create UI
        self.create_ui()
        
        # Initialize systems
        asyncio.create_task(self.initialize_systems())
    
    def create_ui(self):
        """Create the console UI"""
        
        # Header
        header = ctk.CTkFrame(self, fg_color=THEME["bg_secondary"], height=60)
        header.pack(fill="x", padx=10, pady=(10, 0))
        header.pack_propagate(False)
        
        title = ctk.CTkLabel(
            header,
            text="💬 Client Console",
            font=THEME["font_header"],
            text_color=THEME["text_primary"]
        )
        title.pack(side="left", padx=20, pady=15)
        
        # Status indicators
        self.status_frame = ctk.CTkFrame(header, fg_color="transparent")
        self.status_frame.pack(side="right", padx=20)
        
        self.ai_status = ctk.CTkLabel(
            self.status_frame,
            text="🤖 AI: Offline",
            font=THEME["font_body"],
            text_color=THEME["text_secondary"]
        )
        self.ai_status.pack(side="left", padx=10)
        
        self.rcon_status = ctk.CTkLabel(
            self.status_frame,
            text="🎮 RCON: Offline",
            font=THEME["font_body"],
            text_color=THEME["text_secondary"]
        )
        self.rcon_status.pack(side="left", padx=10)
        
        # Main content area
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Console output (chat history)
        output_frame = ctk.CTkFrame(content, fg_color=THEME["bg_secondary"])
        output_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        output_label = ctk.CTkLabel(
            output_frame,
            text="Console Output",
            font=THEME["font_subheader"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        output_label.pack(fill="x", padx=15, pady=(10, 5))
        
        # Text widget for output
        self.output_text = ctk.CTkTextbox(
            output_frame,
            font=("Consolas", 12),
            fg_color=THEME["bg_primary"],
            text_color=THEME["text_primary"],
            wrap="word",
            state="disabled"
        )
        self.output_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Input area
        input_frame = ctk.CTkFrame(content, fg_color=THEME["bg_secondary"], height=120)
        input_frame.pack(fill="x")
        input_frame.pack_propagate(False)
        
        input_label = ctk.CTkLabel(
            input_frame,
            text="Command Input",
            font=THEME["font_subheader"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        input_label.pack(fill="x", padx=15, pady=(10, 5))
        
        # Input field with buttons
        input_controls = ctk.CTkFrame(input_frame, fg_color="transparent")
        input_controls.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.input_field = ctk.CTkEntry(
            input_controls,
            placeholder_text="Type command here... (@ai, /cmd, @project)",
            font=("Consolas", 12),
            height=40
        )
        self.input_field.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.input_field.bind("<Return>", self.handle_enter_key)
        self.input_field.bind("<Up>", self.history_up)
        self.input_field.bind("<Down>", self.history_down)
        
        # Send button
        send_btn = ctk.CTkButton(
            input_controls,
            text="Send",
            command=self.send_command,
            width=100,
            height=40,
            fg_color=THEME["accent_color"],
            hover_color=THEME["accent_hover"]
        )
        send_btn.pack(side="left", padx=(0, 5))
        
        # Help button
        help_btn = ctk.CTkButton(
            input_controls,
            text="Help",
            command=self.show_help,
            width=80,
            height=40,
            fg_color=THEME["bg_primary"],
            hover_color=THEME["bg_secondary"]
        )
        help_btn.pack(side="left")
        
        # Print welcome message
        self.print_welcome()
    
    def print_welcome(self):
        """Print welcome message to console"""
        welcome = """
═══════════════════════════════════════════════════════════════
  ⚡ CLIENT CONSOLE - mc.galion.studio
  Ultra-fast AI chat + Minecraft server control
═══════════════════════════════════════════════════════════════

Welcome! Use the commands below:
  @ai <question>         - Ask AI assistant
  /cmd <minecraft-cmd>   - Execute Minecraft command
  /say <message>         - Send to Minecraft chat
  @project <action>      - Control project
  /status                - Show system status
  /help                  - Show detailed help

Initializing systems...
"""
        self.append_output(welcome, "info")
    
    async def initialize_systems(self):
        """Initialize AI, RCON, and project controller"""
        
        # Initialize Grok AI
        if self.openrouter_api_key and GrokClient:
            try:
                self.grok = GrokClient(api_key=self.openrouter_api_key)
                self.append_output("✓ Grok AI connected", "success")
                self.ai_status.configure(
                    text="🤖 AI: Online",
                    text_color=THEME["success_color"]
                )
            except Exception as e:
                self.append_output(f"✗ Grok AI failed: {e}", "error")
        else:
            self.append_output("⚠ Grok AI not configured", "warning")
        
        # Initialize RCON
        if RconClient:
            try:
                self.rcon = RconClient(
                    host=self.rcon_host,
                    port=self.rcon_port,
                    password=self.rcon_password,
                    docker_container=self.docker_container
                )
                await self.rcon.send_command("list")
                self.append_output("✓ Minecraft RCON connected", "success")
                self.rcon_status.configure(
                    text="🎮 RCON: Online",
                    text_color=THEME["success_color"]
                )
            except Exception as e:
                self.append_output(f"⚠ RCON unavailable: {e}", "warning")
                self.rcon = None
        
        # Initialize project controller
        if ProjectController:
            try:
                self.project = ProjectController(".")
                self.append_output("✓ Project controller ready", "success")
            except Exception as e:
                self.append_output(f"✗ Project controller failed: {e}", "error")
        
        self.append_output("\n✓ Console ready! Type /help for commands\n", "success")
    
    def append_output(self, text: str, level: str = "info"):
        """
        Append text to output console.
        
        Args:
            text: Text to append
            level: Message level (info, success, error, warning, user, ai)
        """
        self.output_text.configure(state="normal")
        
        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Color based on level
        if level == "success":
            prefix = f"[{timestamp}] ✓ "
        elif level == "error":
            prefix = f"[{timestamp}] ✗ "
        elif level == "warning":
            prefix = f"[{timestamp}] ⚠ "
        elif level == "user":
            prefix = f"[{timestamp}] 💬 You: "
        elif level == "ai":
            prefix = f"[{timestamp}] 🤖 Grok: "
        elif level == "info":
            prefix = ""
        else:
            prefix = f"[{timestamp}] "
        
        self.output_text.insert("end", prefix + text + "\n")
        self.output_text.see("end")
        self.output_text.configure(state="disabled")
    
    def handle_enter_key(self, event):
        """Handle Enter key press"""
        self.send_command()
        return "break"
    
    def history_up(self, event):
        """Navigate up in command history"""
        if self.command_history and self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.input_field.delete(0, "end")
            self.input_field.insert(0, self.command_history[-(self.history_index + 1)])
        return "break"
    
    def history_down(self, event):
        """Navigate down in command history"""
        if self.history_index > 0:
            self.history_index -= 1
            self.input_field.delete(0, "end")
            self.input_field.insert(0, self.command_history[-(self.history_index + 1)])
        elif self.history_index == 0:
            self.history_index = -1
            self.input_field.delete(0, "end")
        return "break"
    
    def send_command(self):
        """Send command from input field"""
        command = self.input_field.get().strip()
        
        if not command:
            return
        
        # Add to history
        self.command_history.append(command)
        self.history_index = -1
        
        # Clear input
        self.input_field.delete(0, "end")
        
        # Show user input
        self.append_output(command, "user")
        
        # Handle command asynchronously
        asyncio.create_task(self.handle_command(command))
    
    async def handle_command(self, command: str):
        """
        Route and handle user commands.
        
        Args:
            command: User input command
        """
        try:
            # Help command
            if command == "/help":
                self.show_help()
            
            # Status command
            elif command == "/status":
                await self.show_status()
            
            # Say command (send to Minecraft chat)
            elif command.startswith("/say "):
                message = command[5:]
                await self.handle_say(message)
            
            # Minecraft command
            elif command.startswith("/cmd "):
                mc_command = command[5:]
                await self.handle_minecraft_command(mc_command)
            
            # AI question
            elif command.startswith("@ai "):
                question = command[4:]
                await self.handle_ai_question(question)
            
            # Project command
            elif command.startswith("@project "):
                project_cmd = command[9:]
                await self.handle_project_command(project_cmd)
            
            # Direct Minecraft command (no prefix)
            elif command.startswith("/"):
                await self.handle_minecraft_command(command[1:])
            
            # Default: treat as AI question
            else:
                await self.handle_ai_question(command)
        
        except Exception as e:
            self.append_output(f"Error: {e}", "error")
    
    async def handle_say(self, message: str):
        """Send message to Minecraft chat"""
        if not self.rcon:
            self.append_output("RCON not connected", "error")
            return
        
        try:
            await self.rcon.say(message)
            self.append_output("Message sent to Minecraft", "success")
        except Exception as e:
            self.append_output(f"Failed: {e}", "error")
    
    async def handle_minecraft_command(self, command: str):
        """Execute Minecraft command via RCON"""
        if not self.rcon:
            self.append_output("RCON not connected", "error")
            return
        
        try:
            self.append_output(f"Executing: {command}", "info")
            response = await self.rcon.send_command(command)
            self.append_output(response, "success")
        except Exception as e:
            self.append_output(f"Command failed: {e}", "error")
    
    async def handle_ai_question(self, question: str):
        """Ask Grok AI a question"""
        if not self.grok:
            self.append_output("Grok AI not configured", "error")
            self.append_output("Check OPENROUTER_API_KEY in .env.grok", "warning")
            return
        
        try:
            self.append_output("Thinking...", "info")
            response = await self.grok.ask_minecraft(question)
            self.append_output(response, "ai")
        except Exception as e:
            self.append_output(f"AI error: {e}", "error")
    
    async def handle_project_command(self, command: str):
        """Handle project control commands"""
        if not self.project:
            self.append_output("Project controller not available", "error")
            return
        
        parts = command.split()
        if not parts:
            self.append_output("Usage: @project <action> [args]", "warning")
            return
        
        action = parts[0]
        
        try:
            if action == "status":
                result = await self.project.git_status()
                self.append_output(result, "info")
            
            elif action == "docker":
                result = await self.project.docker_ps()
                self.append_output(result, "info")
            
            elif action == "build":
                self.append_output("Building project...", "info")
                result = await self.project.gradle_build()
                self.append_output(result, "success")
            
            else:
                self.append_output(f"Unknown action: {action}", "warning")
                self.append_output("Available: status, docker, build", "info")
        
        except Exception as e:
            self.append_output(f"Project error: {e}", "error")
    
    async def show_status(self):
        """Show system status"""
        status_text = "\n═══════ SYSTEM STATUS ═══════\n"
        
        # Grok AI status
        if self.grok:
            stats = self.grok.get_stats()
            status_text += f"\n✓ Grok AI:\n"
            status_text += f"  Requests: {stats['total_requests']}\n"
            status_text += f"  Cache hits: {stats['cache_hits']} ({stats['cache_hit_rate']:.1%})\n"
            if stats['total_requests'] > 0:
                status_text += f"  Avg response: {stats['avg_response_time']:.3f}s\n"
        else:
            status_text += "\n✗ Grok AI: Not configured\n"
        
        # RCON status
        if self.rcon:
            stats = self.rcon.get_stats()
            status_text += f"\n✓ Minecraft RCON:\n"
            status_text += f"  Commands: {stats['total_commands']}\n"
            status_text += f"  Success rate: {stats['success_rate']:.1%}\n"
        else:
            status_text += "\n✗ Minecraft RCON: Not connected\n"
        
        # Project status
        if self.project:
            stats = self.project.get_stats()
            status_text += f"\n✓ Project Controller:\n"
            status_text += f"  Commands: {stats['total_commands']}\n"
        
        status_text += "\n═══════════════════════════════\n"
        
        self.append_output(status_text, "info")
    
    def show_help(self):
        """Show help message"""
        help_text = """
═══════════════════════════════════════════════════════════════
  COMMAND REFERENCE
═══════════════════════════════════════════════════════════════

CHAT COMMANDS:
  /say <message>        Send message to Minecraft chat
  @ai <question>        Ask Grok AI a question
  <any text>            Defaults to AI question

MINECRAFT COMMANDS:
  /cmd <command>        Execute Minecraft command
  /<command>            Direct Minecraft command
  
  Examples:
    /list               List online players
    /time set day       Set time to day
    /gamemode creative  Set gamemode

PROJECT COMMANDS:
  @project status       Git status
  @project docker       List containers
  @project build        Build project

SYSTEM COMMANDS:
  /status               Show system status
  /help                 Show this help

KEYBOARD SHORTCUTS:
  Enter                 Send command
  Up/Down arrows        Navigate command history

═══════════════════════════════════════════════════════════════
"""
        self.append_output(help_text, "info")


# Convenience function for creating the view
def create_client_console(parent):
    """Create and return client console view"""
    return ClientConsole(parent)

