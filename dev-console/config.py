"""
Development Console Configuration
Central configuration for all console components
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base paths
BASE_DIR = Path(__file__).parent
PROJECT_ROOT = BASE_DIR.parent

# Load Grok configuration from parent directory
load_dotenv(PROJECT_ROOT / ".env.grok")
SERVER_MODS_DIR = PROJECT_ROOT / "server-mods"
MINECRAFT_PACKAGES_DIR = PROJECT_ROOT / "minecraft-packages"
LOGS_DIR = PROJECT_ROOT / "logs"

# API Configuration
API_HOST = "localhost"
API_PORT = 8080
API_BASE_URL = f"http://{API_HOST}:{API_PORT}"

# Server Configuration
MINECRAFT_SERVER_PORT = 25565
RCON_HOST = os.getenv("MINECRAFT_RCON_HOST", "localhost")
RCON_PORT = int(os.getenv("MINECRAFT_RCON_PORT", "25575"))
RCON_PASSWORD = os.getenv("MINECRAFT_RCON_PASSWORD", "titan123")

# Grok AI Configuration (via OpenRouter)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
GROK_MODEL = os.getenv("GROK_MODEL", "x-ai/grok-4-fast")

# Database
DATABASE_PATH = BASE_DIR / "database" / "dev_console.db"

# UI Theme - Modern gradient design
THEME = {
    # Background gradients
    "bg_primary": "#0a0e27",
    "bg_secondary": "#1a1f4a",
    "bg_tertiary": "#2a0e4a",
    
    # Cards and surfaces
    "card_bg": "#1a1f3a",
    "card_hover": "#252b4a",
    
    # Accent colors
    "accent": "#4a9eff",
    "accent_hover": "#3a8eef",
    
    # Status colors
    "success": "#00d9a3",
    "warning": "#ffb347",
    "error": "#ff5757",
    "info": "#4a9eff",
    
    # Text colors
    "text_primary": "#ffffff",
    "text_secondary": "#8892b0",
    "text_dim": "#5a6580",
    
    # Border and shadow
    "border": "#2a2f4a",
    "shadow": "0 4px 12px rgba(0,0,0,0.3)",
    
    # Fonts
    "font_header": ("Segoe UI", 24, "bold"),
    "font_subheader": ("Segoe UI", 18, "bold"),
    "font_body": ("Segoe UI", 14),
    "font_code": ("Consolas", 12),
    "font_small": ("Segoe UI", 11),
}

# Layout
LAYOUT = {
    "sidebar_width": 200,
    "topbar_height": 60,
    "card_padding": 20,
    "card_gap": 20,
    "border_radius": 12,
}

# Environments
ENVIRONMENTS = {
    "dev": {
        "name": "Development",
        "color": "#4a9eff",
        "server_ip": "localhost",
        "server_port": 25565,
        "hot_reload": True,
    },
    "staging": {
        "name": "Staging",
        "color": "#ffb347",
        "server_ip": "staging.galion.studio",
        "server_port": 25565,
        "hot_reload": False,
    },
    "prod": {
        "name": "Production",
        "color": "#ff5757",
        "server_ip": "mc.galion.studio",
        "server_port": 25565,
        "hot_reload": False,
    },
}

# Roles
ROLES = {
    "admin": {
        "name": "Administrator",
        "permissions": ["all"],
    },
    "internal_dev": {
        "name": "Internal Developer",
        "permissions": [
            "upload_mod",
            "deploy_dev",
            "deploy_staging",
            "hot_reload",
            "view_logs",
            "server_control",
            "rollback",
        ],
    },
    "external_dev": {
        "name": "External Developer",
        "permissions": [
            "upload_mod",
            "view_logs",
        ],
    },
}

# File upload limits
MAX_MOD_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
ALLOWED_MOD_EXTENSIONS = [".jar"]

# Hot reload settings
HOT_RELOAD_WATCH_DELAY = 1.0  # seconds
HOT_RELOAD_DEBOUNCE = 2.0  # seconds

# Ensure directories exist
SERVER_MODS_DIR.mkdir(exist_ok=True)
MINECRAFT_PACKAGES_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
(DATABASE_PATH.parent).mkdir(exist_ok=True)

