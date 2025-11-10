"""
Terminal Configuration Viewer
Simple command-line alternative to the GUI console
Perfect for SSH sessions or quick checks

Features:
- View all configuration
- Copy-friendly output
- No GUI required
- Fast and lightweight
"""

import sys
from pathlib import Path
from colorama import init, Fore, Style

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from config_manager import ConfigManager

# Initialize colorama for Windows
init(autoreset=True)


def print_header():
    """Print welcome header"""
    print(f"\n{Fore.CYAN}{'=' * 70}")
    print(f"{Fore.GREEN}  🔧 TERMINAL CONFIGURATION VIEWER")
    print(f"{Fore.CYAN}  Full Transparency - All Settings Visible")
    print(f"{Fore.CYAN}  mc.galion.studio")
    print(f"{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}\n")


def print_menu():
    """Print main menu"""
    print(f"\n{Fore.YELLOW}MENU:{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}1.{Style.RESET_ALL} View All Configuration")
    print(f"  {Fore.WHITE}2.{Style.RESET_ALL} View Configuration (Masked Secrets)")
    print(f"  {Fore.WHITE}3.{Style.RESET_ALL} View AI Configuration")
    print(f"  {Fore.WHITE}4.{Style.RESET_ALL} View Minecraft Configuration")
    print(f"  {Fore.WHITE}5.{Style.RESET_ALL} View Database Configuration")
    print(f"  {Fore.WHITE}6.{Style.RESET_ALL} View Network/VPN Configuration")
    print(f"  {Fore.WHITE}7.{Style.RESET_ALL} Validate Configuration")
    print(f"  {Fore.WHITE}8.{Style.RESET_ALL} Export Full Configuration")
    print(f"  {Fore.WHITE}9.{Style.RESET_ALL} Quick Setup Guide")
    print(f"  {Fore.WHITE}0.{Style.RESET_ALL} Exit")
    print()


def view_full_config(manager: ConfigManager):
    """View full configuration with all secrets"""
    print(f"\n{Fore.RED}⚠️  WARNING: This shows all secrets!{Style.RESET_ALL}")
    print(manager.export_config_full())


def view_masked_config(manager: ConfigManager):
    """View configuration with masked secrets"""
    print(f"\n{Fore.GREEN}✅ Safe to share (secrets masked){Style.RESET_ALL}")
    print(manager.export_config_text())


def view_category(manager: ConfigManager, category: str, title: str):
    """View specific configuration category"""
    print(f"\n{Fore.CYAN}{'=' * 70}")
    print(f"{Fore.GREEN}  {title}")
    print(f"{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}\n")
    
    config = manager.get_config_category(category)
    
    if not config:
        print(f"{Fore.RED}No configuration found for this category{Style.RESET_ALL}")
        return
    
    # Display as table
    for key, value in config.items():
        # Check if it's a secret
        is_secret = any(keyword in key.lower() 
                       for keyword in ['password', 'secret', 'key'])
        
        # Format output
        if is_secret and value:
            if len(value) > 12:
                display_value = f"{value[:4]}...{value[-4:]}"
            else:
                display_value = "***"
            print(f"{Fore.YELLOW}{key:30s}{Style.RESET_ALL} = {display_value}")
        else:
            print(f"{Fore.WHITE}{key:30s}{Style.RESET_ALL} = {value}")
    
    print()


def validate_config(manager: ConfigManager):
    """Validate configuration and show issues"""
    print(f"\n{Fore.CYAN}{'=' * 70}")
    print(f"{Fore.GREEN}  CONFIGURATION VALIDATION")
    print(f"{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}\n")
    
    issues = manager.validate_config()
    
    # Missing values
    if issues["missing"]:
        print(f"{Fore.RED}❌ MISSING (REQUIRED):{Style.RESET_ALL}")
        for issue in issues["missing"]:
            print(f"  {Fore.RED}•{Style.RESET_ALL} {issue}")
        print()
    else:
        print(f"{Fore.GREEN}✅ All required values present{Style.RESET_ALL}\n")
    
    # Warnings
    if issues["warnings"]:
        print(f"{Fore.YELLOW}⚠️  WARNINGS:{Style.RESET_ALL}")
        for issue in issues["warnings"]:
            print(f"  {Fore.YELLOW}•{Style.RESET_ALL} {issue}")
        print()
    else:
        print(f"{Fore.GREEN}✅ No warnings{Style.RESET_ALL}\n")
    
    # Summary
    if not issues["missing"] and not issues["warnings"]:
        print(f"{Fore.GREEN}🎉 Configuration is valid!{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.YELLOW}💡 Fix these issues for full functionality{Style.RESET_ALL}\n")


