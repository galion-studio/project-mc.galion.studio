"""
Server Mode Integration Examples
=================================

This file demonstrates how to integrate server mode checking
into your existing scripts and applications.

Author: galion.studio (Maciej Grajczyk)
"""

import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from server_mode_config import ServerMode, ServerModeManager
from ai_feature_controller import AIFeatureController


# ============================================================================
# EXAMPLE 1: Basic Mode Checking
# ============================================================================

def example_basic_mode_check():
    """
    Simple example of checking current server mode.
    """
    print("=== EXAMPLE 1: Basic Mode Check ===\n")
    
    # Create manager instance
    manager = ServerModeManager()
    
    # Get current mode
    current_mode = manager.get_current_mode()
    print(f"Current Mode: {current_mode.value}")
    
    # Check if AI is enabled
    if manager.is_ai_enabled():
        print("AI Features: ENABLED ✓")
    else:
        print("AI Features: DISABLED ✗")
    
    # Get server address
    host, port = manager.get_server_address()
    print(f"Server Address: {host}:{port}")
    
    print()


# ============================================================================
# EXAMPLE 2: Conditional AI Features
# ============================================================================

def example_conditional_ai():
    """
    Example of using AI features only when available.
    """
    print("=== EXAMPLE 2: Conditional AI Features ===\n")
    
    controller = AIFeatureController()
    
    # Check if AI is available
    if controller.is_ai_available():
        print("✓ AI is available")
        
        # Use AI features
        response = controller.get_ai_response("Hello!")
        if response:
            print(f"AI Response: {response}")
        else:
            print("AI response failed")
    else:
        print("✗ AI is not available")
        print(controller.get_disabled_features_message())
    
    print()


# ============================================================================
# EXAMPLE 3: Graceful Degradation
# ============================================================================

def get_help_message_with_fallback(question: str) -> str:
    """
    Get help message with graceful fallback.
    
    If AI is available, use AI response.
    Otherwise, return a predefined helpful message.
    
    Args:
        question: User's question
        
    Returns:
        str: Help message (AI-generated or fallback)
    """
    controller = AIFeatureController()
    
    # Try AI first
    if controller.is_ai_available():
        ai_response = controller.get_ai_response(question)
        if ai_response:
            return f"[AI] {ai_response}"
    
    # Fallback to predefined responses
    fallback_responses = {
        "how to play": "Connect to the server and start playing! Use /help for commands.",
        "commands": "Available commands: /help, /spawn, /home, /tpa",
        "rules": "Be respectful, no griefing, have fun!",
    }
    
    # Find matching response
    question_lower = question.lower()
    for key, response in fallback_responses.items():
        if key in question_lower:
            return f"[Fallback] {response}"
    
    return "[Fallback] Type /help for more information."


def example_graceful_degradation():
    """
    Example of graceful degradation when AI is unavailable.
    """
    print("=== EXAMPLE 3: Graceful Degradation ===\n")
    
    questions = [
        "how to play minecraft",
        "what commands are available",
        "what are the server rules"
    ]
    
    for question in questions:
        print(f"Q: {question}")
        answer = get_help_message_with_fallback(question)
        print(f"A: {answer}\n")


# ============================================================================
# EXAMPLE 4: Startup Script with Mode Detection
# ============================================================================

def example_startup_script():
    """
    Example of a startup script that adapts based on server mode.
    """
    print("=== EXAMPLE 4: Startup Script ===\n")
    
    manager = ServerModeManager()
    controller = AIFeatureController()
    
    print("Starting GALION.studio Server...")
    print("-" * 50)
    
    # Get mode configuration
    mode = manager.get_current_mode()
    config = manager.get_mode_config()
    
    print(f"Mode: {config['name']}")
    print(f"Description: {config['description']}")
    print(f"Server: {config['host']}:{config['port']}")
    print()
    
    # Check requirements
    print("Checking requirements...")
    
    # Internet check
    if manager.requires_internet():
        has_internet = manager.check_internet_connection()
        if has_internet:
            print("  ✓ Internet connection: OK")
        else:
            print("  ✗ Internet connection: FAILED")
            print("    Warning: Server requires internet!")
    else:
        print("  ✓ Internet: Not required")
    
    # AI check
    if controller.is_ai_available():
        print("  ✓ AI features: Available")
    else:
        print("  ✗ AI features: Not available")
    
    print()
    
    # Start services based on mode
    print("Starting services...")
    
    services = ["Minecraft Server", "PostgreSQL", "Redis"]
    
    # Add AI services only if available
    if controller.should_start_ai_bridge():
        services.append("AI Bridge")
    
    for service in services:
        print(f"  → Starting {service}...")
    
    print()
    print("✓ Server started successfully!")
    print(f"Connect at: {config['host']}:{config['port']}")


