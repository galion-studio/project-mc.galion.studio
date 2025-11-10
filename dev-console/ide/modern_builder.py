"""
Modern Mod Builder Component
Beautiful, powerful build system with real-time output
"""

import customtkinter as ctk
import subprocess
import threading
from pathlib import Path
from typing import Optional
import time
from datetime import datetime

from config import THEME, LAYOUT, PROJECT_ROOT, SERVER_MODS_DIR
from database.db_manager import DatabaseManager


class ModBuilder(ctk.CTkScrollableFrame):
    """
    Modern mod builder with Gradle integration.
    Build, test, deploy - beautifully.
    """
    
    def __init__(self, parent, db: DatabaseManager):
        super().__init__(
            parent,
            fg_color=THEME["bg_primary"],
            corner_radius=0
        )
        
        self.db = db
        self.build_process = None
        self.is_building = False
        self.build_start_time = None
        
        # Modern header
        header = ctk.CTkFrame(self, fg_color=THEME["bg_secondary"], height=100)
        header.pack(fill="x", padx=20, pady=(20, 10))
        header.pack_propagate(False)
        
        title = ctk.CTkLabel(
            header,
            text="🔨 Mod Builder",
            font=("Segoe UI", 28, "bold"),
            text_color=THEME["text_primary"]
        )
        title.pack(side="left", padx=30, pady=30)
        
        subtitle = ctk.CTkLabel(
            header,
            text="Build and deploy mods with Gradle",
            font=THEME["font_body"],
            text_color=THEME["text_secondary"]
        )
        subtitle.pack(side="left", padx=(0, 30), pady=30)
        
        # Build status card
        self.create_build_status_card()
        
        # Project configuration
        self.create_project_config()
        
        # Build options
        self.create_build_options()
        
        # Quick build actions
        self.create_quick_builds()
        
        # Build output
        self.create_output_section()
    
    def create_build_status_card(self):
        """Create build status display card"""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="x", padx=20, pady=10)
        
        # Status card
        status_card = ctk.CTkFrame(
            container,
            fg_color=THEME["card_bg"],
            corner_radius=15,
            height=140
        )
        status_card.pack(fill="x")
        status_card.pack_propagate(False)
        
        # Left side - Status indicator
        left_frame = ctk.CTkFrame(status_card, fg_color="transparent")
        left_frame.pack(side="left", fill="y", padx=30, pady=30)
        
        # Build status indicator
        self.build_status_indicator = ctk.CTkFrame(
            left_frame,
            fg_color=THEME["text_dim"],
            width=60,
            height=60,
            corner_radius=30
        )
        self.build_status_indicator.pack()
        
        indicator_icon = ctk.CTkLabel(
            self.build_status_indicator,
            text="🔨",
            font=("Segoe UI", 28)
        )
        indicator_icon.place(relx=0.5, rely=0.5, anchor="center")
        
        # Right side - Status text
        right_frame = ctk.CTkFrame(status_card, fg_color="transparent")
        right_frame.pack(side="left", fill="both", expand=True, pady=30)
        
        self.build_status_text = ctk.CTkLabel(
            right_frame,
            text="READY",
            font=("Segoe UI", 32, "bold"),
            text_color=THEME["text_secondary"],
            anchor="w"
        )
        self.build_status_text.pack(anchor="w", pady=(8, 5))
        
        self.build_details = ctk.CTkLabel(
            right_frame,
            text="No builds in progress",
            font=("Segoe UI", 14),
            text_color=THEME["text_dim"],
            anchor="w"
        )
        self.build_details.pack(anchor="w")
        
        # Metrics
        metrics_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        metrics_frame.pack(anchor="w", pady=(15, 0))
        
        self.last_build_badge = self.create_badge(metrics_frame, "⏱", "No builds")
        self.last_build_badge.pack(side="left", padx=(0, 10))
        
        self.success_rate_badge = self.create_badge(metrics_frame, "✓", "0%")
        self.success_rate_badge.pack(side="left")
    
    def create_badge(self, parent, icon, text):
        """Create metric badge"""
        badge = ctk.CTkFrame(
            parent,
            fg_color=THEME["bg_primary"],
            corner_radius=8
        )
        
        label = ctk.CTkLabel(
            badge,
            text=f"{icon} {text}",
            font=THEME["font_body"],
            text_color=THEME["text_secondary"]
        )
        label.pack(padx=15, pady=8)
        
        badge.label = label  # Store reference for updates
        return badge
    
    def create_project_config(self):
        """Create project configuration section"""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="x", padx=20, pady=10)
        
        label = ctk.CTkLabel(
            container,
            text="📁 Project Configuration",
            font=("Segoe UI", 20, "bold"),
            text_color=THEME["text_primary"],
            anchor="w"
        )
        label.pack(fill="x", pady=(0, 10))
        
        config_card = ctk.CTkFrame(
            container,
            fg_color=THEME["card_bg"],
            corner_radius=15
        )
        config_card.pack(fill="x")
        
        config_content = ctk.CTkFrame(config_card, fg_color="transparent")
        config_content.pack(fill="x", padx=25, pady=20)
        
        # Project path
        ctk.CTkLabel(
            config_content,
            text="Project Path:",
            font=("Segoe UI", 13),
            text_color=THEME["text_secondary"]
        ).pack(anchor="w", pady=(0, 8))
        
        path_frame = ctk.CTkFrame(config_content, fg_color="transparent")
        path_frame.pack(fill="x", pady=(0, 15))
        
        self.project_path_entry = ctk.CTkEntry(
            path_frame,
            font=THEME["font_code"],
            placeholder_text="Path to mod project...",
            height=45
        )
        self.project_path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.project_path_entry.insert(0, str(PROJECT_ROOT))
        
        ctk.CTkButton(
            path_frame,
            text="📁 Browse",
            width=120,
            height=45,
            fg_color=THEME["card_bg"],
            hover_color=THEME["card_hover"],
            command=self.browse_project
        ).pack(side="left")
    
    def create_build_options(self):
        """Create build options section"""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="x", padx=20, pady=10)
        
        label = ctk.CTkLabel(
            container,
            text="⚙️ Build Configuration",
            font=("Segoe UI", 20, "bold"),
            text_color=THEME["text_primary"],
            anchor="w"
        )
        label.pack(fill="x", pady=(0, 10))
        
        options_card = ctk.CTkFrame(
            container,
            fg_color=THEME["card_bg"],
            corner_radius=15
        )
        options_card.pack(fill="x")
        
        options_content = ctk.CTkFrame(options_card, fg_color="transparent")
        options_content.pack(fill="x", padx=25, pady=20)
        
        # Build task selection
        task_frame = ctk.CTkFrame(options_content, fg_color="transparent")
        task_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            task_frame,
            text="Build Task:",
            font=("Segoe UI", 13),
            text_color=THEME["text_secondary"],
            width=120,
            anchor="w"
        ).pack(side="left")
        
        self.task_menu = ctk.CTkOptionMenu(
            task_frame,
            values=["build", "clean build", "jar", "shadowJar", "buildAll", "cleanAll"],
            font=THEME["font_body"],
            fg_color=THEME["accent"],
            button_color=THEME["accent"],
            button_hover_color=THEME["accent_hover"],
            width=200,
            height=40
        )
        self.task_menu.set("build")
        self.task_menu.pack(side="left")
        
        # Options checkboxes
        checkbox_frame = ctk.CTkFrame(options_content, fg_color="transparent")
        checkbox_frame.pack(fill="x")
        
        self.auto_deploy_var = ctk.BooleanVar(value=True)
        self.auto_deploy_checkbox = ctk.CTkCheckBox(
            checkbox_frame,
            text="Auto-deploy to server-mods",
            variable=self.auto_deploy_var,
            font=THEME["font_body"],
            text_color=THEME["text_primary"],
            fg_color=THEME["accent"],
            hover_color=THEME["accent_hover"]
        )
        self.auto_deploy_checkbox.pack(side="left", padx=(0, 20))
        
        self.clean_build_var = ctk.BooleanVar(value=False)
        self.clean_build_checkbox = ctk.CTkCheckBox(
            checkbox_frame,
            text="Clean before build",
            variable=self.clean_build_var,
            font=THEME["font_body"],
            text_color=THEME["text_primary"],
            fg_color=THEME["accent"],
            hover_color=THEME["accent_hover"]
        )
        self.clean_build_checkbox.pack(side="left")
    
    def create_quick_builds(self):
        """Create quick build actions"""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="x", padx=20, pady=10)
        
        label = ctk.CTkLabel(
            container,
            text="⚡ Quick Actions",
            font=("Segoe UI", 20, "bold"),
            text_color=THEME["text_primary"],
            anchor="w"
        )
        label.pack(fill="x", pady=(0, 10))
        
        actions_card = ctk.CTkFrame(
            container,
            fg_color=THEME["card_bg"],
            corner_radius=15
        )
        actions_card.pack(fill="x")
        
        buttons_frame = ctk.CTkFrame(actions_card, fg_color="transparent")
        buttons_frame.pack(pady=25, padx=25, fill="x")
        
        # Build button
        self.build_button = ctk.CTkButton(
            buttons_frame,
            text="🔨  BUILD PROJECT",
            font=("Segoe UI", 15, "bold"),
            fg_color=THEME["success"],
            hover_color="#00c993",
            height=60,
            corner_radius=10,
            command=self.start_build
        )
        self.build_button.pack(side="left", fill="x", expand=True, padx=5)
        
        # Clean button
        self.clean_button = ctk.CTkButton(
            buttons_frame,
            text="🧹  CLEAN PROJECT",
            font=("Segoe UI", 15, "bold"),
            fg_color=THEME["warning"],
            hover_color="#ff9937",
            height=60,
            corner_radius=10,
            command=self.clean_project
        )
        self.clean_button.pack(side="left", fill="x", expand=True, padx=5)
        
        # Stop button
        self.stop_button = ctk.CTkButton(
            buttons_frame,
            text="⏹  STOP BUILD",
            font=("Segoe UI", 15, "bold"),
            fg_color=THEME["error"],
            hover_color="#cc4444",
            height=60,
            corner_radius=10,
            state="disabled",
            command=self.stop_build
        )
        self.stop_button.pack(side="left", fill="x", expand=True, padx=5)
    
    def create_output_section(self):
        """Create build output section"""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Header with controls
        header_frame = ctk.CTkFrame(container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            header_frame,
            text="📜 Build Output",
            font=("Segoe UI", 20, "bold"),
            text_color=THEME["text_primary"],
            anchor="w"
        ).pack(side="left")
        
        # Clear button
        ctk.CTkButton(
            header_frame,
            text="🗑 Clear",
            width=100,
            height=35,
            fg_color=THEME["card_bg"],
            hover_color=THEME["card_hover"],
            command=self.clear_output
        ).pack(side="right")
        
        # Output card
        output_card = ctk.CTkFrame(
            container,
            fg_color=THEME["card_bg"],
            corner_radius=15
        )
        output_card.pack(fill="both", expand=True)
        
        # Output text with line numbers
        self.output_text = ctk.CTkTextbox(
            output_card,
            fg_color=THEME["bg_primary"],
            text_color=THEME["text_primary"],
            font=("Consolas", 11),
            wrap="word"
        )
        self.output_text.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Initial message
        welcome = "╔══════════════════════════════════════════════════════════╗\n"
        welcome += "║          GALION MOD BUILDER - READY                     ║\n"
        welcome += "╚══════════════════════════════════════════════════════════╝\n\n"
        welcome += "Click 'BUILD PROJECT' to start building\n"
        welcome += f"Project: {PROJECT_ROOT}\n"
        
        self.output_text.insert("1.0", welcome)
        self.output_text.configure(state="disabled")
    
    def browse_project(self):
        """Browse for project directory"""
        from tkinter import filedialog
        
        directory = filedialog.askdirectory(
            title="Select Mod Project",
            initialdir=str(PROJECT_ROOT)
        )
        
        if directory:
            self.project_path_entry.delete(0, "end")
            self.project_path_entry.insert(0, directory)
    
    def start_build(self):
        """Start build process"""
        if self.is_building:
            self.log_output("\n[!] Build already in progress\n", "warning")
            return
        
        # Get project path
        project_path = Path(self.project_path_entry.get())
        
        if not project_path.exists():
            self.log_output(f"\n[ERROR] Project path does not exist: {project_path}\n", "error")
            return
        
        # Check for build.gradle
        build_file = project_path / "build.gradle"
        build_file_kts = project_path / "build.gradle.kts"
        
        if not build_file.exists() and not build_file_kts.exists():
            self.log_output("\n[ERROR] No build.gradle or build.gradle.kts found\n", "error")
            return
        
        # Clear output
        self.clear_output()
        
        # Update UI
        self.is_building = True
        self.build_start_time = time.time()
        self.build_button.configure(state="disabled", text="⏳  BUILDING...")
        self.clean_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        
        # Update status card
        self.build_status_indicator.configure(fg_color=THEME["info"])
        self.build_status_text.configure(
            text="BUILDING",
            text_color=THEME["info"]
        )
        self.build_details.configure(text="Build in progress...")
        
        # Start build thread
        thread = threading.Thread(
            target=self._build_thread,
            args=(project_path,),
            daemon=True
        )
        thread.start()
    
    def _build_thread(self, project_path: Path):
        """Build thread"""
        try:
            # Clean first if selected
            if self.clean_build_var.get():
                self.log_output("\n[CLEAN] Cleaning project...\n", "info")
                self._run_gradle_task(project_path, "clean")
                self.log_output("[CLEAN] ✓ Complete\n\n", "success")
            
            # Get task
            task = self.task_menu.get()
            
            self.log_output(f"\n[BUILD] Starting: {task}\n", "info")
            self.log_output(f"[BUILD] Project: {project_path}\n", "info")
            self.log_output("="*60 + "\n\n", "info")
            
            # Run build
            return_code = self._run_gradle_task(project_path, task)
            
            # Calculate build time
            build_time = time.time() - self.build_start_time
            
            self.log_output("\n" + "="*60 + "\n", "info")
            
            if return_code == 0:
                self.log_output(f"[SUCCESS] Build completed in {build_time:.1f}s!\n\n", "success")
                
                # Update status
                self.after(0, lambda: self.build_status_indicator.configure(fg_color=THEME["success"]))
                self.after(0, lambda: self.build_status_text.configure(
                    text="SUCCESS",
                    text_color=THEME["success"]
                ))
                self.after(0, lambda: self.build_details.configure(
                    text=f"Build completed in {build_time:.1f}s"
                ))
                
                # Auto-deploy if enabled
                if self.auto_deploy_var.get():
                    self.log_output("[DEPLOY] Auto-deploying to server-mods...\n", "info")
                    self._auto_deploy(project_path)
            else:
                self.log_output(f"[ERROR] Build failed with code {return_code}\n\n", "error")
                
                # Update status
                self.after(0, lambda: self.build_status_indicator.configure(fg_color=THEME["error"]))
                self.after(0, lambda: self.build_status_text.configure(
                    text="FAILED",
                    text_color=THEME["error"]
                ))
                self.after(0, lambda: self.build_details.configure(
                    text="Build failed - check output"
                ))
        
        except Exception as e:
            self.log_output(f"\n[ERROR] Build error: {str(e)}\n", "error")
            
            self.after(0, lambda: self.build_status_indicator.configure(fg_color=THEME["error"]))
            self.after(0, lambda: self.build_status_text.configure(
                text="ERROR",
                text_color=THEME["error"]
            ))
        
        finally:
            self.is_building = False
            
            # Re-enable buttons
            self.after(0, lambda: self.build_button.configure(
                state="normal",
                text="🔨  BUILD PROJECT"
            ))
            self.after(0, lambda: self.clean_button.configure(state="normal"))
            self.after(0, lambda: self.stop_button.configure(state="disabled"))
            
            # Update metrics
            self.update_build_metrics(build_time if 'build_time' in locals() else 0)
    
    def _run_gradle_task(self, project_path: Path, task: str) -> int:
        """Run Gradle task and stream output"""
        # Determine gradle wrapper
        if (project_path / "gradlew.bat").exists():
            gradle_cmd = str(project_path / "gradlew.bat")
        elif (project_path / "gradlew").exists():
            gradle_cmd = str(project_path / "gradlew")
        else:
            gradle_cmd = "gradle"
        
        # Build command
        cmd = [gradle_cmd, task, "--console=plain"]
        
        # Execute
        process = subprocess.Popen(
            cmd,
            cwd=str(project_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        self.build_process = process
        
        # Stream output
        for line in process.stdout:
            self.log_output(line)
        
        # Wait for completion
        return_code = process.wait()
        self.build_process = None
        
        return return_code
    
    def _auto_deploy(self, project_path: Path):
        """Auto-deploy built mod"""
        # Look for built JAR in build/libs
        libs_dir = project_path / "build" / "libs"
        
        if not libs_dir.exists():
            self.log_output("[DEPLOY] No build/libs directory found\n", "warning")
            return
        
        # Find JAR files (exclude sources and javadoc)
        jar_files = [
            f for f in libs_dir.glob("*.jar")
            if "sources" not in f.name.lower() and "javadoc" not in f.name.lower()
        ]
        
        if not jar_files:
            self.log_output("[DEPLOY] No JAR files found\n", "warning")
            return
        
        # Get most recent JAR
        jar_file = max(jar_files, key=lambda f: f.stat().st_mtime)
        
        self.log_output(f"[DEPLOY] Found: {jar_file.name}\n", "info")
        
        # Copy to server-mods
        import shutil
        
        dest = SERVER_MODS_DIR / jar_file.name
        shutil.copy2(jar_file, dest)
        
        self.log_output(f"[DEPLOY] ✓ Deployed to: {dest}\n", "success")
        self.log_output("[DEPLOY] ✓ Deployment complete!\n\n", "success")
    
    def clean_project(self):
        """Clean project"""
        self.task_menu.set("clean")
        self.start_build()
    
    def stop_build(self):
        """Stop running build"""
        if self.build_process:
            self.build_process.terminate()
            self.log_output("\n\n[STOPPED] Build terminated by user\n", "warning")
            
            self.build_status_text.configure(
                text="STOPPED",
                text_color=THEME["warning"]
            )
            self.build_details.configure(text="Build stopped by user")
    
    def clear_output(self):
        """Clear build output"""
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.configure(state="disabled")
    
    def log_output(self, text: str, level: str = "info"):
        """Log output with color coding"""
        self.after(0, lambda: self._append_output(text, level))
    
    def _append_output(self, text: str, level: str):
        """Append output (must run in main thread)"""
        self.output_text.configure(state="normal")
        self.output_text.insert("end", text)
        self.output_text.see("end")
        self.output_text.configure(state="disabled")
    
    def update_build_metrics(self, build_time: float):
        """Update build metrics"""
        # Update last build time
        self.last_build_badge.label.configure(
            text=f"⏱ Last: {build_time:.1f}s"
        )

