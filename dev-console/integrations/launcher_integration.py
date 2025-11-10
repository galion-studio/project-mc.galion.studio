"""
Launcher Integration
Launch GALION game client from developer console
"""

import subprocess
import sys
from pathlib import Path
from typing import Tuple


class LauncherIntegration:
    """
    Integration with GALION game client launcher.
    Allows launching client from developer console.
    """
    
    def __init__(self):
        """Initialize launcher integration"""
        # Find project root (dev-console parent directory)
        self.dev_console_dir = Path(__file__).parent.parent
        self.project_root = self.dev_console_dir.parent
        
        # Client launcher paths
        self.client_launcher_dir = self.project_root / "client-launcher"
        self.launcher_script = self.client_launcher_dir / "galion-launcher.py"
        
        # Check if launcher exists
        self.launcher_available = self.launcher_script.exists()
    
    def launch_client(self) -> Tuple[bool, str]:
        """
        Launch GALION game client.
        
        Returns:
            Tuple of (success, message)
        """
        if not self.launcher_available:
            return False, f"Launcher not found at {self.launcher_script}"
        
        try:
            # Detect Python command
            python_cmd = self._get_python_command()
            
            if not python_cmd:
                return False, "Python not found in system PATH"
            
            # Launch client in separate process
            process = subprocess.Popen(
                [python_cmd, str(self.launcher_script)],
                cwd=str(self.client_launcher_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
            )
            
            return True, f"Client launched (PID: {process.pid})"
        
        except Exception as e:
            return False, f"Failed to launch: {str(e)}"
    
    def _get_python_command(self) -> str:
        """Get Python command for current platform"""
        # Try different Python commands
        commands = ['py', 'python', 'python3']
        
        for cmd in commands:
            try:
                result = subprocess.run(
                    [cmd, '--version'],
                    capture_output=True,
                    timeout=2
                )
                if result.returncode == 0:
                    return cmd
            except:
                continue
        
        return None
    
    def is_launcher_available(self) -> bool:
        """Check if launcher is available"""
        return self.launcher_available
    
    def get_launcher_path(self) -> Path:
        """Get launcher script path"""
        return self.launcher_script
    
    def check_launcher_status(self) -> dict:
        """Get launcher status information"""
        return {
            "available": self.launcher_available,
            "path": str(self.launcher_script),
            "client_dir": str(self.client_launcher_dir),
            "python_command": self._get_python_command()
        }


# Singleton instance
_launcher_integration_instance = None


def get_launcher_integration() -> LauncherIntegration:
    """Get launcher integration singleton instance"""
    global _launcher_integration_instance
    if _launcher_integration_instance is None:
        _launcher_integration_instance = LauncherIntegration()
    return _launcher_integration_instance
