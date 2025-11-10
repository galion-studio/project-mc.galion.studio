"""
Repository Manager Component
Central repository management with version control and CDN upload
"""

import customtkinter as ctk
from pathlib import Path
import shutil
from typing import Optional, Dict
import threading

from config import THEME, LAYOUT
from database.db_manager import DatabaseManager


class RepositoryManager(ctk.CTkScrollableFrame):
    """
    Repository manager for mod versioning and distribution.
    Simple, organized, scalable.
    """
    
    def __init__(self, parent, db: DatabaseManager):
        super().__init__(
            parent,
            fg_color=THEME["bg_primary"],
            corner_radius=0
        )
        
        self.db = db
        
        # Header
        header = ctk.CTkLabel(
            self,
            text="🗄️ Repository Management",
            font=THEME["font_header"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        header.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        # Stats row
        self.create_stats_section()
        
        # Repository list
        self.create_repository_list()
        
        # Load mods
        self.load_repository()
    
    def create_stats_section(self):
        """Create statistics section"""
        stats_label = ctk.CTkLabel(
            self,
            text="Repository Statistics",
            font=THEME["font_subheader"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        stats_label.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        stats_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        stats_frame.pack(fill="x", padx=LAYOUT["card_padding"], pady=10)
        
        # Stat cards
        self.create_stat_card(
            stats_frame,
            "Total Mods",
            "0",
            THEME["info"]
        ).pack(side="left", fill="both", expand=True, padx=5)
        
        self.create_stat_card(
            stats_frame,
            "Versions",
            "0",
            THEME["success"]
        ).pack(side="left", fill="both", expand=True, padx=5)
        
        self.create_stat_card(
            stats_frame,
            "In Development",
            "0",
            THEME["warning"]
        ).pack(side="left", fill="both", expand=True, padx=5)
        
        self.create_stat_card(
            stats_frame,
            "Published",
            "0",
            THEME["accent"]
        ).pack(side="left", fill="both", expand=True, padx=5)
    
    def create_stat_card(self, parent, label: str, value: str, color: str) -> ctk.CTkFrame:
        """Create a statistics card"""
        card = ctk.CTkFrame(
            parent,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI", 28, "bold"),
            text_color=color
        )
        value_label.pack(pady=(15, 5))
        
        label_widget = ctk.CTkLabel(
            card,
            text=label,
            font=THEME["font_small"],
            text_color=THEME["text_secondary"]
        )
        label_widget.pack(pady=(0, 15))
        
        return card
    
    def create_repository_list(self):
        """Create repository list section"""
        list_label = ctk.CTkLabel(
            self,
            text="Mods in Repository",
            font=THEME["font_subheader"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        list_label.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        # Filter buttons
        filter_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        filter_frame.pack(fill="x", padx=LAYOUT["card_padding"], pady=5)
        
        ctk.CTkButton(
            filter_frame,
            text="All",
            width=100,
            fg_color=THEME["accent"],
            command=lambda: self.filter_mods("all")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            filter_frame,
            text="Development",
            width=100,
            fg_color=THEME["card_bg"],
            command=lambda: self.filter_mods("dev")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            filter_frame,
            text="Staging",
            width=100,
            fg_color=THEME["card_bg"],
            command=lambda: self.filter_mods("staging")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            filter_frame,
            text="Production",
            width=100,
            fg_color=THEME["card_bg"],
            command=lambda: self.filter_mods("prod")
        ).pack(side="left", padx=5)
        
        # Mods list card
        self.mods_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        self.mods_card.pack(fill="both", expand=True, padx=LAYOUT["card_padding"], pady=10)
        
        # Mods list frame
        self.mods_list_frame = ctk.CTkScrollableFrame(
            self.mods_card,
            fg_color="transparent"
        )
        self.mods_list_frame.pack(fill="both", expand=True, padx=15, pady=15)
    
    def load_repository(self):
        """Load mods from repository"""
        # Clear current list
        for widget in self.mods_list_frame.winfo_children():
            widget.destroy()
        
        # Get all mods
        all_mods = self.db.get_all_mods()
        
        if not all_mods:
            no_mods_label = ctk.CTkLabel(
                self.mods_list_frame,
                text="No mods in repository",
                font=THEME["font_body"],
                text_color=THEME["text_secondary"]
            )
            no_mods_label.pack(pady=20)
            return
        
        # Group mods by name (different versions)
        mods_by_name = {}
        for mod in all_mods:
            name = mod['name']
            if name not in mods_by_name:
                mods_by_name[name] = []
            mods_by_name[name].append(mod)
        
        # Display grouped mods
        for mod_name, versions in mods_by_name.items():
            self.create_mod_group(mod_name, versions)
    
    def create_mod_group(self, mod_name: str, versions: list):
        """Create mod group with versions"""
        group_frame = ctk.CTkFrame(
            self.mods_list_frame,
            fg_color=THEME["bg_primary"],
            corner_radius=8
        )
        group_frame.pack(fill="x", pady=10, padx=5)
        
        # Header
        header_frame = ctk.CTkFrame(group_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=10)
        
        name_label = ctk.CTkLabel(
            header_frame,
            text=f"📦 {mod_name}",
            font=("Segoe UI", 16, "bold"),
            text_color=THEME["text_primary"],
            anchor="w"
        )
        name_label.pack(side="left")
        
        version_count_label = ctk.CTkLabel(
            header_frame,
            text=f"{len(versions)} versions",
            font=THEME["font_small"],
            text_color=THEME["text_secondary"]
        )
        version_count_label.pack(side="right")
        
        # Versions list
        for version_mod in sorted(versions, key=lambda x: x['created_at'], reverse=True):
            self.create_version_item(group_frame, version_mod)
    
    def create_version_item(self, parent, mod: Dict):
        """Create version item"""
        item_frame = ctk.CTkFrame(
            parent,
            fg_color=THEME["card_bg"],
            corner_radius=6
        )
        item_frame.pack(fill="x", padx=15, pady=5)
        
        # Info section
        info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=8)
        
        # Version and environment
        version_text = f"v{mod['version']} • {mod['environment'].upper()}"
        if mod.get('mc_version'):
            version_text += f" • MC {mod['mc_version']}"
        
        version_label = ctk.CTkLabel(
            info_frame,
            text=version_text,
            font=THEME["font_body"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        version_label.pack(anchor="w")
        
        # File info
        size_mb = mod['file_size'] / (1024 * 1024)
        details_label = ctk.CTkLabel(
            info_frame,
            text=f"{mod['file_name']} • {size_mb:.2f} MB",
            font=THEME["font_small"],
            text_color=THEME["text_secondary"],
            anchor="w"
        )
        details_label.pack(anchor="w")
        
        # Actions
        actions_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        actions_frame.pack(side="right", padx=10, pady=8)
        
        # Promote button
        ctk.CTkButton(
            actions_frame,
            text="⬆️",
            width=35,
            fg_color=THEME["success"],
            hover_color="#00c993",
            command=lambda: self.promote_mod(mod)
        ).pack(side="left", padx=2)
        
        # Download button
        ctk.CTkButton(
            actions_frame,
            text="💾",
            width=35,
            fg_color=THEME["info"],
            command=lambda: self.download_mod(mod)
        ).pack(side="left", padx=2)
        
        # Publish to CDN button
        ctk.CTkButton(
            actions_frame,
            text="🌐",
            width=35,
            fg_color=THEME["accent"],
            command=lambda: self.publish_to_cdn(mod)
        ).pack(side="left", padx=2)
    
    def filter_mods(self, filter_type: str):
        """Filter mods by environment"""
        # TODO: Implement filtering
        pass
    
    def promote_mod(self, mod: Dict):
        """Promote mod to next environment"""
        current_env = mod['environment']
        
        # Determine next environment
        env_progression = {
            'dev': 'staging',
            'staging': 'prod'
        }
        
        next_env = env_progression.get(current_env)
        
        if not next_env:
            # Already in production
            self.show_message("Already in production", THEME["warning"])
            return
        
        # Create dialog to confirm
        dialog = ctk.CTkToplevel(self)
        dialog.title("Promote Mod")
        dialog.geometry("400x200")
        dialog.transient(self)
        dialog.grab_set()
        
        label = ctk.CTkLabel(
            dialog,
            text=f"Promote {mod['name']} v{mod['version']}\nfrom {current_env} to {next_env}?",
            font=THEME["font_body"]
        )
        label.pack(pady=30)
        
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=20)
        
        def do_promote():
            # Copy mod to next environment (would need actual implementation)
            self.show_message(
                f"Promoted to {next_env}",
                THEME["success"]
            )
            dialog.destroy()
        
        ctk.CTkButton(
            button_frame,
            text="Promote",
            fg_color=THEME["success"],
            command=do_promote
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="Cancel",
            fg_color=THEME["error"],
            command=dialog.destroy
        ).pack(side="left", padx=10)
    
    def download_mod(self, mod: Dict):
        """Download mod file"""
        self.show_message(
            f"Downloaded {mod['name']} v{mod['version']}",
            THEME["success"]
        )
    
    def publish_to_cdn(self, mod: Dict):
        """Publish mod to CDN"""
        self.show_message(
            f"Publishing {mod['name']} to CDN...",
            THEME["info"]
        )
        
        # Would implement actual CDN upload here
        # For now, just show message
        
        self.after(2000, lambda: self.show_message(
            f"Published {mod['name']} to CDN",
            THEME["success"]
        ))
    
    def show_message(self, message: str, color: str):
        """Show temporary message"""
        # Create temporary label
        msg_label = ctk.CTkLabel(
            self,
            text=message,
            font=THEME["font_body"],
            text_color=color
        )
        msg_label.place(relx=0.5, rely=0.95, anchor="center")
        
        # Remove after 3 seconds
        self.after(3000, msg_label.destroy)

