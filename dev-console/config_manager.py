"""
Configuration Manager - Full Transparency
Shows all configuration, API keys, passwords, secrets
Everything is visible and editable - open source philosophy
"""

import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv, set_key
import json

class ConfigManager:
    """
    Manages all configuration for the Minecraft server
    Full transparency - all settings visible and editable
    """
    
    def __init__(self, project_root: str = None):
        """Initialize configuration manager"""
        
        # Set project root
        if project_root:
            self.project_root = Path(project_root)
        else:
            self.project_root = Path(__file__).parent.parent
        
        # Configuration file paths
        self.env_grok_file = self.project_root / ".env.grok"
        self.env_file = self.project_root / ".env"
        self.launcher_config_file = self.project_root / "launcher_config.json"
        
        # Load all configuration
        self.load_all_config()
    
    def load_all_config(self):
        """Load all configuration from all sources"""
        
        # Load .env.grok
        if self.env_grok_file.exists():
            load_dotenv(self.env_grok_file)
        
        # Load .env
        if self.env_file.exists():
            load_dotenv(self.env_file)
        
        # Build complete configuration dictionary
        self.config = {
            # AI Configuration
            "ai": {
                "openrouter_api_key": os.getenv("OPENROUTER_API_KEY", ""),
                "grok_model": os.getenv("GROK_MODEL", "x-ai/grok-4-fast"),
                "grok_timeout": os.getenv("GROK_TIMEOUT", "2"),
                "grok_max_tokens": os.getenv("GROK_MAX_TOKENS", "100"),
                "response_cache_size": os.getenv("RESPONSE_CACHE_SIZE", "100"),
            },
            
            # Minecraft Server Configuration
            "minecraft": {
                "version": os.getenv("MC_VERSION", "1.21.1"),
                "eula": os.getenv("MC_EULA", "true"),
                "server_port": os.getenv("SERVER_PORT", "25565"),
                "max_players": os.getenv("MAX_PLAYERS", "100"),
                "rcon_host": os.getenv("MINECRAFT_RCON_HOST", "localhost"),
                "rcon_port": os.getenv("MINECRAFT_RCON_PORT", "25575"),
                "rcon_password": os.getenv("MINECRAFT_RCON_PASSWORD", "titan123"),
                "docker_container": os.getenv("MINECRAFT_DOCKER_CONTAINER", "titan-hub"),
            },
            
            # Database Configuration
            "database": {
                "postgres_host": os.getenv("POSTGRES_HOST", "localhost"),
                "postgres_port": os.getenv("POSTGRES_PORT", "5432"),
                "postgres_db": os.getenv("POSTGRES_DB", "galion_mc"),
                "postgres_user": os.getenv("POSTGRES_USER", "mcserver"),
                "postgres_password": os.getenv("POSTGRES_PASSWORD", ""),
                "redis_host": os.getenv("REDIS_HOST", "localhost"),
                "redis_port": os.getenv("REDIS_PORT", "6379"),
                "redis_password": os.getenv("REDIS_PASSWORD", ""),
            },
            
            # VPN & Network Configuration
            "network": {
                "velocity_secret": os.getenv("VELOCITY_SECRET", ""),
                "velocity_port": os.getenv("VELOCITY_PORT", "25565"),
                "domain": os.getenv("DOMAIN", "galion.studio"),
                "vpn_enabled": os.getenv("VPN_ENABLED", "false"),
                "vpn_provider": os.getenv("VPN_PROVIDER", ""),
                "vpn_username": os.getenv("VPN_USERNAME", ""),
                "vpn_password": os.getenv("VPN_PASSWORD", ""),
            },
            
            # Chat Server Configuration
            "chat_server": {
                "host": os.getenv("CHAT_SERVER_HOST", "localhost"),
                "port": os.getenv("CHAT_SERVER_PORT", "8000"),
            },
            
            # Monitoring Configuration
            "monitoring": {
                "grafana_admin_password": os.getenv("GRAFANA_ADMIN_PASSWORD", ""),
            },
            
            # Project Configuration
            "project": {
                "root": os.getenv("PROJECT_ROOT", str(self.project_root)),
            },
        }
    
    def get_all_config(self) -> Dict[str, Any]:
        """Get all configuration as dictionary"""
        return self.config
    
    def get_config_category(self, category: str) -> Dict[str, Any]:
        """Get configuration for specific category"""
        return self.config.get(category, {})
    
    def get_config_value(self, category: str, key: str) -> str:
        """Get specific configuration value"""
        return self.config.get(category, {}).get(key, "")
    
    def set_config_value(self, category: str, key: str, value: str):
        """
        Set configuration value and save to file
        Updates both in-memory config and .env files
        """
        
        # Update in-memory config
        if category not in self.config:
            self.config[category] = {}
        self.config[category][key] = value
        
        # Determine which file to update
        # AI settings go to .env.grok
        # Others go to .env
        if category in ["ai", "chat_server"]:
            env_file = self.env_grok_file
        else:
            env_file = self.env_file
        
        # Map config keys to env variable names
        env_key = self._get_env_key_name(category, key)
        
        # Update .env file
        if not env_file.exists():
            env_file.touch()
        
        set_key(str(env_file), env_key, value)
    
    def _get_env_key_name(self, category: str, key: str) -> str:
        """Convert category and key to env variable name"""
        
        # Special mappings
        mapping = {
            ("ai", "openrouter_api_key"): "OPENROUTER_API_KEY",
            ("ai", "grok_model"): "GROK_MODEL",
            ("ai", "grok_timeout"): "GROK_TIMEOUT",
            ("ai", "grok_max_tokens"): "GROK_MAX_TOKENS",
            ("ai", "response_cache_size"): "RESPONSE_CACHE_SIZE",
            ("minecraft", "version"): "MC_VERSION",
            ("minecraft", "eula"): "MC_EULA",
            ("minecraft", "server_port"): "SERVER_PORT",
            ("minecraft", "max_players"): "MAX_PLAYERS",
            ("minecraft", "rcon_host"): "MINECRAFT_RCON_HOST",
            ("minecraft", "rcon_port"): "MINECRAFT_RCON_PORT",
            ("minecraft", "rcon_password"): "MINECRAFT_RCON_PASSWORD",
            ("minecraft", "docker_container"): "MINECRAFT_DOCKER_CONTAINER",
            ("database", "postgres_host"): "POSTGRES_HOST",
            ("database", "postgres_port"): "POSTGRES_PORT",
            ("database", "postgres_db"): "POSTGRES_DB",
            ("database", "postgres_user"): "POSTGRES_USER",
            ("database", "postgres_password"): "POSTGRES_PASSWORD",
            ("database", "redis_host"): "REDIS_HOST",
            ("database", "redis_port"): "REDIS_PORT",
            ("database", "redis_password"): "REDIS_PASSWORD",
            ("network", "velocity_secret"): "VELOCITY_SECRET",
            ("network", "velocity_port"): "VELOCITY_PORT",
            ("network", "domain"): "DOMAIN",
            ("network", "vpn_enabled"): "VPN_ENABLED",
            ("network", "vpn_provider"): "VPN_PROVIDER",
            ("network", "vpn_username"): "VPN_USERNAME",
            ("network", "vpn_password"): "VPN_PASSWORD",
            ("chat_server", "host"): "CHAT_SERVER_HOST",
            ("chat_server", "port"): "CHAT_SERVER_PORT",
            ("monitoring", "grafana_admin_password"): "GRAFANA_ADMIN_PASSWORD",
            ("project", "root"): "PROJECT_ROOT",
        }
        
        return mapping.get((category, key), key.upper())
    
    def export_config_text(self) -> str:
        """
        Export all configuration as easy-to-copy text
        Perfect for sharing or backup
        """
        
        lines = []
        lines.append("=" * 70)
        lines.append("  MINECRAFT SERVER CONFIGURATION - FULL TRANSPARENCY")
        lines.append("  All settings visible - Open Source Philosophy")
        lines.append("=" * 70)
        lines.append("")
        
        for category, settings in self.config.items():
            lines.append(f"\n[{category.upper()}]")
            lines.append("-" * 70)
            
            for key, value in settings.items():
                # Show masked value for passwords/secrets
                display_value = value
                if any(keyword in key.lower() for keyword in ['password', 'secret', 'key']):
                    if value and value != "":
                        # Show first 4 and last 4 characters
                        if len(value) > 12:
                            display_value = f"{value[:4]}...{value[-4:]}"
                        else:
                            display_value = "***"
                
                lines.append(f"{key:30s} = {display_value}")
        
        lines.append("\n" + "=" * 70)
        lines.append("  To edit: Use the configuration panel or edit .env files directly")
        lines.append("=" * 70)
        
        return "\n".join(lines)
    
    def export_config_full(self) -> str:
        """
        Export full configuration (including secrets)
        WARNING: Contains sensitive data
        """
        
        lines = []
        lines.append("=" * 70)
        lines.append("  FULL CONFIGURATION EXPORT - CONTAINS SECRETS")
        lines.append("  ⚠️  WARNING: Keep this file secure!")
        lines.append("=" * 70)
        lines.append("")
        
        for category, settings in self.config.items():
            lines.append(f"\n[{category.upper()}]")
            lines.append("-" * 70)
            
            for key, value in settings.items():
                lines.append(f"{key:30s} = {value}")
        
        lines.append("\n" + "=" * 70)
        
        return "\n".join(lines)
    
    def validate_config(self) -> Dict[str, list]:
        """
        Validate configuration
        Returns dict with issues found
        """
        
        issues = {
            "missing": [],
            "warnings": [],
        }
        
        # Check critical settings
        if not self.config["ai"]["openrouter_api_key"]:
            issues["missing"].append("OpenRouter API Key (AI features disabled)")
        
        if not self.config["minecraft"]["rcon_password"]:
            issues["warnings"].append("RCON password not set (default will be used)")
        
        if not self.config["database"]["postgres_password"]:
            issues["warnings"].append("PostgreSQL password not set")
        
        if not self.config["database"]["redis_password"]:
            issues["warnings"].append("Redis password not set")
        
        if not self.config["network"]["velocity_secret"]:
            issues["warnings"].append("Velocity secret not set")
        
        return issues


# Quick test function
def test_config_manager():
    """Test the configuration manager"""
    
    manager = ConfigManager()
    
    print("Testing Configuration Manager...")
    print()
    
    # Show all configuration
    print(manager.export_config_text())
    print()
    
    # Validate
    issues = manager.validate_config()
    if issues["missing"]:
        print("❌ MISSING:")
        for issue in issues["missing"]:
            print(f"  - {issue}")
    
    if issues["warnings"]:
        print("⚠️  WARNINGS:")
        for issue in issues["warnings"]:
            print(f"  - {issue}")
    
    print()
    print("✅ Configuration manager test complete!")


if __name__ == "__main__":
    test_config_manager()

