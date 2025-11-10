#!/usr/bin/env python3
"""
ASCII Logo and Branding for Grok Console Chat
Cool visual elements and server information
"""

from colorama import Fore, Style

# ASCII Art Logo
LOGO = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════╗
║  {Fore.GREEN}████████╗██╗████████╗ █████╗ ███╗   ██╗     █████╗ ██╗{Fore.CYAN}        ║
║  {Fore.GREEN}╚══██╔══╝██║╚══██╔══╝██╔══██╗████╗  ██║    ██╔══██╗██║{Fore.CYAN}        ║
║  {Fore.GREEN}   ██║   ██║   ██║   ███████║██╔██╗ ██║    ███████║██║{Fore.CYAN}        ║
║  {Fore.GREEN}   ██║   ██║   ██║   ██╔══██║██║╚██╗██║    ██╔══██║██║{Fore.CYAN}        ║
║  {Fore.GREEN}   ██║   ██║   ██║   ██║  ██║██║ ╚████║    ██║  ██║██║{Fore.CYAN}        ║
║  {Fore.GREEN}   ╚═╝   ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝    ╚═╝  ╚═╝╚═╝{Fore.CYAN}        ║
╚═══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""

# Compact logo for space-constrained displays
LOGO_COMPACT = f"""
{Fore.CYAN}╔════════════════════════════════════════════════╗
║  {Fore.GREEN}⚡ TITAN AI  {Fore.YELLOW}•  {Fore.MAGENTA}Grok-4 Fast  {Fore.YELLOW}•  {Fore.BLUE}mc.galion.studio{Fore.CYAN}  ║
╚════════════════════════════════════════════════╝{Style.RESET_ALL}
"""

# Server Bio/Information
SERVER_BIO = f"""
{Fore.YELLOW}┌─ SERVER INFORMATION ────────────────────────────────────────────┐{Style.RESET_ALL}
{Fore.WHITE}│{Style.RESET_ALL}  {Fore.GREEN}Project:{Style.RESET_ALL}      Titan - Next-Gen Minecraft Server Platform
{Fore.WHITE}│{Style.RESET_ALL}  {Fore.GREEN}URL:{Style.RESET_ALL}          mc.galion.studio
{Fore.WHITE}│{Style.RESET_ALL}  {Fore.GREEN}Capacity:{Style.RESET_ALL}     20,000+ concurrent players
{Fore.WHITE}│{Style.RESET_ALL}  {Fore.GREEN}AI Model:{Style.RESET_ALL}     Grok-4 Fast (via OpenRouter)
{Fore.WHITE}│{Style.RESET_ALL}  {Fore.GREEN}Response:{Style.RESET_ALL}     <1 second typical (0.3-0.8s)
{Fore.WHITE}│{Style.RESET_ALL}  {Fore.GREEN}Features:{Style.RESET_ALL}     AI Chat, RCON Control, Project Management
{Fore.YELLOW}└──────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}
"""

