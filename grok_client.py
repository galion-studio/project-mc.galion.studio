#!/usr/bin/env python3
"""
Grok-4 Fast API Client via OpenRouter
Ultra-fast AI client using OpenRouter's unified API with <1 second response times

Features:
- Grok-4 Fast via OpenRouter (better uptime, fallback options)
- Async/await for non-blocking operations
- Response caching for instant repeated queries
- Connection pooling for speed
- Timeout optimization (2 second max)
- OpenAI-compatible API format
- Access to 500+ models through one API
"""

import aiohttp
import asyncio
import time
from typing import Optional, Dict, List
from collections import OrderedDict
import json


class GrokClient:
    """
    Ultra-fast Grok API client optimized for <1 second responses
    
    Usage:
        client = GrokClient(api_key="xai-...")
        response = await client.ask("What is Minecraft?")
    """
    
    def __init__(
        self,
        api_key: str,
        model: str = "x-ai/grok-beta",
        timeout: int = 2,
        max_tokens: int = 100,
        temperature: float = 0.7,
        cache_size: int = 100
    ):
        """
        Initialize Grok client via OpenRouter
        
        Args:
            api_key: OpenRouter API key from openrouter.ai/keys
            model: Model to use (x-ai/grok-beta for Grok-4 Fast)
            timeout: Max timeout in seconds (default 2s)
            max_tokens: Max response length (default 100 for speed)
            temperature: Response creativity (0.7 for balanced)
            cache_size: Number of responses to cache
        """
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.max_tokens = max_tokens
        self.temperature = temperature
        
        # OpenRouter API endpoint (unified API for all models)
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # Response cache for instant repeated queries
        self.cache: OrderedDict = OrderedDict()
        self.cache_size = cache_size
        
        # Session for connection pooling (reuse connections)
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Statistics
        self.stats = {
            "total_requests": 0,
            "cache_hits": 0,
            "avg_response_time": 0.0,
            "fastest_response": float('inf'),
            "slowest_response": 0.0
        }
    
    async def _ensure_session(self):
        """Ensure HTTP session exists (connection pooling)"""
        if self.session is None or self.session.closed:
            # Create session with connection pooling
            connector = aiohttp.TCPConnector(
                limit=10,  # Max 10 concurrent connections
                ttl_dns_cache=300  # Cache DNS for 5 minutes
            )
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            )
    
    async def close(self):
        """Close HTTP session (cleanup)"""
        if self.session and not self.session.closed:
            await self.session.close()
    
    def _get_cache_key(self, prompt: str, system: Optional[str] = None) -> str:
        """Generate cache key from prompt and system message"""
        return f"{system or 'default'}:{prompt.lower().strip()}"
    
    def _add_to_cache(self, key: str, response: str):
        """Add response to cache (LRU eviction)"""
        if key in self.cache:
            # Move to end (most recently used)
            self.cache.move_to_end(key)
        else:
            self.cache[key] = response
            # Evict oldest if cache full
            if len(self.cache) > self.cache_size:
                self.cache.popitem(last=False)
    
    async def ask(
        self,
        prompt: str,
        system: Optional[str] = None,
        context: Optional[List[Dict[str, str]]] = None,
        use_cache: bool = True
    ) -> str:
        """
        Ask Grok a question with ultra-fast response
        
        Args:
            prompt: User question/prompt
            system: System prompt (optional)
            context: Conversation history (optional)
            use_cache: Whether to use response cache
        
        Returns:
            AI response text
        """
        start_time = time.time()
        
        # Check cache first (instant!)
        if use_cache:
            cache_key = self._get_cache_key(prompt, system)
            if cache_key in self.cache:
                self.stats["cache_hits"] += 1
                print(f"⚡ Cache hit! ({time.time() - start_time:.3f}s)")
                return self.cache[cache_key]
        
        # Ensure session exists
        await self._ensure_session()
        
        # Build messages array
        messages = []
        
        # Add system message if provided
        if system:
            messages.append({"role": "system", "content": system})
        
        # Add conversation context if provided
        if context:
            messages.extend(context)
        
        # Add user prompt
        messages.append({"role": "user", "content": prompt})
        
        # Build request payload
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "stream": False  # Non-streaming for simplicity
        }
        
        # Build headers (OpenRouter format)
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://mc.galion.studio",  # Optional: for rankings
            "X-Title": "Titan Minecraft Server"  # Optional: for rankings
        }
        
        try:
            # Make API request
            async with self.session.post(
                self.api_url,
                json=payload,
                headers=headers
            ) as response:
                
                # Handle errors
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Grok API error {response.status}: {error_text}")
                
                # Parse response
                data = await response.json()
                
                # Extract response text
                if "choices" in data and len(data["choices"]) > 0:
                    answer = data["choices"][0]["message"]["content"]
                else:
                    raise Exception("No response from Grok API")
                
                # Calculate response time
                elapsed = time.time() - start_time
                
                # Update statistics
                self.stats["total_requests"] += 1
                self.stats["avg_response_time"] = (
                    (self.stats["avg_response_time"] * (self.stats["total_requests"] - 1) + elapsed)
                    / self.stats["total_requests"]
                )
                self.stats["fastest_response"] = min(self.stats["fastest_response"], elapsed)
                self.stats["slowest_response"] = max(self.stats["slowest_response"], elapsed)
                
                # Cache response
                if use_cache:
                    cache_key = self._get_cache_key(prompt, system)
                    self._add_to_cache(cache_key, answer)
                
                print(f"⚡ Grok responded in {elapsed:.3f}s")
                
                return answer
                
        except asyncio.TimeoutError:
            raise Exception(f"Grok API timeout (>{self.timeout}s)")
        except Exception as e:
            raise Exception(f"Grok API error: {str(e)}")
    
    async def ask_minecraft(self, question: str, player_name: str = "Player") -> str:
        """
        Ask Grok with Minecraft-specific system prompt
        Optimized for short, chat-friendly responses
        
        Args:
            question: Player's question
            player_name: Name of player asking
        
        Returns:
            Short, chat-friendly response
        """
        system_prompt = f"""You are Console, an AI assistant in a Minecraft server.
You help with server questions, commands, plugins, and general Minecraft topics.

CRITICAL RULES:
- Keep responses ULTRA SHORT (max 2 sentences, 50 words)
- Minecraft chat is limited - be extremely concise
- Be friendly but brief
- If showing code/commands, show only the essential line

Player: {player_name}
Server: Titan (mc.galion.studio)
"""
        
        return await self.ask(question, system=system_prompt)
    
    async def ask_code(self, question: str) -> str:
        """
        Ask Grok with code/development system prompt
        
        Args:
            question: Development question
        
        Returns:
            Code-focused response
        """
        system_prompt = """You are a code assistant for Minecraft server development.
Focus on practical, working code examples.
Keep responses SHORT and actionable.
Use Python, Java, or Bash as appropriate."""
        
        return await self.ask(question, system=system_prompt)
    
    def get_stats(self) -> Dict:
        """Get client statistics"""
        return {
            **self.stats,
            "cache_size": len(self.cache),
            "cache_hit_rate": (
                self.stats["cache_hits"] / self.stats["total_requests"]
                if self.stats["total_requests"] > 0 else 0
            )
        }
    
    def clear_cache(self):
        """Clear response cache"""
        self.cache.clear()
        print("✓ Cache cleared")


