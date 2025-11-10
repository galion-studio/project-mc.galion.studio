#!/usr/bin/env python3
"""
ULTRA-SIMPLE Launcher - Musk Style + Grok AI Integration
Downloads Minecraft, gets mods, launches. With transparent progress and AI chat!
"""
import tkinter as tk
from tkinter import messagebox, scrolledtext
import minecraft_launcher_lib
import subprocess
import requests
import sys
from pathlib import Path
import uuid
import json
import os
from dotenv import load_dotenv
import asyncio
import threading

# Config
SERVER = "http://localhost:8080"
MC_VERSION = "1.21.1"
MINECRAFT_DIR = str(Path.home() / "AppData" / "Roaming" / ".minecraft")
MODS_DIR = Path(MINECRAFT_DIR) / "mods"

# Hide console
if sys.platform == "win32":
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

class QuickLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Titan Launcher + Grok AI")
        self.root.geometry("800x700")
        self.root.configure(bg="#0a0e27")
        
        # Load Grok API key
        load_dotenv("../.env.grok")
        self.grok_api_key = os.getenv("OPENROUTER_API_KEY")
        self.grok_enabled = bool(self.grok_api_key and self.grok_api_key != "your-openrouter-api-key-here")
        
        # UI
        tk.Label(
            self.root,
            text="TITAN LAUNCHER",
            font=("Arial", 24, "bold"),
            bg="#0a0e27",
            fg="white"
        ).pack(pady=10)
        
        tk.Label(
            self.root,
            text="🌟 Open Source - Everyone Gets Admin! 🌟",
            font=("Arial", 10, "bold"),
            bg="#0a0e27",
            fg="#00d9a3"
        ).pack(pady=5)
        
        self.status = tk.Label(
            self.root,
            text="Ready",
            font=("Arial", 12),
            bg="#0a0e27",
            fg="white"
        )
        self.status.pack(pady=10)
        
        self.progress = tk.Label(
            self.root,
            text="",
            font=("Arial", 10),
            bg="#0a0e27",
            fg="#888"
        )
        self.progress.pack()
        
        # Detailed download log (TRANSPARENT!)
        log_frame = tk.Frame(self.root, bg="#1a1f3a")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(
            log_frame,
            text="📊 Detailed Download Progress (Transparent Build)",
            font=("Arial", 9, "bold"),
            bg="#1a1f3a",
            fg="white"
        ).pack(pady=5)
        
        self.log = scrolledtext.ScrolledText(
            log_frame,
            height=8,
            font=("Consolas", 9),
            bg="#0a0e27",
            fg="#00d9a3",
            insertbackground="white"
        )
        self.log.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log.insert(1.0, "Ready to download. All operations will be shown here transparently.\n")
        self.log.config(state=tk.DISABLED)
        
        # Grok AI Chat (if enabled)
        if self.grok_enabled:
            ai_frame = tk.Frame(self.root, bg="#1a1f3a")
            ai_frame.pack(fill=tk.X, padx=20, pady=5)
            
            tk.Label(
                ai_frame,
                text="🤖 Grok 4 Fast AI Assistant",
                font=("Arial", 9, "bold"),
                bg="#1a1f3a",
                fg="#4a9eff"
            ).pack()
            
            self.ai_entry = tk.Entry(ai_frame, font=("Arial", 10))
            self.ai_entry.pack(fill=tk.X, pady=3)
            self.ai_entry.bind("<Return>", lambda e: self._ask_grok())
            
            tk.Button(
                ai_frame,
                text="Ask Grok",
                font=("Arial", 9),
                bg="#4a9eff",
                fg="white",
                command=self._ask_grok
            ).pack(pady=3)
        
        tk.Label(
            self.root,
            text="Username (Default: galion.studio = Admin):",
            font=("Arial", 10),
            bg="#0a0e27",
            fg="white"
        ).pack(pady=(30, 5))
        
        self.username = tk.Entry(self.root, font=("Arial", 12))
        self.username.insert(0, self._load_username())
        self.username.pack(pady=5)
        
        self.btn = tk.Button(
            self.root,
            text="PLAY",
            font=("Arial", 14, "bold"),
            bg="#00d9a3",
            fg="white",
            command=self._play,
            width=20,
            height=2
        )
        self.btn.pack(pady=30)
    
    def _load_username(self):
        """Default to galion.studio - everyone gets admin freedoms!"""
        try:
            cfg = Path(MINECRAFT_DIR) / "config.json"
            if cfg.exists():
                return json.load(open(cfg)).get("user", "galion.studio")
        except:
            pass
        return "galion.studio"  # Open source = full admin access for all!
    
    def _save_username(self, name):
        try:
            cfg = Path(MINECRAFT_DIR) / "config.json"
            json.dump({"user": name}, open(cfg, 'w'))
        except:
            pass
    
    def _play(self):
        user = self.username.get().strip()
        if not user:
            messagebox.showerror("Error", "Enter username")
            return
        
        self._save_username(user)
        self.btn.config(state=tk.DISABLED)
        
        import threading
        threading.Thread(target=self._launch_thread, args=(user,), daemon=True).start()
    
    def _launch_thread(self, user):
        try:
            # 1. Install Minecraft if needed
            mc_jar = Path(MINECRAFT_DIR) / "versions" / MC_VERSION / f"{MC_VERSION}.jar"
            if not mc_jar.exists() or mc_jar.stat().st_size < 15*1024*1024:
                self._update("Installing Minecraft...", "This takes 5-10 minutes first time")
                self._log(f"[DOWNLOAD] Starting Minecraft {MC_VERSION} installation")
                self._log(f"[DOWNLOAD] Target: {MINECRAFT_DIR}")
                
                # Track download progress
                total_files = 0
                current_file = 0
                
                def progress_callback(data):
                    nonlocal current_file, total_files
                    if "setMax" in str(data):
                        total_files = data
                        self._log(f"[DOWNLOAD] Total files to download: {total_files}")
                    elif "setProgress" in str(data):
                        current_file = data
                        if total_files > 0 and current_file % 10 == 0:
                            percent = int((current_file / total_files) * 100)
                            self._log(f"[PROGRESS] {current_file}/{total_files} files ({percent}%)")
                    elif "setStatus" in str(data):
                        self._log(f"[PHASE] {data}")
                
                minecraft_launcher_lib.install.install_minecraft_version(
                    MC_VERSION,
                    MINECRAFT_DIR,
                    callback={
                        "setMax": lambda x: progress_callback(x),
                        "setProgress": lambda x: progress_callback(x),
                        "setStatus": lambda x: progress_callback(x)
                    }
                )
                
                self._log(f"[DOWNLOAD] Minecraft installation complete!")
                self._log(f"[SIZE] JAR file: {mc_jar.stat().st_size / 1024 / 1024:.2f} MB")
            
            # 2. Get mods from server
            self._update("Getting mods from server...", "")
            self._log(f"[MOD SYNC] Connecting to {SERVER}")
            MODS_DIR.mkdir(parents=True, exist_ok=True)
            
            try:
                self._log(f"[MOD SYNC] Fetching manifest...")
                manifest = requests.get(f"{SERVER}/manifest.json", timeout=3).json()
                mods = manifest.get("mods", [])
                self._log(f"[MOD SYNC] Found {len(mods)} mods on server")
                
                for i, mod in enumerate(mods):
                    mod_file = MODS_DIR / mod["name"]
                    if not mod_file.exists():
                        self._update(f"Downloading {mod['name']}...", f"{i+1}/{len(mods)}")
                        self._log(f"[MOD {i+1}/{len(mods)}] Downloading: {mod['name']}")
                        self._log(f"[MOD {i+1}/{len(mods)}] Size: {mod.get('size', 0) / 1024:.2f} KB")
                        
                        data = requests.get(f"{SERVER}{mod['url']}").content
                        mod_file.write_bytes(data)
                        
                        self._log(f"[MOD {i+1}/{len(mods)}] ✓ Downloaded: {mod['name']}")
                    else:
                        self._log(f"[MOD {i+1}/{len(mods)}] ✓ Already have: {mod['name']}")
                
                self._log(f"[MOD SYNC] Complete! All mods ready.")
            except Exception as e:
                self._log(f"[MOD SYNC] Server offline or error: {e}")
                self._update("Server offline - launching without mods", "")
            
            # 3. Launch
            self._update("Launching Minecraft...", "")
            self._log(f"[LAUNCH] Building launch command...")
            self._log(f"[LAUNCH] Username: {user}")
            self._log(f"[LAUNCH] Version: {MC_VERSION}")
            self._log(f"[LAUNCH] Directory: {MINECRAFT_DIR}")
            
            options = {
                "username": user,
                "uuid": str(uuid.uuid4()),
                "token": ""
            }
            
            command = minecraft_launcher_lib.command.get_minecraft_command(
                MC_VERSION,
                MINECRAFT_DIR,
                options
            )
            
            self._log(f"[LAUNCH] Command built: {len(command)} arguments")
            self._log(f"[LAUNCH] Java executable: {command[0]}")
            
            # Launch hidden
            si = None
            if sys.platform == "win32":
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                si.wShowWindow = 0
            
            process = subprocess.Popen(
                command,
                cwd=MINECRAFT_DIR,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                startupinfo=si,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            )
            
            self._log(f"[LAUNCH] ✓ Minecraft process started (PID: {process.pid})")
            self._log(f"[LAUNCH] Game should open in 10-30 seconds")
            self._log(f"[SUCCESS] All systems go! Enjoy playing!")
            if self.grok_enabled:
                self._log(f"[AI] Grok 4 Fast is ready - ask me anything!")
            
            self._update("Launched!", "Minimizing in 2 seconds...")
            self.root.after(2000, self.root.iconify)
            
        except Exception as e:
            self._update(f"Error: {e}", "")
            messagebox.showerror("Error", str(e))
            self.btn.config(state=tk.NORMAL)
    
    def _log(self, message):
        """Add message to transparent log"""
        def append():
            self.log.config(state=tk.NORMAL)
            self.log.insert(tk.END, f"{message}\n")
            self.log.see(tk.END)
            self.log.config(state=tk.DISABLED)
        self.root.after(0, append)
    
    def _update(self, status, progress):
        self.root.after(0, lambda: self.status.config(text=status))
        self.root.after(0, lambda: self.progress.config(text=progress))
        self._log(f"[STATUS] {status} - {progress}")
    
    def _ask_grok(self):
        """Ask Grok AI a question"""
        if not self.grok_enabled:
            messagebox.showinfo("Grok AI", "Grok API key not configured. Add OPENROUTER_API_KEY to .env.grok")
            return
        
        question = self.ai_entry.get().strip()
        if not question:
            return
        
        self.ai_entry.delete(0, tk.END)
        self._log(f"[YOU] {question}")
        self._log("[GROK] Thinking...")
        
        # Ask in background
        threading.Thread(target=self._grok_thread, args=(question,), daemon=True).start()
    
    def _grok_thread(self, question):
        """Background Grok API call"""
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
                        {"role": "user", "content": question}
                    ],
                    "max_tokens": 150
                },
                timeout=10
            )
            
            if response.status_code == 200:
                answer = response.json()["choices"][0]["message"]["content"]
                self._log(f"[GROK] {answer}")
            else:
                self._log(f"[GROK] Error: {response.status_code}")
        except Exception as e:
            self._log(f"[GROK] Failed: {str(e)}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    QuickLauncher().run()

