"""
Mod Uploader Component
Drag-and-drop mod upload with progress tracking
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import shutil
import hashlib
import zipfile
import json
from typing import Optional, Dict
import threading

from config import THEME, LAYOUT, SERVER_MODS_DIR, MAX_MOD_FILE_SIZE, ALLOWED_MOD_EXTENSIONS
from database.db_manager import DatabaseManager


class ModUploader(ctk.CTkScrollableFrame):
    """
    Mod uploader with drag-and-drop support.
    Fast, intuitive, effective.
    """
    
    def __init__(self, parent, db: DatabaseManager, current_user: Dict, environment: str):
        super().__init__(
            parent,
            fg_color=THEME["bg_primary"],
            corner_radius=0
        )
        
        self.db = db
        self.current_user = current_user
        self.environment = environment
        
        # Header
        header = ctk.CTkLabel(
            self,
            text="📦 Mod Management",
            font=THEME["font_header"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        header.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        # Upload section
        self.create_upload_section()
        
        # Mod list section
        self.create_mod_list_section()
        
        # Load existing mods
        self.load_mods()
    
    def create_upload_section(self):
        """Create upload section with drag-and-drop"""
        upload_label = ctk.CTkLabel(
            self,
            text="Upload New Mod",
            font=THEME["font_subheader"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        upload_label.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        # Upload card
        self.upload_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        self.upload_card.pack(fill="x", padx=LAYOUT["card_padding"], pady=10)
        
        # Drop zone
        self.drop_zone = ctk.CTkFrame(
            self.upload_card,
            fg_color=THEME["bg_primary"],
            corner_radius=LAYOUT["border_radius"],
            height=150,
            border_width=2,
            border_color=THEME["accent"]
        )
        self.drop_zone.pack(fill="x", padx=20, pady=20)
        
        # Drop zone label
        self.drop_label = ctk.CTkLabel(
            self.drop_zone,
            text="📦 Drop .jar file here or click to browse",
            font=THEME["font_body"],
            text_color=THEME["text_secondary"]
        )
        self.drop_label.pack(expand=True)
        
        # Make drop zone clickable
        self.drop_zone.bind("<Button-1>", lambda e: self.browse_file())
        self.drop_label.bind("<Button-1>", lambda e: self.browse_file())
        
        # Upload button (initially disabled)
        self.upload_button = ctk.CTkButton(
            self.upload_card,
            text="Upload Mod",
            font=THEME["font_body"],
            fg_color=THEME["accent"],
            hover_color=THEME["accent_hover"],
            height=40,
            state="disabled",
            command=self.upload_mod
        )
        self.upload_button.pack(pady=(0, 20), padx=20, fill="x")
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self.upload_card,
            fg_color=THEME["bg_primary"],
            progress_color=THEME["success"]
        )
        self.progress_bar.set(0)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.upload_card,
            text="",
            font=THEME["font_small"],
            text_color=THEME["text_secondary"]
        )
        
        # Selected file info
        self.selected_file = None
        self.file_info_label = ctk.CTkLabel(
            self.upload_card,
            text="",
            font=THEME["font_small"],
            text_color=THEME["text_secondary"]
        )
    
    def create_mod_list_section(self):
        """Create section showing uploaded mods"""
        list_label = ctk.CTkLabel(
            self,
            text="Uploaded Mods",
            font=THEME["font_subheader"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        list_label.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        # Mods list card
        self.mods_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        self.mods_card.pack(fill="both", expand=True, padx=LAYOUT["card_padding"], pady=10)
        
        # Mods list (scrollable frame)
        self.mods_list_frame = ctk.CTkScrollableFrame(
            self.mods_card,
            fg_color="transparent"
        )
        self.mods_list_frame.pack(fill="both", expand=True, padx=15, pady=15)
    
    def browse_file(self):
        """Open file browser to select mod"""
        file_path = filedialog.askopenfilename(
            title="Select Mod File",
            filetypes=[("JAR Files", "*.jar"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.select_file(Path(file_path))
    
    def select_file(self, file_path: Path):
        """Select a file for upload"""
        # Validate file
        if not file_path.exists():
            self.show_error("File does not exist")
            return
        
        if file_path.suffix not in ALLOWED_MOD_EXTENSIONS:
            self.show_error("Only .jar files are allowed")
            return
        
        file_size = file_path.stat().st_size
        if file_size > MAX_MOD_FILE_SIZE:
            self.show_error(f"File too large (max {MAX_MOD_FILE_SIZE // (1024*1024)}MB)")
            return
        
        # Store selected file
        self.selected_file = file_path
        
        # Update UI
        self.drop_label.configure(
            text=f"✓ {file_path.name}",
            text_color=THEME["success"]
        )
        
        # Show file info
        size_mb = file_size / (1024 * 1024)
        self.file_info_label.configure(
            text=f"Size: {size_mb:.2f} MB"
        )
        self.file_info_label.pack(pady=(0, 10), padx=20)
        
        # Enable upload button
        self.upload_button.configure(state="normal")
    
    def upload_mod(self):
        """Upload selected mod"""
        if not self.selected_file:
            return
        
        # Disable upload button
        self.upload_button.configure(state="disabled")
        
        # Show progress bar
        self.progress_bar.pack(pady=(0, 5), padx=20, fill="x")
        self.status_label.pack(pady=(0, 20), padx=20)
        
        # Upload in thread
        thread = threading.Thread(target=self._upload_thread, daemon=True)
        thread.start()
    
    def _upload_thread(self):
        """Upload thread (runs in background)"""
        try:
            self.update_status("Calculating checksum...", 0.1)
            
            # Calculate checksum
            checksum = self.calculate_checksum(self.selected_file)
            
            self.update_status("Parsing mod metadata...", 0.3)
            
            # Parse mod metadata
            metadata = self.parse_mod_metadata(self.selected_file)
            
            self.update_status("Copying file...", 0.5)
            
            # Copy to server-mods directory
            dest_path = SERVER_MODS_DIR / self.selected_file.name
            shutil.copy2(self.selected_file, dest_path)
            
            self.update_status("Saving to database...", 0.7)
            
            # Save to database
            mod_id = self.db.create_mod(
                name=metadata.get("name", self.selected_file.stem),
                version=metadata.get("version", "1.0.0"),
                file_name=self.selected_file.name,
                file_path=str(dest_path),
                file_size=self.selected_file.stat().st_size,
                checksum=checksum,
                mc_version=metadata.get("mc_version"),
                author_id=self.current_user["id"],
                environment=self.environment,
                description=metadata.get("description"),
                dependencies=metadata.get("dependencies", [])
            )
            
            # Log activity
            self.db.log_activity(
                self.current_user["id"],
                "upload_mod",
                {
                    "mod_id": mod_id,
                    "mod_name": metadata.get("name", self.selected_file.stem),
                    "environment": self.environment
                }
            )
            
            # Create deployment record
            self.db.create_deployment(
                mod_id=mod_id,
                environment=self.environment,
                user_id=self.current_user["id"],
                status="success",
                deployment_type="upload"
            )
            
            self.update_status("Upload complete!", 1.0)
            
            # Reset UI after success
            self.after(2000, self.reset_upload_ui)
            self.after(2100, self.load_mods)
            
        except Exception as e:
            self.update_status(f"Error: {str(e)}", 0)
            self.show_error(str(e))
    
    def calculate_checksum(self, file_path: Path) -> str:
        """Calculate SHA256 checksum"""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def parse_mod_metadata(self, file_path: Path) -> Dict:
        """Parse mod metadata from JAR file"""
        metadata = {
            "name": file_path.stem,
            "version": "1.0.0",
            "mc_version": None,
            "description": None,
            "dependencies": []
        }
        
        try:
            # Try to read mods.toml or mcmod.info from JAR
            with zipfile.ZipFile(file_path, 'r') as jar:
                # Try Forge 1.13+ (mods.toml)
                if 'META-INF/mods.toml' in jar.namelist():
                    # Simple TOML parsing (just extract key values)
                    content = jar.read('META-INF/mods.toml').decode('utf-8')
                    for line in content.split('\n'):
                        if 'modId' in line and '=' in line:
                            metadata["name"] = line.split('=')[1].strip().strip('"')
                        elif 'version' in line and '=' in line:
                            metadata["version"] = line.split('=')[1].strip().strip('"')
                        elif 'description' in line and '=' in line:
                            metadata["description"] = line.split('=')[1].strip().strip('"')
                
                # Try Forge 1.12 and older (mcmod.info)
                elif 'mcmod.info' in jar.namelist():
                    content = jar.read('mcmod.info').decode('utf-8')
                    info = json.loads(content)
                    if isinstance(info, list) and len(info) > 0:
                        mod_info = info[0]
                        metadata["name"] = mod_info.get("modid", file_path.stem)
                        metadata["version"] = mod_info.get("version", "1.0.0")
                        metadata["description"] = mod_info.get("description")
                        metadata["mc_version"] = mod_info.get("mcversion")
        except:
            # If parsing fails, use defaults
            pass
        
        return metadata
    
    def update_status(self, message: str, progress: float):
        """Update status and progress"""
        self.after(0, lambda: self.status_label.configure(text=message))
        self.after(0, lambda: self.progress_bar.set(progress))
    
    def show_error(self, message: str):
        """Show error message"""
        self.after(0, lambda: self.status_label.configure(
            text=f"❌ {message}",
            text_color=THEME["error"]
        ))
    
    def reset_upload_ui(self):
        """Reset upload UI to initial state"""
        self.selected_file = None
        self.drop_label.configure(
            text="📦 Drop .jar file here or click to browse",
            text_color=THEME["text_secondary"]
        )
        self.file_info_label.pack_forget()
        self.progress_bar.pack_forget()
        self.status_label.pack_forget()
        self.upload_button.configure(state="disabled")
    
    def load_mods(self):
        """Load and display uploaded mods"""
        # Clear current list
        for widget in self.mods_list_frame.winfo_children():
            widget.destroy()
        
        # Get mods from database
        mods = self.db.get_mods_by_environment(self.environment)
        
        if not mods:
            no_mods_label = ctk.CTkLabel(
                self.mods_list_frame,
                text="No mods uploaded yet",
                font=THEME["font_body"],
                text_color=THEME["text_secondary"]
            )
            no_mods_label.pack(pady=20)
            return
        
        # Display mods
        for mod in mods:
            self.create_mod_item(mod)
    
    def create_mod_item(self, mod: Dict):
        """Create mod list item"""
        item_frame = ctk.CTkFrame(
            self.mods_list_frame,
            fg_color=THEME["bg_primary"],
            corner_radius=8
        )
        item_frame.pack(fill="x", pady=5, padx=5)
        
        # Mod info
        info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)
        
        name_label = ctk.CTkLabel(
            info_frame,
            text=f"📦 {mod['name']} v{mod['version']}",
            font=("Segoe UI", 14, "bold"),
            text_color=THEME["text_primary"],
            anchor="w"
        )
        name_label.pack(anchor="w")
        
        # File info
        size_mb = mod['file_size'] / (1024 * 1024)
        details = f"{mod['file_name']} • {size_mb:.2f} MB"
        if mod.get('mc_version'):
            details += f" • MC {mod['mc_version']}"
        
        details_label = ctk.CTkLabel(
            info_frame,
            text=details,
            font=THEME["font_small"],
            text_color=THEME["text_secondary"],
            anchor="w"
        )
        details_label.pack(anchor="w")
        
        # Action buttons
        actions_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        actions_frame.pack(side="right", padx=10, pady=10)
        
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="🗑️",
            width=40,
            fg_color=THEME["error"],
            hover_color="#cc4444",
            command=lambda: self.delete_mod(mod['id'])
        )
        delete_btn.pack(side="right", padx=2)
    
    def delete_mod(self, mod_id: int):
        """Delete a mod"""
        # Get mod info
        mod = self.db.get_mod_by_id(mod_id)
        if not mod:
            return
        
        # Delete file
        try:
            file_path = Path(mod['file_path'])
            if file_path.exists():
                file_path.unlink()
        except:
            pass
        
        # Delete from database
        self.db.delete_mod(mod_id)
        
        # Log activity
        self.db.log_activity(
            self.current_user["id"],
            "delete_mod",
            {
                "mod_id": mod_id,
                "mod_name": mod['name']
            }
        )
        
        # Reload mods list
        self.load_mods()