def export_config(manager: ConfigManager):
    """Export full configuration to file"""
    output_file = Path.cwd() / "CONFIG_EXPORT_TERMINAL.txt"
    
    try:
        config_text = manager.export_config_full()
        output_file.write_text(config_text, encoding='utf-8')
        
        print(f"\n{Fore.GREEN}✅ Configuration exported!{Style.RESET_ALL}")
        print(f"   File: {output_file}")
        print(f"{Fore.RED}⚠️  WARNING: Contains secrets - keep secure!{Style.RESET_ALL}\n")
    
    except Exception as e:
        print(f"\n{Fore.RED}❌ Export failed: {e}{Style.RESET_ALL}\n")


def show_quick_setup():
    """Show quick setup guide"""
    print(f"\n{Fore.CYAN}{'=' * 70}")
    print(f"{Fore.GREEN}  QUICK SETUP GUIDE")
    print(f"{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}\n")
    
    print(f"{Fore.YELLOW}Step 1: Get OpenRouter API Key{Style.RESET_ALL}")
    print(f"  1. Go to https://openrouter.ai/")
    print(f"  2. Sign up for free account")
    print(f"  3. Go to https://openrouter.ai/keys")
    print(f"  4. Create new API key")
    print(f"  5. Copy your key\n")
    
    print(f"{Fore.YELLOW}Step 2: Add to Configuration{Style.RESET_ALL}")
    print(f"  1. Open .env.grok file")
    print(f"  2. Find: OPENROUTER_API_KEY=")
    print(f"  3. Paste your key after the =")
    print(f"  4. Save file\n")
    
    print(f"{Fore.YELLOW}Step 3: Set Passwords (Optional but Recommended){Style.RESET_ALL}")
    print(f"  Edit .env file:")
    print(f"  • POSTGRES_PASSWORD - Database password")
    print(f"  • REDIS_PASSWORD - Cache password")
    print(f"  • VELOCITY_SECRET - Proxy security key")
    print(f"  • MINECRAFT_RCON_PASSWORD - Server control password\n")
    
    print(f"{Fore.YELLOW}Step 4: Launch Console{Style.RESET_ALL}")
    print(f"  Double-click: START-TRANSPARENT-CONSOLE.cmd")
    print(f"  Or run: python dev-console/transparent_console.py\n")
    
    print(f"{Fore.GREEN}✅ That's it! You're ready to go!{Style.RESET_ALL}\n")


def main():
    """Main program loop"""
    
    # Print header
    print_header()
    
    # Initialize configuration manager
    try:
        manager = ConfigManager()
        print(f"{Fore.GREEN}✅ Configuration loaded successfully{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Error loading configuration: {e}{Style.RESET_ALL}")
        return
    
    # Main loop
    while True:
        print_menu()
        
        try:
            choice = input(f"{Fore.CYAN}Select option (0-9): {Style.RESET_ALL}").strip()
            
            if choice == "1":
                view_full_config(manager)
            
            elif choice == "2":
                view_masked_config(manager)
            
            elif choice == "3":
                view_category(manager, "ai", "AI CONFIGURATION")
            
            elif choice == "4":
                view_category(manager, "minecraft", "MINECRAFT CONFIGURATION")
            
            elif choice == "5":
                view_category(manager, "database", "DATABASE CONFIGURATION")
            
            elif choice == "6":
                view_category(manager, "network", "NETWORK/VPN CONFIGURATION")
            
            elif choice == "7":
                validate_config(manager)
            
            elif choice == "8":
                export_config(manager)
            
            elif choice == "9":
                show_quick_setup()
            
            elif choice == "0":
                print(f"\n{Fore.GREEN}Goodbye!{Style.RESET_ALL}\n")
                break
            
            else:
                print(f"\n{Fore.RED}Invalid option. Please choose 0-9.{Style.RESET_ALL}")
        
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Interrupted. Use option 0 to exit.{Style.RESET_ALL}\n")
        
        except Exception as e:
            print(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()

