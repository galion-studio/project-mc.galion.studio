"""
Mod Builder Component
Build mods from source with Gradle integration
"""

import customtkinter as ctk
import subprocess
import threading
from pathlib import Path
from typing import Optional

from config import THEME, LAYOUT, PROJECT_ROOT
from database.db_manager import DatabaseManager


class ModBuilder(ctk.CTkScrollableFrame):
    """
    Mod builder with Gradle integration.
    Build, test, deploy - all in one place.
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
        
        # Header
        header = ctk.CTkLabel(
            self,
            text="🔨 Mod Builder",
            font=THEME["font_header"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        header.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        # Project selection
        self.create_project_section()
        
        # Build options
        self.create_build_options()
        
        # Build output
        self.create_output_section()
    
    def create_project_section(self):
        """Create project selection section"""
        project_label = ctk.CTkLabel(
            self,
            text="Project",
            font=THEME["font_subheader"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        project_label.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        project_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        project_card.pack(fill="x", padx=LAYOUT["card_padding"], pady=10)
        
        # Project path
        path_frame = ctk.CTkFrame(project_card, fg_color="transparent")
        path_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            path_frame,
            text="Project Path:",
            font=THEME["font_body"],
            text_color=THEME["text_secondary"]
        ).pack(side="left", padx=(0, 10))
        
        self.project_path_entry = ctk.CTkEntry(
            path_frame,
            font=THEME["font_code"],
            placeholder_text="Path to mod project..."
        )
        self.project_path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.project_path_entry.insert(0, str(PROJECT_ROOT))
        
        ctk.CTkButton(
            path_frame,
            text="Browse",
            width=80,
            fg_color=THEME["accent"],
            command=self.browse_project
        ).pack(side="left")
    
    def create_build_options(self):
        """Create build options section"""
        options_label = ctk.CTkLabel(
            self,
            text="Build Options",
            font=THEME["font_subheader"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        options_label.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        options_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        options_card.pack(fill="x", padx=LAYOUT["card_padding"], pady=10)
        
        # Build tasks
        tasks_frame = ctk.CTkFrame(options_card, fg_color="transparent")
        tasks_frame.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(
            tasks_frame,
            text="Build Task:",
            font=THEME["font_body"],
            text_color=THEME["text_secondary"]
        ).pack(side="left", padx=(0, 10))
        
        self.task_menu = ctk.CTkOptionMenu(
            tasks_frame,
            values=["build", "clean build", "jar", "shadowJar", "runClient", "runServer"],
            font=THEME["font_body"],
            fg_color=THEME["accent"],
            button_color=THEME["accent"],
            button_hover_color=THEME["accent_hover"]
        )
        self.task_menu.set("build")
        self.task_menu.pack(side="left", padx=(0, 20))
        
        # Auto-deploy checkbox
        self.auto_deploy_var = ctk.BooleanVar(value=True)
        self.auto_deploy_checkbox = ctk.CTkCheckBox(
            tasks_frame,
            text="Auto-deploy after build",
            variable=self.auto_deploy_var,
            font=THEME["font_body"],
            text_color=THEME["text_primary"],
            fg_color=THEME["accent"]
        )
        self.auto_deploy_checkbox.pack(side="left")
        
        # Build button
        self.build_button = ctk.CTkButton(
            options_card,
            text="🔨 BUILD",
            font=("Segoe UI", 16, "bold"),
            fg_color=THEME["success"],
            hover_color="#00c993",
            height=50,
            command=self.start_build
        )
        self.build_button.pack(fill="x", padx=20, pady=(10, 20))
    
    def create_output_section(self):
        """Create build output section"""
        output_label = ctk.CTkLabel(
            self,
            text="Build Output",
            font=THEME["font_subheader"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        output_label.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        output_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        output_card.pack(fill="both", expand=True, padx=LAYOUT["card_padding"], pady=10)
        
        # Output text
        self.output_text = ctk.CTkTextbox(
            output_card,
            fg_color=THEME["bg_primary"],
            text_color=THEME["text_primary"],
            font=THEME["font_code"],
            wrap="word"
        )
        self.output_text.pack(fill="both", expand=True, padx=15, pady=15)
        self.output_text.insert("1.0", "Ready to build...\n")
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
            self.log_output("[!] Build already in progress\n")
            return
        
        # Get project path
        project_path = Path(self.project_path_entry.get())
        
        if not project_path.exists():
            self.log_output(f"[ERROR] Project path does not exist: {project_path}\n")
            return
        
        # Check for build.gradle
        build_file = project_path / "build.gradle"
        build_file_kts = project_path / "build.gradle.kts"
        
        if not build_file.exists() and not build_file_kts.exists():
            self.log_output("[ERROR] No build.gradle or build.gradle.kts found\n")
            return
        
        # Clear output
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.configure(state="disabled")
        
        # Disable build button
        self.build_button.configure(
            state="disabled",
            text="⏳ BUILDING..."
        )
        
        self.is_building = True
        
        # Start build in thread
        thread = threading.Thread(
            target=self._build_thread,
            args=(project_path,),
            daemon=True
        )
        thread.start()
    
    def _build_thread(self, project_path: Path):
        """Build thread"""
        try:
            # Get task
            task = self.task_menu.get()
            
            self.log_output(f"[BUILD] Starting build: {task}\n")
            self.log_output(f"[BUILD] Project: {project_path}\n")
            self.log_output("="*50 + "\n")
            
            # Determine gradle wrapper
            if Path(project_path / "gradlew.bat").exists():
                gradle_cmd = str(project_path / "gradlew.bat")
            elif Path(project_path / "gradlew").exists():
                gradle_cmd = str(project_path / "gradlew")
            else:
                gradle_cmd = "gradle"  # System gradle
            
            # Build command
            cmd = [gradle_cmd, task]
            
            # Execute build
            process = subprocess.Popen(
                cmd,
                cwd=str(project_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Stream output
            for line in process.stdout:
                self.log_output(line)
            
            # Wait for completion
            return_code = process.wait()
            
            self.log_output("\n" + "="*50 + "\n")
            
            if return_code == 0:
                self.log_output("[SUCCESS] Build completed successfully!\n")
                
                # Auto-deploy if enabled
                if self.auto_deploy_var.get():
                    self.log_output("[DEPLOY] Auto-deploying...\n")
                    self._auto_deploy(project_path)
            else:
                self.log_output(f"[ERROR] Build failed with code {return_code}\n")
        
        except Exception as e:
            self.log_output(f"[ERROR] Build error: {str(e)}\n")
        
        finally:
            self.is_building = False
            
            # Re-enable build button
            self.after(0, lambda: self.build_button.configure(
                state="normal",
                text="🔨 BUILD"
            ))
    
    def _auto_deploy(self, project_path: Path):
        """Auto-deploy built mod"""
        # Look for built JAR in build/libs
        libs_dir = project_path / "build" / "libs"
        
        if not libs_dir.exists():
            self.log_output("[DEPLOY] No build/libs directory found\n")
            return
        
        # Find JAR files (exclude sources and javadoc)
        jar_files = [
            f for f in libs_dir.glob("*.jar")
            if "sources" not in f.name.lower() and "javadoc" not in f.name.lower()
        ]
        
        if not jar_files:
            self.log_output("[DEPLOY] No JAR files found\n")
            return
        
        # Get most recent JAR
        jar_file = max(jar_files, key=lambda f: f.stat().st_mtime)
        
        self.log_output(f"[DEPLOY] Found: {jar_file.name}\n")
        
        # Copy to server-mods
        from config import SERVER_MODS_DIR
        import shutil
        
        dest = SERVER_MODS_DIR / jar_file.name
        shutil.copy2(jar_file, dest)
        
        self.log_output(f"[DEPLOY] Deployed to: {dest}\n")
        self.log_output("[DEPLOY] ✓ Deployment complete!\n")
    
    def log_output(self, text: str):
        """Log output to text widget"""
        self.after(0, lambda: self._append_output(text))
    
    def _append_output(self, text: str):
        """Append output (must run in main thread)"""
        self.output_text.configure(state="normal")
        self.output_text.insert("end", text)
        self.output_text.see("end")
        self.output_text.configure(state="disabled")

