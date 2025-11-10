"""
Minecraft Chat Bridge
Monitor Minecraft chat and respond with AI when triggered
"""

import asyncio
import time
from pathlib import Path
from typing import Optional, Callable
import re

from config import PROJECT_ROOT, LOGS_DIR, RCON_HOST, RCON_PORT, RCON_PASSWORD


class MinecraftChatBridge:
    """
    Bridge between Minecraft chat and Grok AI.
    Monitors logs for chat messages and responds via RCON.
    """
    
    def __init__(self, grok_client, trigger_word: str = "ai"):
        self.grok_client = grok_client
        self.trigger_word = trigger_word.lower()
        self.log_file = LOGS_DIR / "latest.log"
        self.last_position = 0
        self.is_running = False
        self.on_message_callback = None
    
    def set_message_callback(self, callback: Callable):
        """Set callback for when messages are processed"""
        self.on_message_callback = callback
    
    async def start(self):
        """Start monitoring Minecraft chat"""
        self.is_running = True
        print(f"[AI Bridge] Monitoring chat for '{self.trigger_word}' commands...")
        
        while self.is_running:
            try:
                if self.log_file.exists():
                    with open(self.log_file, 'r', encoding='utf-8', errors='ignore') as f:
                        f.seek(self.last_position)
                        new_lines = f.readlines()
                        self.last_position = f.tell()
                        
                        for line in new_lines:
                            await self.process_line(line)
                
                await asyncio.sleep(0.5)
            
            except Exception as e:
                print(f"[AI Bridge] Error: {e}")
                await asyncio.sleep(1)
    
    def stop(self):
        """Stop monitoring"""
        self.is_running = False
        print("[AI Bridge] Stopped")
    
    async def process_line(self, line: str):
        """Process log line for chat messages"""
        # Match chat pattern: [timestamp] [Server thread/INFO]: <PlayerName> message
        chat_pattern = r'\[.*?\]: <(\w+)> (.+)'
        match = re.search(chat_pattern, line)
        
        if not match:
            return
        
        player_name = match.group(1)
        message = match.group(2).strip()
        
        # Check if message starts with trigger word
        if not message.lower().startswith(self.trigger_word):
            return
        
        # Extract question (remove trigger word)
        question = message[len(self.trigger_word):].strip()
        
        if not question:
            return
        
        print(f"[AI Bridge] {player_name} asked: {question}")
        
        # Notify callback
        if self.on_message_callback:
            self.on_message_callback(f"[MC] {player_name}: {question}")
        
        # Get AI response
        try:
            response = await self.grok_client.ask_minecraft(question, player_name)
            
            # Send to Minecraft
            await self.send_to_minecraft(player_name, response)
            
            # Notify callback
            if self.on_message_callback:
                self.on_message_callback(f"[AI] {response}")
        
        except Exception as e:
            print(f"[AI Bridge] Error getting response: {e}")
            error_msg = "Sorry, I had trouble processing that."
            await self.send_to_minecraft(player_name, error_msg)
    
    async def send_to_minecraft(self, player_name: str, message: str):
        """Send message to Minecraft via RCON"""
        try:
            # Import here to avoid circular dependency
            from mcrcon import MCRcon
            
            # Format message
            formatted = f"[AI → {player_name}] {message}"
            
            # Truncate if too long
            if len(formatted) > 200:
                formatted = formatted[:197] + "..."
            
            # Send via RCON in executor (blocking operation)
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                self._send_rcon,
                formatted
            )
            
            print(f"[AI Bridge] Sent response to Minecraft")
        
        except Exception as e:
            print(f"[AI Bridge] Failed to send to Minecraft: {e}")
    
    def _send_rcon(self, message: str):
        """Send RCON command (blocking)"""
        try:
            from mcrcon import MCRcon
            
            with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
                mcr.command(f'say {message}')
        except Exception as e:
            print(f"[RCON] Error: {e}")


async def run_bridge():
    """Run the chat bridge standalone"""
    import sys
    import os
    from dotenv import load_dotenv
    
    # Load environment
    load_dotenv(PROJECT_ROOT / ".env.grok")
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key or api_key == "your-openrouter-api-key-here":
        print("[ERROR] OPENROUTER_API_KEY not set in .env.grok")
        print("Get your API key from: https://openrouter.ai/keys")
        return
    
    # Create Grok client
    sys.path.insert(0, str(PROJECT_ROOT))
    from grok_client import GrokClient
    
    client = GrokClient(api_key=api_key, model="x-ai/grok-4-fast", max_tokens=150)
    
    # Create bridge
    bridge = MinecraftChatBridge(client, trigger_word="ai")
    
    print("="*50)
    print("  MINECRAFT AI CHAT BRIDGE")
    print("  Grok 4 Fast Integration")
    print("="*50)
    print()
    print("Bridge is running!")
    print(f"Players can type: ai <question>")
    print("Example: ai what is redstone?")
    print()
    print("Press Ctrl+C to stop")
    print()
    
    try:
        await bridge.start()
    except KeyboardInterrupt:
        print("\n\nStopping bridge...")
        bridge.stop()
        await client.close()
        print("Done!")


if __name__ == "__main__":
    asyncio.run(run_bridge())

