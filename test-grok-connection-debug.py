#!/usr/bin/env python3
"""
Debug script to test Grok connection
This will help identify why Grok is not responding
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

async def test_connection():
    """Test Grok connection with detailed debugging"""
    print("=" * 60)
    print("GROK CONNECTION DEBUG TEST")
    print("=" * 60)
    print()
    
    # Step 1: Check if .env.grok exists
    print("[1] Checking .env.grok file...")
    env_file = PROJECT_ROOT / ".env.grok"
    if not env_file.exists():
        print("[X] ERROR: .env.grok file not found!")
        print("   Please copy env.grok.example to .env.grok and add your API key")
        return
    print("[OK] .env.grok file found")
    print()
    
    # Step 2: Load API key
    print("[2] Loading API key from .env.grok...")
    api_key = None
    try:
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith("OPENROUTER_API_KEY="):
                    api_key = line.split('=', 1)[1].strip()
                    break
        
        if not api_key:
            print("[X] ERROR: OPENROUTER_API_KEY not found in .env.grok")
            return
        
        if api_key == "your-openrouter-api-key-here":
            print("[X] ERROR: API key is still the default placeholder!")
            print("   Please get your API key from: https://openrouter.ai/keys")
            print("   Then add it to .env.grok file")
            return
        
        # Show first and last 4 characters for verification (security)
        masked_key = f"{api_key[:4]}...{api_key[-4:]}"
        print(f"[OK] API key loaded: {masked_key}")
        print()
        
    except Exception as e:
        print(f"[X] ERROR loading API key: {e}")
        return
    
    # Step 3: Import GrokClient
    print("[3] Importing GrokClient...")
    try:
        from grok_client import GrokClient
        print("[OK] GrokClient imported successfully")
        print()
    except Exception as e:
        print(f"[X] ERROR importing GrokClient: {e}")
        return
    
    # Step 4: Create client
    print("[4] Creating GrokClient instance...")
    try:
        client = GrokClient(
            api_key=api_key,
            model="x-ai/grok-4-fast",
            max_tokens=100,
            timeout=30  # 30 seconds timeout
        )
        print("[OK] GrokClient created")
        print(f"   Model: x-ai/grok-4-fast")
        print(f"   Timeout: 30 seconds")
        print(f"   Max tokens: 100")
        print()
    except Exception as e:
        print(f"[X] ERROR creating client: {e}")
        return
    
    # Step 5: Test simple query
    print("[5] Testing simple query...")
    print("   Sending: 'hi'")
    print("   Waiting for response...")
    print()
    
    try:
        # This is the actual test
        response = await client.ask("hi", system=None)
        
        print("=" * 60)
        print("[OK] SUCCESS! Grok is responding!")
        print("=" * 60)
        print(f"Response: {response}")
        print()
        
        # Show stats
        stats = client.get_stats()
        print("[STATS]")
        print(f"  Total requests: {stats['total_requests']}")
        print(f"  Response time: {stats['avg_response_time']:.3f}s")
        print()
        
    except asyncio.TimeoutError:
        print("[X] ERROR: Request timed out after 30 seconds")
        print("   Possible causes:")
        print("   1. Slow internet connection")
        print("   2. OpenRouter API is down")
        print("   3. API rate limit reached")
        print()
    except Exception as e:
        print("[X] ERROR during API call:")
        print(f"   {str(e)}")
        print()
        print("   Possible causes:")
        print("   1. Invalid API key")
        print("   2. Network connection issues")
        print("   3. OpenRouter API issues")
        print("   4. Model not available")
        print()
    
    finally:
        # Clean up
        await client.close()
        print("[6] Connection closed")
    
    print()
    print("=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    # Run the test
    try:
        asyncio.run(test_connection())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()

