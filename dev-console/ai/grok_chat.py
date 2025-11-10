"""
Grok AI Chat Component
Real-time AI chat with Grok 4 Fast for admins and Minecraft integration
"""

import customtkinter as ctk
import asyncio
import threading
from typing import Optional, List, Dict
from datetime import datetime
import os
from pathlib import Path

from config import THEME, LAYOUT, PROJECT_ROOT


class GrokChatPanel(ctk.CTkFrame):
    """
    AI chat panel with Grok 4 Fast.
    Admin can chat with AI and send responses to Minecraft.
    """
    
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color=THEME["bg_primary"],
            corner_radius=0
        )
        
        self.grok_client = None
        self.conversation_history = []
        self.minecraft_mode = False
        
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        header = ctk.CTkLabel(
            header_frame,
            text="🤖 AI Chat - Grok 4 Fast",
            font=THEME["font_header"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        header.pack(side="left")
        
        # Status indicator
        self.status_label = ctk.CTkLabel(
            header_frame,
            text="● Not Connected",
            font=THEME["font_small"],
            text_color=THEME["error"]
        )
        self.status_label.pack(side="right", padx=10)
        
        # API Key setup
        self.create_api_setup()
        
        # Chat area
        self.create_chat_area()
        
        # Input area
        self.create_input_area()
        
        # Load API key if exists
        self.load_api_key()
    
    def create_api_setup(self):
        """Create API key setup section"""
        setup_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        setup_card.pack(fill="x", padx=LAYOUT["card_padding"], pady=10)
        
        setup_label = ctk.CTkLabel(
            setup_card,
            text="OpenRouter API Key Setup",
            font=THEME["font_body"],
            text_color=THEME["text_primary"]
        )
        setup_label.pack(padx=20, pady=(15, 5))
        
        help_text = ctk.CTkLabel(
            setup_card,
            text="Get your FREE API key at openrouter.ai/keys ($1 free credit!)",
            font=THEME["font_small"],
            text_color=THEME["text_secondary"]
        )
        help_text.pack(padx=20, pady=(0, 10))
        
        # API key entry
        key_frame = ctk.CTkFrame(setup_card, fg_color="transparent")
        key_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.api_key_entry = ctk.CTkEntry(
            key_frame,
            placeholder_text="Enter OpenRouter API key...",
            font=THEME["font_code"],
            show="*"
        )
        self.api_key_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        connect_btn = ctk.CTkButton(
            key_frame,
            text="Connect",
            width=100,
            fg_color=THEME["success"],
            hover_color="#00c993",
            command=self.connect_grok
        )
        connect_btn.pack(side="left")
    
    def create_chat_area(self):
        """Create chat message area"""
        chat_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        chat_card.pack(fill="both", expand=True, padx=LAYOUT["card_padding"], pady=10)
        
        # Chat messages
        self.chat_frame = ctk.CTkScrollableFrame(
            chat_card,
            fg_color=THEME["bg_primary"]
        )
        self.chat_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Welcome message
        self.add_system_message(
            "Welcome to Grok 4 Fast AI Chat!\n\n"
            "Features:\n"
            "• Ultra-fast responses (<1 second)\n"
            "• Minecraft-specific knowledge\n"
            "• Code assistance\n"
            "• Send responses to Minecraft chat\n\n"
            "Enter your OpenRouter API key above to start."
        )
    
    def create_input_area(self):
        """Create message input area"""
        input_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        input_card.pack(fill="x", padx=LAYOUT["card_padding"], pady=10)
        
        # Options row
        options_frame = ctk.CTkFrame(input_card, fg_color="transparent")
        options_frame.pack(fill="x", padx=20, pady=(15, 5))
        
        # Mode selector
        ctk.CTkLabel(
            options_frame,
            text="Mode:",
            font=THEME["font_body"],
            text_color=THEME["text_secondary"]
        ).pack(side="left", padx=(0, 10))
        
        self.mode_menu = ctk.CTkOptionMenu(
            options_frame,
            values=["General Chat", "Minecraft Helper", "Code Assistant"],
            font=THEME["font_body"],
            fg_color=THEME["accent"],
            button_color=THEME["accent"],
            button_hover_color=THEME["accent_hover"]
        )
        self.mode_menu.set("General Chat")
        self.mode_menu.pack(side="left", padx=(0, 20))
        
        # Minecraft chat toggle
        self.mc_chat_var = ctk.BooleanVar(value=False)
        self.mc_chat_checkbox = ctk.CTkCheckBox(
            options_frame,
            text="Send to Minecraft chat",
            variable=self.mc_chat_var,
            font=THEME["font_body"],
            text_color=THEME["text_primary"],
            fg_color=THEME["accent"]
        )
        self.mc_chat_checkbox.pack(side="left")
        
        # Clear button
        clear_btn = ctk.CTkButton(
            options_frame,
            text="Clear Chat",
            width=100,
            fg_color=THEME["error"],
            hover_color="#cc4444",
            command=self.clear_chat
        )
        clear_btn.pack(side="right")
        
        # Input row
        input_frame = ctk.CTkFrame(input_card, fg_color="transparent")
        input_frame.pack(fill="x", padx=20, pady=(5, 15))
        
        self.message_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Ask Grok anything...",
            font=THEME["font_body"],
            height=40
        )
        self.message_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.message_entry.bind("<Return>", lambda e: self.send_message())
        
        self.send_btn = ctk.CTkButton(
            input_frame,
            text="Send",
            width=100,
            height=40,
            fg_color=THEME["accent"],
            hover_color=THEME["accent_hover"],
            command=self.send_message,
            state="disabled"
        )
        self.send_btn.pack(side="left")
    
    def load_api_key(self):
        """Load API key from environment"""
        try:
            env_file = PROJECT_ROOT / ".env.grok"
            if env_file.exists():
                with open(env_file, 'r') as f:
                    for line in f:
                        if line.startswith("OPENROUTER_API_KEY="):
                            api_key = line.split('=', 1)[1].strip()
                            if api_key and api_key != "your-openrouter-api-key-here":
                                self.api_key_entry.insert(0, api_key)
                                # Auto-connect
                                self.after(100, self.connect_grok)
                                break
        except Exception as e:
            print(f"[Grok] Error loading API key: {e}")
    
    def connect_grok(self):
        """Connect to Grok API"""
        api_key = self.api_key_entry.get().strip()
        
        if not api_key:
            self.add_system_message("❌ Please enter your OpenRouter API key")
            return
        
        # Import GrokClient
        try:
            import sys
            sys.path.insert(0, str(PROJECT_ROOT))
            from grok_client import GrokClient
            
            # Create client
            self.grok_client = GrokClient(
                api_key=api_key,
                model="x-ai/grok-4-fast",
                max_tokens=200,
                timeout=30
            )
            
            # Update UI
            self.status_label.configure(
                text="● Connected",
                text_color=THEME["success"]
            )
            self.send_btn.configure(state="normal")
            
            self.add_system_message("✅ Connected to Grok 4 Fast! Ready to chat.")
            
            # Save API key
            self.save_api_key(api_key)
            
        except Exception as e:
            self.add_system_message(f"❌ Connection failed: {str(e)}")
            self.status_label.configure(
                text="● Connection Failed",
                text_color=THEME["error"]
            )
    
    def save_api_key(self, api_key: str):
        """Save API key to .env.grok"""
        try:
            env_file = PROJECT_ROOT / ".env.grok"
            
            # Read existing file or create new
            if env_file.exists():
                with open(env_file, 'r') as f:
                    lines = f.readlines()
            else:
                lines = []
            
            # Update or add API key line
            updated = False
            for i, line in enumerate(lines):
                if line.startswith("OPENROUTER_API_KEY="):
                    lines[i] = f"OPENROUTER_API_KEY={api_key}\n"
                    updated = True
                    break
            
            if not updated:
                lines.append(f"OPENROUTER_API_KEY={api_key}\n")
            
            # Write back
            with open(env_file, 'w') as f:
                f.writelines(lines)
            
        except Exception as e:
            print(f"[Grok] Error saving API key: {e}")
    
    def send_message(self):
        """Send message to Grok"""
        if not self.grok_client:
            self.add_system_message("❌ Not connected. Enter API key and click Connect.")
            return
        
        message = self.message_entry.get().strip()
        if not message:
            return
        
        # Clear input
        self.message_entry.delete(0, "end")
        
        # Disable send button
        self.send_btn.configure(state="disabled", text="Thinking...")
        
        # Add user message
        self.add_user_message(message)
        
        # Get response in thread
        thread = threading.Thread(
            target=self._get_response_thread,
            args=(message,),
            daemon=True
        )
        thread.start()
    
    def _get_response_thread(self, message: str):
        """Get response from Grok (in thread)"""
        try:
            # Get mode
            mode = self.mode_menu.get()
            
            # Determine system prompt based on mode
            if mode == "Minecraft Helper":
                system_prompt = """You are a helpful Minecraft assistant.
Help with Minecraft gameplay, server management, commands, and plugins.
Keep responses concise and practical."""
            elif mode == "Code Assistant":
                system_prompt = """You are a coding assistant for Minecraft development.
Help with Java, Bukkit/Spigot plugins, Forge mods, and server development.
Provide code examples when relevant."""
            else:
                system_prompt = None
            
            # Create async loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                # Get response
                response = loop.run_until_complete(
                    self.grok_client.ask(message, system=system_prompt)
                )
                
                # Add to conversation history
                self.conversation_history.append({
                    "role": "user",
                    "content": message
                })
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response
                })
                
                # Display response
                self.after(0, lambda: self.add_ai_message(response))
                
                # Send to Minecraft if enabled
                if self.mc_chat_var.get():
                    self.after(0, lambda: self.send_to_minecraft(response))
                
            finally:
                loop.close()
            
        except Exception as e:
            self.after(0, lambda: self.add_system_message(f"❌ Error: {str(e)}"))
        
        finally:
            # Re-enable send button
            self.after(0, lambda: self.send_btn.configure(state="normal", text="Send"))
    
    def add_system_message(self, message: str):
        """Add system message"""
        msg_frame = ctk.CTkFrame(
            self.chat_frame,
            fg_color=THEME["card_hover"],
            corner_radius=8
        )
        msg_frame.pack(fill="x", pady=5, padx=5)
        
        ctk.CTkLabel(
            msg_frame,
            text=message,
            font=THEME["font_small"],
            text_color=THEME["text_secondary"],
            anchor="w",
            justify="left",
            wraplength=600
        ).pack(padx=15, pady=10, anchor="w")
        
        # Auto-scroll
        self.chat_frame._parent_canvas.yview_moveto(1.0)
    
    def add_user_message(self, message: str):
        """Add user message"""
        msg_frame = ctk.CTkFrame(
            self.chat_frame,
            fg_color=THEME["accent"],
            corner_radius=8
        )
        msg_frame.pack(fill="x", pady=5, padx=5)
        
        header = ctk.CTkLabel(
            msg_frame,
            text="👤 You",
            font=("Segoe UI", 11, "bold"),
            text_color=THEME["text_primary"],
            anchor="w"
        )
        header.pack(padx=15, pady=(10, 2), anchor="w")
        
        ctk.CTkLabel(
            msg_frame,
            text=message,
            font=THEME["font_body"],
            text_color=THEME["text_primary"],
            anchor="w",
            justify="left",
            wraplength=600
        ).pack(padx=15, pady=(0, 10), anchor="w")
        
        # Auto-scroll
        self.chat_frame._parent_canvas.yview_moveto(1.0)
    
    def add_ai_message(self, message: str):
        """Add AI message"""
        msg_frame = ctk.CTkFrame(
            self.chat_frame,
            fg_color=THEME["success"],
            corner_radius=8
        )
        msg_frame.pack(fill="x", pady=5, padx=5)
        
        header = ctk.CTkLabel(
            msg_frame,
            text="🤖 Grok 4 Fast",
            font=("Segoe UI", 11, "bold"),
            text_color="#ffffff",
            anchor="w"
        )
        header.pack(padx=15, pady=(10, 2), anchor="w")
        
        ctk.CTkLabel(
            msg_frame,
            text=message,
            font=THEME["font_body"],
            text_color="#ffffff",
            anchor="w",
            justify="left",
            wraplength=600
        ).pack(padx=15, pady=(0, 10), anchor="w")
        
        # Auto-scroll
        self.chat_frame._parent_canvas.yview_moveto(1.0)
    
    def send_to_minecraft(self, message: str):
        """Send AI response to Minecraft chat"""
        try:
            from mcrcon import MCRcon
            from config import RCON_HOST, RCON_PORT, RCON_PASSWORD
            
            # Format message for Minecraft
            mc_message = f"[AI] {message[:200]}"  # Limit length
            
            # Send via RCON
            with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
                mcr.command(f'say {mc_message}')
            
            self.add_system_message("✅ Sent to Minecraft chat")
            
        except Exception as e:
            self.add_system_message(f"❌ Failed to send to Minecraft: {str(e)}")
    
    def clear_chat(self):
        """Clear chat history"""
        # Clear UI
        for widget in self.chat_frame.winfo_children():
            widget.destroy()
        
        # Clear history
        self.conversation_history = []
        
        # Clear Grok cache if exists
        if self.grok_client:
            self.grok_client.clear_cache()
        
        # Add welcome message
        self.add_system_message("Chat cleared. Start a new conversation!")

