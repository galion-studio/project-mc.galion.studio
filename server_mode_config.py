"""
GALION.studio Server Mode Configuration
========================================

This module manages two server modes:
1. LOCAL MODE - Self-hosted, offline, no AI features
2. OFFICIAL MODE - Full-featured with AI, requires internet

Author: galion.studio (Maciej Grajczyk)
"""

import os
import json
from enum import Enum
from typing import Dict, Optional

# Define server modes as enum for type safety
class ServerMode(Enum):
    """
    Two server modes available:
    - LOCAL: Offline server, no AI features
    - OFFICIAL: Online server with all premium features
    """
    LOCAL = "local"
    OFFICIAL = "official"

# Configuration for each server mode
SERVER_MODE_CONFIG = {
    ServerMode.LOCAL: {
        "name": "Self-Hosted Local Server",
        "description": "Run your own server on localhost. No internet required.",
        "host": "localhost",
        "port": 25565,
        "ai_enabled": False,
        "requires_internet": False,
        "features": [
            "✓ Fully offline",
            "✓ Self-hosted control",
            "✓ Open source",
            "✗ No AI features",
            "✗ Limited to local network"
        ],
        "icon": "🏠"
    },
    ServerMode.OFFICIAL: {
        "name": "Official GALION.studio Server",
        "description": "Connect to official server with full AI features.",
        "host": "mc.galion.studio",  # Replace with your actual server address
        "port": 25565,
        "ai_enabled": True,
        "requires_internet": True,
        "features": [
            "✓ Full AI integration (Grok 4 Fast)",
            "✓ Multiplayer community",
            "✓ Premium features",
            "✓ Automatic updates",
            "✓ 24/7 uptime"
        ],
        "icon": "🌐"
    }
}

class ServerModeManager:
    """
    Manages server mode configuration and persistence.
    
    This class handles:
    - Loading and saving server mode preferences
    - Validating server mode settings
    - Checking internet connectivity for online mode
    """
    
    def __init__(self, config_dir: str = None):
        """
        Initialize the server mode manager.
        
        Args:
            config_dir: Directory to store configuration. Defaults to current directory.
        """
        # Set configuration directory
        if config_dir is None:
            config_dir = os.path.join(os.getcwd(), "config")
        
        self.config_dir = config_dir
        self.config_file = os.path.join(config_dir, "server_mode.json")
        
        # Create config directory if it doesn't exist
        os.makedirs(config_dir, exist_ok=True)
    
    def get_current_mode(self) -> ServerMode:
        """
        Get the currently configured server mode.
        
        Returns:
            ServerMode: Current mode (LOCAL or OFFICIAL)
        """
        config = self._load_config()
        mode_str = config.get("mode", ServerMode.LOCAL.value)
        
        # Convert string to enum, default to LOCAL if invalid
        try:
            return ServerMode(mode_str)
        except ValueError:
            return ServerMode.LOCAL
    
    def set_mode(self, mode: ServerMode) -> bool:
        """
        Set the server mode.
        
        Args:
            mode: ServerMode to set (LOCAL or OFFICIAL)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            config = self._load_config()
            config["mode"] = mode.value
            self._save_config(config)
            return True
        except Exception as e:
            print(f"Error setting server mode: {e}")
            return False
    
    def get_mode_config(self, mode: Optional[ServerMode] = None) -> Dict:
        """
        Get configuration for a specific server mode.
        
        Args:
            mode: ServerMode to get config for. If None, returns current mode config.
            
        Returns:
            Dict: Configuration dictionary for the mode
        """
        if mode is None:
            mode = self.get_current_mode()
        
        return SERVER_MODE_CONFIG[mode].copy()
    
    def is_ai_enabled(self) -> bool:
        """
        Check if AI features are enabled in current mode.
        
        Returns:
            bool: True if AI is enabled, False otherwise
        """
        mode = self.get_current_mode()
        return SERVER_MODE_CONFIG[mode]["ai_enabled"]
    
    def requires_internet(self) -> bool:
        """
        Check if current mode requires internet connection.
        
        Returns:
            bool: True if internet required, False otherwise
        """
        mode = self.get_current_mode()
        return SERVER_MODE_CONFIG[mode]["requires_internet"]
    
    def get_server_address(self) -> tuple[str, int]:
        """
        Get server address (host and port) for current mode.
        
        Returns:
            tuple: (host, port) for the server
        """
        config = self.get_mode_config()
        return config["host"], config["port"]
    
    def check_internet_connection(self) -> bool:
        """
        Check if internet connection is available.
        Used to verify if OFFICIAL mode can be used.
        
        Returns:
            bool: True if internet is available, False otherwise
        """
        import socket
        
        try:
            # Try to connect to Google DNS (8.8.8.8) on port 53
            # This is a reliable way to check internet connectivity
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False
    
    def _load_config(self) -> Dict:
        """
        Load configuration from JSON file.
        
        Returns:
            Dict: Configuration dictionary
        """
        if not os.path.exists(self.config_file):
            # Return default config if file doesn't exist
            return {"mode": ServerMode.LOCAL.value}
        
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return {"mode": ServerMode.LOCAL.value}
    
    def _save_config(self, config: Dict) -> None:
        """
        Save configuration to JSON file.
        
        Args:
            config: Configuration dictionary to save
        """
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")


# Convenience functions for quick access
def get_current_server_mode() -> ServerMode:
    """Get current server mode (convenience function)"""
    manager = ServerModeManager()
    return manager.get_current_mode()

def is_ai_enabled() -> bool:
    """Check if AI is enabled in current mode (convenience function)"""
    manager = ServerModeManager()
    return manager.is_ai_enabled()

def get_server_address() -> tuple[str, int]:
    """Get server address for current mode (convenience function)"""
    manager = ServerModeManager()
    return manager.get_server_address()


# Example usage and testing
if __name__ == "__main__":
    print("=== GALION.studio Server Mode Configuration ===\n")
    
    # Create manager instance
    manager = ServerModeManager()
    
    # Display current mode
    current_mode = manager.get_current_mode()
    print(f"Current Mode: {current_mode.value.upper()}")
    print(f"AI Enabled: {manager.is_ai_enabled()}")
    print(f"Internet Required: {manager.requires_internet()}")
    print(f"Server Address: {manager.get_server_address()}")
    
    print("\n--- Available Modes ---\n")
    
    # Display all available modes
    for mode in ServerMode:
        config = manager.get_mode_config(mode)
        print(f"{config['icon']} {config['name']}")
        print(f"   {config['description']}")
        print(f"   Host: {config['host']}:{config['port']}")
        print(f"   Features:")
        for feature in config['features']:
            print(f"      {feature}")
        print()
    
    # Test internet connection
    print("--- Connection Test ---")
    has_internet = manager.check_internet_connection()
    print(f"Internet Available: {'Yes ✓' if has_internet else 'No ✗'}")
    
    if not has_internet and manager.get_current_mode() == ServerMode.OFFICIAL:
        print("⚠️  Warning: OFFICIAL mode requires internet connection!")

