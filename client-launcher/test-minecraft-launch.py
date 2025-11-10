"""
Simple test script to launch Minecraft and see errors
"""
import minecraft_launcher_lib
import subprocess
import uuid
import os
from pathlib import Path

# Configuration
USERNAME = "TestPlayer"
MC_VERSION = "1.21.1"  # Updated to match server version
MINECRAFT_DIR = str(Path.home() / "AppData" / "Roaming" / "GalionLauncher" / "minecraft")

print("=" * 60)
print("MINECRAFT LAUNCHER DEBUG TEST")
print("=" * 60)
print()
print(f"Username: {USERNAME}")
print(f"MC Version: {MC_VERSION}")
print(f"Minecraft Dir: {MINECRAFT_DIR}")
print()

# Ensure directory exists
os.makedirs(MINECRAFT_DIR, exist_ok=True)

# Check if version is installed
print("[1/4] Checking if Minecraft is installed...")
version_path = Path(MINECRAFT_DIR) / "versions" / MC_VERSION
if not version_path.exists():
    print(f"[!] Minecraft {MC_VERSION} not found!")
    print(f"[!] Installing now... (this may take a few minutes)")
    print()
    
    # Install callback
    def set_status(status: str):
        print(f"  {status}")
    
    def set_progress(progress: int):
        if progress % 10 == 0:
            print(f"  Progress: {progress}%")
    
    def set_max(new_max: int):
        pass
    
    callback = {
        "setStatus": set_status,
        "setProgress": set_progress,
        "setMax": set_max
    }
    
    minecraft_launcher_lib.install.install_minecraft_version(
        MC_VERSION,
        MINECRAFT_DIR,
        callback=callback
    )
    print("[OK] Minecraft installed!")
else:
    print("[OK] Minecraft already installed")

print()
print("[2/4] Building launch command...")

# Offline authentication
options = {
    "username": USERNAME,
    "uuid": str(uuid.uuid4()),
    "token": ""
}

try:
    command = minecraft_launcher_lib.command.get_minecraft_command(
        MC_VERSION,
        MINECRAFT_DIR,
        options
    )
    print("[OK] Command built successfully")
except Exception as e:
    print(f"[ERROR] Failed to build command: {e}")
    exit(1)

print()
print("[3/4] Launching Minecraft...")
print(f"Command: {' '.join(command[:5])}... (truncated)")
print()

try:
    process = subprocess.Popen(
        command,
        cwd=MINECRAFT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print("[OK] Process started")
    print(f"[OK] PID: {process.pid}")
except Exception as e:
    print(f"[ERROR] Failed to start: {e}")
    exit(1)

print()
print("[4/4] Checking if Minecraft started successfully...")
print("Waiting 5 seconds...")
print()

import time
time.sleep(5)

# Check if still running
if process.poll() is None:
    print("=" * 60)
    print("[SUCCESS] Minecraft is running!")
    print("=" * 60)
    print()
    print("Minecraft should now be opening on your screen.")
    print("If you see the Minecraft window, it's working!")
    print()
    print("Press Ctrl+C to stop monitoring...")
    
    # Keep monitoring
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped monitoring.")
else:
    # Process ended - capture error
    print("=" * 60)
    print("[ERROR] Minecraft crashed immediately!")
    print("=" * 60)
    print()
    
    stdout_data = process.stdout.read().decode('utf-8', errors='ignore')
    stderr_data = process.stderr.read().decode('utf-8', errors='ignore')
    
    if stderr_data:
        print("ERROR OUTPUT:")
        print("-" * 60)
        print(stderr_data[:2000])  # First 2000 chars
        print("-" * 60)
    
    if stdout_data:
        print()
        print("STANDARD OUTPUT:")
        print("-" * 60)
        print(stdout_data[:2000])
        print("-" * 60)
    
    print()
    print("COMMON FIXES:")
    print("1. Install Java 17 or newer from: https://adoptium.net/")
    print("2. Make sure no other Minecraft is running")
    print("3. Try running this script as Administrator")
    print()

