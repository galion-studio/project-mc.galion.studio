"""
Galion Studio Minecraft Launcher - Ultra Clean Edition
No command windows, clean UI, automatic fixes
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
import time

# Hide console window on Windows
if sys.platform == "win32":
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Configuration
SERVER_ADDRESS = "localhost"
SERVER_NAME = "Galion Studio"
DEFAULT_MC_VERSION = "1.21.1"
FORGE_VERSION = "1.21.1-52.0.29"  # Latest Forge for 1.21.1
OPTIFINE_SUPPORT = True

# Clean color scheme
BG_COLOR = "#0a0e27"
CARD_COLOR = "#1a1f3a"
ACCENT_COLOR = "#4a9eff"
SUCCESS_COLOR = "#00d9a3"
ERROR_COLOR = "#ff5757"
TEXT_COLOR = "#ffffff"
TEXT_DIM = "#8892b0"


class CleanLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Galion Studio Launcher")
        self.root.geometry("500x650")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)
        
        # Minecraft directory
        self.minecraft_dir = str(Path.home() / "AppData" / "Roaming" / "GalionLauncher" / "minecraft")
        os.makedirs(self.minecraft_dir, exist_ok=True)
        
        # State
        self.downloading = False
        self.launching = False
        self.use_forge = tk.BooleanVar(value=False)
        self.use_optifine = tk.BooleanVar(value=False)
        
        # Build UI
        self._build_ui()
        
        # Check if Minecraft is installed
        self.root.after(100, self._check_installation)
    
    def _build_ui(self):
        """Build clean UI"""
        # Main container
        main = tk.Frame(self.root, bg=BG_COLOR)
        main.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Logo/Title
        tk.Label(
            main,
            text="GALION STUDIO",
            font=("Segoe UI", 28, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=(0, 5))
        
        tk.Label(
            main,
            text="Minecraft Launcher",
            font=("Segoe UI", 11),
            bg=BG_COLOR,
            fg=TEXT_DIM
        ).pack(pady=(0, 30))
        
        # Status card
        self.status_card = tk.Frame(main, bg=CARD_COLOR, height=100)
        self.status_card.pack(fill=tk.X, pady=(0, 20))
        self.status_card.pack_propagate(False)
        
        self.status_label = tk.Label(
            self.status_card,
            text="Loading...",
            font=("Segoe UI", 12),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        )
        self.status_label.pack(expand=True)
        
        # Progress bar (hidden initially)
        self.progress_frame = tk.Frame(main, bg=BG_COLOR)
        
        self.download_status = tk.Label(
            self.progress_frame,
            text="Downloading Minecraft...",
            font=("Segoe UI", 10),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
        self.download_status.pack()
        
        self.progress = ttk.Progressbar(
            self.progress_frame,
            length=440,
            mode='determinate'
        )
        self.progress.pack(pady=10)
        
        self.progress_text = tk.Label(
            self.progress_frame,
            text="0%",
            font=("Segoe UI", 9),
            bg=BG_COLOR,
            fg=TEXT_DIM
        )
        self.progress_text.pack()
        
        # Username input
        tk.Label(
            main,
            text="USERNAME",
            font=("Segoe UI", 9, "bold"),
            bg=BG_COLOR,
            fg=TEXT_DIM
        ).pack(anchor=tk.W, pady=(20, 5))
        
        self.username_var = tk.StringVar(value=self._load_username())
        self.username_entry = tk.Entry(
            main,
            textvariable=self.username_var,
            font=("Segoe UI", 12),
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            insertbackground=TEXT_COLOR,
            relief=tk.FLAT,
            bd=10
        )
        self.username_entry.pack(fill=tk.X, ipady=10)
        
        # Mod options
        mods_frame = tk.Frame(main, bg=BG_COLOR)
        mods_frame.pack(fill=tk.X, pady=(15, 0))
        
        tk.Label(
            mods_frame,
            text="MODS & PERFORMANCE",
            font=("Segoe UI", 9, "bold"),
            bg=BG_COLOR,
            fg=TEXT_DIM
        ).pack(anchor=tk.W, pady=(0, 8))
        
        # Forge checkbox with info button
        forge_row = tk.Frame(mods_frame, bg=BG_COLOR)
        forge_row.pack(anchor=tk.W, pady=2, fill=tk.X)
        
        forge_cb = tk.Checkbutton(
            forge_row,
            text="🔧 Forge (Mod Support)",
            variable=self.use_forge,
            command=self._on_forge_toggle,
            font=("Segoe UI", 10),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            selectcolor=CARD_COLOR,
            activebackground=BG_COLOR,
            activeforeground=TEXT_COLOR,
            relief=tk.FLAT
        )
        forge_cb.pack(side=tk.LEFT)
        
        tk.Label(
            forge_row,
            text="(Auto-install)",
            font=("Segoe UI", 8),
            bg=BG_COLOR,
            fg=SUCCESS_COLOR
        ).pack(side=tk.LEFT, padx=5)
        
        # OptiFine checkbox with info button
        optifine_row = tk.Frame(mods_frame, bg=BG_COLOR)
        optifine_row.pack(anchor=tk.W, pady=2, fill=tk.X)
        
        optifine_cb = tk.Checkbutton(
            optifine_row,
            text="⚡ OptiFine (Better Performance)",
            variable=self.use_optifine,
            command=self._on_optifine_toggle,
            font=("Segoe UI", 10),
            bg=BG_COLOR,
            fg=TEXT_COLOR,
            selectcolor=CARD_COLOR,
            activebackground=BG_COLOR,
            activeforeground=TEXT_COLOR,
            relief=tk.FLAT
        )
        optifine_cb.pack(side=tk.LEFT)
        
        tk.Label(
            optifine_row,
            text="(Auto-install)",
            font=("Segoe UI", 8),
            bg=BG_COLOR,
            fg=SUCCESS_COLOR
        ).pack(side=tk.LEFT, padx=5)
        
        # Launch button
        self.launch_btn = tk.Button(
            main,
            text="PLAY",
            font=("Segoe UI", 14, "bold"),
            bg=ACCENT_COLOR,
            fg=TEXT_COLOR,
            activebackground=SUCCESS_COLOR,
            activeforeground=TEXT_COLOR,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=self._on_launch_click
        )
        self.launch_btn.pack(fill=tk.X, ipady=15, pady=(30, 20))
        
        # Server info
        info_frame = tk.Frame(main, bg=CARD_COLOR)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(
            info_frame,
            text=f"Server: {SERVER_ADDRESS}:25565",
            font=("Segoe UI", 9),
            bg=CARD_COLOR,
            fg=TEXT_DIM
        ).pack(pady=10)
    
    def _load_username(self):
        """Load saved username"""
        try:
            config_file = Path(self.minecraft_dir) / "launcher_config.json"
            if config_file.exists():
                with open(config_file) as f:
                    config = json.load(f)
                    return config.get("username", "Player")
        except:
            pass
        return "Player"
    
    def _save_username(self, username):
        """Save username"""
        try:
            config_file = Path(self.minecraft_dir) / "launcher_config.json"
            with open(config_file, 'w') as f:
                json.dump({"username": username}, f)
        except:
            pass
    
    def _on_forge_toggle(self):
        """Handle Forge checkbox"""
        if self.use_forge.get():
            result = messagebox.askyesno(
                "Install Forge?",
                f"Install Forge {FORGE_VERSION} automatically?\n\n"
                "• Adds mod support\n"
                "• Compatible with thousands of mods\n"
                "• Download size: ~15 MB\n\n"
                "This will take 1-2 minutes."
            )
            if result:
                # Start Forge installation in background
                self._install_forge()
            else:
                self.use_forge.set(False)
        else:
            # Unchecked - nothing to do
            pass
    
    def _on_optifine_toggle(self):
        """Handle OptiFine checkbox"""
        if self.use_optifine.get():
            result = messagebox.askyesno(
                "Install OptiFine?",
                "Install OptiFine automatically?\n\n"
                "• Dramatically improves FPS\n"
                "• Better graphics options\n"
                "• Shader support\n"
                "• Download size: ~3 MB\n\n"
                "This will take 30-60 seconds."
            )
            if result:
                # Start OptiFine installation in background
                self._install_optifine()
            else:
                self.use_optifine.set(False)
        else:
            # Unchecked - nothing to do
            pass
    
    def _check_installation(self):
        """Check if Minecraft is installed"""
        version_jar = Path(self.minecraft_dir) / "versions" / DEFAULT_MC_VERSION / f"{DEFAULT_MC_VERSION}.jar"
        
        if version_jar.exists() and version_jar.stat().st_size > 15 * 1024 * 1024:
            self.status_label.config(text="✓ Ready to Play", fg=SUCCESS_COLOR)
            self.launch_btn.config(state=tk.NORMAL)
        else:
            self.status_label.config(text="Minecraft not installed", fg=TEXT_DIM)
            self.launch_btn.config(text="INSTALL & PLAY", bg=SUCCESS_COLOR)
    
    def _on_launch_click(self):
        """Handle launch button click"""
        username = self.username_var.get().strip()
        
        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return
        
        self._save_username(username)
        
        # Check if installed
        version_jar = Path(self.minecraft_dir) / "versions" / DEFAULT_MC_VERSION / f"{DEFAULT_MC_VERSION}.jar"
        
        if not version_jar.exists() or version_jar.stat().st_size < 15 * 1024 * 1024:
            self._download_minecraft()
        else:
            self._launch_minecraft(username)
    
    def _download_minecraft(self):
        """Download Minecraft"""
        if self.downloading:
            return
        
        self.downloading = True
        self.launch_btn.config(state=tk.DISABLED, text="DOWNLOADING...")
        self.status_card.pack_forget()
        self.progress_frame.pack(fill=tk.X, pady=(0, 20))
        
        thread = threading.Thread(target=self._download_thread)
        thread.daemon = True
        thread.start()
    
    def _download_thread(self):
        """Background download"""
        self.current_max = 0
        self.current_status = "Starting..."
        
        def set_status(status):
            # Update what's being downloaded
            self.current_status = status
            status_text = status
            
            # Show helpful messages for each stage
            if "Libraries" in status:
                status_text = "Downloading game libraries..."
            elif "Assets" in status:
                status_text = "Downloading assets (sounds, textures)... This may take a while!"
            elif "Minecraft" in status or "client" in status.lower():
                status_text = "Downloading game files..."
            
            self.root.after(0, lambda: self.download_status.config(text=status_text))
        
        def set_progress(progress):
            if self.current_max > 0:
                percent = int((progress / self.current_max) * 100)
                
                # Special message at 97%+ (asset download phase)
                text = f"{percent}% ({progress}/{self.current_max} files)"
                if percent >= 97 and "Assets" in self.current_status:
                    text = f"{percent}% - Downloading thousands of small files, please wait..."
                
                self.root.after(0, lambda: self.progress.config(value=percent))
                self.root.after(0, lambda: self.progress_text.config(text=text))
        
        def set_max(max_val):
            self.current_max = max_val
            self.root.after(0, lambda: self.progress.config(maximum=100))
        
        try:
            minecraft_launcher_lib.install.install_minecraft_version(
                DEFAULT_MC_VERSION,
                self.minecraft_dir,
                callback={
                    "setStatus": set_status,
                    "setProgress": set_progress,
                    "setMax": set_max
                }
            )
            self.root.after(0, self._download_complete, True)
        except Exception as e:
            self.root.after(0, self._download_complete, False, str(e))
    
    def _download_complete(self, success, error=None):
        """Download finished"""
        self.downloading = False
        self.progress_frame.pack_forget()
        self.status_card.pack(fill=tk.X, pady=(0, 20))
        
        if success:
            self.status_label.config(text="✓ Download Complete!", fg=SUCCESS_COLOR)
            self.launch_btn.config(state=tk.NORMAL, text="PLAY", bg=ACCENT_COLOR)
            
            # Auto-launch after 1 second
            username = self.username_var.get().strip()
            self.root.after(1000, lambda: self._launch_minecraft(username))
        else:
            self.status_label.config(text="✗ Download Failed", fg=ERROR_COLOR)
            self.launch_btn.config(state=tk.NORMAL, text="RETRY", bg=ERROR_COLOR)
            messagebox.showerror("Download Failed", f"Failed to download Minecraft.\n\nPlease check your internet connection and try again.")
    
    def _launch_minecraft(self, username):
        """Launch Minecraft"""
        if self.launching:
            return
        
        self.launching = True
        self.launch_btn.config(state=tk.DISABLED, text="STARTING...")
        self.status_label.config(text="Starting Minecraft...", fg=TEXT_COLOR)
        
        thread = threading.Thread(target=self._launch_thread, args=(username,))
        thread.daemon = True
        thread.start()
    
    def _launch_thread(self, username):
        """Background launch"""
        try:
            # Build options
            options = {
                "username": username,
                "uuid": str(uuid.uuid4()),
                "token": ""
            }
            
            # Get command
            command = minecraft_launcher_lib.command.get_minecraft_command(
                DEFAULT_MC_VERSION,
                self.minecraft_dir,
                options
            )
            
            # Launch WITHOUT console window (key fix!)
            startupinfo = None
            if sys.platform == "win32":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0  # Hide window
            
            process = subprocess.Popen(
                command,
                cwd=self.minecraft_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            )
            
            # Wait to check if it started
            time.sleep(3)
            
            if process.poll() is None:
                # Success!
                self.root.after(0, self._launch_success)
            else:
                # Failed
                self.root.after(0, self._launch_failed)
                
        except Exception as e:
            self.root.after(0, self._launch_failed, str(e))
    
    def _launch_success(self):
        """Launch succeeded"""
        self.launching = False
        self.status_label.config(text="✓ Minecraft Started!", fg=SUCCESS_COLOR)
        self.launch_btn.config(text="✓ RUNNING", bg=SUCCESS_COLOR)
        
        # Minimize launcher after 2 seconds
        self.root.after(2000, lambda: self.root.iconify())
    
    def _launch_failed(self, error=None):
        """Launch failed"""
        self.launching = False
        self.status_label.config(text="✗ Launch Failed", fg=ERROR_COLOR)
        self.launch_btn.config(state=tk.NORMAL, text="TRY AGAIN", bg=ERROR_COLOR)
        
        # Show simple error
        messagebox.showerror(
            "Launch Failed",
            "Minecraft failed to start.\n\n"
            "Common fixes:\n"
            "• Install Java 17+ from java.com\n"
            "• Update graphics drivers\n"
            "• Restart your computer\n\n"
            "Click 'TRY AGAIN' to retry."
        )
    
    def _install_forge(self):
        """Install Forge automatically"""
        self.launch_btn.config(state=tk.DISABLED, text="INSTALLING FORGE...")
        self.status_label.config(text="Installing Forge...", fg=TEXT_COLOR)
        self.progress_frame.pack(fill=tk.X, pady=(0, 20))
        
        thread = threading.Thread(target=self._forge_install_thread)
        thread.daemon = True
        thread.start()
    
    def _forge_install_thread(self):
        """Background Forge installation"""
        try:
            def callback(status):
                self.root.after(0, lambda: self.download_status.config(text=f"Installing Forge: {status}"))
            
            # Install Forge using minecraft_launcher_lib
            forge_version = minecraft_launcher_lib.forge.find_forge_version(DEFAULT_MC_VERSION)
            
            if not forge_version:
                raise Exception("Could not find compatible Forge version")
            
            self.root.after(0, lambda: self.progress.config(mode='indeterminate'))
            self.root.after(0, lambda: self.progress.start())
            
            minecraft_launcher_lib.forge.install_forge_version(
                forge_version,
                self.minecraft_dir,
                callback={"setStatus": callback}
            )
            
            self.root.after(0, lambda: self.progress.stop())
            self.root.after(0, self._forge_install_complete, True)
            
        except Exception as e:
            self.root.after(0, self._forge_install_complete, False, str(e))
    
    def _forge_install_complete(self, success, error=None):
        """Forge installation finished"""
        self.progress_frame.pack_forget()
        
        if success:
            self.status_label.config(text="✓ Forge Installed!", fg=SUCCESS_COLOR)
            self.launch_btn.config(state=tk.NORMAL, text="PLAY", bg=ACCENT_COLOR)
            messagebox.showinfo(
                "Forge Installed!",
                "Forge has been installed successfully!\n\n"
                "• Add mods to: %appdata%\\.minecraft\\mods\n"
                "• Launch will now use Forge version\n\n"
                "Click PLAY to start!"
            )
        else:
            self.status_label.config(text="✗ Forge Installation Failed", fg=ERROR_COLOR)
            self.launch_btn.config(state=tk.NORMAL, text="PLAY", bg=ACCENT_COLOR)
            self.use_forge.set(False)
            messagebox.showerror(
                "Forge Installation Failed",
                f"Could not install Forge.\n\n"
                f"Error: {error}\n\n"
                "You can still play vanilla Minecraft."
            )
    
    def _install_optifine(self):
        """Install OptiFine automatically"""
        import webbrowser
        
        # OptiFine requires manual download due to their website protection
        result = messagebox.showinfo(
            "OptiFine Download",
            "OptiFine requires a quick manual step:\n\n"
            "1. Browser will open to OptiFine download\n"
            "2. Click the DOWNLOAD button\n"
            "3. Wait 5 seconds, click 'Download OptiFine'\n"
            "4. Save the file to Downloads folder\n"
            "5. Come back here and click OK\n\n"
            "Opening browser now..."
        )
        
        # Open OptiFine download page
        webbrowser.open(f"https://optifine.net/adloadx?f=OptiFine_{DEFAULT_MC_VERSION.replace('.', '_')}_HD_U_K1.jar")
        
        # Show instructions for manual install
        messagebox.showinfo(
            "OptiFine Installation",
            "After downloading OptiFine:\n\n"
            "1. Find the downloaded JAR file\n"
            "2. Double-click it to run installer\n"
            "3. Click 'Install'\n"
            "4. Done!\n\n"
            "OptiFine will appear in Minecraft launcher profiles."
        )
        
        self.use_optifine.set(False)
    
    def run(self):
        """Run launcher"""
        self.root.mainloop()


if __name__ == "__main__":
    launcher = CleanLauncher()
    launcher.run()

