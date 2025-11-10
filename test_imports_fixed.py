#!/usr/bin/env python3
"""Quick test to verify all imports work"""

import sys
import os

print("Testing imports...")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Python path: {sys.path}")
print()

try:
    from dotenv import load_dotenv
    print("[OK] dotenv imported")
except ImportError as e:
    print(f"[FAIL] dotenv import failed: {e}")

try:
    from colorama import init, Fore, Style
    print("[OK] colorama imported")
except ImportError as e:
    print(f"[FAIL] colorama import failed: {e}")

try:
    from prompt_toolkit import PromptSession
    print("[OK] prompt_toolkit imported")
except ImportError as e:
    print(f"[FAIL] prompt_toolkit import failed: {e}")

try:
    import asyncio
    print("[OK] asyncio imported")
except ImportError as e:
    print(f"[FAIL] asyncio import failed: {e}")

try:
    import aiohttp
    print("[OK] aiohttp imported")
except ImportError as e:
    print(f"[FAIL] aiohttp import failed: {e}")

print()
print("Testing custom modules...")

try:
    from grok_client import GrokClient
    print("[OK] grok_client imported")
except ImportError as e:
    print(f"[FAIL] grok_client import failed: {e}")
    print("  Make sure grok-client.py exists in the current directory")

try:
    from rcon_client import RconClient
    print("[OK] rcon_client imported")
except ImportError as e:
    print(f"[FAIL] rcon_client import failed: {e}")
    print("  Make sure rcon-client.py exists in the current directory")

try:
    from project_controller import ProjectController
    print("[OK] project_controller imported")
except ImportError as e:
    print(f"[FAIL] project_controller import failed: {e}")
    print("  Make sure project-controller.py exists in the current directory")

print()
print("Testing .env.grok file...")

try:
    load_dotenv(".env.grok")
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    if api_key and api_key != "your-openrouter-api-key-here":
        print(f"[OK] API key configured (starts with: {api_key[:10]}...)")
    else:
        print("[WARN] API key not set in .env.grok")
        print("  Edit .env.grok and add your OpenRouter API key")
except Exception as e:
    print(f"[FAIL] Error loading .env.grok: {e}")

print()
print("All import tests complete!")

