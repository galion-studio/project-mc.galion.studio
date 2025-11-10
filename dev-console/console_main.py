"""
Development Minecraft Console - Main Entry Point
Modern console for rapid mod development and deployment

Built following Elon Musk principles:
- First principles thinking
- Rapid iteration
- Vertical integration
"""

import customtkinter as ctk
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import THEME, LAYOUT
from ui.sidebar import Sidebar
from ui.topbar import TopBar
from ui.dashboard import Dashboard
from database.db_manager import get_db


class DevConsole(ctk.CTk):
    """
    Main Development Console Application.
    Simple, modern, effective.
    """
    
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("Development Minecraft Console - Galion.Studio")
        self.geometry("1400x900")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Configure window background with gradient effect
        self.configure(fg_color=THEME["bg_primary"])
        
        # Initialize database
        self.db = get_db()
        
        # Current user (default admin for now)
        self.current_user = {
            "id": 1,
            "username": "admin",
            "role": "admin"
        }
        
        # Current view
        self.current_view = None
        
        # Create UI
        self.create_ui()
        
        # Show dashboard by default
        self.show_dashboard()
    
    def create_ui(self):
        """Create the main UI layout"""
        # Top bar
        self.topbar = TopBar(
            self,
            user_name=self.current_user["username"],
            user_role=self.current_user["role"]
        )
        self.topbar.pack(side="top", fill="x")
        
        # Main container
        self.main_container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.main_container.pack(side="top", fill="both", expand=True)
        
        # Sidebar
        self.sidebar = Sidebar(
            self.main_container,
            on_navigate=self.navigate_to
        )
        self.sidebar.pack(side="left", fill="y")
        
        # Content area
        self.content_area = ctk.CTkFrame(
            self.main_container,
            fg_color=THEME["bg_primary"],
            corner_radius=0
        )
        self.content_area.pack(side="left", fill="both", expand=True)
    
    def navigate_to(self, section: str):
        """Navigate to a section"""
        # Clear current view
        if self.current_view:
            self.current_view.pack_forget()
            self.current_view.destroy()
        
        # Show new view
        if section == "dashboard":
            self.show_dashboard()
        elif section == "mods":
            self.show_mods()
        elif section == "server":
            self.show_server()
        elif section == "logs":
            self.show_logs()
        elif section == "repository":
            self.show_repository()
        elif section == "environments":
            self.show_environments()
        elif section == "team":
            self.show_team()
        elif section == "snippets":
            self.show_snippets()
        elif section == "builder":
            self.show_builder()
        elif section == "profiler":
            self.show_profiler()
        elif section == "ai_chat":
            self.show_ai_chat()
        elif section == "settings":
            self.show_settings()
        else:
            self.show_dashboard()
    
    def show_dashboard(self):
        """Show dashboard view"""
        self.current_view = Dashboard(
            self.content_area,
            on_quick_action=self.handle_quick_action
        )
        self.current_view.pack(fill="both", expand=True)
    
    def show_mods(self):
        """Show mods management view"""
        # Lazy import to avoid circular dependencies
        from mods.mod_uploader import ModUploader
        
        self.current_view = ModUploader(
            self.content_area,
            db=self.db,
            current_user=self.current_user,
            environment=self.topbar.get_current_environment()
        )
        self.current_view.pack(fill="both", expand=True)
    
    def show_server(self):
        """Show server control view"""
        from server.server_controller import ServerController
        
        self.current_view = ServerController(
            self.content_area,
            db=self.db,
            on_status_change=self.topbar.update_server_status
        )
        self.current_view.pack(fill="both", expand=True)
    
    def show_logs(self):
        """Show logs viewer"""
        from server.logs_viewer import LogsViewer
        
        self.current_view = LogsViewer(self.content_area)
        self.current_view.pack(fill="both", expand=True)
    
    def show_repository(self):
        """Show repository management"""
        from repository.repo_manager import RepositoryManager
        
        self.current_view = RepositoryManager(
            self.content_area,
            db=self.db
        )
        self.current_view.pack(fill="both", expand=True)
    
    def show_environments(self):
        """Show environment manager"""
        from environments.env_manager import EnvironmentManager
        
        self.current_view = EnvironmentManager(
            self.content_area,
            db=self.db
        )
        self.current_view.pack(fill="both", expand=True)
    
    def show_team(self):
        """Show team collaboration"""
        from team.activity_feed import ActivityFeed
        
        self.current_view = ActivityFeed(
            self.content_area,
            db=self.db
        )
        self.current_view.pack(fill="both", expand=True)
    
    def show_snippets(self):
        """Show code snippets"""
        from ide.snippets import SnippetsLibrary
        
        self.current_view = SnippetsLibrary(self.content_area)
        self.current_view.pack(fill="both", expand=True)
    
    def show_builder(self):
        """Show mod builder"""
        from ide.builder import ModBuilder
        
        self.current_view = ModBuilder(
            self.content_area,
            db=self.db
        )
        self.current_view.pack(fill="both", expand=True)
    
    def show_profiler(self):
        """Show profiler"""
        from debug.profiler import Profiler
        
        self.current_view = Profiler(self.content_area)
        self.current_view.pack(fill="both", expand=True)
    
    def show_ai_chat(self):
        """Show AI chat with Grok"""
        from ai.ai_control_center import AIControlCenter
        
        self.current_view = AIControlCenter(self.content_area)
        self.current_view.pack(fill="both", expand=True)
    
    def show_settings(self):
        """Show settings"""
        # Create a simple placeholder for now
        self.current_view = ctk.CTkFrame(
            self.content_area,
            fg_color=THEME["bg_primary"]
        )
        self.current_view.pack(fill="both", expand=True)
        
        label = ctk.CTkLabel(
            self.current_view,
            text="⚙️ Settings",
            font=THEME["font_header"],
            text_color=THEME["text_primary"]
        )
        label.pack(pady=50)
        
        info = ctk.CTkLabel(
            self.current_view,
            text="Settings panel - Coming soon",
            font=THEME["font_body"],
            text_color=THEME["text_secondary"]
        )
        info.pack(pady=10)
    
    def handle_quick_action(self, action: str):
        """Handle quick action from dashboard"""
        if action == "upload_mod":
            self.navigate_to("mods")
        elif action == "start_server":
            self.navigate_to("server")
        elif action == "view_logs":
            self.navigate_to("logs")


def main():
    """Main entry point"""
    print("="*50)
    print("  DEVELOPMENT MINECRAFT CONSOLE")
    print("  Galion.Studio")
    print("="*50)
    print()
    print("Initializing...")
    
    # Create and run application
    app = DevConsole()
    
    print("[OK] Console started!")
    print()
    
    app.mainloop()


if __name__ == "__main__":
    main()