# ============================================================================
# EXAMPLE 5: Chat Bot with Mode Awareness
# ============================================================================

class ChatBot:
    """
    Example chat bot that adapts to server mode.
    """
    
    def __init__(self):
        self.controller = AIFeatureController()
        self.manager = ServerModeManager()
    
    def get_response(self, message: str) -> str:
        """
        Get chat response, using AI if available.
        
        Args:
            message: User message
            
        Returns:
            str: Bot response
        """
        # Check if AI is available
        if self.controller.is_ai_available():
            # Use AI for response
            response = self.controller.get_ai_response(message)
            if response:
                return response
        
        # Fallback to simple responses
        return self._get_simple_response(message)
    
    def _get_simple_response(self, message: str) -> str:
        """
        Simple rule-based responses (fallback).
        
        Args:
            message: User message
            
        Returns:
            str: Simple response
        """
        message = message.lower()
        
        if "hello" in message or "hi" in message:
            return "Hello! How can I help you today?"
        elif "help" in message:
            return "I can answer questions about the server. What do you need help with?"
        elif "ai" in message:
            mode = self.manager.get_current_mode()
            if mode == ServerMode.LOCAL:
                return "AI features are disabled in LOCAL mode. Use OFFICIAL mode for AI features."
            else:
                return "AI features are available! Ask me anything."
        else:
            return "I didn't quite understand that. Can you rephrase?"
    
    def get_status_message(self) -> str:
        """
        Get bot status message.
        
        Returns:
            str: Status message
        """
        status = self.controller.get_ai_status()
        
        if status['ai_available']:
            return "🤖 AI Bot (Powered by Grok 4 Fast)"
        else:
            return "🤖 Simple Bot (AI disabled)"


def example_chat_bot():
    """
    Example of a chat bot with mode awareness.
    """
    print("=== EXAMPLE 5: Chat Bot ===\n")
    
    bot = ChatBot()
    
    print(f"Bot Status: {bot.get_status_message()}\n")
    
    # Example conversation
    messages = [
        "Hello!",
        "Can you help me?",
        "Does this server have AI?",
    ]
    
    for message in messages:
        print(f"User: {message}")
        response = bot.get_response(message)
        print(f"Bot: {response}\n")


# ============================================================================
# EXAMPLE 6: Configuration Validator
# ============================================================================

def validate_configuration() -> bool:
    """
    Validate server configuration based on mode.
    
    Returns:
        bool: True if configuration is valid, False otherwise
    """
    print("=== EXAMPLE 6: Configuration Validator ===\n")
    
    manager = ServerModeManager()
    controller = AIFeatureController()
    
    mode = manager.get_current_mode()
    issues = []
    
    print(f"Validating configuration for {mode.value.upper()} mode...")
    print()
    
    # Check internet connectivity
    if manager.requires_internet():
        if not manager.check_internet_connection():
            issues.append("No internet connection (required for this mode)")
    
    # Check AI configuration
    if manager.is_ai_enabled():
        if not controller._has_valid_api_keys():
            issues.append("No valid API keys configured")
    
    # Report results
    if issues:
        print("❌ Configuration Issues Found:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        print()
        print("To fix:")
        print("  - Run SETUP-GROK-NOW.cmd to configure API keys")
        print("  - Check your internet connection")
        print("  - Or switch to LOCAL mode for offline play")
        return False
    else:
        print("✅ Configuration is valid!")
        return True


# ============================================================================
# RUN ALL EXAMPLES
# ============================================================================

def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("   SERVER MODE INTEGRATION EXAMPLES")
    print("="*60 + "\n")
    
    try:
        example_basic_mode_check()
        print("\n" + "-"*60 + "\n")
        
        example_conditional_ai()
        print("\n" + "-"*60 + "\n")
        
        example_graceful_degradation()
        print("\n" + "-"*60 + "\n")
        
        example_startup_script()
        print("\n" + "-"*60 + "\n")
        
        example_chat_bot()
        print("\n" + "-"*60 + "\n")
        
        validate_configuration()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

