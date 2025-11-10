"""
Build Script for Galion Studio Launcher
This script helps create standalone executables for Windows and Linux
"""

import os
import sys
import platform
import subprocess


def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False


def install_pyinstaller():
    """Install PyInstaller using pip"""
    print("Installing PyInstaller...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install PyInstaller")
        return False


def build_executable():
    """Build the standalone executable"""
    
    print("\n" + "="*50)
    print("Galion Studio Launcher - Build Script")
    print("="*50 + "\n")
    
    # Check if PyInstaller is installed
    if not check_pyinstaller():
        print("PyInstaller is not installed.")
        response = input("Do you want to install it now? (y/n): ")
        
        if response.lower() == 'y':
            if not install_pyinstaller():
                print("\nBuild failed. Please install PyInstaller manually:")
                print(f"  {sys.executable} -m pip install pyinstaller")
                return False
        else:
            print("\nBuild cancelled. PyInstaller is required to build executables.")
            return False
    
    # Build command
    system = platform.system()
    launcher_name = "GalionLauncher"
    
    print(f"\nBuilding for {system}...")
    print("This may take a few minutes...\n")
    
    # PyInstaller command
    command = [
        "pyinstaller",
        "--onefile",           # Single executable file
        "--windowed",          # No console window (GUI only)
        "--name", launcher_name,
        "launcher.py"
    ]
    
    try:
        # Run PyInstaller
        subprocess.check_call(command)
        
        print("\n" + "="*50)
        print("✓ Build completed successfully!")
        print("="*50 + "\n")
        
        # Show output location
        if system == "Windows":
            exe_path = os.path.join("dist", f"{launcher_name}.exe")
            print(f"Executable created at: {exe_path}")
            print(f"\nYou can now distribute '{launcher_name}.exe' to your users!")
        else:
            exe_path = os.path.join("dist", launcher_name)
            print(f"Executable created at: {exe_path}")
            print(f"\nYou can now distribute '{launcher_name}' to your users!")
            print("\nNote: Make sure to set execute permissions:")
            print(f"  chmod +x {exe_path}")
        
        return True
        
    except subprocess.CalledProcessError:
        print("\n✗ Build failed!")
        print("Check the output above for error details.")
        return False
    except Exception as e:
        print(f"\n✗ Build failed with error: {e}")
        return False


def clean_build_files():
    """Clean up build artifacts"""
    import shutil
    
    print("\nCleaning up build files...")
    
    dirs_to_remove = ["build", "__pycache__"]
    files_to_remove = ["GalionLauncher.spec"]
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  Removed: {dir_name}/")
    
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"  Removed: {file_name}")
    
    print("✓ Cleanup complete")


def main():
    """Main build function"""
    
    # Check if we're in the right directory
    if not os.path.exists("launcher.py"):
        print("Error: launcher.py not found!")
        print("Please run this script from the client-launcher directory.")
        sys.exit(1)
    
    # Build the executable
    success = build_executable()
    
    if success:
        # Ask if user wants to clean up build files
        response = input("\nDo you want to clean up build files? (y/n): ")
        if response.lower() == 'y':
            clean_build_files()
        
        print("\n✓ All done!")
    else:
        print("\nBuild process failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()

