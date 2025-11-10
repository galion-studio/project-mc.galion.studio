"""
Fix Minecraft installation by properly downloading all files
This will install Minecraft 1.20.1 and all required libraries
"""
import minecraft_launcher_lib
import subprocess
import uuid
import os
from pathlib import Path
import sys

# Configuration
MC_VERSION = "1.21.1"  # Updated to match server version
MINECRAFT_DIR = str(Path.home() / "AppData" / "Roaming" / "GalionLauncher" / "minecraft")

print("=" * 70)
print(" MINECRAFT INSTALLATION FIX")
print("=" * 70)
print()
print(f"Minecraft Version: {MC_VERSION}")
print(f"Install Directory: {MINECRAFT_DIR}")
print()

# Ensure directory exists
os.makedirs(MINECRAFT_DIR, exist_ok=True)

# Progress tracking
current_max = 0
current_progress = 0

def set_status(status: str):
    """Display status messages"""
    print(f"[STATUS] {status}")

def set_progress(progress: int):
    """Display progress"""
    global current_progress
    current_progress = progress
    # Only show every 5%
    if progress % 5 == 0:
        percentage = (progress / current_max * 100) if current_max > 0 else 0
        print(f"[PROGRESS] {progress}/{current_max} ({percentage:.1f}%)")

def set_max(new_max: int):
    """Set maximum progress value"""
    global current_max
    current_max = new_max
    print(f"[INFO] Total files to download: {new_max}")

# Create callback dictionary
callback = {
    "setStatus": set_status,
    "setProgress": set_progress,
    "setMax": set_max
}

print()
print("[STEP 1/3] Checking Minecraft installation...")
version_path = Path(MINECRAFT_DIR) / "versions" / MC_VERSION / f"{MC_VERSION}.jar"

if version_path.exists():
    print(f"[INFO] Found existing Minecraft JAR at: {version_path}")
    print("[INFO] Checking if it's complete...")
    
    # Check file size (should be around 20+ MB)
    size_mb = version_path.stat().st_size / (1024 * 1024)
    print(f"[INFO] JAR size: {size_mb:.2f} MB")
    
    if size_mb < 15:
        print("[WARNING] JAR file seems too small, will re-download")
        version_path.unlink()  # Delete incomplete file
    else:
        print("[OK] Minecraft JAR looks good")
else:
    print(f"[INFO] Minecraft not found, will download")

print()
print("[STEP 2/3] Installing Minecraft (this may take 2-5 minutes)...")
print()

try:
    minecraft_launcher_lib.install.install_minecraft_version(
        MC_VERSION,
        MINECRAFT_DIR,
        callback=callback
    )
    print()
    print("[OK] Minecraft installation complete!")
except Exception as e:
    print()
    print(f"[ERROR] Installation failed: {e}")
    print()
    print("TROUBLESHOOTING:")
    print("1. Check your internet connection")
    print("2. Make sure you have enough disk space (need ~500 MB)")
    print("3. Try running as Administrator")
    print("4. Temporarily disable antivirus")
    sys.exit(1)

print()
print("[STEP 3/3] Testing Minecraft launch...")
print()

# Test if we can build the launch command
USERNAME = "TestPlayer"

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
    print("[OK] Launch command built successfully")
except Exception as e:
    print(f"[ERROR] Failed to build launch command: {e}")
    sys.exit(1)

# Quick launch test
print()
print("[INFO] Testing Minecraft startup...")
print()

try:
    process = subprocess.Popen(
        command,
        cwd=MINECRAFT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print(f"[OK] Process started (PID: {process.pid})")
except Exception as e:
    print(f"[ERROR] Failed to start: {e}")
    sys.exit(1)

# Wait to see if it crashes immediately
import time
time.sleep(5)

if process.poll() is None:
    # Still running - success!
    print()
    print("=" * 70)
    print(" SUCCESS! MINECRAFT IS STARTING!")
    print("=" * 70)
    print()
    print("Minecraft window should appear shortly.")
    print()
    print("TO CONNECT TO YOUR SERVER:")
    print("1. Wait for Minecraft to fully load")
    print("2. Click 'Multiplayer'")
    print("3. Click 'Add Server'")
    print("4. Server Address: localhost:25565")
    print("5. Click 'Done' and join!")
    print()
    print("The game is running in the background...")
    print("You can close this window.")
    print()
    
    # Let it run
    sys.exit(0)
else:
    # Crashed - show error
    print()
    print("=" * 70)
    print(" ERROR: MINECRAFT CRASHED")
    print("=" * 70)
    print()
    
    stderr = process.stderr.read().decode('utf-8', errors='ignore')
    stdout = process.stdout.read().decode('utf-8', errors='ignore')
    
    if stderr:
        print("ERROR OUTPUT:")
        print(stderr[:1000])
    
    print()
    print("COMMON FIXES:")
    print("1. Install/Update Java: https://adoptium.net/")
    print("2. Update graphics drivers")
    print("3. Close other programs (especially other Minecraft instances)")
    print("4. Restart computer and try again")
    print()
    
    sys.exit(1)

