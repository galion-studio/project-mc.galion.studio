"""
Hot Reloader System
File watcher with automatic plugin reloading via RCON
"""

import time
from pathlib import Path
from typing import Optional, Callable
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

from config import SERVER_MODS_DIR, RCON_HOST, RCON_PORT, RCON_PASSWORD, HOT_RELOAD_WATCH_DELAY, HOT_RELOAD_DEBOUNCE


class ModFileHandler(FileSystemEventHandler):
    """
    File system event handler for mod files.
    Detects changes and triggers reloads.
    """
    
    def __init__(self, on_change: Callable):
        super().__init__()
        self.on_change = on_change
        self.last_modified = {}
        self.debounce_time = HOT_RELOAD_DEBOUNCE
    
    def on_created(self, event: FileSystemEvent):
        """Handle file creation"""
        if event.is_directory:
            return
        
        if event.src_path.endswith('.jar'):
            self.trigger_reload('created', event.src_path)
    
    def on_modified(self, event: FileSystemEvent):
        """Handle file modification"""
        if event.is_directory:
            return
        
        if event.src_path.endswith('.jar'):
            # Debounce - only trigger if enough time has passed
            current_time = time.time()
            last_time = self.last_modified.get(event.src_path, 0)
            
            if current_time - last_time > self.debounce_time:
                self.last_modified[event.src_path] = current_time
                self.trigger_reload('modified', event.src_path)
    
    def on_deleted(self, event: FileSystemEvent):
        """Handle file deletion"""
        if event.is_directory:
            return
        
        if event.src_path.endswith('.jar'):
            self.trigger_reload('deleted', event.src_path)
    
    def trigger_reload(self, action: str, file_path: str):
        """Trigger reload callback"""
        file_name = Path(file_path).name
        self.on_change(action, file_name)


class HotReloader:
    """
    Hot reloader system.
    Watches for mod file changes and reloads plugins automatically.
    
    First principles approach:
    - Watch file system for changes
    - Debounce rapid changes
    - Use RCON to reload plugins
    - Provide clear feedback
    """
    
    def __init__(self, on_reload: Optional[Callable] = None):
        self.watch_dir = SERVER_MODS_DIR
        self.on_reload = on_reload or (lambda a, f, s: None)
        self.observer = None
        self.is_running = False
        self.rcon_connection = None
    
    def start(self):
        """Start watching for file changes"""
        if self.is_running:
            return
        
        # Create event handler
        event_handler = ModFileHandler(self.handle_file_change)
        
        # Create and start observer
        self.observer = Observer()
        self.observer.schedule(event_handler, str(self.watch_dir), recursive=False)
        self.observer.start()
        
        self.is_running = True
        print(f"[Hot Reload] Watching: {self.watch_dir}")
    
    def stop(self):
        """Stop watching for file changes"""
        if not self.is_running:
            return
        
        if self.observer:
            self.observer.stop()
            self.observer.join()
        
        self.is_running = False
        print("[Hot Reload] Stopped")
    
    def handle_file_change(self, action: str, file_name: str):
        """
        Handle file change event.
        
        This is where the magic happens:
        1. File changed detected
        2. Extract plugin name from filename
        3. Send RCON command to reload
        4. Report success/failure
        """
        print(f"[Hot Reload] {action.upper()}: {file_name}")
        
        # Extract plugin name (remove -version.jar)
        plugin_name = file_name.replace('.jar', '')
        # Remove version numbers (simple heuristic)
        plugin_name = plugin_name.split('-')[0]
        
        if action == 'deleted':
            # Plugin deleted - unload it
            self.unload_plugin(plugin_name, file_name)
        else:
            # Plugin created or modified - reload it
            self.reload_plugin(plugin_name, file_name)
    
    def reload_plugin(self, plugin_name: str, file_name: str):
        """
        Reload a plugin using RCON.
        
        Strategy:
        1. Try to use PlugManX (if installed)
        2. Otherwise tell user to restart server
        """
        try:
            # Try RCON reload
            success = self.send_rcon_command(f"plugman reload {plugin_name}")
            
            if success:
                self.on_reload(
                    'reload',
                    file_name,
                    True,
                    f"Plugin {plugin_name} reloaded successfully"
                )
            else:
                # Fallback message
                self.on_reload(
                    'reload',
                    file_name,
                    False,
                    f"Could not hot-reload {plugin_name}. Restart server to load changes."
                )
        
        except Exception as e:
            self.on_reload(
                'reload',
                file_name,
                False,
                f"Error reloading {plugin_name}: {str(e)}"
            )
    
    def unload_plugin(self, plugin_name: str, file_name: str):
        """Unload a plugin"""
        try:
            success = self.send_rcon_command(f"plugman unload {plugin_name}")
            
            if success:
                self.on_reload(
                    'unload',
                    file_name,
                    True,
                    f"Plugin {plugin_name} unloaded"
                )
            else:
                self.on_reload(
                    'unload',
                    file_name,
                    False,
                    f"Could not unload {plugin_name}"
                )
        
        except Exception as e:
            self.on_reload(
                'unload',
                file_name,
                False,
                f"Error unloading {plugin_name}: {str(e)}"
            )
    
    def send_rcon_command(self, command: str) -> bool:
        """
        Send RCON command to server.
        
        Returns True if successful, False otherwise.
        """
        try:
            # Try to import mcrcon
            try:
                from mcrcon import MCRcon
            except ImportError:
                print("[Hot Reload] mcrcon not installed. Install with: pip install mcrcon")
                return False
            
            # Connect and send command
            with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
                response = mcr.command(command)
                print(f"[RCON] {command} -> {response}")
                return True
        
        except Exception as e:
            print(f"[RCON] Error: {e}")
            return False
    
    def test_rcon_connection(self) -> bool:
        """Test RCON connection"""
        try:
            from mcrcon import MCRcon
            
            with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
                response = mcr.command("list")
                print(f"[RCON] Connection successful. Server response: {response}")
                return True
        
        except Exception as e:
            print(f"[RCON] Connection failed: {e}")
            return False


# Singleton instance
_hot_reloader = None


def get_hot_reloader(on_reload: Optional[Callable] = None) -> HotReloader:
    """Get hot reloader singleton"""
    global _hot_reloader
    if _hot_reloader is None:
        _hot_reloader = HotReloader(on_reload)
    return _hot_reloader


# Test function
if __name__ == "__main__":
    print("="*50)
    print("  HOT RELOADER TEST")
    print("="*50)
    print()
    
    def reload_callback(action, filename, success, message):
        print(f"[Callback] {action} - {filename}")
        print(f"  Success: {success}")
        print(f"  Message: {message}")
        print()
    
    reloader = get_hot_reloader(reload_callback)
    
    # Test RCON connection
    print("Testing RCON connection...")
    if reloader.test_rcon_connection():
        print("[OK] RCON connection working!")
    else:
        print("[!] RCON connection failed. Make sure:")
        print("  1. Server is running")
        print("  2. RCON is enabled in server.properties")
        print("  3. RCON password is correct in config.py")
    print()
    
    # Start watching
    print(f"Starting hot reloader...")
    print(f"Watching: {SERVER_MODS_DIR}")
    print("Try adding, modifying, or removing .jar files...")
    print("Press Ctrl+C to stop")
    print()
    
    reloader.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nStopping...")
        reloader.stop()
        print("Done!")

