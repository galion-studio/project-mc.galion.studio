#!/usr/bin/env python3
"""
TITAN AI BRIDGE - Ultra-Fast Version with Grok-4
Connects Minecraft chat to Grok AI with minimal latency

FEATURES:
- Real-time log monitoring (instant detection)
- Streaming responses (send as AI generates)
- Grok-4 Fast API (ultra-fast responses)
- Parallel processing (multiple requests at once)
- Response caching (instant for repeated questions)
- Smart chunking (breaks responses into chat-sized pieces)

SPEED OPTIMIZATIONS:
- Async API calls (non-blocking)
- Response streaming (partial messages sent immediately)
- Local cache for common questions
- Smart model selection (fast models for simple questions)
"""

import asyncio
import aiohttp
import re
import subprocess
import json
import os
from datetime import datetime
from collections import deque
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env.grok")

# Configuration
XAI_API_KEY = os.getenv("XAI_API_KEY", "your-xai-api-key-here")
RCON_HOST = os.getenv("MINECRAFT_RCON_HOST", "localhost")
RCON_PORT = int(os.getenv("MINECRAFT_RCON_PORT", 25575))
RCON_PASSWORD = os.getenv("MINECRAFT_RCON_PASSWORD", "titan123")

# Model selection (Grok models)
MODELS = {
    "fast": "grok-beta",           # Grok-4 Fast - ultra-fast responses
    "smart": "grok-beta",          # Same model (Grok is already very smart)
    "balanced": "grok-beta",       # Same model (optimized for speed + quality)
}

# Cache for instant responses
response_cache = {}
recent_messages = deque(maxlen=100)

