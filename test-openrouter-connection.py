#!/usr/bin/env python3
"""
Quick test script to verify OpenRouter API connection
Tests the connection and reports detailed results
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Fix Windows console encoding for emojis
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Initialize colorama for Windows
init(autoreset=True)

# Load environment
load_dotenv(".env.grok")

# Import our Grok client
try:
    from grok_client import GrokClient
except ImportError:
    import sys
    sys.path.insert(0, '.')
    from grok_client import GrokClient


async def test_connection():
    """Test OpenRouter connection with detailed output"""
    
    print(f"\n{Fore.CYAN}{'=' * 70}")
    print(f"{Fore.GREEN}  🧪 OpenRouter API Connection Test")
    print(f"{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}\n")
    
    # Check API key
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    
    if not api_key or api_key == "your-openrouter-api-key-here":
        print(f"{Fore.RED}❌ ERROR: OPENROUTER_API_KEY not set in .env.grok{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   Get your API key from: https://openrouter.ai/keys{Style.RESET_ALL}")
        return False
    
    # Show API key (masked)
    masked_key = api_key[:15] + "..." + api_key[-10:]
    print(f"{Fore.BLUE}📋 API Key: {masked_key}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}🌐 Endpoint: https://openrouter.ai/api/v1/chat/completions{Style.RESET_ALL}")
    print(f"{Fore.BLUE}🤖 Model: x-ai/grok-beta{Style.RESET_ALL}\n")
    
    # Create client
    print(f"{Fore.CYAN}🔧 Initializing Grok client...{Style.RESET_ALL}")
    try:
        client = GrokClient(api_key=api_key)
        print(f"{Fore.GREEN}✓ Client initialized{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"{Fore.RED}❌ Failed to initialize client: {e}{Style.RESET_ALL}")
        return False
    
    # Test 1: Simple question
    print(f"{Fore.CYAN}📝 Test 1: Simple question{Style.RESET_ALL}")
    print(f"{Fore.BLUE}   Question: What is 2+2?{Style.RESET_ALL}")
    
    try:
        response = await client.ask("What is 2+2?")
        print(f"{Fore.GREEN}✓ Response received:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}   {response}{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"{Fore.RED}❌ Test 1 failed: {e}{Style.RESET_ALL}\n")
        await client.close()
        return False
    
    # Test 2: Minecraft-specific question
    print(f"{Fore.CYAN}📝 Test 2: Minecraft question{Style.RESET_ALL}")
    print(f"{Fore.BLUE}   Question: What is redstone?{Style.RESET_ALL}")
    
    try:
        response = await client.ask_minecraft("What is redstone?", "TestPlayer")
        print(f"{Fore.GREEN}✓ Response received:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}   {response}{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"{Fore.RED}❌ Test 2 failed: {e}{Style.RESET_ALL}\n")
        await client.close()
        return False
    
    # Show statistics
    print(f"{Fore.CYAN}{'=' * 70}")
    print(f"{Fore.GREEN}  📊 Statistics")
    print(f"{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}")
    stats = client.get_stats()
    print(f"{Fore.WHITE}Total requests:   {stats['total_requests']}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Cache hits:       {stats['cache_hits']}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Avg response:     {stats['avg_response_time']:.3f}s{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Fastest response: {stats['fastest_response']:.3f}s{Style.RESET_ALL}")
    print()
    
    # Cleanup
    await client.close()
    
    print(f"{Fore.GREEN}{'=' * 70}")
    print(f"{Fore.GREEN}  ✅ ALL TESTS PASSED!")
    print(f"{Fore.GREEN}  Your OpenRouter connection is working correctly!")
    print(f"{Fore.GREEN}{'=' * 70}{Style.RESET_ALL}\n")
    
    return True


async def main():
    """Entry point"""
    success = await test_connection()
    
    if not success:
        print(f"\n{Fore.YELLOW}🔧 Troubleshooting Tips:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1. Check your internet connection{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}2. Verify your API key at: https://openrouter.ai/keys{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}3. Check you have credits at: https://openrouter.ai/credits{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}4. Review error messages above for details{Style.RESET_ALL}\n")
        return 1
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Test interrupted{Style.RESET_ALL}")
        exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
        exit(1)

