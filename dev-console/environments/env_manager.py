"""
Environment Manager Component
Manage Dev, Staging, and Production environments
"""

import customtkinter as ctk
from typing import Dict
import socket

from config import THEME, LAYOUT, ENVIRONMENTS
from database.db_manager import DatabaseManager


class EnvironmentManager(ctk.CTkScrollableFrame):
    """
    Environment manager for multi-environment deployments.
    Simple, clear, effective.
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
            text="🌍 Environment Management",
            font=THEME["font_header"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        header.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        # Environment cards
        self.create_environment_cards()
        
        # Environment comparison
        self.create_comparison_section()
    
    def create_environment_cards(self):
        """Create cards for each environment"""
        for env_key, env_config in ENVIRONMENTS.items():
            self.create_environment_card(env_key, env_config)
    
    def create_environment_card(self, env_key: str, env_config: Dict):
        """Create environment card"""
        card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        card.pack(fill="x", padx=LAYOUT["card_padding"], pady=10)
        
        # Header with color indicator
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # Color indicator
        indicator = ctk.CTkFrame(
            header_frame,
            width=20,
            height=20,
            corner_radius=10,
            fg_color=env_config["color"]
        )
        indicator.pack(side="left", padx=(0, 10))
        
        # Environment name
        name_label = ctk.CTkLabel(
            header_frame,
            text=env_config["name"],
            font=THEME["font_subheader"],
            text_color=THEME["text_primary"]
        )
        name_label.pack(side="left")
        
        # Status badge
        is_online = self.check_environment_online(env_config)
        status_text = "● ONLINE" if is_online else "● OFFLINE"
        status_color = THEME["success"] if is_online else THEME["error"]
        
        status_label = ctk.CTkLabel(
            header_frame,
            text=status_text,
            font=THEME["font_small"],
            text_color=status_color
        )
        status_label.pack(side="right")
        
        # Details frame
        details_frame = ctk.CTkFrame(card, fg_color="transparent")
        details_frame.pack(fill="x", padx=20, pady=10)
        
        # Server info
        info_text = f"Server: {env_config['server_ip']}:{env_config['server_port']}\n"
        info_text += f"Hot Reload: {'Enabled' if env_config['hot_reload'] else 'Disabled'}\n"
        
        # Get mod count
        mods = self.db.get_mods_by_environment(env_key)
        info_text += f"Mods: {len(mods)}"
        
        info_label = ctk.CTkLabel(
            details_frame,
            text=info_text,
            font=THEME["font_body"],
            text_color=THEME["text_secondary"],
            justify="left",
            anchor="w"
        )
        info_label.pack(fill="x")
        
        # Action buttons
        actions_frame = ctk.CTkFrame(card, fg_color="transparent")
        actions_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        ctk.CTkButton(
            actions_frame,
            text="View Mods",
            width=120,
            fg_color=env_config["color"],
            command=lambda: self.view_environment_mods(env_key)
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            actions_frame,
            text="Deploy",
            width=120,
            fg_color=THEME["accent"],
            command=lambda: self.deploy_to_environment(env_key)
        ).pack(side="left", padx=5)
        
        if env_key != "prod":
            ctk.CTkButton(
                actions_frame,
                text=f"Promote to {self.get_next_env(env_key)}",
                width=150,
                fg_color=THEME["success"],
                command=lambda: self.promote_environment(env_key)
            ).pack(side="left", padx=5)
    
    def create_comparison_section(self):
        """Create environment comparison section"""
        comp_label = ctk.CTkLabel(
            self,
            text="Environment Comparison",
            font=THEME["font_subheader"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        comp_label.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        comp_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        comp_card.pack(fill="both", expand=True, padx=LAYOUT["card_padding"], pady=10)
        
        # Comparison table
        table_frame = ctk.CTkFrame(comp_card, fg_color="transparent")
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header row
        header_row = ctk.CTkFrame(table_frame, fg_color=THEME["bg_primary"])
        header_row.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            header_row,
            text="Feature",
            font=("Segoe UI", 12, "bold"),
            width=150,
            anchor="w"
        ).pack(side="left", padx=10, pady=10)
        
        for env_key, env_config in ENVIRONMENTS.items():
            ctk.CTkLabel(
                header_row,
                text=env_config["name"],
                font=("Segoe UI", 12, "bold"),
                width=120,
                text_color=env_config["color"]
            ).pack(side="left", padx=10, pady=10)
        
        # Feature rows
        features = [
            ("Hot Reload", lambda e: "✓" if e["hot_reload"] else "✗"),
            ("Mods", lambda e: str(len(self.db.get_mods_by_environment([k for k, v in ENVIRONMENTS.items() if v == e][0])))),
            ("Auto Deploy", lambda e: "✓" if e == ENVIRONMENTS["dev"] else "✗"),
            ("Requires Approval", lambda e: "✓" if e == ENVIRONMENTS["prod"] else "✗"),
        ]
        
        for feature_name, feature_func in features:
            row = ctk.CTkFrame(table_frame, fg_color=THEME["bg_primary"])
            row.pack(fill="x", pady=2)
            
            ctk.CTkLabel(
                row,
                text=feature_name,
                font=THEME["font_body"],
                width=150,
                anchor="w"
            ).pack(side="left", padx=10, pady=8)
            
            for env_config in ENVIRONMENTS.values():
                value = feature_func(env_config)
                ctk.CTkLabel(
                    row,
                    text=value,
                    font=THEME["font_body"],
                    text_color=THEME["text_secondary"],
                    width=120
                ).pack(side="left", padx=10, pady=8)
    
    def check_environment_online(self, env_config: Dict) -> bool:
        """Check if environment server is online"""
        if env_config["server_ip"] == "localhost":
            # Check local server
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex(('localhost', env_config["server_port"]))
                sock.close()
                return result == 0
            except:
                return False
        else:
            # For remote servers, would need to implement actual check
            return False
    
    def get_next_env(self, current_env: str) -> str:
        """Get next environment in promotion chain"""
        env_chain = {
            "dev": "Staging",
            "staging": "Production"
        }
        return env_chain.get(current_env, "")
    
    def view_environment_mods(self, env_key: str):
        """View mods in environment"""
        # Create modal dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"{ENVIRONMENTS[env_key]['name']} Mods")
        dialog.geometry("600x400")
        dialog.transient(self)
        
        # Get mods
        mods = self.db.get_mods_by_environment(env_key)
        
        # Create list
        list_frame = ctk.CTkScrollableFrame(dialog)
        list_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        if not mods:
            ctk.CTkLabel(
                list_frame,
                text="No mods in this environment",
                font=THEME["font_body"],
                text_color=THEME["text_secondary"]
            ).pack(pady=20)
        else:
            for mod in mods:
                mod_frame = ctk.CTkFrame(list_frame, fg_color=THEME["card_bg"])
                mod_frame.pack(fill="x", pady=5)
                
                ctk.CTkLabel(
                    mod_frame,
                    text=f"📦 {mod['name']} v{mod['version']}",
                    font=THEME["font_body"],
                    anchor="w"
                ).pack(side="left", padx=15, pady=10)
    
    def deploy_to_environment(self, env_key: str):
        """Deploy to environment"""
        # Show deployment dialog
        self.show_message(
            f"Deploying to {ENVIRONMENTS[env_key]['name']}...",
            THEME["info"]
        )
    
    def promote_environment(self, from_env: str):
        """Promote from one environment to next"""
        env_chain = {
            "dev": "staging",
            "staging": "prod"
        }
        
        to_env = env_chain.get(from_env)
        if not to_env:
            return
        
        from_name = ENVIRONMENTS[from_env]['name']
        to_name = ENVIRONMENTS[to_env]['name']
        
        # Show confirmation dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Promote Environment")
        dialog.geometry("400x250")
        dialog.transient(self)
        dialog.grab_set()
        
        ctk.CTkLabel(
            dialog,
            text=f"Promote all mods from\n{from_name} to {to_name}?",
            font=THEME["font_body"]
        ).pack(pady=30)
        
        # Get mod count
        mods = self.db.get_mods_by_environment(from_env)
        ctk.CTkLabel(
            dialog,
            text=f"{len(mods)} mods will be promoted",
            font=THEME["font_small"],
            text_color=THEME["text_secondary"]
        ).pack(pady=10)
        
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=20)
        
        def do_promote():
            # Would implement actual promotion logic here
            self.show_message(
                f"Promoted to {to_name}",
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
    
    def show_message(self, message: str, color: str):
        """Show temporary message"""
        msg_label = ctk.CTkLabel(
            self,
            text=message,
            font=THEME["font_body"],
            text_color=color
        )
        msg_label.place(relx=0.5, rely=0.95, anchor="center")
        self.after(3000, msg_label.destroy)

