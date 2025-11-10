"""
Galion Studio Minecraft Launcher - Enhanced UI/UX Edition
Beautiful modern launcher with custom design and prominent progress tracking

Features:
- Custom styled window with modern design
- Large, prominent progress bar with percentage
- Real-time download speed display
- Smooth animations
- Professional appearance
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
import time

# Server configuration
SERVER_ADDRESS = "mc.galion.studio"
SERVER_NAME = "Galion Studio"
LAUNCHER_VERSION = "2.1.0"
DEFAULT_MC_VERSION = "1.21.1"  # Updated to match server version

# Color scheme - Modern dark theme
COLOR_PRIMARY = "#1a1a2e"      # Dark blue-black
COLOR_SECONDARY = "#16213e"    # Slightly lighter
COLOR_ACCENT = "#0f3460"       # Blue accent
COLOR_SUCCESS = "#00c853"      # Green for success
COLOR_WARNING = "#ff6b35"      # Orange for warnings
COLOR_TEXT = "#eaeaea"         # Light text
COLOR_TEXT_DIM = "#a0a0a0"     # Dimmed text
COLOR_BUTTON = "#0f3460"       # Button color
COLOR_BUTTON_HOVER = "#1e5a8e" # Button hover
COLOR_PROGRESS = "#00c853"     # Progress bar color


class ModernButton(tk.Canvas):
    """Custom modern button with hover effects"""
    
    def __init__(self, parent, text, command, **kwargs):
        """Initialize custom button"""
        width = kwargs.get('width', 200)
        height = kwargs.get('height', 50)
        bg = kwargs.get('bg', COLOR_BUTTON)
        
        super().__init__(parent, width=width, height=height, bg=bg, 
                        highlightthickness=0, cursor="hand2")
        
        self.command = command
        self.text = text
        self.bg_color = bg
        self.hover_color = kwargs.get('hover_color', COLOR_BUTTON_HOVER)
        self.text_color = kwargs.get('fg', COLOR_TEXT)
        
        # Create rounded rectangle
        self._create_rounded_rect()
        
        # Bind events
        self.bind("<Button-1>", lambda e: self.command())
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _create_rounded_rect(self):
        """Create button shape with text"""
        # Background
        self.bg_rect = self.create_rectangle(
            2, 2, self.winfo_reqwidth()-2, self.winfo_reqheight()-2,
            fill=self.bg_color, outline="", tags="bg"
        )
        
        # Text
        self.text_item = self.create_text(
            self.winfo_reqwidth()//2, self.winfo_reqheight()//2,
            text=self.text, fill=self.text_color,
            font=("Segoe UI", 12, "bold"), tags="text"
        )
    
    def _on_enter(self, event):
        """Mouse hover effect"""
        self.itemconfig(self.bg_rect, fill=self.hover_color)
    
    def _on_leave(self, event):
        """Mouse leave effect"""
        self.itemconfig(self.bg_rect, fill=self.bg_color)
    
    def set_text(self, text):
        """Update button text"""
        self.text = text
        self.itemconfig(self.text_item, text=text)
    
    def set_state(self, state):
        """Enable or disable button"""
        if state == "disabled":
            self.itemconfig(self.bg_rect, fill=COLOR_TEXT_DIM)
            self.unbind("<Button-1>")
            self.config(cursor="")
        else:
            self.itemconfig(self.bg_rect, fill=self.bg_color)
            self.bind("<Button-1>", lambda e: self.command())
            self.config(cursor="hand2")


class EnhancedLauncher:
    """Enhanced launcher with beautiful UI/UX"""
    
    def __init__(self, root):
        """Initialize the enhanced launcher"""
        self.root = root
        self.root.title(f"{SERVER_NAME} Launcher v{LAUNCHER_VERSION}")
        
        # Custom window size
        window_width = 700
        window_height = 600
        
        # Center window on screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(False, False)
        self.root.configure(bg=COLOR_PRIMARY)
        
        # Remove default window border for custom look
        # self.root.overrideredirect(True)  # Uncomment for borderless window
        
        # Download stats
        self.download_start_time = 0
        self.bytes_downloaded = 0
        self.total_bytes = 0
        
        # Minecraft directory
        self.minecraft_dir = self._get_launcher_dir()
        os.makedirs(self.minecraft_dir, exist_ok=True)
        
        # Setup UI
        self._setup_ui()
        
        # Check Minecraft
        self.root.after(100, self._check_minecraft_installed)
    
    def _get_launcher_dir(self):
        """Get custom launcher directory"""
        if sys.platform == "win32":
            base_dir = os.getenv("APPDATA")
        else:
            base_dir = str(Path.home())
        
        return os.path.join(base_dir, "GalionLauncher", "minecraft")
    
    def _setup_ui(self):
        """Create beautiful modern UI"""
        
        # ============ HEADER ============
        header_frame = tk.Frame(self.root, bg=COLOR_SECONDARY, height=120)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Server name with large text
        title_label = tk.Label(
            header_frame,
            text=SERVER_NAME,
            font=("Segoe UI", 32, "bold"),
            bg=COLOR_SECONDARY,
            fg=COLOR_TEXT
        )
        title_label.pack(pady=(20, 5))
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Made for Galion Studio Minecraft Project",
            font=("Segoe UI", 10),
            bg=COLOR_SECONDARY,
            fg=COLOR_TEXT_DIM
        )
        subtitle_label.pack()
        
        # ============ MAIN CONTENT ============
        content_frame = tk.Frame(self.root, bg=COLOR_PRIMARY)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Server info card
        info_card = tk.Frame(content_frame, bg=COLOR_ACCENT, padx=20, pady=15)
        info_card.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            info_card,
            text="🌐 SERVER INFO",
            font=("Segoe UI", 9, "bold"),
            bg=COLOR_ACCENT,
            fg=COLOR_TEXT_DIM
        ).pack(anchor=tk.W)
        
        tk.Label(
            info_card,
            text=f"Address: {SERVER_ADDRESS}",
            font=("Segoe UI", 11),
            bg=COLOR_ACCENT,
            fg=COLOR_TEXT
        ).pack(anchor=tk.W, pady=(5, 0))
        
        tk.Label(
            info_card,
            text=f"Minecraft Version: {DEFAULT_MC_VERSION}",
            font=("Segoe UI", 11),
            bg=COLOR_ACCENT,
            fg=COLOR_TEXT
        ).pack(anchor=tk.W, pady=(2, 0))
        
        # Username section
        username_card = tk.Frame(content_frame, bg=COLOR_ACCENT, padx=20, pady=15)
        username_card.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            username_card,
            text="👤 PLAYER NAME",
            font=("Segoe UI", 9, "bold"),
            bg=COLOR_ACCENT,
            fg=COLOR_TEXT_DIM
        ).pack(anchor=tk.W)
        
        self.username_var = tk.StringVar(value=self._load_username())
        username_entry = tk.Entry(
            username_card,
            textvariable=self.username_var,
            font=("Segoe UI", 14),
            bg=COLOR_SECONDARY,
            fg=COLOR_TEXT,
            insertbackground=COLOR_TEXT,
            relief=tk.FLAT,
            bd=5
        )
        username_entry.pack(fill=tk.X, pady=(10, 0))
        
        # ============ DOWNLOAD PROGRESS SECTION ============
        self.progress_card = tk.Frame(content_frame, bg=COLOR_ACCENT, padx=20, pady=20)
        # Hidden by default
        
        tk.Label(
            self.progress_card,
            text="⬇️ DOWNLOADING MINECRAFT",
            font=("Segoe UI", 10, "bold"),
            bg=COLOR_ACCENT,
            fg=COLOR_TEXT
        ).pack()
        
        # Download status
        self.download_status_var = tk.StringVar(value="Preparing download...")
        tk.Label(
            self.progress_card,
            textvariable=self.download_status_var,
            font=("Segoe UI", 9),
            bg=COLOR_ACCENT,
            fg=COLOR_TEXT_DIM
        ).pack(pady=(5, 10))
        
        # Progress bar frame
        progress_bg = tk.Frame(self.progress_card, bg=COLOR_SECONDARY, height=40)
        progress_bg.pack(fill=tk.X, pady=(0, 10))
        progress_bg.pack_propagate(False)
        
        # Custom progress bar (using Canvas for better styling)
        self.progress_canvas = tk.Canvas(
            progress_bg,
            bg=COLOR_SECONDARY,
            height=40,
            highlightthickness=0
        )
        self.progress_canvas.pack(fill=tk.BOTH, padx=5, pady=5)
        
        # Progress percentage label
        self.progress_percent_var = tk.StringVar(value="0%")
        tk.Label(
            self.progress_card,
            textvariable=self.progress_percent_var,
            font=("Segoe UI", 16, "bold"),
            bg=COLOR_ACCENT,
            fg=COLOR_SUCCESS
        ).pack()
        
        # Download speed and ETA
        self.download_details_var = tk.StringVar(value="")
        tk.Label(
            self.progress_card,
            textvariable=self.download_details_var,
            font=("Segoe UI", 9),
            bg=COLOR_ACCENT,
            fg=COLOR_TEXT_DIM
        ).pack(pady=(5, 0))
        
        # ============ STATUS MESSAGE ============
        self.status_var = tk.StringVar(value="Checking installation...")
        status_label = tk.Label(
            content_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 10),
            bg=COLOR_PRIMARY,
            fg=COLOR_TEXT_DIM
        )
        status_label.pack(pady=(10, 15))
        
        # ============ LAUNCH BUTTON ============
        button_frame = tk.Frame(content_frame, bg=COLOR_PRIMARY)
        button_frame.pack()
        
        self.launch_button = ModernButton(
            button_frame,
            text="CHECKING...",
            command=self._launch_or_download,
            width=300,
            height=60,
            bg=COLOR_TEXT_DIM
        )
        self.launch_button.pack()
        self.launch_button.set_state("disabled")
        
        # ============ FOOTER ============
        footer_frame = tk.Frame(self.root, bg=COLOR_PRIMARY, height=60)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)
        
        tk.Label(
            footer_frame,
            text=f"v{LAUNCHER_VERSION} • Enhanced Edition • Made for Galion Studio Minecraft Project",
            font=("Segoe UI", 8),
            bg=COLOR_PRIMARY,
            fg=COLOR_TEXT_DIM
        ).pack(pady=(5, 0))
        
        # GitHub link
        github_label = tk.Label(
            footer_frame,
            text="🔗 GitHub: github.com/galion-studio/minecraft-launcher",
            font=("Segoe UI", 8),
            bg=COLOR_PRIMARY,
            fg=COLOR_ACCENT,
            cursor="hand2"
        )
        github_label.pack(pady=(2, 5))
        
        # Make GitHub link clickable
        def open_github(event):
            import webbrowser
            webbrowser.open("https://github.com/galion-studio/minecraft-launcher")
        
        github_label.bind("<Button-1>", open_github)
        github_label.bind("<Enter>", lambda e: github_label.config(fg=COLOR_SUCCESS))
        github_label.bind("<Leave>", lambda e: github_label.config(fg=COLOR_ACCENT))
    
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
        except Exception as e:
            print(f"Failed to save username: {e}")
    
    def _check_minecraft_installed(self):
        """Check if Minecraft is installed"""
        version_path = os.path.join(
            self.minecraft_dir,
            "versions",
            DEFAULT_MC_VERSION
        )
        
        if os.path.exists(version_path):
            # Minecraft is installed
            self.status_var.set(f"✅ Minecraft {DEFAULT_MC_VERSION} is ready to play!")
            self.launch_button.set_text("🎮 PLAY NOW")
            self.launch_button.set_state("normal")
            self.minecraft_installed = True
        else:
            # Need to download
            self.status_var.set(f"⚠️ Minecraft {DEFAULT_MC_VERSION} not found - Ready to download")
            self.launch_button.set_text("⬇️ DOWNLOAD & INSTALL")
            self.launch_button.set_state("normal")
            self.minecraft_installed = False
    
    def _launch_or_download(self):
        """Launch or download Minecraft"""
        username = self.username_var.get().strip()
        
        if not username:
            self.status_var.set("❌ Please enter a player name")
            return
        
        self._save_username(username)
        
        if self.minecraft_installed:
            self._launch_minecraft(username)
        else:
            self._download_minecraft()
    
    def _download_minecraft(self):
        """Start Minecraft download"""
        self.launch_button.set_state("disabled")
        self.launch_button.set_text("⏳ DOWNLOADING...")
        self.progress_card.pack(fill=tk.X, pady=(0, 20))
        self.download_start_time = time.time()
        
        # Start download thread
        thread = threading.Thread(target=self._download_thread)
        thread.daemon = True
        thread.start()
    
    def _download_thread(self):
        """Background download thread"""
        def callback(status_type, value):
            self._update_download_progress(status_type, value)
        
        try:
            callback_dict = {
                "setStatus": lambda status: callback("status", status),
                "setProgress": lambda progress: callback("progress", progress),
                "setMax": lambda max_val: callback("max", max_val)
            }
            
            minecraft_launcher_lib.install.install_minecraft_version(
                DEFAULT_MC_VERSION,
                self.minecraft_dir,
                callback=callback_dict
            )
            
            self.root.after(0, self._download_complete, True)
        except Exception as e:
            print(f"Download error: {e}")
            self.root.after(0, self._download_complete, False)
    
    def _update_download_progress(self, status_type, value):
        """Update progress bar and stats"""
        def update():
            if status_type == "status":
                # Update status message
                self.download_status_var.set(value)
            
            elif status_type == "max":
                # Set total bytes
                self.total_bytes = value
            
            elif status_type == "progress":
                # Update progress
                self.bytes_downloaded = value
                
                if self.total_bytes > 0:
                    # Calculate percentage
                    percent = (value / self.total_bytes) * 100
                    self.progress_percent_var.set(f"{percent:.1f}%")
                    
                    # Draw progress bar (force update)
                    try:
                        self._draw_progress_bar(percent)
                    except Exception as e:
                        print(f"Progress bar draw error: {e}")
                    
                    # Calculate speed and ETA
                    elapsed = time.time() - self.download_start_time
                    if elapsed > 0:
                        speed = value / elapsed / 1024 / 1024  # MB/s
                        remaining = (self.total_bytes - value) / (value / elapsed) if value > 0 else 0
                        
                        # Format details
                        downloaded_mb = value / 1024 / 1024
                        total_mb = self.total_bytes / 1024 / 1024
                        eta_min = int(remaining / 60)
                        eta_sec = int(remaining % 60)
                        
                        details = f"📊 {downloaded_mb:.1f} MB / {total_mb:.1f} MB  •  🚀 {speed:.2f} MB/s  •  ⏱️ ETA: {eta_min}m {eta_sec}s"
                        self.download_details_var.set(details)
        
        self.root.after(0, update)
    
    def _draw_progress_bar(self, percent):
        """Draw custom progress bar"""
        self.progress_canvas.delete("all")
        
        # Force canvas to update geometry first
        self.progress_canvas.update_idletasks()
        
        width = self.progress_canvas.winfo_width()
        height = self.progress_canvas.winfo_height()
        
        if width <= 1:  # Not rendered yet, use fixed width
            width = 580
        if height <= 1:
            height = 30
        
        # Calculate progress width
        progress_width = int((width * percent) / 100)
        
        # Draw background (empty part)
        self.progress_canvas.create_rectangle(
            0, 0, width, height,
            fill=COLOR_ACCENT,
            outline=""
        )
        
        # Draw progress (filled part)
        if progress_width > 0:
            self.progress_canvas.create_rectangle(
                0, 0, progress_width, height,
                fill=COLOR_PROGRESS,
                outline=""
            )
        
        # Force canvas to redraw
        self.progress_canvas.update()
    
    def _download_complete(self, success):
        """Download complete callback"""
        self.progress_card.pack_forget()
        
        if success:
            self.minecraft_installed = True
            self.status_var.set("✅ Download complete! Ready to play!")
            self.launch_button.set_text("🎮 PLAY NOW")
            self.launch_button.set_state("normal")
        else:
            self.status_var.set("❌ Download failed - Click to retry")
            self.launch_button.set_text("🔄 RETRY DOWNLOAD")
            self.launch_button.set_state("normal")
    
    def _launch_minecraft(self, username):
        """Launch Minecraft with progress feedback"""
        # Show launch progress
        self.launch_button.set_state("disabled")
        self.launch_button.set_text("⏳ PREPARING...")
        
        # Start launch in background thread
        thread = threading.Thread(target=self._launch_thread, args=(username,))
        thread.daemon = True
        thread.start()
    
    def _find_java(self):
        """Find Java installation"""
        import shutil
        
        # Try to find java executable
        java_executable = shutil.which("java")
        if java_executable:
            return java_executable
        
        # Try common Java locations on Windows
        if sys.platform == "win32":
            common_paths = [
                r"C:\Program Files\Java\jre-1.8\bin\java.exe",
                r"C:\Program Files\Java\jre8\bin\java.exe",
                r"C:\Program Files (x86)\Java\jre-1.8\bin\java.exe",
                r"C:\Program Files\Microsoft\jdk-17\bin\java.exe",
                r"C:\Program Files\Microsoft\jdk-11\bin\java.exe",
                r"C:\Program Files\Eclipse Adoptium\jre-17\bin\java.exe",
                r"C:\Program Files\Eclipse Adoptium\jre-8\bin\java.exe",
            ]
            
            # Also check JAVA_HOME
            java_home = os.getenv("JAVA_HOME")
            if java_home:
                java_path = os.path.join(java_home, "bin", "java.exe")
                if os.path.exists(java_path):
                    return java_path
            
            # Check common paths
            for path in common_paths:
                if os.path.exists(path):
                    return path
        
        return None
    
    def _launch_thread(self, username):
        """Background thread for launching"""
        try:
            # Step 1: Verify files
            self.root.after(0, lambda: self.status_var.set("🔍 Verifying game files..."))
            self.root.after(0, lambda: self.launch_button.set_text("🔍 VERIFYING..."))
            
            version_path = os.path.join(
                self.minecraft_dir,
                "versions",
                DEFAULT_MC_VERSION
            )
            
            if not os.path.exists(version_path):
                raise Exception("Minecraft files not found. Please download again.")
            
            time.sleep(0.5)  # Brief pause for visual feedback
            
            # Step 1.5: Check Java
            self.root.after(0, lambda: self.status_var.set("☕ Checking Java installation..."))
            java_path = self._find_java()
            
            if not java_path:
                raise Exception(
                    "Java not found!\n\n"
                    "Minecraft requires Java to run.\n\n"
                    "Please install Java:\n"
                    "1. Download from: https://www.java.com/download/\n"
                    "2. Or install Java 17: https://adoptium.net/\n"
                    "3. Restart this launcher\n\n"
                    "After installing Java, try again."
                )
            
            # Step 2: Prepare launch
            self.root.after(0, lambda: self.status_var.set("⚙️ Preparing Minecraft..."))
            self.root.after(0, lambda: self.launch_button.set_text("⚙️ PREPARING..."))
            
            # Offline authentication
            options = {
                "username": username,
                "uuid": str(uuid.uuid4()),
                "token": ""
            }
            
            # Step 3: Get launch command
            self.root.after(0, lambda: self.status_var.set("🚀 Building launch command..."))
            self.root.after(0, lambda: self.launch_button.set_text("🚀 LAUNCHING..."))
            
            try:
                command = minecraft_launcher_lib.command.get_minecraft_command(
                    DEFAULT_MC_VERSION,
                    self.minecraft_dir,
                    options
                )
            except Exception as e:
                raise Exception(f"Failed to build launch command:\n{str(e)}\n\nTry re-downloading Minecraft.")
            
            # Log the command (for debugging)
            print(f"Launch command: {' '.join(command)}")
            
            time.sleep(0.3)  # Brief pause
            
            # Step 4: Launch process
            self.root.after(0, lambda: self.status_var.set("🎮 Starting Minecraft process..."))
            
            try:
                # Launch with proper working directory
                # NOTE: Removed CREATE_NEW_CONSOLE so we can capture errors properly
                process = subprocess.Popen(
                    command,
                    cwd=self.minecraft_dir,  # Set working directory
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            except Exception as e:
                raise Exception(f"Failed to start Minecraft process:\n{str(e)}\n\nMake sure Java is installed correctly.")
            
            # Wait to check if it started successfully
            time.sleep(3)
            
            # Check if process is still running
            if process.poll() is not None:
                # Process ended immediately - there was an error
                stdout_data = process.stdout.read().decode('utf-8', errors='ignore')
                stderr_data = process.stderr.read().decode('utf-8', errors='ignore')
                
                error_msg = "Minecraft failed to start.\n\n"
                
                if stderr_data:
                    error_msg += f"Error:\n{stderr_data[:500]}\n\n"
                
                if "java" in stderr_data.lower() or "java" in stdout_data.lower():
                    error_msg += "This looks like a Java error.\n"
                    error_msg += "Try installing/updating Java:\n"
                    error_msg += "https://www.java.com/download/\n\n"
                
                if "memory" in stderr_data.lower():
                    error_msg += "Not enough memory.\n"
                    error_msg += "Close other programs and try again.\n\n"
                
                error_msg += "If problem persists:\n"
                error_msg += "1. Install Java from java.com\n"
                error_msg += "2. Restart your computer\n"
                error_msg += "3. Run launcher as Administrator"
                
                raise Exception(error_msg)
            
            # Success!
            self.root.after(0, self._launch_success)
            
        except Exception as e:
            # Show error on main thread
            error_msg = str(e)  # Capture error message before lambda
            self.root.after(0, lambda: self._launch_error(error_msg))
    
    def _launch_success(self):
        """Called when launch succeeds"""
        self.status_var.set(f"✅ Minecraft launched! Connect to: {SERVER_ADDRESS}")
        self.launch_button.set_text("✅ LAUNCHED")
        
        # Show success message
        success_card = tk.Frame(self.root, bg=COLOR_SUCCESS, padx=20, pady=15)
        success_card.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        tk.Label(
            success_card,
            text="✅ Minecraft Started!",
            font=("Segoe UI", 14, "bold"),
            bg=COLOR_SUCCESS,
            fg=COLOR_TEXT
        ).pack()
        
        tk.Label(
            success_card,
            text=f"Connect to: {SERVER_ADDRESS}",
            font=("Segoe UI", 10),
            bg=COLOR_SUCCESS,
            fg=COLOR_TEXT
        ).pack(pady=(5, 0))
        
        # Close launcher after delay
        self.root.after(3000, self.root.destroy)
    
    def _launch_error(self, error_msg):
        """Called when launch fails"""
        self.status_var.set(f"❌ Launch failed - Click to retry")
        self.launch_button.set_text("🔄 RETRY LAUNCH")
        self.launch_button.set_state("normal")
        
        # Show detailed error
        error_window = tk.Toplevel(self.root)
        error_window.title("Launch Error")
        error_window.geometry("500x300")
        error_window.configure(bg=COLOR_PRIMARY)
        
        tk.Label(
            error_window,
            text="❌ Launch Failed",
            font=("Segoe UI", 14, "bold"),
            bg=COLOR_PRIMARY,
            fg=COLOR_WARNING
        ).pack(pady=(20, 10))
        
        # Error message
        error_text = tk.Text(
            error_window,
            height=10,
            width=55,
            bg=COLOR_SECONDARY,
            fg=COLOR_TEXT,
            font=("Consolas", 9),
            wrap=tk.WORD
        )
        error_text.pack(padx=20, pady=10)
        error_text.insert("1.0", error_msg)
        error_text.config(state=tk.DISABLED)
        
        # Close button
        tk.Button(
            error_window,
            text="Close",
            command=error_window.destroy,
            bg=COLOR_BUTTON,
            fg=COLOR_TEXT,
            font=("Segoe UI", 10),
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=10
        ).pack(pady=10)


def main():
    """Main entry point"""
    root = tk.Tk()
    launcher = EnhancedLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()

