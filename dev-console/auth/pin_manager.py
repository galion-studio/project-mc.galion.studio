"""
PIN Manager
Secure PIN-based authentication for console access
"""

import hashlib
import json
from pathlib import Path
from typing import Optional


class PinManager:
    """
    Manages console PIN authentication.
    Stores hashed PINs for security.
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize PIN manager"""
        if config_path is None:
            config_path = Path(__file__).parent / "pin_config.json"
        
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """Load PIN configuration"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[PIN] Error loading config: {e}")
                return self._default_config()
        else:
            return self._default_config()
    
    def _default_config(self) -> dict:
        """Create default configuration with PIN 1234"""
        default_pin = "1234"
        return {
            "pin_hash": self._hash_pin(default_pin),
            "attempts": 0,
            "locked": False
        }
    
    def _save_config(self):
        """Save PIN configuration"""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"[PIN] Error saving config: {e}")
    
    def _hash_pin(self, pin: str) -> str:
        """Hash PIN using SHA256"""
        return hashlib.sha256(pin.encode()).hexdigest()
    
    def verify_pin(self, pin: str) -> bool:
        """
        Verify PIN.
        
        Args:
            pin: PIN to verify
            
        Returns:
            True if PIN is correct, False otherwise
        """
        # Check if locked
        if self.config.get("locked", False):
            print("[PIN] Console is locked due to too many attempts")
            return False
        
        # Verify PIN
        pin_hash = self._hash_pin(pin)
        is_correct = pin_hash == self.config["pin_hash"]
        
        if is_correct:
            # Reset attempts on success
            self.config["attempts"] = 0
            self._save_config()
            return True
        else:
            # Increment attempts
            self.config["attempts"] = self.config.get("attempts", 0) + 1
            
            # Lock after 5 failed attempts
            if self.config["attempts"] >= 5:
                self.config["locked"] = True
                print("[PIN] Console locked after 5 failed attempts")
            
            self._save_config()
            return False
    
    def set_pin(self, new_pin: str):
        """
        Set new PIN.
        
        Args:
            new_pin: New PIN to set (should be 4 digits)
        """
        if len(new_pin) != 4 or not new_pin.isdigit():
            raise ValueError("PIN must be 4 digits")
        
        self.config["pin_hash"] = self._hash_pin(new_pin)
        self.config["attempts"] = 0
        self.config["locked"] = False
        self._save_config()
        
        print("[PIN] PIN changed successfully")
    
    def is_locked(self) -> bool:
        """Check if console is locked"""
        return self.config.get("locked", False)
    
    def unlock(self, master_password: str = "galion_admin_reset"):
        """
        Unlock console (for emergency recovery).
        
        Args:
            master_password: Master password to unlock
        """
        if master_password == "galion_admin_reset":
            self.config["locked"] = False
            self.config["attempts"] = 0
            self._save_config()
            print("[PIN] Console unlocked")
            return True
        return False
    
    def get_attempts(self) -> int:
        """Get number of failed attempts"""
        return self.config.get("attempts", 0)
    
    def reset_to_default(self):
        """Reset PIN to default (1234)"""
        self.config = self._default_config()
        self._save_config()
        print("[PIN] PIN reset to default (1234)")


# Singleton instance
_pin_manager_instance = None


def get_pin_manager() -> PinManager:
    """Get PIN manager singleton instance"""
    global _pin_manager_instance
    if _pin_manager_instance is None:
        _pin_manager_instance = PinManager()
    return _pin_manager_instance
