"""
Titan Minecraft Launcher
Professional client with automatic mod synchronization and Forge installation
"""

import tkinter as tk
from tkinter import ttk, messagebox
import minecraft_launcher_lib
import subprocess
import os
import sys
import uuid
import json
import hashlib
from pathlib import Path
import threading
import time
import requests
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor

# Hide console on Windows
if sys.platform == "win32":
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Configuration
SERVER_API = "http://localhost:8080"
MC_VERSION = "1.21.1"
MAX_PARALLEL_DOWNLOADS = 5

# Colors
BG = "#0a0e27"
CARD = "#1a1f3a"
ACCENT = "#4a9eff"
SUCCESS = "#00d9a3"
ERROR = "#ff5757"
TEXT = "#ffffff"
DIM = "#8892b0"


class TitanLauncher:
    """Professional Minecraft launcher with mod sync"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Titan Launcher")
        self.root.geometry("600x750")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        
        # Paths
        self.minecraft_dir = str(Path.home() / "AppData" / "Roaming" / ".minecraft")
        self.mods_dir = Path(self.minecraft_dir) / "mods"
        
        # State
        self.is_working = False
        self.manifest = None
        
        # Build UI
        self._build_ui()
        
        # Start initialization
        self.root.after(100, self._initialize)
    
    def _build_ui(self):
        """Build the UI"""
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Header
        tk.Label(
            main,
            text="TITAN LAUNCHER",
            font=("Segoe UI", 32, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(pady=(0, 5))
        
        tk.Label(
            main,
            text="Professional Mod-Synced Client",
            font=("Segoe UI", 11),
            bg=BG,
            fg=DIM
        ).pack(pady=(0, 30))
        
        # Status card
        status_frame = tk.Frame(main, bg=CARD, height=120)
        status_frame.pack(fill=tk.X, pady=(0, 20))
        status_frame.pack_propagate(False)
        
        self.status_text = tk.Label(
            status_frame,
            text="Initializing...",
            font=("Segoe UI", 13),
            bg=CARD,
            fg=TEXT,
            wraplength=500
        )
        self.status_text.pack(expand=True, pady=10)
        
        self.status_detail = tk.Label(
            status_frame,
            text="",
            font=("Segoe UI", 9),
            bg=CARD,
            fg=DIM
        )
        self.status_detail.pack()
        
        # Progress section
        self.progress_frame = tk.Frame(main, bg=BG)
        self.progress_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.progress_label = tk.Label(
            self.progress_frame,
            text="",
            font=("Segoe UI", 10),
            bg=BG,
            fg=TEXT
        )
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            length=540,
            mode='determinate'
        )
        self.progress_bar.pack(pady=10)
        
        self.progress_detail = tk.Label(
            self.progress_frame,
            text="",
            font=("Segoe UI", 9),
            bg=BG,
            fg=DIM
        )
        self.progress_detail.pack()
        
        self.progress_frame.pack_forget()  # Hidden initially
        
        # Username
        tk.Label(
            main,
            text="USERNAME",
            font=("Segoe UI", 9, "bold"),
            bg=BG,
            fg=DIM
        ).pack(anchor=tk.W, pady=(10, 5))
        
        self.username_var = tk.StringVar(value=self._load_username())
        self.username_entry = tk.Entry(
            main,
            textvariable=self.username_var,
            font=("Segoe UI", 12),
            bg=CARD,
            fg=TEXT,
            insertbackground=TEXT,
            relief=tk.FLAT,
            bd=10
        )
        self.username_entry.pack(fill=tk.X, ipady=10)
        
        # Info panel
        info_frame = tk.Frame(main, bg=CARD)
        info_frame.pack(fill=tk.X, pady=(20, 20))
        
        self.info_mc = tk.Label(
            info_frame,
            text=f"📦 Minecraft: {MC_VERSION}",
            font=("Segoe UI", 9),
            bg=CARD,
            fg=DIM
        )
        self.info_mc.pack(pady=5)
        
        self.info_forge = tk.Label(
            info_frame,
            text="🔧 Forge: Checking...",
            font=("Segoe UI", 9),
            bg=CARD,
            fg=DIM
        )
        self.info_forge.pack(pady=5)
        
        self.info_mods = tk.Label(
            info_frame,
            text="📂 Mods: Checking...",
            font=("Segoe UI", 9),
            bg=CARD,
            fg=DIM
        )
        self.info_mods.pack(pady=5)
        
        # Launch button
        self.launch_btn = tk.Button(
            main,
            text="INITIALIZING...",
            font=("Segoe UI", 14, "bold"),
            bg=CARD,
            fg=DIM,
            activebackground=SUCCESS,
            activeforeground=TEXT,
            relief=tk.FLAT,
            bd=0,
            state=tk.DISABLED,
            command=self._on_play_click
        )
        self.launch_btn.pack(fill=tk.X, ipady=18, pady=(10, 0))
    
    def _load_username(self):
        """Load saved username"""
        try:
            config = Path(self.minecraft_dir) / "titan_config.json"
            if config.exists():
                with open(config) as f:
                    return json.load(f).get("username", "Player")
        except:
            pass
        return "Player"
    
    def _save_username(self, username):
        """Save username"""
        try:
            config = Path(self.minecraft_dir) / "titan_config.json"
            with open(config, 'w') as f:
                json.dump({"username": username}, f)
        except:
            pass
    
    def _initialize(self):
        """Initialize launcher - check everything"""
        thread = threading.Thread(target=self._init_thread)
        thread.daemon = True
        thread.start()
    
    def _init_thread(self):
        """Background initialization"""
        try:
            # Step 1: Check Minecraft
            self._update_status("Checking Minecraft installation...")
            mc_installed = self._check_minecraft()
            
            # Step 2: Check server connection
            self._update_status("Connecting to server...")
            self.manifest = self._fetch_manifest()
            
            if self.manifest:
                forge_ver = self.manifest.get("forge", {}).get("version", "Unknown")
                mod_count = self.manifest.get("mod_count", 0)
                
                self.root.after(0, lambda: self.info_forge.config(text=f"🔧 Forge: {forge_ver}"))
                self.root.after(0, lambda: self.info_mods.config(text=f"📂 Mods: {mod_count} required"))
            
            # Step 3: Determine what needs to be done
            if not mc_installed:
                self._update_status("Ready to install", "Minecraft + Forge + Mods will be installed")
                self.root.after(0, lambda: self.launch_btn.config(
                    text="INSTALL & PLAY",
                    bg=SUCCESS,
                    fg=TEXT,
                    state=tk.NORMAL
                ))
            else:
                # Check if mods are synced
                needs_sync = self._check_mods_sync()
                if needs_sync:
                    self._update_status("Mods need updating", f"{needs_sync} mods to download")
                    self.root.after(0, lambda: self.launch_btn.config(
                        text="UPDATE & PLAY",
                        bg=ACCENT,
                        fg=TEXT,
                        state=tk.NORMAL
                    ))
                else:
                    self._update_status("Ready to play!", "Everything is up to date")
                    self.root.after(0, lambda: self.launch_btn.config(
                        text="PLAY",
                        bg=SUCCESS,
                        fg=TEXT,
                        state=tk.NORMAL
                    ))
        
        except Exception as e:
            self._update_status(f"Error: {str(e)}", "Check if server is running")
            self.root.after(0, lambda: self.launch_btn.config(
                text="RETRY",
                bg=ERROR,
                fg=TEXT,
                state=tk.NORMAL
            ))
    
    def _check_minecraft(self):
        """Check if Minecraft is installed"""
        version_jar = Path(self.minecraft_dir) / "versions" / MC_VERSION / f"{MC_VERSION}.jar"
        return version_jar.exists() and version_jar.stat().st_size > 15 * 1024 * 1024
    
    def _fetch_manifest(self):
        """Fetch mod manifest from server"""
        try:
            response = requests.get(f"{SERVER_API}/api/mods/manifest", timeout=5)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None
    
    def _check_mods_sync(self):
        """Check how many mods need to be synced"""
        if not self.manifest:
            return 0
        
        self.mods_dir.mkdir(parents=True, exist_ok=True)
        local_mods = {f.name for f in self.mods_dir.glob("*.jar")}
        required_mods = {mod["file"] for mod in self.manifest.get("mods", [])}
        
        missing = required_mods - local_mods
        return len(missing)
    
    def _update_status(self, text, detail=""):
        """Update status display"""
        self.root.after(0, lambda: self.status_text.config(text=text))
        self.root.after(0, lambda: self.status_detail.config(text=detail))
    
    def _on_play_click(self):
        """Handle play button click"""
        if self.is_working:
            return
        
        username = self.username_var.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return
        
        self._save_username(username)
        self.is_working = True
        self.launch_btn.config(state=tk.DISABLED)
        
        # Start full installation/launch
        thread = threading.Thread(target=self._full_launch_thread, args=(username,))
        thread.daemon = True
        thread.start()
    
    def _full_launch_thread(self, username):
        """Complete launch process"""
        try:
            # Show progress
            self.root.after(0, lambda: self.progress_frame.pack(fill=tk.X, pady=(0, 20)))
            
            # Step 1: Install Minecraft if needed
            if not self._check_minecraft():
                self._install_minecraft()
            
            # Step 2: Install Forge if needed
            self._install_forge()
            
            # Step 3: Sync mods
            self._sync_mods()
            
            # Step 4: Launch
            self._launch_game(username)
            
        except Exception as e:
            self._update_status(f"Error: {str(e)}", "")
            self.is_working = False
            self.root.after(0, lambda: self.launch_btn.config(state=tk.NORMAL))
    
    def _install_minecraft(self):
        """Install Minecraft"""
        self._update_status("Installing Minecraft...", "Downloading game files (this may take 5-10 minutes)")
        self.root.after(0, lambda: self.progress_label.config(text="Downloading Minecraft..."))
        
        total_files = 0
        current_file = 0
        
        def set_progress(progress):
            nonlocal current_file
            current_file = progress
            if total_files > 0:
                percent = int((progress / total_files) * 100)
                self.root.after(0, lambda: self.progress_bar.config(value=percent))
                self.root.after(0, lambda: self.progress_detail.config(text=f"{progress}/{total_files} files ({percent}%)"))
        
        def set_max(max_val):
            nonlocal total_files
            total_files = max_val
            self.root.after(0, lambda: self.progress_bar.config(maximum=100))
        
        def set_status(status):
            if "Assets" in status:
                self.root.after(0, lambda: self.progress_label.config(text="Downloading assets (this takes longest)..."))
            elif "Libraries" in status:
                self.root.after(0, lambda: self.progress_label.config(text="Downloading libraries..."))
        
        minecraft_launcher_lib.install.install_minecraft_version(
            MC_VERSION,
            self.minecraft_dir,
            callback={
                "setProgress": set_progress,
                "setMax": set_max,
                "setStatus": set_status
            }
        )
        
        self._update_status("Minecraft installed!", "")
    
    def _install_forge(self):
        """Install Forge automatically"""
        if not self.manifest:
            return
        
        forge_version = self.manifest.get("forge", {}).get("version")
        if not forge_version:
            return
        
        self._update_status("Installing Forge...", f"Version: {forge_version}")
        self.root.after(0, lambda: self.progress_label.config(text="Installing Forge..."))
        self.root.after(0, lambda: self.progress_bar.config(mode='indeterminate'))
        self.root.after(0, lambda: self.progress_bar.start())
        
        try:
            # Find and install Forge
            forge_ver = minecraft_launcher_lib.forge.find_forge_version(MC_VERSION)
            if forge_ver:
                minecraft_launcher_lib.forge.install_forge_version(
                    forge_ver,
                    self.minecraft_dir
                )
                self._update_status("Forge installed!", "")
        except Exception as e:
            print(f"Forge installation error: {e}")
            # Continue anyway - vanilla will work
        
        self.root.after(0, lambda: self.progress_bar.stop())
        self.root.after(0, lambda: self.progress_bar.config(mode='determinate'))
    
    def _sync_mods(self):
        """Sync mods from server in parallel"""
        if not self.manifest:
            return
        
        mods = self.manifest.get("mods", [])
        if not mods:
            return
        
        self._update_status(f"Syncing {len(mods)} mods...", "Downloading in parallel")
        self.root.after(0, lambda: self.progress_label.config(text=f"Downloading {len(mods)} mods..."))
        
        self.mods_dir.mkdir(parents=True, exist_ok=True)
        
        # Download each mod
        total_mods = len(mods)
        completed = 0
        
        for i, mod in enumerate(mods):
            mod_file = self.mods_dir / mod["file"]
            
            # Skip if already exists with correct checksum
            if mod_file.exists():
                existing_hash = self._calculate_checksum(mod_file)
                expected_hash = mod["checksum"].replace("sha256:", "")
                if existing_hash == expected_hash:
                    completed += 1
                    percent = int((completed / total_mods) * 100)
                    self.root.after(0, lambda p=percent: self.progress_bar.config(value=p))
                    self.root.after(0, lambda i=i, t=total_mods: self.progress_detail.config(text=f"Mod {i+1}/{t} (already downloaded)"))
                    continue
            
            # Download mod
            try:
                self.root.after(0, lambda name=mod["name"]: self.progress_detail.config(text=f"Downloading: {name}"))
                
                url = f"{SERVER_API}{mod['url']}"
                response = requests.get(url, stream=True)
                
                if response.status_code == 200:
                    with open(mod_file, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    completed += 1
                    percent = int((completed / total_mods) * 100)
                    self.root.after(0, lambda p=percent: self.progress_bar.config(value=p))
                    self.root.after(0, lambda i=i, t=total_mods: self.progress_detail.config(text=f"Mod {i+1}/{t} completed"))
            
            except Exception as e:
                print(f"Failed to download {mod['name']}: {e}")
        
        self._update_status(f"Downloaded {completed}/{total_mods} mods", "")
    
    def _calculate_checksum(self, file_path):
        """Calculate SHA256 checksum"""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def _launch_game(self, username):
        """Launch Minecraft with Forge and mods"""
        self._update_status("Launching Minecraft...", "")
        self.root.after(0, lambda: self.progress_frame.pack_forget())
        
        # Build launch options
        options = {
            "username": username,
            "uuid": str(uuid.uuid4()),
            "token": ""
        }
        
        # Try to use Forge version if available
        try:
            versions = minecraft_launcher_lib.utils.get_installed_versions(self.minecraft_dir)
            forge_version = None
            
            for version in versions:
                if "forge" in version["id"].lower():
                    forge_version = version["id"]
                    break
            
            launch_version = forge_version if forge_version else MC_VERSION
            
            # Get launch command
            command = minecraft_launcher_lib.command.get_minecraft_command(
                launch_version,
                self.minecraft_dir,
                options
            )
            
            # Launch WITHOUT console window
            startupinfo = None
            if sys.platform == "win32":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0
            
            subprocess.Popen(
                command,
                cwd=self.minecraft_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            )
            
            # Success!
            self._update_status("Minecraft launched!", "Minimizing launcher...")
            self.root.after(2000, lambda: self.root.iconify())
            
        except Exception as e:
            self._update_status(f"Launch failed: {str(e)}", "")
            messagebox.showerror("Launch Error", f"Failed to start Minecraft:\n\n{str(e)}\n\nTry installing Java 17+ from java.com")
            self.is_working = False
            self.launch_btn.config(state=tk.NORMAL)
    
    def run(self):
        """Run the launcher"""
        self.root.mainloop()


if __name__ == "__main__":
    launcher = TitanLauncher()
    launcher.run()

