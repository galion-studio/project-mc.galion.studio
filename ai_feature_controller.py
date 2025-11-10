"""
AI Feature Controller
=====================

This module controls AI features based on server mode.
In LOCAL mode: AI features are disabled
In OFFICIAL mode: AI features are enabled

This ensures the open source version can run without API keys
while the official server has full AI capabilities.

Author: galion.studio (Maciej Grajczyk)
"""

import os
import sys
from typing import Optional, Dict, Any
from server_mode_config import ServerMode, ServerModeManager, is_ai_enabled


class AIFeatureController:
    """
    Controls AI feature availability based on server mode.
    
    This class provides:
    - AI feature enable/disable logic
    - API key validation
    - Graceful degradation when AI is unavailable
    - Feature flags for different AI components
    """
    
    def __init__(self):
        """Initialize the AI feature controller"""
        self.manager = ServerModeManager()
        self._api_keys = {}
        self._load_api_keys()
    
    def is_ai_available(self) -> bool:
        """
        Check if AI features are available in current mode.
        
        Returns:
            bool: True if AI is available, False otherwise
        """
        # Check server mode first
        if not self.manager.is_ai_enabled():
            return False
        
        # Check if we have required API keys
        if not self._has_valid_api_keys():
            return False
        
        # Check internet connection for online AI services
        if self.manager.requires_internet():
            return self.manager.check_internet_connection()
        
        return True
    
    def get_ai_status(self) -> Dict[str, Any]:
        """
        Get comprehensive AI status information.
        
        Returns:
            Dict with AI status details
        """
        mode = self.manager.get_current_mode()
        
        status = {
            "mode": mode.value,
            "ai_enabled": self.manager.is_ai_enabled(),
            "ai_available": self.is_ai_available(),
            "has_api_keys": self._has_valid_api_keys(),
            "internet_required": self.manager.requires_internet(),
            "internet_available": self.manager.check_internet_connection(),
            "features": {
                "grok": self._is_grok_available(),
                "chat": self._is_chat_available(),
                "console": self._is_console_available()
            }
        }
        
        return status
    
    def _load_api_keys(self):
        """Load API keys from environment files"""
        # Try to load from .env.grok
        grok_env = ".env.grok"
        if os.path.exists(grok_env):
            try:
                with open(grok_env, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            self._api_keys[key.strip()] = value.strip()
            except Exception as e:
                print(f"Warning: Could not load API keys: {e}")
    
    def _has_valid_api_keys(self) -> bool:
        """
        Check if we have valid API keys for AI services.
        
        Returns:
            bool: True if API keys are present and valid
        """
        # Check for OpenRouter API key (used for Grok)
        openrouter_key = self._api_keys.get('OPENROUTER_API_KEY', '')
        
        # Key should exist and not be a placeholder
        if not openrouter_key or openrouter_key == 'your-api-key-here':
            return False
        
        return True
    
    def _is_grok_available(self) -> bool:
        """Check if Grok AI is available"""
        return self.is_ai_available()
    
    def _is_chat_available(self) -> bool:
        """Check if AI chat is available"""
        return self.is_ai_available()
    
    def _is_console_available(self) -> bool:
        """Check if AI console is available"""
        return self.is_ai_available()
    
    def get_ai_response(self, prompt: str) -> Optional[str]:
        """
        Get AI response if available, otherwise return None.
        
        This is a wrapper that gracefully handles unavailable AI.
        
        Args:
            prompt: User prompt for AI
            
        Returns:
            str: AI response, or None if AI unavailable
        """
        if not self.is_ai_available():
            return None
        
        # Import AI client only if available
        # This prevents import errors when AI is disabled
        try:
            from grok_client import get_grok_response
            return get_grok_response(prompt)
        except ImportError:
            print("Warning: AI client not available")
            return None
        except Exception as e:
            print(f"Error getting AI response: {e}")
            return None
    
    def should_start_ai_bridge(self) -> bool:
        """
        Check if AI bridge should be started.
        
        Returns:
            bool: True if AI bridge should start, False otherwise
        """
        return self.is_ai_available()
    
    def get_disabled_features_message(self) -> str:
        """
        Get a user-friendly message explaining why AI is disabled.
        
        Returns:
            str: Message explaining AI status
        """
        if self.is_ai_available():
            return "✓ AI features are enabled and available"
        
        # Determine why AI is disabled
        reasons = []
        
        if not self.manager.is_ai_enabled():
            reasons.append("Current server mode (LOCAL) does not include AI features")
        
        if not self._has_valid_api_keys():
            reasons.append("API keys not configured (run SETUP-GROK-NOW.cmd)")
        
        if self.manager.requires_internet() and not self.manager.check_internet_connection():
            reasons.append("No internet connection available")
        
        if not reasons:
            reasons.append("Unknown reason")
        
        message = "✗ AI features are disabled:\n"
        for i, reason in enumerate(reasons, 1):
            message += f"  {i}. {reason}\n"
        
        message += "\nTo enable AI features:\n"
        message += "  - Use START-OFFICIAL-SERVER.cmd for full AI features\n"
        message += "  - Run SETUP-GROK-NOW.cmd to configure API keys\n"
        message += "  - Ensure internet connection is available\n"
        
        return message


# Convenience function for checking AI availability
def check_ai_available() -> bool:
    """
    Quick check if AI is available (convenience function).
    
    Returns:
        bool: True if AI is available, False otherwise
    """
    controller = AIFeatureController()
    return controller.is_ai_available()


# Function to conditionally import AI modules
def import_ai_module(module_name: str, fallback=None):
    """
    Conditionally import AI modules only if AI is enabled.
    
    This prevents import errors in LOCAL mode where AI dependencies
    might not be installed.
    
    Args:
        module_name: Name of module to import
        fallback: Fallback value if import fails
        
    Returns:
        Imported module or fallback value
    """
    controller = AIFeatureController()
    
    if not controller.is_ai_available():
        print(f"AI disabled - skipping import of {module_name}")
        return fallback
    
    try:
        return __import__(module_name)
    except ImportError as e:
        print(f"Could not import {module_name}: {e}")
        return fallback


# Display AI status when run directly
if __name__ == "__main__":
    print("=== AI Feature Controller Status ===\n")
    
    controller = AIFeatureController()
    status = controller.get_ai_status()
    
    print(f"Server Mode: {status['mode'].upper()}")
    print(f"AI Enabled in Mode: {status['ai_enabled']}")
    print(f"AI Available: {status['ai_available']}")
    print(f"Has API Keys: {status['has_api_keys']}")
    print(f"Internet Required: {status['internet_required']}")
    print(f"Internet Available: {status['internet_available']}")
    
    print("\nAI Features:")
    print(f"  - Grok: {'✓' if status['features']['grok'] else '✗'}")
    print(f"  - Chat: {'✓' if status['features']['chat'] else '✗'}")
    print(f"  - Console: {'✓' if status['features']['console'] else '✗'}")
    
    print("\n" + "="*40)
    print(controller.get_disabled_features_message())
    
    # Test AI response (only if available)
    if controller.is_ai_available():
        print("\nTesting AI response...")
        response = controller.get_ai_response("Hello, test!")
        if response:
            print(f"AI Response: {response[:100]}...")
    
    # Check if AI bridge should start
    print(f"\nShould start AI bridge: {controller.should_start_ai_bridge()}")