# Feature highlights
FEATURES = f"""
{Fore.CYAN}╔══ POWERED FEATURES ══════════════════════════════════════════════╗{Style.RESET_ALL}
{Fore.WHITE}║{Style.RESET_ALL}  {Fore.YELLOW}⚡{Style.RESET_ALL} Ultra-Fast AI      {Fore.WHITE}│{Style.RESET_ALL}  {Fore.YELLOW}🎮{Style.RESET_ALL} RCON Commands     {Fore.WHITE}│{Style.RESET_ALL}  {Fore.YELLOW}🔧{Style.RESET_ALL} Git Integration
{Fore.WHITE}║{Style.RESET_ALL}  {Fore.YELLOW}💾{Style.RESET_ALL} Smart Caching      {Fore.WHITE}│{Style.RESET_ALL}  {Fore.YELLOW}🐳{Style.RESET_ALL} Docker Control    {Fore.WHITE}│{Style.RESET_ALL}  {Fore.YELLOW}📊{Style.RESET_ALL} Live Statistics
{Fore.WHITE}║{Style.RESET_ALL}  {Fore.YELLOW}🌐{Style.RESET_ALL} REST API           {Fore.WHITE}│{Style.RESET_ALL}  {Fore.YELLOW}🔌{Style.RESET_ALL} Plugin System     {Fore.WHITE}│{Style.RESET_ALL}  {Fore.YELLOW}📝{Style.RESET_ALL} Command History
{Fore.CYAN}╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""

# Cool animated banner
BANNER_LINES = [
    f"{Fore.CYAN}{'═' * 70}{Style.RESET_ALL}",
    f"{Fore.GREEN}  ⚡⚡⚡  TITAN AI CONSOLE  ⚡⚡⚡{Style.RESET_ALL}",
    f"{Fore.YELLOW}  The Future of Minecraft Server Management{Style.RESET_ALL}",
    f"{Fore.CYAN}{'═' * 70}{Style.RESET_ALL}",
]

# Status indicators
STATUS_ONLINE = f"{Fore.GREEN}● ONLINE{Style.RESET_ALL}"
STATUS_OFFLINE = f"{Fore.RED}● OFFLINE{Style.RESET_ALL}"
STATUS_WARNING = f"{Fore.YELLOW}⚠ WARNING{Style.RESET_ALL}"
STATUS_LOADING = f"{Fore.BLUE}⟳ LOADING{Style.RESET_ALL}"

# Fun facts about the system
FACTS = [
    "💡 Titan can handle 20,000+ players simultaneously!",
    "⚡ Grok-4 Fast responds in under 1 second!",
    "🚀 Commands execute in milliseconds!",
    "🧠 AI has access to 500+ models through OpenRouter!",
    "🔥 Built with first principles thinking!",
    "🎯 Response caching makes repeated queries instant!",
    "🌐 OpenRouter provides 99.9% uptime with fallbacks!",
    "🎮 Full RCON integration for complete server control!",
]

# Tips for users
TIPS = [
    f"{Fore.YELLOW}💡 TIP:{Style.RESET_ALL} Use arrow keys to navigate command history",
    f"{Fore.YELLOW}💡 TIP:{Style.RESET_ALL} Start commands with @ai for AI assistance",
    f"{Fore.YELLOW}💡 TIP:{Style.RESET_ALL} Type /status to see live system statistics",
    f"{Fore.YELLOW}💡 TIP:{Style.RESET_ALL} Cache hits are instant - try asking the same question twice!",
    f"{Fore.YELLOW}💡 TIP:{Style.RESET_ALL} Use @project to control git, builds, and Docker",
    f"{Fore.YELLOW}💡 TIP:{Style.RESET_ALL} All Minecraft commands work with / prefix",
    f"{Fore.YELLOW}💡 TIP:{Style.RESET_ALL} Type /help to see all available commands",
]

def get_random_fact():
    """Get a random fun fact"""
    import random
    return random.choice(FACTS)

def get_random_tip():
    """Get a random tip"""
    import random
    return random.choice(TIPS)

def print_logo(compact=False):
    """Print the logo"""
    if compact:
        print(LOGO_COMPACT)
    else:
        print(LOGO)

def print_server_info():
    """Print server information"""
    print(SERVER_BIO)

def print_features():
    """Print feature highlights"""
    print(FEATURES)

def print_banner():
    """Print animated banner"""
    for line in BANNER_LINES:
        print(line)

def print_startup_screen():
    """Print complete startup screen"""
    print("\n")
    print_logo()
    print()
    print_server_info()
    print()
    print_features()
    print()
    print(get_random_tip())
    print()

# Decorative separators
SEPARATOR_HEAVY = f"{Fore.CYAN}{'═' * 70}{Style.RESET_ALL}"
SEPARATOR_LIGHT = f"{Fore.CYAN}{'─' * 70}{Style.RESET_ALL}"
SEPARATOR_DOUBLE = f"{Fore.CYAN}{'═' * 70}\n{'═' * 70}{Style.RESET_ALL}"

