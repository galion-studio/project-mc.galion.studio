"""
GALION Platform Build System
Comprehensive build orchestration for all components
"""

import subprocess
import sys
import shutil
from pathlib import Path
from typing import List, Tuple, Optional
import time


class GalionBuilder:
    """
    Comprehensive build system for GALION platform.
    Handles console, launcher, mods, and server components.
    """
    
    def __init__(self, project_root: Optional[Path] = None):
        """Initialize builder"""
        self.project_root = project_root or Path(__file__).parent
        self.python_cmd = self._detect_python()
        self.gradle_cmd = self._detect_gradle()
        
        # Build results
        self.results = {
            "console": {"status": "pending", "time": 0},
            "launcher": {"status": "pending", "time": 0},
            "gradle": {"status": "pending", "time": 0},
            "deploy": {"status": "pending", "time": 0}
        }
    
    def _detect_python(self) -> str:
        """Detect Python command"""
        for cmd in ['py', 'python', 'python3']:
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
        return 'python'
    
    def _detect_gradle(self) -> Optional[str]:
        """Detect Gradle command"""
        # Check for wrapper first
        if (self.project_root / "gradlew.bat").exists():
            return str(self.project_root / "gradlew.bat")
        elif (self.project_root / "gradlew").exists():
            return str(self.project_root / "gradlew")
        
        # Check system gradle
        try:
            result = subprocess.run(
                ['gradle', '--version'],
                capture_output=True,
                timeout=2
            )
            if result.returncode == 0:
                return 'gradle'
        except:
            pass
        
        return None
    
    def build_all(self, clean: bool = False, deploy: bool = True) -> bool:
        """
        Build all components.
        
        Args:
            clean: Clean before building
            deploy: Auto-deploy artifacts
            
        Returns:
            True if all builds succeeded
        """
        print("\n" + "="*60)
        print("  GALION PLATFORM - COMPREHENSIVE BUILD")
        print("="*60 + "\n")
        
        all_success = True
        
        # Build console
        print("[1/4] Building Developer Console...")
        success, build_time = self.build_console()
        self.results["console"] = {"status": "success" if success else "failed", "time": build_time}
        if not success:
            all_success = False
        print()
        
        # Build launcher
        print("[2/4] Building Client Launcher...")
        success, build_time = self.build_launcher()
        self.results["launcher"] = {"status": "success" if success else "failed", "time": build_time}
        if not success:
            all_success = False
        print()
        
        # Build Gradle modules
        if self.gradle_cmd:
            print("[3/4] Building Gradle Modules...")
            success, build_time = self.build_gradle(clean)
            self.results["gradle"] = {"status": "success" if success else "failed", "time": build_time}
            if not success:
                all_success = False
        else:
            print("[3/4] Skipping Gradle (not available)")
            self.results["gradle"] = {"status": "skipped", "time": 0}
        print()
        
        # Deploy artifacts
        if deploy and all_success:
            print("[4/4] Deploying Artifacts...")
            success, build_time = self.deploy_artifacts()
            self.results["deploy"] = {"status": "success" if success else "failed", "time": build_time}
        else:
            print("[4/4] Skipping Deployment")
            self.results["deploy"] = {"status": "skipped", "time": 0}
        print()
        
        # Print summary
        self.print_summary()
        
        return all_success
    
    def build_console(self) -> Tuple[bool, float]:
        """Build developer console"""
        start = time.time()
        
        try:
            console_dir = self.project_root / "dev-console"
            requirements = console_dir / "requirements-dev-console.txt"
            
            if requirements.exists():
                result = subprocess.run(
                    [self.python_cmd, '-m', 'pip', 'install', '-r', 
                     str(requirements), '--quiet'],
                    cwd=str(console_dir),
                    capture_output=True
                )
                
                if result.returncode != 0:
                    print(f"   [!] Failed: {result.stderr.decode()}")
                    return False, time.time() - start
            
            print("   [OK] Developer Console built successfully")
            return True, time.time() - start
        
        except Exception as e:
            print(f"   [ERROR] {e}")
            return False, time.time() - start
    
    def build_launcher(self) -> Tuple[bool, float]:
        """Build client launcher"""
        start = time.time()
        
        try:
            launcher_dir = self.project_root / "client-launcher"
            requirements = launcher_dir / "requirements.txt"
            
            if requirements.exists():
                result = subprocess.run(
                    [self.python_cmd, '-m', 'pip', 'install', '-r',
                     str(requirements), '--quiet'],
                    cwd=str(launcher_dir),
                    capture_output=True
                )
                
                if result.returncode != 0:
                    print(f"   [!] Failed: {result.stderr.decode()}")
                    return False, time.time() - start
            
            print("   [OK] Client Launcher built successfully")
            return True, time.time() - start
        
        except Exception as e:
            print(f"   [ERROR] {e}")
            return False, time.time() - start
    
    def build_gradle(self, clean: bool = False) -> Tuple[bool, float]:
        """Build Gradle modules"""
        start = time.time()
        
        try:
            # Clean if requested
            if clean:
                print("   Cleaning...")
                result = subprocess.run(
                    [self.gradle_cmd, 'cleanAll'],
                    cwd=str(self.project_root),
                    capture_output=True
                )
            
            # Build
            print("   Building modules...")
            result = subprocess.run(
                [self.gradle_cmd, 'buildAll', '--console=plain'],
                cwd=str(self.project_root),
                capture_output=False  # Show output
            )
            
            if result.returncode != 0:
                print(f"   [!] Build failed")
                return False, time.time() - start
            
            print("   [OK] Gradle modules built successfully")
            return True, time.time() - start
        
        except Exception as e:
            print(f"   [ERROR] {e}")
            return False, time.time() - start
    
    def deploy_artifacts(self) -> Tuple[bool, float]:
        """Deploy built artifacts"""
        start = time.time()
        
        try:
            deployed_count = 0
            
            # Copy JARs from build/libs to server-mods
            build_libs = self.project_root / "build" / "libs"
            server_mods = self.project_root / "server-mods"
            
            if build_libs.exists():
                server_mods.mkdir(exist_ok=True)
                
                for jar_file in build_libs.glob("*.jar"):
                    # Skip sources and javadoc
                    if "sources" in jar_file.name.lower() or "javadoc" in jar_file.name.lower():
                        continue
                    
                    dest = server_mods / jar_file.name
                    shutil.copy2(jar_file, dest)
                    deployed_count += 1
                    print(f"   [OK] Deployed: {jar_file.name}")
            
            # Check subproject builds
            for subproject in self.project_root.glob("titan-*"):
                subproject_libs = subproject / "build" / "libs"
                if subproject_libs.exists():
                    for jar_file in subproject_libs.glob("*.jar"):
                        if "sources" not in jar_file.name.lower() and "javadoc" not in jar_file.name.lower():
                            dest = server_mods / jar_file.name
                            shutil.copy2(jar_file, dest)
                            deployed_count += 1
                            print(f"   [OK] Deployed: {jar_file.name}")
            
            if deployed_count > 0:
                print(f"   [OK] Deployed {deployed_count} artifacts")
                return True, time.time() - start
            else:
                print("   [!] No artifacts to deploy")
                return True, time.time() - start
        
        except Exception as e:
            print(f"   [ERROR] {e}")
            return False, time.time() - start
    
    def print_summary(self):
        """Print build summary"""
        print("\n" + "="*60)
        print("  BUILD SUMMARY")
        print("="*60)
        
        total_time = sum(r["time"] for r in self.results.values())
        success_count = sum(1 for r in self.results.values() if r["status"] == "success")
        total_count = len([r for r in self.results.values() if r["status"] != "skipped"])
        
        for component, result in self.results.items():
            status = result["status"]
            build_time = result["time"]
            
            if status == "success":
                icon = "[OK]"
                color_status = "SUCCESS"
            elif status == "failed":
                icon = "[!!]"
                color_status = "FAILED"
            else:
                icon = "[--]"
                color_status = "SKIPPED"
            
            print(f"  {icon} {component.capitalize()}: {color_status} ({build_time:.1f}s)")
        
        print()
        print(f"  Total Time: {total_time:.1f}s")
        print(f"  Success Rate: {success_count}/{total_count}")
        print("="*60)
        
        if success_count == total_count:
            print("\n  === ALL BUILDS SUCCESSFUL! ===")
            print("\n  Ready to launch: py dev-console/console_main.py")
        else:
            print("\n  === SOME BUILDS FAILED ===")
            print("  Check output above for errors")
        
        print()


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="GALION Platform Build System")
    parser.add_argument('--clean', action='store_true', help='Clean before building')
    parser.add_argument('--no-deploy', action='store_true', help='Skip artifact deployment')
    parser.add_argument('--console-only', action='store_true', help='Build console only')
    parser.add_argument('--launcher-only', action='store_true', help='Build launcher only')
    parser.add_argument('--gradle-only', action='store_true', help='Build Gradle modules only')
    
    args = parser.parse_args()
    
    builder = GalionBuilder()
    
    if args.console_only:
        success, build_time = builder.build_console()
        sys.exit(0 if success else 1)
    elif args.launcher_only:
        success, build_time = builder.build_launcher()
        sys.exit(0 if success else 1)
    elif args.gradle_only:
        if builder.gradle_cmd:
            success, build_time = builder.build_gradle(args.clean)
            sys.exit(0 if success else 1)
        else:
            print("Error: Gradle not available")
            sys.exit(1)
    else:
        # Build all
        success = builder.build_all(clean=args.clean, deploy=not args.no_deploy)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

