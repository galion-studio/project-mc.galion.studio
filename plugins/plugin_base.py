#!/usr/bin/env python3
"""
Plugin Base Class
All plugins inherit from this base class

Features:
- Command registration
- Event hooks
- Configuration
- Logging
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import asyncio


class PluginBase(ABC):
    """
    Base class for all plugins
    
    Plugins can add custom commands, handle events, and extend functionality
    """
    
    def __init__(self, console_instance):
        """
        Initialize plugin
        
        Args:
            console_instance: Reference to main console instance
        """
        self.console = console_instance
        self.enabled = True
        self.config = {}
    
    @abstractmethod
    def get_name(self) -> str:
        """Return plugin name"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Return plugin description"""
        pass
    
    @abstractmethod
    def get_version(self) -> str:
        """Return plugin version"""
        pass
    
    def get_commands(self) -> Dict[str, dict]:
        """
        Return plugin commands
        
        Returns:
            Dict of commands: {
                "command_name": {
                    "description": "What it does",
                    "usage": "command [args]",
                    "handler": self.handle_command
                }
            }
        """
        return {}
    
    async def on_load(self):
        """Called when plugin is loaded"""
        pass
    
    async def on_unload(self):
        """Called when plugin is unloaded"""
        pass
    
    async def on_message(self, message: str) -> Optional[str]:
        """
        Called for every message (before routing)
        
        Args:
            message: User message
        
        Returns:
            Modified message or None to block
        """
        return message
    
    async def on_ai_response(self, question: str, response: str) -> Optional[str]:
        """
        Called after AI responds (can modify response)
        
        Args:
            question: Original question
            response: AI response
        
        Returns:
            Modified response or original
        """
        return response
    
    async def on_command_executed(self, command: str, result: str):
        """
        Called after any command executes
        
        Args:
            command: Command that was executed
            result: Result of command
        """
        pass
    
    def log(self, message: str, level: str = "INFO"):
        """
        Log a message
        
        Args:
            message: Log message
            level: Log level (INFO, WARNING, ERROR)
        """
        print(f"[{self.get_name()}] [{level}] {message}")


class PluginManager:
    """
    Plugin Manager
    Loads, manages, and coordinates plugins
    """
    
    def __init__(self, console_instance):
        """
        Initialize plugin manager
        
        Args:
            console_instance: Main console instance
        """
        self.console = console_instance
        self.plugins: List[PluginBase] = []
        self.commands: Dict[str, dict] = {}
    
    async def load_plugin(self, plugin_class):
        """
        Load a plugin
        
        Args:
            plugin_class: Plugin class to instantiate
        """
        try:
            plugin = plugin_class(self.console)
            await plugin.on_load()
            
            # Register commands
            for cmd_name, cmd_info in plugin.get_commands().items():
                self.commands[cmd_name] = {
                    **cmd_info,
                    "plugin": plugin
                }
            
            self.plugins.append(plugin)
            print(f"✓ Loaded plugin: {plugin.get_name()} v{plugin.get_version()}")
            
        except Exception as e:
            print(f"✗ Failed to load plugin: {e}")
    
    async def unload_plugin(self, plugin_name: str):
        """Unload a plugin"""
        for plugin in self.plugins:
            if plugin.get_name() == plugin_name:
                await plugin.on_unload()
                
                # Unregister commands
                self.commands = {
                    k: v for k, v in self.commands.items()
                    if v["plugin"] != plugin
                }
                
                self.plugins.remove(plugin)
                print(f"✓ Unloaded plugin: {plugin_name}")
                return
        
        print(f"✗ Plugin not found: {plugin_name}")
    
    async def handle_message(self, message: str) -> Optional[str]:
        """Process message through all plugins"""
        for plugin in self.plugins:
            if not plugin.enabled:
                continue
            message = await plugin.on_message(message)
            if message is None:
                return None  # Plugin blocked message
        return message
    
    async def handle_ai_response(self, question: str, response: str) -> str:
        """Process AI response through all plugins"""
        for plugin in self.plugins:
            if not plugin.enabled:
                continue
            response = await plugin.on_ai_response(question, response) or response
        return response
    
    async def handle_command(self, command: str) -> Optional[str]:
        """Handle plugin command"""
        if command in self.commands:
            cmd_info = self.commands[command]
            plugin = cmd_info["plugin"]
            
            if plugin.enabled:
                return await cmd_info["handler"]()
        
        return None
    
    def get_all_commands(self) -> Dict[str, dict]:
        """Get all plugin commands"""
        return self.commands
    
    def list_plugins(self) -> List[Dict[str, str]]:
        """List all loaded plugins"""
        return [
            {
                "name": p.get_name(),
                "version": p.get_version(),
                "description": p.get_description(),
                "enabled": p.enabled
            }
            for p in self.plugins
        ]

