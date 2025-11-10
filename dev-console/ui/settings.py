"""
Admin Settings Panel
Console configuration and PIN management
"""

import customtkinter as ctk
from config import THEME, LAYOUT
from database.db_manager import DatabaseManager
from auth.pin_manager import get_pin_manager


class AdminSettings(ctk.CTkScrollableFrame):
    """Admin settings and configuration"""
    
    def __init__(self, parent, db: DatabaseManager):
        super().__init__(
            parent,
            fg_color=THEME["bg_primary"],
            corner_radius=0
        )
        
        self.db = db
        self.pin_manager = get_pin_manager()
        
        # Header
        header = ctk.CTkLabel(
            self,
            text="⚙️ Settings",
            font=THEME["font_header"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        header.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        # Security section
        self.create_security_section()
        
        # Console section
        self.create_console_section()
    
    def create_security_section(self):
        """Create security settings"""
        section_label = ctk.CTkLabel(
            self,
            text="Security",
            font=THEME["font_subheader"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        section_label.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        # PIN change card
        pin_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        pin_card.pack(fill="x", padx=LAYOUT["card_padding"], pady=10)
        
        # Current PIN info
        info_frame = ctk.CTkFrame(pin_card, fg_color="transparent")
        info_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            info_frame,
            text="Console PIN",
            font=("Segoe UI", 14, "bold"),
            text_color=THEME["text_primary"]
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            info_frame,
            text="Protect console access with a 4-digit PIN",
            font=THEME["font_small"],
            text_color=THEME["text_secondary"]
        ).pack(anchor="w", pady=(5, 0))
        
        # PIN change form
        form_frame = ctk.CTkFrame(pin_card, fg_color="transparent")
        form_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        # Current PIN
        ctk.CTkLabel(
            form_frame,
            text="Current PIN:",
            font=THEME["font_body"],
            text_color=THEME["text_secondary"]
        ).pack(anchor="w", pady=(10, 5))
        
        self.current_pin_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Enter current PIN",
            show="●",
            height=40
        )
        self.current_pin_entry.pack(fill="x", pady=(0, 10))
        
        # New PIN
        ctk.CTkLabel(
            form_frame,
            text="New PIN:",
            font=THEME["font_body"],
            text_color=THEME["text_secondary"]
        ).pack(anchor="w", pady=(10, 5))
        
        self.new_pin_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Enter new 4-digit PIN",
            show="●",
            height=40
        )
        self.new_pin_entry.pack(fill="x", pady=(0, 10))
        
        # Confirm PIN
        ctk.CTkLabel(
            form_frame,
            text="Confirm PIN:",
            font=THEME["font_body"],
            text_color=THEME["text_secondary"]
        ).pack(anchor="w", pady=(10, 5))
        
        self.confirm_pin_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Confirm new PIN",
            show="●",
            height=40
        )
        self.confirm_pin_entry.pack(fill="x", pady=(0, 15))
        
        # Change button
        change_btn = ctk.CTkButton(
            form_frame,
            text="Change PIN",
            font=THEME["font_body"],
            height=45,
            fg_color=THEME["accent"],
            hover_color=THEME["accent_hover"],
            command=self.change_pin
        )
        change_btn.pack(fill="x")
        
        # Status label
        self.pin_status = ctk.CTkLabel(
            form_frame,
            text="",
            font=THEME["font_small"]
        )
        self.pin_status.pack(pady=(10, 0))
    
    def create_console_section(self):
        """Create console settings"""
        section_label = ctk.CTkLabel(
            self,
            text="Console Configuration",
            font=THEME["font_subheader"],
            text_color=THEME["text_primary"],
            anchor="w"
        )
        section_label.pack(fill="x", padx=LAYOUT["card_padding"], pady=(20, 10))
        
        # Console info card
        info_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=LAYOUT["border_radius"]
        )
        info_card.pack(fill="x", padx=LAYOUT["card_padding"], pady=10)
        
        info_text = (
            "Console Version: 2.0\n"
            "Database: Connected\n"
            "AI Integration: Grok 4 Fast\n"
            "Server Control: RCON\n"
            "Hot Reload: Enabled\n"
        )
        
        ctk.CTkLabel(
            info_card,
            text=info_text,
            font=THEME["font_code"],
            text_color=THEME["text_secondary"],
            justify="left",
            anchor="w"
        ).pack(padx=20, pady=20, anchor="w")
    
    def change_pin(self):
        """Change PIN"""
        current = self.current_pin_entry.get().strip()
        new_pin = self.new_pin_entry.get().strip()
        confirm = self.confirm_pin_entry.get().strip()
        
        # Validate
        if not current or not new_pin or not confirm:
            self.show_pin_status("All fields required", "error")
            return
        
        if len(new_pin) != 4 or not new_pin.isdigit():
            self.show_pin_status("PIN must be 4 digits", "error")
            return
        
        if new_pin != confirm:
            self.show_pin_status("PINs don't match", "error")
            return
        
        # Verify current PIN
        if not self.pin_manager.verify_pin(current):
            self.show_pin_status("Current PIN incorrect", "error")
            return
        
        # Set new PIN
        self.pin_manager.set_pin(new_pin)
        
        # Log activity
        self.db.log_activity(1, "change_pin", {"success": True})
        
        # Clear fields
        self.current_pin_entry.delete(0, "end")
        self.new_pin_entry.delete(0, "end")
        self.confirm_pin_entry.delete(0, "end")
        
        self.show_pin_status("✓ PIN changed successfully", "success")
    
    def show_pin_status(self, message: str, status: str):
        """Show PIN change status"""
        color = THEME["success"] if status == "success" else THEME["error"]
        self.pin_status.configure(
            text=message,
            text_color=color
        )