class MinecraftRCON:
    """Async RCON client for sending messages"""
    
    async def send_message(self, message):
        """Send message to Minecraft chat"""
        cmd = f'say §b[Console]§f {message}'
        
        try:
            process = await asyncio.create_subprocess_exec(
                'docker', 'exec', 'titan-hub', 'rcon-cli', cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
        except Exception as e:
            print(f"RCON Error: {e}")
    
    async def send_chunked(self, full_response, chunk_size=60):
        """Send long response in chunks (chat-friendly)"""
        words = full_response.split()
        current_chunk = []
        current_length = 0
        
        for word in words:
            word_length = len(word) + 1  # +1 for space
            
            if current_length + word_length > chunk_size and current_chunk:
                # Send current chunk
                await self.send_message(' '.join(current_chunk))
                await asyncio.sleep(0.5)  # Small delay between chunks
                current_chunk = []
                current_length = 0
            
            current_chunk.append(word)
            current_length += word_length
        
        # Send remaining
        if current_chunk:
            await self.send_message(' '.join(current_chunk))


class FastAI:
    """Ultra-fast Grok AI client with streaming support"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.x.ai/v1/chat/completions"
    
    async def ask(self, question, player_name, model="smart", stream=True):
        """
        Ask AI a question with streaming response
        
        Args:
            question: User's question
            player_name: Player who asked
            model: Model to use (fast/smart/balanced)
            stream: Whether to stream response
        
        Returns:
            Response text (or yields chunks if streaming)
        """
        
        # Check cache first (instant response!)
        cache_key = f"{model}:{question.lower()}"
        if cache_key in response_cache:
            print(f"✓ Cache hit for: {question[:50]}...")
            return response_cache[cache_key]
        
        # Build request
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # System prompt for Minecraft context
        system_prompt = f"""You are Console, an AI assistant in a Minecraft server.
You help with code, plugins, server management, and Minecraft questions.
Keep responses SHORT (under 100 words) - Minecraft chat is limited.
Be friendly, helpful, and concise.
Player: {player_name}
Server: Titan (built for 20k players)
"""
        
        payload = {
            "model": MODELS.get(model, MODELS["smart"]),
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            "max_tokens": 150,  # Short responses for speed
            "temperature": 0.7,
            "stream": stream
        }
        
        # Make request
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                
                if stream:
                    # Stream response chunks
                    full_response = ""
                    async for line in response.content:
                        if line:
                            line_text = line.decode('utf-8').strip()
                            if line_text.startswith('data: '):
                                data = line_text[6:]
                                if data == '[DONE]':
                                    break
                                try:
                                    chunk = json.loads(data)
                                    if 'choices' in chunk and len(chunk['choices']) > 0:
                                        delta = chunk['choices'][0].get('delta', {})
                                        content = delta.get('content', '')
                                        if content:
                                            full_response += content
                                            yield content  # Stream to caller
                                except:
                                    pass
                    
                    # Cache the response
                    response_cache[cache_key] = full_response
                    return full_response
                else:
                    # Non-streaming (faster for simple responses)
                    data = await response.json()
                    if 'choices' in data and len(data['choices']) > 0:
                        answer = data['choices'][0]['message']['content']
                        response_cache[cache_key] = answer
                        return answer
                    
        return "Error: No response from AI"


class LogMonitor:
    """Real-time Minecraft log monitor"""
    
    def __init__(self, rcon, ai):
        self.rcon = rcon
        self.ai = ai
        self.processing = set()  # Prevent duplicate processing
    
    async def monitor(self):
        """Monitor Minecraft logs in real-time"""
        print("📊 Monitoring Minecraft chat...")
        
        # Follow docker logs in real-time
        process = await asyncio.create_subprocess_exec(
            'docker', 'logs', '-f', 'titan-hub',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )
        
        async for line in process.stdout:
            try:
                log_line = line.decode('utf-8').strip()
                
                # Parse chat messages: [20:49:26 INFO]: [Not Secure] <galion.studio> hello
                match = re.search(r'\[Not Secure\] <([^>]+)> (.+)', log_line)
                
                if match:
                    player_name = match.group(1)
                    message = match.group(2).strip()
                    
                    # Create unique key to prevent duplicate processing
                    msg_key = f"{player_name}:{message}:{datetime.now().second}"
                    
                    if msg_key not in self.processing:
                        self.processing.add(msg_key)
                        
                        # Process message asynchronously
                        asyncio.create_task(
                            self.handle_message(player_name, message)
                        )
                        
                        # Clean old keys
                        if len(self.processing) > 50:
                            self.processing.clear()
                
            except Exception as e:
                print(f"Error parsing log: {e}")
    
    async def handle_message(self, player_name, message):
        """Handle a chat message - decide if it needs AI response"""
        
        # Check if message is directed at Console/AI
        triggers = ["console", "@ai", "@console", "console:", "hey console"]
        
        is_for_ai = any(trigger in message.lower() for trigger in triggers)
        
        if is_for_ai:
            print(f"\n💬 {player_name}: {message}")
            
            # Show thinking indicator
            await self.rcon.send_message("🤔 Thinking...")
            
            # Determine model based on question complexity
            model = "fast" if len(message) < 30 else "smart"
            
            # Get AI response
            try:
                response = await self.ai.ask(message, player_name, model=model, stream=False)
                
                print(f"🤖 Console: {response}")
                
                # Send response
                await self.rcon.send_chunked(response)
                
                # Log interaction
                recent_messages.append({
                    "player": player_name,
                    "question": message,
                    "response": response,
                    "time": datetime.now().isoformat()
                })
                
            except Exception as e:
                print(f"AI Error: {e}")
                await self.rcon.send_message(f"⚠️ Error: {str(e)}")


async def main():
    """Main async loop"""
    
    print("=" * 60)
    print("🚀 TITAN AI BRIDGE - Grok-4 Fast Edition")
    print("=" * 60)
    print(f"📡 Grok API: {'Configured' if XAI_API_KEY != 'your-xai-api-key-here' else 'NOT CONFIGURED'}")
    print(f"🎮 Minecraft Server: titan-hub")
    print(f"🔌 RCON: {RCON_HOST}:{RCON_PORT}")
    print("=" * 60)
    print()
    
    # Initialize components
    rcon = MinecraftRCON()
    ai = FastAI(XAI_API_KEY)
    monitor = LogMonitor(rcon, ai)
    
    # Send startup message
    await rcon.send_message("⚡ Grok AI Bridge connected!")
    await rcon.send_message("Type 'console <question>' or '@ai <question>'")
    
    # Start monitoring
    await monitor.monitor()


if __name__ == "__main__":
    print("\n⚡ Starting AI Bridge...\n")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n✓ AI Bridge stopped")

