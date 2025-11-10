"""
Galion Studio Minecraft Launcher - TLauncher Style
A standalone launcher that downloads Minecraft directly

This launcher downloads Minecraft automatically without needing
the official Microsoft launcher (like TLauncher does)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import minecraft_launcher_lib
import subprocess
import os
import sys
import uuid
import json
from pathlib import Path
import threading

# Server configuration
SERVER_ADDRESS = "mc.galion.studio"
SERVER_NAME = "Galion Studio"
LAUNCHER_VERSION = "2.0.0"
DEFAULT_MC_VERSION = "1.20.1"  # Change this to your preferred version


class MinecraftDownloader:
    """Handles Minecraft downloading and installation"""
    
    def __init__(self, minecraft_dir, callback=None):
        """Initialize downloader with callback for progress updates"""
        self.minecraft_dir = minecraft_dir
        self.callback = callback
        self.current_max = 0
        
    def download_minecraft(self, version):
        """Download specified Minecraft version"""
        try:
            # Set up callback for progress tracking
            callback = {
                "setStatus": self._set_status,
                "setProgress": self._set_progress,
                "setMax": self._set_max
            }
            
            # Install Minecraft version
            minecraft_launcher_lib.install.install_minecraft_version(
                version,
                self.minecraft_dir,
                callback=callback
            )
            
            return True
        except Exception as e:
            print(f"Error downloading Minecraft: {e}")
            return False
    
    def _set_status(self, status):
        """Update status message"""
        if self.callback:
            self.callback("status", status)
    
    def _set_progress(self, progress):
        """Update progress bar"""
        if self.callback:
            self.callback("progress", progress)
    
    def _set_max(self, max_value):
        """Set maximum progress value"""
        self.current_max = max_value
        if self.callback:
            self.callback("max", max_value)


class TLauncherStyleLauncher:
    """Main launcher class - TLauncher style"""
    
    def __init__(self, root):
        """Initialize the launcher window"""
        self.root = root
        self.root.title(f"{SERVER_NAME} Launcher v{LAUNCHER_VERSION}")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Minecraft directory (custom, not official .minecraft)
        self.minecraft_dir = self._get_launcher_dir()
        os.makedirs(self.minecraft_dir, exist_ok=True)
        
        # Setup UI
        self._setup_ui()
        
        # Check if Minecraft is downloaded
        self.root.after(100, self._check_minecraft_installed)
    
    def _get_launcher_dir(self):
        """Get custom launcher directory (not .minecraft)"""
        if sys.platform == "win32":
            base_dir = os.getenv("APPDATA")
        else:
            base_dir = str(Path.home())
        
        # Use custom directory name (like TLauncher does)
        return os.path.join(base_dir, "GalionLauncher", "minecraft")
    
    def _setup_ui(self):
        """Create all UI elements"""
        
        # Header
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text=SERVER_NAME,
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Main content
        content_frame = tk.Frame(self.root, bg="#ecf0f1")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Server info
        info_frame = tk.LabelFrame(
            content_frame,
            text="Server Information",
            font=("Arial", 10, "bold"),
            bg="#ecf0f1",
            padx=10,
            pady=10
        )
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            info_frame,
            text=f"Server: {SERVER_ADDRESS}",
            font=("Arial", 10),
            bg="#ecf0f1"
        ).pack(anchor=tk.W)
        
        tk.Label(
            info_frame,
            text=f"Minecraft Version: {DEFAULT_MC_VERSION}",
            font=("Arial", 10),
            bg="#ecf0f1"
        ).pack(anchor=tk.W)
        
        # Username input
        username_frame = tk.LabelFrame(
            content_frame,
            text="Player Name",
            font=("Arial", 10, "bold"),
            bg="#ecf0f1",
            padx=10,
            pady=10
        )
        username_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.username_var = tk.StringVar(value=self._load_username())
        username_entry = tk.Entry(
            username_frame,
            textvariable=self.username_var,
            font=("Arial", 11),
            width=30
        )
        username_entry.pack()
        
        # Progress frame (hidden by default)
        self.progress_frame = tk.LabelFrame(
            content_frame,
            text="Download Progress",
            font=("Arial", 10, "bold"),
            bg="#ecf0f1",
            padx=10,
            pady=10
        )
        
        self.progress_status = tk.StringVar(value="")
        tk.Label(
            self.progress_frame,
            textvariable=self.progress_status,
            font=("Arial", 9),
            bg="#ecf0f1"
        ).pack()
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='determinate',
            length=400
        )
        self.progress_bar.pack(pady=5)
        
        # Status label
        self.status_var = tk.StringVar(value="Checking Minecraft installation...")
        status_label = tk.Label(
            content_frame,
            textvariable=self.status_var,
            font=("Arial", 9),
            bg="#ecf0f1",
            fg="#7f8c8d"
        )
        status_label.pack(pady=(0, 15))
        
        # Launch button
        self.launch_button = tk.Button(
            content_frame,
            text="CHECKING...",
            font=("Arial", 14, "bold"),
            bg="#95a5a6",
            fg="white",
            activebackground="#7f8c8d",
            activeforeground="white",
            cursor="hand2",
            padx=40,
            pady=15,
            state=tk.DISABLED,
            command=self._launch_or_download
        )
        self.launch_button.pack()
        
        # Info label
        tk.Label(
            content_frame,
            text="This launcher downloads Minecraft automatically",
            font=("Arial", 8, "italic"),
            bg="#ecf0f1",
            fg="#95a5a6"
        ).pack(pady=(10, 0))
        
        # Footer
        footer_label = tk.Label(
            self.root,
            text=f"Launcher v{LAUNCHER_VERSION} - TLauncher Style",
            font=("Arial", 8),
            fg="#95a5a6"
        )
        footer_label.pack(side=tk.BOTTOM, pady=5)
    
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
        """Save username for next launch"""
        config_file = os.path.join(self.minecraft_dir, "..", "launcher_config.json")
        try:
            os.makedirs(os.path.dirname(config_file), exist_ok=True)
            with open(config_file, "w") as f:
                json.dump({"username": username}, f)
        except Exception as e:
            print(f"Failed to save username: {e}")
    
    def _check_minecraft_installed(self):
        """Check if Minecraft is already installed"""
        version_path = os.path.join(
            self.minecraft_dir,
            "versions",
            DEFAULT_MC_VERSION
        )
        
        if os.path.exists(version_path):
            # Minecraft is installed
            self.status_var.set(f"✓ Minecraft {DEFAULT_MC_VERSION} ready!")
            self.launch_button.config(
                text="PLAY",
                bg="#27ae60",
                state=tk.NORMAL
            )
            self.minecraft_installed = True
        else:
            # Need to download
            self.status_var.set(f"Minecraft {DEFAULT_MC_VERSION} not found - Ready to download")
            self.launch_button.config(
                text="DOWNLOAD & INSTALL",
                bg="#3498db",
                state=tk.NORMAL
            )
            self.minecraft_installed = False
    
    def _launch_or_download(self):
        """Launch Minecraft or download if not installed"""
        username = self.username_var.get().strip()
        
        if not username:
            messagebox.showerror("Error", "Please enter a player name")
            return
        
        self._save_username(username)
        
        if self.minecraft_installed:
            self._launch_minecraft(username)
        else:
            self._download_minecraft()
    
    def _download_minecraft(self):
        """Download Minecraft in background thread"""
        self.launch_button.config(state=tk.DISABLED, text="DOWNLOADING...")
        self.progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Start download in background thread
        thread = threading.Thread(target=self._download_thread)
        thread.daemon = True
        thread.start()
    
    def _download_thread(self):
        """Background thread for downloading"""
        downloader = MinecraftDownloader(
            self.minecraft_dir,
            callback=self._update_progress
        )
        
        success = downloader.download_minecraft(DEFAULT_MC_VERSION)
        
        # Update UI on main thread
        self.root.after(0, self._download_complete, success)
    
    def _update_progress(self, type, value):
        """Update progress bar (called from download thread)"""
        def update():
            if type == "status":
                self.progress_status.set(value)
            elif type == "max":
                self.progress_bar["maximum"] = value
            elif type == "progress":
                self.progress_bar["value"] = value
        
        self.root.after(0, update)
    
    def _download_complete(self, success):
        """Called when download is complete"""
        self.progress_frame.pack_forget()
        
        if success:
            self.minecraft_installed = True
            self.status_var.set(f"✓ Download complete! Ready to play")
            self.launch_button.config(
                text="PLAY",
                bg="#27ae60",
                state=tk.NORMAL
            )
            messagebox.showinfo(
                "Success",
                f"Minecraft {DEFAULT_MC_VERSION} downloaded successfully!\n\n"
                "Click PLAY to start the game."
            )
        else:
            self.status_var.set("Download failed")
            self.launch_button.config(
                text="RETRY DOWNLOAD",
                bg="#e74c3c",
                state=tk.NORMAL
            )
            messagebox.showerror(
                "Download Failed",
                "Failed to download Minecraft.\n\n"
                "Please check your internet connection and try again."
            )
    
    def _launch_minecraft(self, username):
        """Launch Minecraft with offline authentication"""
        try:
            self.status_var.set("Launching Minecraft...")
            self.launch_button.config(state=tk.DISABLED)
            
            # Create offline player profile (like TLauncher)
            options = {
                "username": username,
                "uuid": str(uuid.uuid4()),  # Generate random UUID for offline mode
                "token": ""  # Empty token for offline mode
            }
            
            # Get launch command
            command = minecraft_launcher_lib.command.get_minecraft_command(
                DEFAULT_MC_VERSION,
                self.minecraft_dir,
                options
            )
            
            # Add server auto-connect (optional)
            # command.extend(["--server", SERVER_ADDRESS])
            
            # Launch Minecraft
            subprocess.Popen(command)
            
            # Show success message
            messagebox.showinfo(
                "Launching",
                f"Minecraft is starting!\n\n"
                f"Server: {SERVER_ADDRESS}\n"
                f"Player: {username}\n\n"
                "To connect:\n"
                "1. Go to Multiplayer\n"
                f"2. Add server: {SERVER_ADDRESS}\n"
                "3. Join and play!"
            )
            
            # Close launcher
            self.root.after(2000, self.root.destroy)
            
        except Exception as e:
            messagebox.showerror(
                "Launch Error",
                f"Failed to launch Minecraft:\n{str(e)}"
            )
            self.status_var.set("Launch failed")
            self.launch_button.config(state=tk.NORMAL)


def main():
    """Main entry point"""
    
    # Create main window
    root = tk.Tk()
    
    # Create launcher
    launcher = TLauncherStyleLauncher(root)
    
    # Start GUI
    root.mainloop()


if __name__ == "__main__":
    main()

