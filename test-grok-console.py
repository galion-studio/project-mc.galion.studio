#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Grok 4 Fast Communication - Console Demo
Shows real-time AI responses from Grok in the terminal
"""

import sys
import os
import requests
import time
from datetime import datetime
from dotenv import load_dotenv

# Fix Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Load environment
load_dotenv(".env.grok")

API_KEY = os.getenv("OPENROUTER_API_KEY", "")
MODEL = os.getenv("GROK_MODEL", "x-ai/grok-4-fast")

def print_header():
    print("\n" + "=" * 60)
    print("  GROK 4 FAST - LIVE CONSOLE TEST")
    print("  Admin: galion.studio")
    print("=" * 60 + "\n")

def ask_grok(question):
    """Ask Grok 4 Fast a question"""
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] You: {question}")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Grok: Thinking...", end="\r")
    
    start = time.time()
    
    try:
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': MODEL,
                'messages': [
                    {'role': 'user', 'content': question}
                ],
                'max_tokens': 200
            },
            timeout=10
        )
        
        elapsed = time.time() - start
        
        if response.status_code == 200:
            answer = response.json()['choices'][0]['message']['content']
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Grok: {answer}")
            print(f"                Response time: {elapsed:.2f}s")
            return answer
        else:
            print(f"\n[ERROR] Status {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print(f"\n[ERROR] {e}")
        return None

def main():
    """Run interactive console test"""
    
    print_header()
    
    # Check API key
    if not API_KEY or API_KEY == "your-openrouter-api-key-here":
        print("[ERROR] No API key configured!")
        print("Please set OPENROUTER_API_KEY in .env.grok")
        return
    
    print(f"Model: {MODEL}")
    print(f"API: OpenRouter")
    print(f"Admin: galion.studio\n")
    print("-" * 60)
    
    # Test questions
    questions = [
        "Hello! Can you introduce yourself in 15 words?",
        "What makes you fast compared to other AI models?",
        "Give me a quick tip for Minecraft in 10 words"
    ]
    
    print("\nRunning automated tests...\n")
    
    for i, question in enumerate(questions, 1):
        print(f"\n--- Test {i}/3 ---")
        answer = ask_grok(question)
        
        if answer:
            print("\n" + "-" * 60)
            time.sleep(1)
        else:
            print("\n[!] Test failed, stopping...")
            break
    
    # Interactive mode
    print("\n" + "=" * 60)
    print("  INTERACTIVE MODE - Type your questions")
    print("  (Type 'exit' or 'quit' to stop)")
    print("=" * 60 + "\n")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\n[INFO] Goodbye from galion.studio!")
                break
                
            if not user_input:
                continue
                
            ask_grok(user_input)
            
        except KeyboardInterrupt:
            print("\n\n[INFO] Interrupted. Goodbye!")
            break
        except EOFError:
            break

if __name__ == "__main__":
    main()

