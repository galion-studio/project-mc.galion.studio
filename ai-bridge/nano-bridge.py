#!/usr/bin/env python3
"""
NANO AI BRIDGE - Minimal & Fast
Direct connection: Minecraft ↔ Grok-4 Fast

Ultra simple. Ultra fast. Just works.
Now powered by Grok for even faster responses!
"""

import subprocess
import re
import time
import requests
import threading
import os
from dotenv import load_dotenv

# ========================================
# CONFIGURATION (EDIT THESE)
# ========================================

# Load environment variables
load_dotenv(".env.grok")

# Your xAI API key (get from console.x.ai)
API_KEY = os.getenv("XAI_API_KEY", "your-xai-api-key-here")

# Trigger words (player types these to talk to AI)
TRIGGERS = ["console", "@ai", "hey console"]

# ========================================
# CORE FUNCTIONS
# ========================================

def send_to_minecraft(message):
    """Send message to Minecraft chat as [Console]"""
    try:
        cmd = ['docker', 'exec', 'titan-hub', 'rcon-cli', f'say §b[Console]§f {message}']
        subprocess.run(cmd, capture_output=True, timeout=5)
        print(f"→ Sent: {message}")
    except Exception as e:
        print(f"Error sending: {e}")

def ask_grok(question):
    """Ask Grok-4 Fast with speed optimization"""
    
    if API_KEY == "your-xai-api-key-here":
        return "⚠️ API key not configured! Set XAI_API_KEY in .env.grok"
    
    # Optimized prompt for SHORT, FAST responses
    system_prompt = """You are Console - an AI assistant in a Minecraft server.
CRITICAL: Keep responses VERY SHORT (max 2 sentences, 40 words).
Be helpful but ULTRA concise. Minecraft chat is limited.
If code: show only the key line, not full examples."""
    
    try:
        response = requests.post(
            'https://api.x.ai/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'grok-beta',  # Grok-4 Fast - ultra-fast responses!
                'max_tokens': 100,  # SHORT responses only
                'temperature': 0.7,
                'messages': [
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': question}
                ]
            },
            timeout=5  # Even faster timeout with Grok
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data['choices'][0]['message']['content']
            return answer
        else:
            return f"Error {response.status_code}"
            
    except Exception as e:
        return f"Error: {str(e)}"

def monitor_chat():
    """Monitor Minecraft logs for chat messages"""
    print("📊 Monitoring chat...")
    
    # Start tailing logs
    process = subprocess.Popen(
        ['docker', 'logs', '-f', 'titan-hub'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    
    for line in process.stdout:
        # Parse chat: [20:49:26 INFO]: [Not Secure] <galion.studio> hello
        match = re.search(r'<([^>]+)> (.+)', line)
        
        if match:
            player = match.group(1)
            message = match.group(2).strip()
            
            # Check if message is for AI
            if any(trigger in message.lower() for trigger in TRIGGERS):
                print(f"\n💬 {player}: {message}")
                
                # Process in background thread (don't block log monitoring)
                threading.Thread(
                    target=handle_question,
                    args=(player, message)
                ).start()

def handle_question(player, question):
    """Handle AI question in background"""
    
    # Show thinking
    send_to_minecraft("🤔...")
    
    # Get AI response (FAST!)
    start = time.time()
    answer = ask_grok(question)
    elapsed = time.time() - start
    
    print(f"🤖 Grok Response ({elapsed:.2f}s): {answer}")
    
    # Send to Minecraft (break into chunks if needed)
    send_chunked(answer)

def send_chunked(text, chunk_size=70):
    """Send long text in chat-friendly chunks"""
    words = text.split()
    chunk = []
    length = 0
    
    for word in words:
        if length + len(word) > chunk_size and chunk:
            send_to_minecraft(' '.join(chunk))
            time.sleep(0.3)  # Small delay between chunks
            chunk = []
            length = 0
        
        chunk.append(word)
        length += len(word) + 1
    
    if chunk:
        send_to_minecraft(' '.join(chunk))

# ========================================
# MAIN
# ========================================

if __name__ == "__main__":
    print("=" * 60)
    print("⚡ NANO AI BRIDGE - GROK EDITION")
    print("=" * 60)
    print(f"🤖 Model: Grok-4 Fast")
    print(f"🎮 Server: titan-hub")
    print(f"⚡ Optimized for: ULTRA SPEED")
    print("=" * 60)
    print()
    
    # Check API key
    if API_KEY == "your-xai-api-key-here":
        print("⚠️  WARNING: XAI_API_KEY not set!")
        print("Set it in .env.grok file")
        print("Get your API key from: https://console.x.ai/")
        print()
        print("Bridge will run but won't respond to questions.")
        print()
    
    # Send startup message
    send_to_minecraft("⚡ Grok AI Bridge connected!")
    send_to_minecraft("Type 'console <question>' to chat with me")
    
    # Start monitoring
    try:
        monitor_chat()
    except KeyboardInterrupt:
        print("\n\n✓ Bridge stopped")
        send_to_minecraft("Grok AI Bridge disconnected")

