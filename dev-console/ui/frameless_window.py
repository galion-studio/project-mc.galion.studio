"""
Custom Frameless Window with Built-in Controls
Modern, sleek window with ESC to close, minimize, maximize, and resize
"""

import customtkinter as ctk
from config import THEME


class FramelessWindow(ctk.CTk):
    """
    Custom frameless window with modern title bar.
    Features:
    - Custom title bar with controls
    - ESC key to close
    - Minimize, maximize, close buttons
    - Window dragging
    - Resize functionality
    """
    
    def __init__(self, title="GALION Developer Console", **kwargs):
        super().__init__(**kwargs)
        
        # Remove default title bar
        self.overrideredirect(True)
        
        # Window title
        self.window_title = title
        
        # Drag variables
        self._drag_data = {"x": 0, "y": 0}
        self._is_maximized = False
        self._normal_geometry = None
        
        # Configure window
        self.geometry("1400x900")
        self.minsize(800, 600)
        self.configure(fg_color=THEME["bg_primary"])
        
        # Create custom title bar
        self.create_title_bar()
        
        # Bind ESC key to close
        self.bind("<Escape>", lambda e: self.quit_window())
        
        # Enable window resize (add resize grips)
        self.create_resize_grips()
    
    def create_title_bar(self):
        """Create custom title bar with controls"""
        # Title bar frame
        self.title_bar = ctk.CTkFrame(
            self,
            height=40,
            fg_color=THEME["bg_secondary"],
            corner_radius=0
        )
        self.title_bar.pack(side="top", fill="x")
        self.title_bar.pack_propagate(False)
        
        # Make title bar draggable
        self.title_bar.bind("<Button-1>", self.start_drag)
        self.title_bar.bind("<B1-Motion>", self.on_drag)
        self.title_bar.bind("<Double-Button-1>", self.toggle_maximize)
        
        # Icon and title (left side)
        title_frame = ctk.CTkFrame(self.title_bar, fg_color="transparent")
        title_frame.pack(side="left", fill="both", expand=True)
        title_frame.bind("<Button-1>", self.start_drag)
        title_frame.bind("<B1-Motion>", self.on_drag)
        title_frame.bind("<Double-Button-1>", self.toggle_maximize)
        
        # Icon
        icon_label = ctk.CTkLabel(
            title_frame,
            text="⚡",
            font=("Segoe UI", 16),
            text_color=THEME["accent"]
        )
        icon_label.pack(side="left", padx=(15, 5))
        icon_label.bind("<Button-1>", self.start_drag)
        icon_label.bind("<B1-Motion>", self.on_drag)
        
        # Title text
        title_label = ctk.CTkLabel(
            title_frame,
            text=self.window_title,
            font=("Segoe UI", 12, "bold"),
            text_color=THEME["text_primary"]
        )
        title_label.pack(side="left", padx=5)
        title_label.bind("<Button-1>", self.start_drag)
        title_label.bind("<B1-Motion>", self.on_drag)
        title_label.bind("<Double-Button-1>", self.toggle_maximize)
        
        # Control buttons (right side)
        controls_frame = ctk.CTkFrame(self.title_bar, fg_color="transparent")
        controls_frame.pack(side="right", padx=5)
        
        # Minimize button
        self.minimize_btn = ctk.CTkButton(
            controls_frame,
            text="─",
            width=40,
            height=30,
            fg_color="transparent",
            hover_color=THEME["card_hover"],
            text_color=THEME["text_primary"],
            font=("Segoe UI", 16),
            corner_radius=0,
            command=self.minimize_window
        )
        self.minimize_btn.pack(side="left", padx=2)
        
        # Maximize/Restore button
        self.maximize_btn = ctk.CTkButton(
            controls_frame,
            text="□",
            width=40,
            height=30,
            fg_color="transparent",
            hover_color=THEME["card_hover"],
            text_color=THEME["text_primary"],
            font=("Segoe UI", 16),
            corner_radius=0,
            command=self.toggle_maximize
        )
        self.maximize_btn.pack(side="left", padx=2)
        
        # Close button
        self.close_btn = ctk.CTkButton(
            controls_frame,
            text="✕",
            width=40,
            height=30,
            fg_color="transparent",
            hover_color=THEME["error"],
            text_color=THEME["text_primary"],
            font=("Segoe UI", 16),
            corner_radius=0,
            command=self.quit_window
        )
        self.close_btn.pack(side="left", padx=2)
    
    def create_resize_grips(self):
        """Create invisible resize grips at window edges"""
        # Bottom-right corner resize grip (most common)
        resize_grip = ctk.CTkFrame(
            self,
            width=20,
            height=20,
            fg_color="transparent"
        )
        resize_grip.place(relx=1.0, rely=1.0, anchor="se")
        
        # Bind resize events
        resize_grip.bind("<Button-1>", self.start_resize)
        resize_grip.bind("<B1-Motion>", self.on_resize)
    
    def start_drag(self, event):
        """Start window drag"""
        self._drag_data["x"] = event.x_root - self.winfo_x()
        self._drag_data["y"] = event.y_root - self.winfo_y()
    
    def on_drag(self, event):
        """Handle window drag"""
        if not self._is_maximized:
            x = event.x_root - self._drag_data["x"]
            y = event.y_root - self._drag_data["y"]
            self.geometry(f"+{x}+{y}")
    
    def start_resize(self, event):
        """Start window resize"""
        self._drag_data["width"] = self.winfo_width()
        self._drag_data["height"] = self.winfo_height()
        self._drag_data["x"] = event.x_root
        self._drag_data["y"] = event.y_root
    
    def on_resize(self, event):
        """Handle window resize"""
        if not self._is_maximized:
            delta_x = event.x_root - self._drag_data["x"]
            delta_y = event.y_root - self._drag_data["y"]
            
            new_width = max(800, self._drag_data["width"] + delta_x)
            new_height = max(600, self._drag_data["height"] + delta_y)
            
            self.geometry(f"{new_width}x{new_height}")
    
    def minimize_window(self):
        """Minimize window"""
        self.iconify()
    
    def toggle_maximize(self, event=None):
        """Toggle maximize/restore window"""
        if self._is_maximized:
            # Restore to normal
            if self._normal_geometry:
                self.geometry(self._normal_geometry)
            self._is_maximized = False
            self.maximize_btn.configure(text="□")
        else:
            # Save current geometry
            self._normal_geometry = self.geometry()
            
            # Maximize to screen size
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            self.geometry(f"{screen_width}x{screen_height}+0+0")
            self._is_maximized = True
            self.maximize_btn.configure(text="❐")
    
    def quit_window(self):
        """Close window"""
        self.quit()
        self.destroy()

