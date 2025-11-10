"""
INSTANT LAUNCHER - Super Fast Minecraft Launch
Optimized for minimal startup time - skips all non-essential checks
"""

import tkinter as tk
from tkinter import ttk
import minecraft_launcher_lib
import subprocess
import os
import sys
import uuid
import json
from pathlib import Path
import threading

# Configuration
SERVER_ADDRESS = "mc.galion.studio"
SERVER_NAME = "Galion Studio"
MC_VERSION = "1.21.1"

class InstantLauncher:
    """Ultra-fast launcher - minimal UI, maximum speed"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(f"{SERVER_NAME} - Instant Launcher")
        self.root.geometry("450x300")
        self.root.resizable(False, False)
        
        # Get minecraft directory
        self.minecraft_dir = self._get_launcher_dir()
        os.makedirs(self.minecraft_dir, exist_ok=True)
        
        # Setup minimal UI
        self._setup_ui()
        
        # Auto-launch immediately if everything is ready
        self.root.after(100, self._auto_launch)
    
    def _get_launcher_dir(self):
        """Get launcher directory"""
        if sys.platform == "win32":
            base_dir = os.getenv("APPDATA")
        else:
            base_dir = str(Path.home())
        return os.path.join(base_dir, "GalionLauncher", "minecraft")
    
    def _setup_ui(self):
        """Minimal UI - only essentials"""
        
        # Header
        header = tk.Frame(self.root, bg="#1a1a1a", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="⚡ INSTANT LAUNCH",
            font=("Arial", 18, "bold"),
            bg="#1a1a1a",
            fg="#00ff00"
        ).pack(pady=15)
        
        # Content
        content = tk.Frame(self.root, bg="#2a2a2a")
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Username (quick entry)
        tk.Label(
            content,
            text="Player Name:",
            font=("Arial", 10),
            bg="#2a2a2a",
            fg="white"
        ).pack(pady=(10, 5))
        
        self.username_var = tk.StringVar(value=self._load_username())
        username_entry = tk.Entry(
            content,
            textvariable=self.username_var,
            font=("Arial", 12),
            width=25,
            bg="#3a3a3a",
            fg="white",
            insertbackground="white"
        )
        username_entry.pack(pady=(0, 15))
        username_entry.bind('<Return>', lambda e: self._quick_launch())
        
        # Status
        self.status_var = tk.StringVar(value="Ready to launch")
        tk.Label(
            content,
            textvariable=self.status_var,
            font=("Arial", 9),
            bg="#2a2a2a",
            fg="#aaaaaa"
        ).pack(pady=10)
        
        # Launch button (BIG)
        self.launch_btn = tk.Button(
            content,
            text="🚀 LAUNCH NOW",
            font=("Arial", 14, "bold"),
            bg="#00aa00",
            fg="white",
            activebackground="#00ff00",
            activeforeground="black",
            cursor="hand2",
            padx=30,
            pady=15,
            command=self._quick_launch,
            relief=tk.FLAT
        )
        self.launch_btn.pack(pady=20)
        
        # Hint
        tk.Label(
            content,
            text="Press ENTER to launch instantly",
            font=("Arial", 8, "italic"),
            bg="#2a2a2a",
            fg="#666666"
        ).pack()
    
    def _load_username(self):
        """Load saved username"""
        config_file = os.path.join(self.minecraft_dir, "..", "launcher_config.json")
        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    return json.load(f).get("username", "Player")
            except:
                pass
        return "Player"
    
    def _save_username(self, username):
        """Save username"""
        config_file = os.path.join(self.minecraft_dir, "..", "launcher_config.json")
        try:
            os.makedirs(os.path.dirname(config_file), exist_ok=True)
            with open(config_file, "w") as f:
                json.dump({"username": username}, f)
        except:
            pass
    
    def _auto_launch(self):
        """Auto-launch if Minecraft is installed"""
        version_path = Path(self.minecraft_dir) / "versions" / MC_VERSION / f"{MC_VERSION}.jar"
        
        if version_path.exists() and version_path.stat().st_size > 15 * 1024 * 1024:
            # Minecraft is ready - show instant launch option
            self.status_var.set("✓ Ready for instant launch!")
            self.launch_btn.config(bg="#00ff00", fg="black")
        else:
            # First time - need to download
            self.status_var.set("First launch: Will download Minecraft")
            self.launch_btn.config(text="DOWNLOAD & LAUNCH")
    
    def _quick_launch(self):
        """Launch Minecraft immediately"""
        username = self.username_var.get().strip()
        if not username:
            username = "Player"
        
        self._save_username(username)
        
        # Check if installed
        version_path = Path(self.minecraft_dir) / "versions" / MC_VERSION / f"{MC_VERSION}.jar"
        
        if not version_path.exists() or version_path.stat().st_size < 15 * 1024 * 1024:
            # Need to download first
            self._download_and_launch(username)
        else:
            # Launch immediately
            self._launch_now(username)
    
    def _download_and_launch(self, username):
        """Download in background then launch"""
        self.launch_btn.config(state=tk.DISABLED, text="DOWNLOADING...")
        self.status_var.set("Downloading Minecraft...")
        
        def download():
            try:
                # Fast download with minimal callbacks
                minecraft_launcher_lib.install.install_minecraft_version(
                    MC_VERSION,
                    self.minecraft_dir
                )
                self.root.after(0, lambda: self._launch_now(username))
            except Exception as e:
                self.root.after(0, lambda: self._download_failed(str(e)))
        
        threading.Thread(target=download, daemon=True).start()
    
    def _download_failed(self, error):
        """Download failed"""
        self.status_var.set(f"Download failed: {error}")
        self.launch_btn.config(state=tk.NORMAL, text="RETRY", bg="#ff0000")
    
    def _launch_now(self, username):
        """Launch Minecraft NOW - no delays"""
        try:
            self.status_var.set("Launching...")
            self.launch_btn.config(text="LAUNCHING...", bg="#ffaa00")
            
            # Create player profile (offline mode - instant)
            options = {
                "username": username,
                "uuid": str(uuid.uuid4()),
                "token": ""
            }
            
            # Build launch command
            command = minecraft_launcher_lib.command.get_minecraft_command(
                MC_VERSION,
                self.minecraft_dir,
                options
            )
            
            # Launch in background
            subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            )
            
            # Show quick success and close
            self.status_var.set("✓ Minecraft launched!")
            self.launch_btn.config(text="✓ LAUNCHED", bg="#00ff00", fg="black")
            
            # Auto-close after 1 second
            self.root.after(1000, self.root.destroy)
            
        except Exception as e:
            self.status_var.set(f"Launch error: {e}")
            self.launch_btn.config(state=tk.NORMAL, text="RETRY", bg="#ff0000")


def main():
    """Main entry point"""
    root = tk.Tk()
    
    # Set dark theme
    root.configure(bg="#2a2a2a")
    
    # Create launcher
    launcher = InstantLauncher(root)
    
    # Run
    root.mainloop()


if __name__ == "__main__":
    main()

