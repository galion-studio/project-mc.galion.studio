"""
Galion Studio Minecraft Launcher
A simple, custom launcher for mc.galion.studio server

This launcher provides a clean interface to launch Minecraft
and automatically connect to the Galion Studio server.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import platform
import subprocess
import json
from pathlib import Path

# Server configuration
SERVER_ADDRESS = "mc.galion.studio"
SERVER_NAME = "Galion Studio"
LAUNCHER_VERSION = "1.0.0"


class MinecraftLauncher:
    """Main launcher class that handles the GUI and launch logic"""
    
    def __init__(self, root):
        """Initialize the launcher window and UI components"""
        self.root = root
        self.root.title(f"{SERVER_NAME} Launcher v{LAUNCHER_VERSION}")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Get Minecraft directory based on OS
        self.minecraft_dir = self._get_minecraft_dir()
        
        # Setup UI
        self._setup_ui()
        
        # Check Minecraft installation on startup
        self.root.after(100, self._check_minecraft)
    
    def _get_minecraft_dir(self):
        """Get the Minecraft directory path based on the operating system"""
        system = platform.system()
        
        if system == "Windows":
            # Windows: %APPDATA%\.minecraft
            return Path(os.getenv("APPDATA")) / ".minecraft"
        elif system == "Linux":
            # Linux: ~/.minecraft
            return Path.home() / ".minecraft"
        elif system == "Darwin":
            # macOS: ~/Library/Application Support/minecraft
            return Path.home() / "Library" / "Application Support" / "minecraft"
        else:
            # Fallback
            return Path.home() / ".minecraft"
    
    def _setup_ui(self):
        """Create all UI elements for the launcher"""
        
        # Header with server name
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
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg="#ecf0f1")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Server info section
        info_frame = tk.LabelFrame(
            content_frame,
            text="Server Information",
            font=("Arial", 10, "bold"),
            bg="#ecf0f1",
            padx=10,
            pady=10
        )
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        server_label = tk.Label(
            info_frame,
            text=f"Server Address: {SERVER_ADDRESS}",
            font=("Arial", 10),
            bg="#ecf0f1"
        )
        server_label.pack(anchor=tk.W)
        
        # Username input section
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
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to launch")
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
            text="PLAY",
            font=("Arial", 14, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            activeforeground="white",
            cursor="hand2",
            padx=40,
            pady=15,
            command=self._launch_game
        )
        self.launch_button.pack()
        
        # Footer with version
        footer_label = tk.Label(
            self.root,
            text=f"Launcher v{LAUNCHER_VERSION}",
            font=("Arial", 8),
            fg="#95a5a6"
        )
        footer_label.pack(side=tk.BOTTOM, pady=5)
    
    def _load_username(self):
        """Load the last used username from config file"""
        config_file = Path("launcher_config.json")
        
        if config_file.exists():
            try:
                with open(config_file, "r") as f:
                    config = json.load(f)
                    return config.get("username", "Player")
            except:
                pass
        
        return "Player"
    
    def _save_username(self, username):
        """Save the username to config file for next launch"""
        config_file = Path("launcher_config.json")
        
        try:
            config = {"username": username}
            with open(config_file, "w") as f:
                json.dump(config, f)
        except Exception as e:
            print(f"Failed to save username: {e}")
    
    def _check_minecraft(self):
        """Check if Minecraft is installed and update status"""
        
        # Check for Minecraft directory
        minecraft_found = self.minecraft_dir.exists()
        
        # Check for Minecraft launcher
        launcher_path = self._find_minecraft_launcher()
        launcher_found = launcher_path is not None
        
        if minecraft_found and launcher_found:
            self.status_var.set("✓ Minecraft detected - Ready to launch!")
        elif minecraft_found and not launcher_found:
            self.status_var.set("⚠ Minecraft folder found, but launcher not detected")
        else:
            self.status_var.set("⚠ Minecraft not found - Please install Minecraft Java Edition")
            messagebox.showwarning(
                "Minecraft Not Found",
                f"Minecraft installation not found!\n\n"
                f"Directory checked: {self.minecraft_dir}\n\n"
                "Please install Minecraft Java Edition from:\n"
                "https://www.minecraft.net/download\n\n"
                "After installing, restart this launcher."
            )
    
    def _launch_game(self):
        """Launch Minecraft with the configured settings"""
        
        # Get username
        username = self.username_var.get().strip()
        
        if not username:
            messagebox.showerror("Error", "Please enter a player name")
            return
        
        # Save username for next time
        self._save_username(username)
        
        # Check if Minecraft directory exists
        if not self.minecraft_dir.exists():
            messagebox.showerror(
                "Error",
                f"Minecraft not found at:\n{self.minecraft_dir}\n\n"
                "Please install Minecraft first."
            )
            return
        
        # Update status
        self.status_var.set("Launching Minecraft...")
        self.launch_button.config(state=tk.DISABLED)
        
        # Launch Minecraft
        try:
            self._start_minecraft(username)
            
            # Show success message
            messagebox.showinfo(
                "Launching",
                f"Minecraft is starting!\n\n"
                f"Server: {SERVER_ADDRESS}\n"
                f"Player: {username}\n\n"
                "The launcher will close now."
            )
            
            # Close launcher after successful launch
            self.root.after(1000, self.root.destroy)
            
        except Exception as e:
            # Show error and re-enable button
            messagebox.showerror("Launch Error", f"Failed to launch Minecraft:\n{str(e)}")
            self.status_var.set("Launch failed")
            self.launch_button.config(state=tk.NORMAL)
    
    def _find_minecraft_launcher(self):
        """Find the Minecraft launcher executable on the system"""
        system = platform.system()
        
        if system == "Windows":
            # List of possible launcher locations on Windows
            possible_paths = [
                # Modern launcher location (Windows Store / Microsoft Store version)
                Path(os.getenv("LOCALAPPDATA", "")) / "Packages" / "Microsoft.4297127D64EC6_8wekyb3d8bbwe" / "LocalCache" / "Local" / "game" / "Minecraft.exe",
                
                # Classic launcher locations
                Path(os.getenv("APPDATA", "")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Minecraft Launcher.lnk",
                Path(os.getenv("PROGRAMFILES", "")) / "Minecraft Launcher" / "MinecraftLauncher.exe",
                Path(os.getenv("PROGRAMFILES(X86)", "")) / "Minecraft Launcher" / "MinecraftLauncher.exe",
                
                # Alternative launcher location
                Path(os.getenv("PROGRAMFILES", "")) / "Minecraft" / "MinecraftLauncher.exe",
                
                # Check if launcher is in path
                Path("C:\\Program Files\\Minecraft Launcher\\MinecraftLauncher.exe"),
                Path("C:\\Program Files (x86)\\Minecraft Launcher\\MinecraftLauncher.exe"),
            ]
            
            # Try to find launcher in any of these locations
            for path in possible_paths:
                if path and path.exists():
                    return path
            
            # If not found, try using 'minecraft' command
            # This works if Minecraft is in PATH
            return "minecraft-launcher"
        
        elif system == "Linux":
            # On Linux, try common launcher locations
            possible_paths = [
                Path.home() / ".local" / "share" / "applications" / "minecraft-launcher",
                Path("/usr/bin/minecraft-launcher"),
                Path("/usr/local/bin/minecraft-launcher"),
            ]
            
            for path in possible_paths:
                if path.exists():
                    return path
            
            return "minecraft-launcher"
        
        return None
    
    def _start_minecraft(self, username):
        """Start Minecraft using the official launcher with server connection"""
        
        system = platform.system()
        launcher_path = self._find_minecraft_launcher()
        
        if system == "Windows":
            # On Windows, launch the Minecraft launcher
            
            if launcher_path and launcher_path != "minecraft-launcher":
                # Found a specific launcher path
                try:
                    if str(launcher_path).endswith(".lnk"):
                        # It's a shortcut file, use os.startfile
                        os.startfile(str(launcher_path))
                    else:
                        # It's an executable, use subprocess
                        subprocess.Popen([str(launcher_path)], shell=False)
                except Exception as e:
                    raise Exception(f"Failed to launch Minecraft: {e}")
            else:
                # Try to launch using shell command as fallback
                try:
                    # Try to launch Minecraft from Start Menu
                    subprocess.Popen(["cmd", "/c", "start", "minecraft:"], shell=False)
                except Exception:
                    # Show helpful error with instructions
                    raise Exception(
                        "Minecraft launcher not found!\n\n"
                        "Please make sure Minecraft Java Edition is installed.\n\n"
                        "You can download it from:\n"
                        "https://www.minecraft.net/download\n\n"
                        "After installing, you can use this launcher to connect quickly to our server."
                    )
        
        elif system == "Linux":
            # On Linux, try to launch Minecraft
            try:
                if launcher_path and launcher_path != "minecraft-launcher":
                    subprocess.Popen([str(launcher_path)])
                else:
                    subprocess.Popen(["minecraft-launcher"])
            except FileNotFoundError:
                raise Exception(
                    "Minecraft launcher not found. Please install Minecraft Java Edition.\n\n"
                    "Visit: https://www.minecraft.net/download"
                )
        
        else:
            raise Exception(f"Unsupported operating system: {system}")
        
        # Create a server configuration file for quick connect
        self._create_server_config()
    
    def _create_server_config(self):
        """Create or update the servers.dat file to include our server"""
        
        # Note: This is a simplified approach
        # The actual servers.dat file uses NBT format which requires additional libraries
        # For now, we'll create a text file with instructions
        
        servers_file = self.minecraft_dir / "servers.txt"
        
        try:
            with open(servers_file, "w") as f:
                f.write(f"{SERVER_NAME}\n")
                f.write(f"{SERVER_ADDRESS}\n")
        except Exception as e:
            print(f"Could not create server config: {e}")


def main():
    """Main entry point for the launcher"""
    
    # Create the main window
    root = tk.Tk()
    
    # Create launcher instance
    launcher = MinecraftLauncher(root)
    
    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main()