# Example usage and testing
async def test_grok_client():
    """Test Grok client with sample queries"""
    import os
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv(".env.grok")
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key or api_key == "your-openrouter-api-key-here":
        print("⚠️  ERROR: OPENROUTER_API_KEY not set in .env.grok")
        print("Get your API key from: https://openrouter.ai/keys")
        return
    
    # Create client
    client = GrokClient(api_key=api_key)
    
    print("=" * 60)
    print("🚀 Testing Grok-4 Fast Client")
    print("=" * 60)
    print()
    
    try:
        # Test 1: Simple question
        print("📝 Test 1: Simple question")
        response = await client.ask_minecraft("What is redstone?", "TestPlayer")
        print(f"Response: {response}")
        print()
        
        # Test 2: Same question (should hit cache)
        print("📝 Test 2: Cache test (same question)")
        response = await client.ask_minecraft("What is redstone?", "TestPlayer")
        print(f"Response: {response}")
        print()
        
        # Test 3: Code question
        print("📝 Test 3: Code question")
        response = await client.ask_code("How to get player location in Bukkit?")
        print(f"Response: {response}")
        print()
        
        # Show statistics
        print("=" * 60)
        print("📊 Statistics")
        print("=" * 60)
        stats = client.get_stats()
        for key, value in stats.items():
            if isinstance(value, float):
                print(f"{key}: {value:.3f}")
            else:
                print(f"{key}: {value}")
        
    finally:
        await client.close()


if __name__ == "__main__":
    # Run test
    asyncio.run(test_grok_client())

