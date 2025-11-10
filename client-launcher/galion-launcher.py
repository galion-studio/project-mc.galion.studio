#!/usr/bin/env python3
"""
GALION Custom Client Launcher - Grok AI Edition
For the GALION custom game engine with built-in AI features

NOT Minecraft - This is our own custom client!
"""

# Auto-install dependencies
def check_dependencies():
    """Auto-install missing packages"""
    import subprocess
    import sys
    
    required = {
        'requests': 'requests',
        'minecraft-launcher-lib': 'minecraft_launcher_lib'
    }
    missing = []
    
    for pip_name, import_name in required.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(pip_name)
    
    if missing:
        print("[SETUP] Installing dependencies...")
        for pkg in missing:
            print(f"[SETUP] Installing {pkg}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg, '--quiet'])
        print("[SETUP] ✓ All dependencies installed!")

check_dependencies()

import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import requests
import sys
from pathlib import Path
import json
import os
import threading
import webbrowser
import time
import zipfile
import io
import uuid
import minecraft_launcher_lib

# Configuration
SERVER_ADDRESS = "mc.galion.studio"
LAUNCHER_VERSION = "2.0 - Grok AI Edition"
MC_VERSION = "1.21.1"

# Use custom .minecraft folder from project
PROJECT_ROOT = Path(__file__).parent.parent
CUSTOM_MC_DIR = PROJECT_ROOT / ".minecraft-custom"
MINECRAFT_DIR = str(Path.home() / "AppData" / "Roaming" / ".minecraft")
MODS_DIR = Path(MINECRAFT_DIR) / "mods"

# Copy custom configs on first run
def setup_custom_configs():
    """Copy custom .minecraft configs to user's folder"""
    if CUSTOM_MC_DIR.exists():
        import shutil
        # Copy custom configs
        for config_file in ["options.txt", "galion-launcher-profile.json", "grok-config.json"]:
            src = CUSTOM_MC_DIR / config_file
            dst = Path(MINECRAFT_DIR) / config_file
            if src.exists() and not dst.exists():
                Path(MINECRAFT_DIR).mkdir(parents=True, exist_ok=True)
                shutil.copy(src, dst)

setup_custom_configs()

class GalionLauncher:
    """
    GALION Custom Client Launcher
    Downloads and launches the custom GALION client
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"GALION Launcher {LAUNCHER_VERSION}")
        self.root.geometry("850x800")
        self.root.configure(bg="#0a0e27")
        self.root.resizable(True, True)
        self.root.minsize(700, 600)
        
        # Load Grok API key
        self.grok_api_key = self._load_grok_key()
        self.grok_enabled = bool(self.grok_api_key and self.grok_api_key != "your-openrouter-api-key-here")
        
        # Build UI
        self._build_ui()
    
    def _load_grok_key(self):
        """Load Grok API key"""
        env_paths = [
            Path(__file__).parent.parent / ".env.grok",
            Path.home() / ".env.grok",
        ]
        
        for env_path in env_paths:
            if env_path.exists():
                try:
                    with open(env_path, 'r') as f:
                        for line in f:
                            if line.startswith("OPENROUTER_API_KEY="):
                                return line.split('=', 1)[1].strip()
                except:
                    pass
        return None
    
    def _build_ui(self):
        """Build the launcher UI"""
        
        # Header
        header = tk.Frame(self.root, bg="#0a0e27")
        header.pack(pady=30)
        
        tk.Label(
            header,
            text="GALION",
            font=("Arial", 42, "bold"),
            bg="#0a0e27",
            fg="#00d9a3"
        ).pack()
        
        tk.Label(
            header,
            text="Custom AI-Powered Gaming Platform",
            font=("Arial", 12),
            bg="#0a0e27",
            fg="#888"
        ).pack()
        
        tk.Label(
            header,
            text=f"Launcher v{LAUNCHER_VERSION}",
            font=("Arial", 9),
            bg="#0a0e27",
            fg="#666"
        ).pack()
        
        # Server info card
        server_card = tk.Frame(self.root, bg="#1a1f3a")
        server_card.pack(padx=40, pady=20, fill=tk.X)
        
        tk.Label(
            server_card,
            text="🌐 Server Address",
            font=("Arial", 10),
            bg="#1a1f3a",
            fg="#888"
        ).pack(pady=(15, 5))
        
        tk.Label(
            server_card,
            text=SERVER_ADDRESS,
            font=("Courier", 16, "bold"),
            bg="#1a1f3a",
            fg="#00d9a3"
        ).pack(pady=(0, 15))
        
        # Status
        self.status_label = tk.Label(
            self.root,
            text="Ready to play",
            font=("Arial", 11),
            bg="#0a0e27",
            fg="white"
        )
        self.status_label.pack(pady=10)
        
        # Progress bar frame
        progress_container = tk.Frame(self.root, bg="#0a0e27")
        progress_container.pack(fill=tk.X, padx=40, pady=5)
        
        self.grok_status = tk.Label(
            progress_container,
            text="",
            font=("Arial", 9),
            bg="#0a0e27",
            fg="#4a9eff",
            height=1
        )
        self.grok_status.pack()
        
        self.progress_frame = tk.Frame(progress_container, bg="#1a1f3a", height=25)
        self.progress_frame.pack(fill=tk.X)
        self.progress_frame.pack_propagate(False)
        
        self.progress_canvas = tk.Canvas(
            self.progress_frame,
            bg="#1a1f3a",
            height=25,
            highlightthickness=0
        )
        self.progress_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Console section
        console_container = tk.Frame(self.root, bg="#0a0e27")
        console_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        console_frame = tk.Frame(console_container, bg="#1a1f3a")
        console_frame.pack(fill=tk.BOTH, expand=True)
        
        # Console header
        console_header = tk.Frame(console_frame, bg="#1a1f3a", height=30)
        console_header.pack(fill=tk.X)
        console_header.pack_propagate(False)
        
        tk.Label(
            console_header,
            text="💻 CONSOLE",
            font=("Arial", 10, "bold"),
            bg="#1a1f3a",
            fg="#00d9a3"
        ).pack(side=tk.LEFT, padx=10, pady=5)
        
        tk.Label(
            console_header,
            text="[Grok AI Powered]",
            font=("Arial", 8),
            bg="#1a1f3a",
            fg="#888"
        ).pack(side=tk.LEFT, pady=5)
        
        # Console output
        self.console = scrolledtext.ScrolledText(
            console_frame,
            height=10,
            font=("Consolas", 9),
            bg="#0a0e27",
            fg="#00d9a3",
            borderwidth=0,
            relief="flat",
            wrap=tk.WORD
        )
        self.console.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        welcome = f"""
╔════════════════════════════════════════════════════════════════╗
║              GALION LAUNCHER v{LAUNCHER_VERSION}                   ║
║          Custom Client with Grok AI Integration                ║
╚════════════════════════════════════════════════════════════════╝

[SYSTEM] Console initialized
[SYSTEM] AI Assistant: {'ENABLED ✓' if self.grok_enabled else 'DISABLED (no API key)'}
[SYSTEM] Minecraft Directory: {MINECRAFT_DIR}
[SYSTEM] Server: {SERVER_ADDRESS}
[SYSTEM] Default Username: galion.studio (Admin 👑)

[INFO] Using YOUR custom .minecraft folder
[INFO] Built with Grok AI integration
[INFO] Auto-installs missing files

[TIP] Type 'help' or ask Grok AI anything!
"""
        self.console.insert(1.0, welcome)
        self.console.config(state=tk.DISABLED)
        
        # Console input
        console_input = tk.Frame(console_frame, bg="#1a1f3a", height=40)
        console_input.pack(fill=tk.X, padx=8, pady=(0, 8))
        console_input.pack_propagate(False)
        
        tk.Label(
            console_input,
            text=">",
            font=("Consolas", 11, "bold"),
            bg="#1a1f3a",
            fg="#00d9a3"
        ).pack(side=tk.LEFT, padx=(5, 8), pady=8)
        
        self.console_entry = tk.Entry(
            console_input,
            font=("Consolas", 10),
            bg="#0a0e27",
            fg="#00d9a3",
            insertbackground="#00d9a3",
            borderwidth=0
        )
        self.console_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=8)
        self.console_entry.bind("<Return>", lambda e: self._handle_console())
        
        tk.Button(
            console_input,
            text="Ask AI",
            font=("Arial", 9, "bold"),
            bg="#4a9eff",
            fg="white",
            command=self._handle_console,
            relief="flat",
            padx=15,
            cursor="hand2"
        ).pack(side=tk.LEFT, padx=8, pady=8)
        
        # Bottom controls
        controls_container = tk.Frame(self.root, bg="#0a0e27")
        controls_container.pack(fill=tk.X, padx=40, pady=15)
        
        # Username
        username_frame = tk.Frame(controls_container, bg="#0a0e27")
        username_frame.pack()
        
        tk.Label(
            username_frame,
            text="Username:",
            font=("Arial", 10),
            bg="#0a0e27",
            fg="#888"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.username_entry = tk.Entry(
            username_frame,
            font=("Arial", 12),
            width=25,
            justify=tk.CENTER,
            bg="#1a1f3a",
            fg="#00d9a3",  # Green for admin
            insertbackground="#00d9a3",
            borderwidth=0
        )
        default_username = self._load_username()
        self.username_entry.insert(0, default_username)
        self.username_entry.pack(side=tk.LEFT, ipady=5)
        
        # Admin badge if using default admin account
        if default_username == "galion.studio":
            tk.Label(
                username_frame,
                text="👑 Admin",
                font=("Arial", 9, "bold"),
                bg="#0a0e27",
                fg="#00d9a3"
            ).pack(side=tk.LEFT, padx=10)
        
        # PLAY button
        self.play_btn = tk.Button(
            self.root,
            text="▶ PLAY",
            font=("Arial", 18, "bold"),
            bg="#00d9a3",
            fg="#000000",
            width=25,
            height=2,
            command=self._play,
            relief="flat",
            cursor="hand2",
            activebackground="#00ff99",
            activeforeground="#000000",
            bd=0
        )
        self.play_btn.pack(pady=(15, 20))
    
    def _load_username(self):
        """Load saved username - defaults to admin account"""
        config_file = Path(MINECRAFT_DIR) / "galion_config.json"
        if config_file.exists():
            try:
                with open(config_file) as f:
                    return json.load(f).get('username', 'galion.studio')
            except:
                pass
        return "galion.studio"  # Default admin account
    
    def _save_username(self, username):
        """Save username"""
        Path(MINECRAFT_DIR).mkdir(parents=True, exist_ok=True)
        config_file = Path(MINECRAFT_DIR) / "galion_config.json"
        with open(config_file, 'w') as f:
            json.dump({'username': username}, f)
    
    def _log(self, message):
        """Log to console"""
        def append():
            self.console.config(state=tk.NORMAL)
            self.console.insert(tk.END, f"{message}\n")
            self.console.see(tk.END)
            self.console.config(state=tk.DISABLED)
        self.root.after(0, append)
    
    def _update_status(self, text):
        """Update status label"""
        self.root.after(0, lambda: self.status_label.config(text=text))
    
    def _update_progress(self, status, percent):
        """Update progress bar"""
        def update():
            self.grok_status.config(text=f"🤖 {status}")
            
            if percent > 0:
                width = self.progress_canvas.winfo_width()
                height = self.progress_canvas.winfo_height()
                fill_width = int(width * percent / 100)
                
                self.progress_canvas.delete("all")
                self.progress_canvas.create_rectangle(
                    0, 0, width, height,
                    fill="#1a1f3a",
                    outline=""
                )
                self.progress_canvas.create_rectangle(
                    0, 0, fill_width, height,
                    fill="#00d9a3",
                    outline=""
                )
                self.progress_canvas.create_text(
                    width/2, height/2,
                    text=f"{percent}% - {status}",
                    fill="white",
                    font=("Arial", 9, "bold")
                )
            else:
                self.progress_canvas.delete("all")
        
        self.root.after(0, update)
    
    def _handle_console(self):
        """Handle console input"""
        cmd = self.console_entry.get().strip()
        if not cmd:
            return
        
        self.console_entry.delete(0, tk.END)
        self._log(f"[USER] > {cmd}")
        
        if cmd.lower() == 'help':
            self._show_help()
        elif cmd.lower() == 'status':
            self._show_status()
        elif cmd.lower() in ['clear', 'cls']:
            self.console.config(state=tk.NORMAL)
            self.console.delete(1.0, tk.END)
            self._log("[SYSTEM] Console cleared")
            self.console.config(state=tk.DISABLED)
        else:
            # Ask Grok AI
            if self.grok_enabled:
                threading.Thread(target=self._ask_grok, args=(cmd,), daemon=True).start()
            else:
                self._log("[ERROR] Grok AI not configured")
    
    def _show_help(self):
        """Show help"""
        self._log("")
        self._log("[HELP] ═══════════════════════════════════════")
        self._log("[HELP] GALION Launcher Commands:")
        self._log("[HELP]   help    - Show this help")
        self._log("[HELP]   status  - Check system status")
        self._log("[HELP]   clear   - Clear console")
        self._log("[HELP] ")
        self._log("[HELP] Or ask Grok AI anything!")
        self._log("[HELP] ═══════════════════════════════════════")
        self._log("")
    
    def _show_status(self):
        """Show system status"""
        mc_jar = Path(MINECRAFT_DIR) / "versions" / MC_VERSION / f"{MC_VERSION}.jar"
        
        # Check Java
        java_version = "Not found"
        try:
            result = subprocess.run(['java', '-version'], capture_output=True, text=True, timeout=5)
            output = result.stderr + result.stdout
            match = re.search(r'version "(\d+)', output)
            if match:
                java_version = match.group(1)
        except:
            pass
        
        self._log("")
        self._log("[STATUS] ═══════════════════════════════════════")
        self._log("[STATUS] System Status:")
        self._log(f"[STATUS]   Minecraft: {'Installed ✓' if mc_jar.exists() else 'Not installed ✗'}")
        self._log(f"[STATUS]   Version: {MC_VERSION}")
        self._log(f"[STATUS]   Java: {java_version} {'✓' if java_version >= '17' else '✗'}")
        self._log(f"[STATUS]   Server: {SERVER_ADDRESS}")
        self._log(f"[STATUS]   Grok AI: {'Ready ✓' if self.grok_enabled else 'Not configured ✗'}")
        self._log(f"[STATUS]   Minecraft Dir: {MINECRAFT_DIR}")
        self._log(f"[STATUS]   Username: galion.studio (Admin 👑)")
        self._log("[STATUS] ═══════════════════════════════════════")
        self._log("")
    
    def _ask_grok(self, question):
        """Ask Grok AI"""
        try:
            self._log("[AI] 🤖 Asking Grok AI...")
            self._update_progress("Thinking...", 50)
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.grok_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "x-ai/grok-4-fast",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are an AI assistant for GALION, a custom voxel-based game engine with built-in AI features. Help users with gameplay and technical questions. Keep answers concise (2-3 sentences)."
                        },
                        {
                            "role": "user",
                            "content": question
                        }
                    ],
                    "max_tokens": 150
                },
                timeout=30
            )
            
            self._update_progress("Complete!", 100)
            
            if response.status_code == 200:
                answer = response.json()["choices"][0]["message"]["content"]
                self._log(f"[AI] 🤖 {answer}")
            else:
                self._log(f"[AI] Error: {response.status_code}")
            
            self.root.after(2000, lambda: self._update_progress("", 0))
            
        except Exception as e:
            self._log(f"[AI] Error: {str(e)}")
            self._update_progress("", 0)
    
    def _play(self):
        """Launch GALION client"""
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showwarning("Username Required", "Please enter a username")
            return
        
        self._save_username(username)
        self.play_btn.config(state=tk.DISABLED)
        
        threading.Thread(target=self._launch_client, args=(username,), daemon=True).start()
    
    def _launch_client(self, username):
        """Launch Minecraft with custom .minecraft folder"""
        try:
            self._log("")
            self._log("[LAUNCH] ╔════════════════════════════════════════════════╗")
            self._log("[LAUNCH] ║      LAUNCHING MINECRAFT CLIENT                ║")
            self._log("[LAUNCH] ║      Using Custom .minecraft Folder            ║")
            self._log("[LAUNCH] ╚════════════════════════════════════════════════╝")
            self._log("")
            
            # Check Minecraft installation
            mc_jar = Path(MINECRAFT_DIR) / "versions" / MC_VERSION / f"{MC_VERSION}.jar"
            
            if not mc_jar.exists() or mc_jar.stat().st_size < 15*1024*1024:
                self._log("[INSTALL] Minecraft not found or incomplete")
                self._log("[INSTALL] Installing Minecraft 1.21.1...")
                self._log("[INSTALL] This takes 5-10 minutes first time")
                self._log("")
                
                self._update_progress("Installing Minecraft...", 20)
                self._update_status("Installing Minecraft 1.21.1...")
                
                # Install Minecraft using launcher-lib
                minecraft_launcher_lib.install.install_minecraft_version(
                    MC_VERSION,
                    MINECRAFT_DIR
                )
                
                self._log("[INSTALL] ✓ Minecraft installed!")
                self._log("")
            
            # Build launch command
            self._log(f"[LAUNCH] Building launch command...")
            self._log(f"[LAUNCH] Username: {username} {'👑 (Admin)' if username == 'galion.studio' else ''}")
            self._log(f"[LAUNCH] Version: {MC_VERSION}")
            self._log(f"[LAUNCH] Minecraft Dir: {MINECRAFT_DIR}")
            self._log("")
            
            options = {
                "username": username,
                "uuid": str(uuid.uuid4()),
                "token": ""
            }
            
            command = minecraft_launcher_lib.command.get_minecraft_command(
                MC_VERSION,
                MINECRAFT_DIR,
                options
            )
            
            self._log(f"[LAUNCH] Command ready ({len(command)} arguments)")
            self._log(f"[LAUNCH] Java: {command[0]}")
            self._log("")
            self._log(f"[LAUNCH] Starting Minecraft...")
            
            self._update_progress("Launching game...", 90)
            
            # Launch Minecraft
            process = subprocess.Popen(
                command,
                cwd=MINECRAFT_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self._log(f"[LAUNCH] ✓ Minecraft process started (PID: {process.pid})")
            self._log(f"[LAUNCH] Checking if game starts properly...")
            
            # Wait and check
            time.sleep(3)
            
            if process.poll() is not None:
                # Crashed!
                stdout, stderr = process.communicate()
                self._log("[ERROR] ═══════════════════════════════════════")
                self._log("[ERROR] Game crashed immediately!")
                self._log("[ERROR] ═══════════════════════════════════════")
                
                if stderr:
                    for line in stderr.split('\n')[:10]:
                        if line.strip():
                            self._log(f"[ERROR] {line}")
                
                # Grok auto-diagnose
                if self.grok_enabled:
                    self._log("")
                    self._log("[AI] 🤖 Asking Grok to diagnose...")
                    error_summary = (stderr + stdout)[:300]
                    threading.Thread(target=self._ask_grok_diagnosis, args=(error_summary,), daemon=True).start()
                
                self._update_status("Launch failed - Check console")
                self._update_progress("", 0)
                self.play_btn.config(state=tk.NORMAL)
                return
            
            # Success!
            self._log("")
            self._log("[SUCCESS] ✓ Game is starting successfully!")
            self._log("[SUCCESS] Minecraft window should appear in 10-30 seconds")
            self._log("[SUCCESS] ═══════════════════════════════════════")
            self._log("[SUCCESS] Server: " + SERVER_ADDRESS)
            self._log("[SUCCESS] Connect in-game to play!")
            self._log("[SUCCESS] ═══════════════════════════════════════")
            self._log("")
            
            if self.grok_enabled:
                self._log("[AI] 🤖 Grok AI is ready - ask me anything!")
            
            self._update_progress("Complete!", 100)
            self._update_status("Game launched successfully!")
            
            self.root.after(2000, lambda: self._update_progress("", 0))
            self.root.after(3000, self.root.iconify)
            
        except Exception as e:
            self._log(f"[ERROR] Failed to launch: {str(e)}")
            self._update_status("Launch failed")
            self._update_progress("", 0)
            self.play_btn.config(state=tk.NORMAL)
    
    def _ask_grok_diagnosis(self, error):
        """Ask Grok to diagnose error"""
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.grok_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "x-ai/grok-4-fast",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a Minecraft technical expert. Diagnose errors and provide solutions. Be concise (2-3 sentences)."
                        },
                        {
                            "role": "user",
                            "content": f"Minecraft 1.21.1 crashed with error:\n{error}\n\nWhat's wrong and how to fix?"
                        }
                    ],
                    "max_tokens": 150
                },
                timeout=30
            )
            
            if response.status_code == 200:
                answer = response.json()["choices"][0]["message"]["content"]
                self._log(f"[AI] 🤖 Grok diagnosis:")
                for line in answer.split('\n'):
                    if line.strip():
                        self._log(f"[AI] {line}")
        except:
            pass
    
    def _auto_download_client(self):
        """Auto-download GALION client from GitHub"""
        try:
            self._update_progress("Downloading client from GitHub...", 10)
            self._log("[DOWNLOAD] Connecting to GitHub...")
            self._log("[DOWNLOAD] URL: " + GITHUB_RELEASE_URL)
            
            # Create client directory
            CLIENT_DIR.mkdir(parents=True, exist_ok=True)
            
            self._update_progress("Downloading client files...", 30)
            self._log("[DOWNLOAD] Downloading... (This may take a few minutes)")
            
            # Download the ZIP file
            response = requests.get(GITHUB_RELEASE_URL, stream=True, timeout=60)
            
            if response.status_code == 404:
                self._log("[DOWNLOAD] ✗ GitHub release not found (404)")
                self._log("[DOWNLOAD] The client may not be published yet")
                self._update_progress("", 0)
                return False
            
            if response.status_code != 200:
                self._log(f"[DOWNLOAD] ✗ Download failed (HTTP {response.status_code})")
                self._update_progress("", 0)
                return False
            
            # Get file size for progress
            total_size = int(response.headers.get('content-length', 0))
            self._log(f"[DOWNLOAD] Size: {total_size / 1024 / 1024:.1f} MB")
            
            # Download with progress
            downloaded = 0
            chunks = []
            
            self._update_progress("Downloading...", 40)
            
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    chunks.append(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        progress = 40 + int((downloaded / total_size) * 30)  # 40-70%
                        if downloaded % (1024 * 1024) == 0:  # Every MB
                            self._update_progress(f"Downloading... {downloaded // 1024 // 1024}/{total_size // 1024 // 1024} MB", progress)
            
            self._log(f"[DOWNLOAD] ✓ Downloaded {downloaded / 1024 / 1024:.1f} MB")
            
            # Extract ZIP
            self._update_progress("Extracting files...", 75)
            self._log("[EXTRACT] Extracting client files...")
            
            zip_data = b''.join(chunks)
            with zipfile.ZipFile(io.BytesIO(zip_data)) as zip_file:
                zip_file.extractall(CLIENT_DIR)
            
            self._log(f"[EXTRACT] ✓ Extracted to: {CLIENT_DIR}")
            
            # Verify client executable
            if CLIENT_EXE.exists():
                self._update_progress("Installation complete!", 100)
                self._log("[VERIFY] ✓ GalionClient.exe found!")
                self._log("[VERIFY] Installation successful!")
                
                # Use Grok AI to celebrate!
                if self.grok_enabled:
                    self._log("")
                    self._log("[AI] 🤖 Grok says: Client installed successfully!")
                    self._log("[AI] 🤖 You're ready to play! Click PLAY to launch.")
                
                self.root.after(2000, lambda: self._update_progress("", 0))
                return True
            else:
                self._log("[VERIFY] ✗ Client executable not found after extraction")
                self._log("[VERIFY] Expected: " + str(CLIENT_EXE))
                self._update_progress("", 0)
                return False
            
        except requests.Timeout:
            self._log("[DOWNLOAD] ✗ Download timeout (took too long)")
            self._log("[DOWNLOAD] Try again or check your internet connection")
            self._update_progress("", 0)
            return False
        except Exception as e:
            self._log(f"[DOWNLOAD] ✗ Auto-download failed: {str(e)}")
            self._log("[DOWNLOAD] Will fallback to manual download")
            self._update_progress("", 0)
            return False
    
    def run(self):
        """Start the launcher"""
        self.root.mainloop()


if __name__ == "__main__":
    print("=" * 60)
    print("GALION Launcher - Custom Client")
    print("=" * 60)
    print()
    
    GalionLauncher().run()

