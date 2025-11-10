"""
Login Screen
PIN-based authentication for console access
"""

import customtkinter as ctk
from config import THEME
from auth.pin_manager import get_pin_manager
from typing import Callable


class LoginScreen(ctk.CTkFrame):
    """
    PIN login screen.
    Beautiful, secure, simple.
    """
    
    def __init__(self, parent, on_success: Callable):
        super().__init__(
            parent,
            fg_color=THEME["bg_primary"]
        )
        
        self.on_success = on_success
        self.pin_manager = get_pin_manager()
        self.pin_entry_value = ""
        
        # Pack to fill parent
        self.pack(fill="both", expand=True)
        
        # Create login UI
        self.create_ui()
        
        # Check if locked
        if self.pin_manager.is_locked():
            self.show_locked_message()
    
    def create_ui(self):
        """Create login screen UI"""
        # Center container
        center_frame = ctk.CTkFrame(self, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo
        logo_label = ctk.CTkLabel(
            center_frame,
            text="⚡",
            font=("Segoe UI", 80),
            text_color=THEME["accent"]
        )
        logo_label.pack(pady=(0, 10))
        
        # Title
        title = ctk.CTkLabel(
            center_frame,
            text="GALION Developer Console",
            font=("Segoe UI", 28, "bold"),
            text_color=THEME["text_primary"]
        )
        title.pack(pady=(0, 5))
        
        # Subtitle
        subtitle = ctk.CTkLabel(
            center_frame,
            text="Enter your PIN to continue",
            font=("Segoe UI", 14),
            text_color=THEME["text_secondary"]
        )
        subtitle.pack(pady=(0, 40))
        
        # PIN display
        pin_display_frame = ctk.CTkFrame(
            center_frame,
            fg_color="transparent"
        )
        pin_display_frame.pack(pady=(0, 30))
        
        # 4 PIN dots
        self.pin_dots = []
        for i in range(4):
            dot_frame = ctk.CTkFrame(
                pin_display_frame,
                fg_color=THEME["card_bg"],
                width=60,
                height=60,
                corner_radius=30
            )
            dot_frame.pack(side="left", padx=10)
            dot_frame.pack_propagate(False)
            
            dot = ctk.CTkLabel(
                dot_frame,
                text="",
                font=("Segoe UI", 28),
                text_color=THEME["text_primary"]
            )
            dot.place(relx=0.5, rely=0.5, anchor="center")
            
            self.pin_dots.append((dot_frame, dot))
        
        # Number pad
        numpad_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        numpad_frame.pack(pady=(0, 20))
        
        # Number buttons (1-9)
        for i in range(1, 10):
            row = (i - 1) // 3
            col = (i - 1) % 3
            
            btn = ctk.CTkButton(
                numpad_frame,
                text=str(i),
                font=("Segoe UI", 24, "bold"),
                width=80,
                height=80,
                corner_radius=15,
                fg_color=THEME["card_bg"],
                hover_color=THEME["accent"],
                command=lambda n=i: self.add_digit(str(n))
            )
            btn.grid(row=row, column=col, padx=8, pady=8)
        
        # Bottom row: Clear, 0, Enter
        clear_btn = ctk.CTkButton(
            numpad_frame,
            text="⌫",
            font=("Segoe UI", 24),
            width=80,
            height=80,
            corner_radius=15,
            fg_color=THEME["card_bg"],
            hover_color=THEME["error"],
            command=self.clear_digit
        )
        clear_btn.grid(row=3, column=0, padx=8, pady=8)
        
        zero_btn = ctk.CTkButton(
            numpad_frame,
            text="0",
            font=("Segoe UI", 24, "bold"),
            width=80,
            height=80,
            corner_radius=15,
            fg_color=THEME["card_bg"],
            hover_color=THEME["accent"],
            command=lambda: self.add_digit("0")
        )
        zero_btn.grid(row=3, column=1, padx=8, pady=8)
        
        enter_btn = ctk.CTkButton(
            numpad_frame,
            text="✓",
            font=("Segoe UI", 24),
            width=80,
            height=80,
            corner_radius=15,
            fg_color=THEME["success"],
            hover_color="#00c993",
            command=self.verify_pin
        )
        enter_btn.grid(row=3, column=2, padx=8, pady=8)
        
        # Status message
        self.status_label = ctk.CTkLabel(
            center_frame,
            text="",
            font=("Segoe UI", 12),
            text_color=THEME["error"]
        )
        self.status_label.pack(pady=(20, 0))
        
        # Default PIN hint
        hint = ctk.CTkLabel(
            center_frame,
            text="Default PIN: 2424",
            font=("Segoe UI", 11),
            text_color=THEME["text_dim"]
        )
        hint.pack(pady=(10, 0))
        
        # Bind keyboard
        self.master.bind("<Key>", self.on_key_press)
    
    def add_digit(self, digit: str):
        """Add digit to PIN entry"""
        if len(self.pin_entry_value) < 4:
            self.pin_entry_value += digit
            self.update_pin_display()
            
            # Auto-verify when 4 digits entered
            if len(self.pin_entry_value) == 4:
                self.after(200, self.verify_pin)
    
    def clear_digit(self):
        """Remove last digit"""
        if self.pin_entry_value:
            self.pin_entry_value = self.pin_entry_value[:-1]
            self.update_pin_display()
    
    def update_pin_display(self):
        """Update PIN dots display"""
        for i, (frame, dot) in enumerate(self.pin_dots):
            if i < len(self.pin_entry_value):
                # Filled dot
                frame.configure(fg_color=THEME["accent"])
                dot.configure(text="●")
            else:
                # Empty dot
                frame.configure(fg_color=THEME["card_bg"])
                dot.configure(text="")
    
    def verify_pin(self):
        """Verify entered PIN"""
        if len(self.pin_entry_value) != 4:
            self.show_error("Enter 4-digit PIN")
            return
        
        # Check if locked
        if self.pin_manager.is_locked():
            self.show_locked_message()
            return
        
        # Verify PIN
        if self.pin_manager.verify_pin(self.pin_entry_value):
            # Success!
            self.show_success()
        else:
            # Failed
            attempts = self.pin_manager.get_attempts()
            remaining = 5 - attempts
            
            if remaining > 0:
                self.show_error(f"Incorrect PIN. {remaining} attempts remaining")
            else:
                self.show_locked_message()
            
            # Shake animation
            self.shake_pin_display()
            
            # Clear entry
            self.pin_entry_value = ""
            self.update_pin_display()
    
    def show_success(self):
        """Show success and proceed"""
        self.status_label.configure(
            text="✓ Access granted",
            text_color=THEME["success"]
        )
        
        # Animate success
        for frame, dot in self.pin_dots:
            frame.configure(fg_color=THEME["success"])
        
        # Proceed to main UI
        self.after(500, self.proceed_to_main)
    
    def proceed_to_main(self):
        """Proceed to main console"""
        # Unbind keyboard
        self.master.unbind("<Key>")
        
        # Destroy login screen
        self.destroy()
        
        # Call success callback
        self.on_success()
    
    def show_error(self, message: str):
        """Show error message"""
        self.status_label.configure(
            text=message,
            text_color=THEME["error"]
        )
    
    def show_locked_message(self):
        """Show locked message"""
        self.status_label.configure(
            text="❌ Console locked. Contact administrator.",
            text_color=THEME["error"]
        )
        
        for frame, dot in self.pin_dots:
            frame.configure(fg_color=THEME["error"])
    
    def shake_pin_display(self):
        """Animate shake effect on wrong PIN"""
        # Simple shake animation
        original_x = 0.5
        offsets = [0.48, 0.52, 0.48, 0.52, 0.5]
        
        def animate_shake(index=0):
            if index < len(offsets):
                for frame, dot in self.pin_dots:
                    frame.master.place(relx=offsets[index], rely=0.5, anchor="center")
                self.after(50, lambda: animate_shake(index + 1))
        
        # Start animation
        # animate_shake()  # Disabled for simplicity, can enable if desired
    
    def on_key_press(self, event):
        """Handle keyboard input"""
        key = event.char
        
        # Number keys
        if key.isdigit():
            self.add_digit(key)
        
        # Backspace
        elif event.keysym == "BackSpace":
            self.clear_digit()
        
        # Enter
        elif event.keysym == "Return":
            self.verify_pin()
