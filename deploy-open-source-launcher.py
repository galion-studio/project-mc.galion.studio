"""
Quick Deployment Script for Open Source Minecraft Launchers
This script helps you choose and deploy an open-source launcher for your server
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


SERVER_ADDRESS = "mc.galion.studio"
SERVER_NAME = "Galion Studio"


def print_header():
    """Print header"""
    print("=" * 60)
    print("GALION STUDIO - OPEN SOURCE LAUNCHER DEPLOYMENT")
    print("=" * 60)
    print()


def print_menu():
    """Display launcher options"""
    print("Choose your launcher deployment option:\n")
    print("1. Prism Launcher (RECOMMENDED)")
    print("   - Most popular and feature-rich")
    print("   - Cross-platform (Windows, Linux, macOS)")
    print("   - Full mod support")
    print("   - Easy to pre-configure\n")
    
    print("2. MultiMC (Original)")
    print("   - Very stable and reliable")
    print("   - Simple interface")
    print("   - Good for basic setups\n")
    
    print("3. OpenLauncher (Python - Easy to customize)")
    print("   - Lightweight Python launcher")
    print("   - Simple to modify")
    print("   - Good for learning\n")
    
    print("4. Keep our custom launcher")
    print("   - Use the Python launcher we already built")
    print("   - Simple and focused\n")
    
    print("5. Show download links only")
    print("   - Get links to download launchers\n")
    
    print("0. Exit\n")


def open_url(url):
    """Open URL in default browser"""
    system = platform.system()
    try:
        if system == "Windows":
            os.startfile(url)
        elif system == "Darwin":  # macOS
            subprocess.Popen(["open", url])
        else:  # Linux
            subprocess.Popen(["xdg-open", url])
        print(f"✓ Opened: {url}")
    except Exception as e:
        print(f"Please visit: {url}")


def deploy_prism_launcher():
    """Deploy Prism Launcher"""
    print("\n" + "=" * 60)
    print("DEPLOYING: PRISM LAUNCHER")
    print("=" * 60 + "\n")
    
    print("Prism Launcher is the BEST choice for your server!\n")
    
    print("STEP 1: Download Prism Launcher")
    print("-" * 60)
    print("Opening download page...")
    open_url("https://prismlauncher.org/download/")
    print("\nDownload and install Prism Launcher for your system.\n")
    
    input("Press Enter after installing Prism Launcher...")
    
    print("\nSTEP 2: Create Pre-configured Instance")
    print("-" * 60)
    print("""
    1. Open Prism Launcher
    2. Click "Add Instance"
    3. Choose your Minecraft version
    4. Name it "Galion Studio Server"
    5. Click "OK"
    6. Launch the instance
    7. Go to Multiplayer
    8. Add Server:
       - Name: Galion Studio
       - Address: mc.galion.studio
    9. Exit Minecraft
    """)
    
    input("Press Enter after configuring the instance...")
    
    print("\nSTEP 3: Export Instance for Distribution")
    print("-" * 60)
    print("""
    1. Right-click on "Galion Studio Server" instance
    2. Choose "Export Instance"
    3. Select format (CurseForge recommended)
    4. Save as "GalionStudio-Instance.zip"
    5. Upload this ZIP to your website/Discord
    """)
    
    print("\nSTEP 4: Share with Players")
    print("-" * 60)
    print("""
    Create a guide for your players:
    
    =====================================
    GALION STUDIO - QUICK CONNECT
    =====================================
    
    1. Download Prism Launcher:
       https://prismlauncher.org/download/
    
    2. Download our server instance:
       [Your hosted GalionStudio-Instance.zip]
    
    3. In Prism Launcher:
       - Click "Add Instance"
       - Choose "Import from zip"
       - Select GalionStudio-Instance.zip
    
    4. Click "Launch" - You're ready!
       Server is pre-configured!
    =====================================
    """)
    
    print("\n✓ Prism Launcher deployment complete!")
    print("Upload your instance ZIP and share the guide with players.\n")


def deploy_multimc():
    """Deploy MultiMC"""
    print("\n" + "=" * 60)
    print("DEPLOYING: MULTIMC")
    print("=" * 60 + "\n")
    
    print("Opening MultiMC download page...")
    open_url("https://multimc.org/#Download")
    
    print("""
    MultiMC Setup:
    1. Download and install MultiMC
    2. Create instance with desired Minecraft version
    3. Configure server (same steps as Prism Launcher)
    4. Export and distribute to players
    
    Note: MultiMC has similar features to Prism Launcher
    """)


def deploy_openlauncher():
    """Deploy OpenLauncher"""
    print("\n" + "=" * 60)
    print("DEPLOYING: OPENLAUNCHER (Python)")
    print("=" * 60 + "\n")
    
    print("Cloning OpenLauncher repository...\n")
    
    try:
        subprocess.run([
            "git", "clone",
            "https://github.com/CesarGarza55/OpenLauncher.git",
            "open-launcher"
        ], check=True)
        
        print("\n✓ Repository cloned to: open-launcher/\n")
        print("Next steps:")
        print("-" * 60)
        print("""
        1. cd open-launcher
        2. pip install -r requirements.txt
        3. Customize the launcher for your server
        4. Run: python main.py
        
        To customize for mc.galion.studio:
        - Edit configuration files
        - Add your server details
        - Modify branding
        """)
    except subprocess.CalledProcessError:
        print("Error: Git not found or clone failed")
        print("\nManual steps:")
        print("1. Visit: https://github.com/CesarGarza55/OpenLauncher")
        print("2. Download ZIP")
        print("3. Extract and follow README")
    except FileExistsError:
        print("✓ OpenLauncher already exists in 'open-launcher/' directory")


def show_downloads():
    """Show download links"""
    print("\n" + "=" * 60)
    print("DOWNLOAD LINKS")
    print("=" * 60 + "\n")
    
    links = {
        "Prism Launcher (Recommended)": "https://prismlauncher.org/download/",
        "MultiMC": "https://multimc.org/#Download",
        "ATLauncher": "https://atlauncher.com/downloads",
        "GDLauncher": "https://gdlauncher.com/",
        "OpenLauncher (GitHub)": "https://github.com/CesarGarza55/OpenLauncher"
    }
    
    for name, url in links.items():
        print(f"• {name}")
        print(f"  {url}\n")


def keep_custom_launcher():
    """Info about keeping custom launcher"""
    print("\n" + "=" * 60)
    print("KEEPING CUSTOM PYTHON LAUNCHER")
    print("=" * 60 + "\n")
    
    print("Your custom launcher is ready in: client-launcher/\n")
    print("Distribution package: GalionLauncher-Windows-v1.0.0.zip\n")
    print("Advantages:")
    print("✓ Already built and working")
    print("✓ Fully customized for your server")
    print("✓ Simple and lightweight (10.5 MB)")
    print("✓ No additional setup needed\n")
    
    print("Just upload and distribute GalionLauncher-Windows-v1.0.0.zip!\n")


def main():
    """Main function"""
    print_header()
    
    while True:
        print_menu()
        
        try:
            choice = input("Enter your choice (0-5): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nExiting...")
            sys.exit(0)
        
        if choice == "1":
            deploy_prism_launcher()
            break
        elif choice == "2":
            deploy_multimc()
            break
        elif choice == "3":
            deploy_openlauncher()
            break
        elif choice == "4":
            keep_custom_launcher()
            break
        elif choice == "5":
            show_downloads()
        elif choice == "0":
            print("\nExiting. Good luck with your server!")
            sys.exit(0)
        else:
            print("\n❌ Invalid choice. Please try again.\n")
    
    print("\n" + "=" * 60)
    print("DEPLOYMENT GUIDE COMPLETE")
    print("=" * 60)
    print(f"\nYour server: {SERVER_ADDRESS}")
    print("Need help? Check OPEN-SOURCE-LAUNCHER-GUIDE.md\n")


if __name__ == "__main__":
    main()

