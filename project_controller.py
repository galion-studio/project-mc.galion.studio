#!/usr/bin/env python3
"""
Project Controller for Cursor mc.galion.studio
Execute project-level operations from the console

Features:
- Git operations (status, commit, push, pull)
- Build commands (gradle, npm)
- File operations (read, write, list)
- Script execution
- Project automation
"""

import asyncio
import subprocess
import os
from typing import Optional, List, Dict
from pathlib import Path
import json


class ProjectController:
    """
    Controller for Cursor project operations
    Allows console chat to control the development project
    
    Usage:
        controller = ProjectController(project_root="C:/path/to/project")
        await controller.git_status()
    """
    
    def __init__(self, project_root: str):
        """
        Initialize project controller
        
        Args:
            project_root: Path to project root directory
        """
        self.project_root = Path(project_root)
        
        # Validate project exists
        if not self.project_root.exists():
            raise ValueError(f"Project root does not exist: {project_root}")
        
        # Statistics
        self.stats = {
            "total_commands": 0,
            "successful_commands": 0,
            "failed_commands": 0
        }
    
    async def _execute_command(
        self,
        command: List[str],
        cwd: Optional[Path] = None,
        timeout: int = 30
    ) -> Dict[str, any]:
        """
        Execute shell command safely
        
        Args:
            command: Command and arguments as list
            cwd: Working directory (defaults to project_root)
            timeout: Command timeout in seconds
        
        Returns:
            Dict with stdout, stderr, returncode
        """
        if cwd is None:
            cwd = self.project_root
        
        try:
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(cwd)
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout
            )
            
            self.stats["total_commands"] += 1
            if process.returncode == 0:
                self.stats["successful_commands"] += 1
            else:
                self.stats["failed_commands"] += 1
            
            return {
                "stdout": stdout.decode().strip(),
                "stderr": stderr.decode().strip(),
                "returncode": process.returncode,
                "success": process.returncode == 0
            }
            
        except asyncio.TimeoutError:
            process.kill()
            self.stats["failed_commands"] += 1
            return {
                "stdout": "",
                "stderr": f"Command timeout (>{timeout}s)",
                "returncode": -1,
                "success": False
            }
        except Exception as e:
            self.stats["failed_commands"] += 1
            return {
                "stdout": "",
                "stderr": str(e),
                "returncode": -1,
                "success": False
            }
    
    # ========================================
    # GIT OPERATIONS
    # ========================================
    
    async def git_status(self) -> str:
        """Get git status"""
        result = await self._execute_command(["git", "status", "--short"])
        if result["success"]:
            return result["stdout"] if result["stdout"] else "Working tree clean"
        return f"Error: {result['stderr']}"
    
    async def git_log(self, limit: int = 5) -> str:
        """Get recent git commits"""
        result = await self._execute_command([
            "git", "log",
            f"-{limit}",
            "--oneline"
        ])
        return result["stdout"] if result["success"] else f"Error: {result['stderr']}"
    
    async def git_diff(self) -> str:
        """Get git diff"""
        result = await self._execute_command(["git", "diff", "--stat"])
        return result["stdout"] if result["success"] else f"Error: {result['stderr']}"
    
    async def git_add(self, files: str = ".") -> str:
        """Stage files for commit"""
        result = await self._execute_command(["git", "add", files])
        return "Files staged" if result["success"] else f"Error: {result['stderr']}"
    
    async def git_commit(self, message: str) -> str:
        """Commit staged changes"""
        result = await self._execute_command(["git", "commit", "-m", message])
        return result["stdout"] if result["success"] else f"Error: {result['stderr']}"
    
    async def git_push(self) -> str:
        """Push commits to remote"""
        result = await self._execute_command(["git", "push"], timeout=60)
        return "Pushed successfully" if result["success"] else f"Error: {result['stderr']}"
    
    async def git_pull(self) -> str:
        """Pull from remote"""
        result = await self._execute_command(["git", "pull"], timeout=60)
        return result["stdout"] if result["success"] else f"Error: {result['stderr']}"
    
    # ========================================
    # BUILD OPERATIONS
    # ========================================
    
    async def gradle_build(self) -> str:
        """Run gradle build"""
        result = await self._execute_command(
            ["gradlew.bat", "build"] if os.name == 'nt' else ["./gradlew", "build"],
            timeout=300  # 5 minutes for build
        )
        if result["success"]:
            return "Build successful"
        return f"Build failed: {result['stderr']}"
    
    async def gradle_clean(self) -> str:
        """Clean gradle build"""
        result = await self._execute_command(
            ["gradlew.bat", "clean"] if os.name == 'nt' else ["./gradlew", "clean"],
            timeout=60
        )
        return "Cleaned" if result["success"] else f"Error: {result['stderr']}"
    
    async def gradle_tasks(self) -> str:
        """List available gradle tasks"""
        result = await self._execute_command(
            ["gradlew.bat", "tasks"] if os.name == 'nt' else ["./gradlew", "tasks"],
            timeout=30
        )
        return result["stdout"] if result["success"] else f"Error: {result['stderr']}"
    
    # ========================================
    # FILE OPERATIONS
    # ========================================
    
    async def list_files(self, directory: str = ".") -> List[str]:
        """List files in directory"""
        try:
            path = self.project_root / directory
            if not path.exists():
                return [f"Directory not found: {directory}"]
            
            files = []
            for item in path.iterdir():
                prefix = "[D]" if item.is_dir() else "[F]"
                files.append(f"{prefix} {item.name}")
            
            return sorted(files)
        except Exception as e:
            return [f"Error: {str(e)}"]
    
    async def read_file(self, filepath: str, max_lines: int = 50) -> str:
        """
        Read file contents
        
        Args:
            filepath: Relative path to file
            max_lines: Maximum lines to return
        
        Returns:
            File contents (truncated if needed)
        """
        try:
            full_path = self.project_root / filepath
            
            if not full_path.exists():
                return f"File not found: {filepath}"
            
            with open(full_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if len(lines) > max_lines:
                content = ''.join(lines[:max_lines])
                content += f"\n... ({len(lines) - max_lines} more lines)"
            else:
                content = ''.join(lines)
            
            return content
            
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    async def write_file(self, filepath: str, content: str) -> str:
        """
        Write content to file
        
        Args:
            filepath: Relative path to file
            content: Content to write
        
        Returns:
            Success message or error
        """
        try:
            full_path = self.project_root / filepath
            
            # Create parent directories if needed
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"File written: {filepath}"
            
        except Exception as e:
            return f"Error writing file: {str(e)}"
    
    async def file_exists(self, filepath: str) -> bool:
        """Check if file exists"""
        full_path = self.project_root / filepath
        return full_path.exists()
    
    # ========================================
    # SCRIPT EXECUTION
    # ========================================
    
    async def run_script(self, script_path: str, args: List[str] = None) -> str:
        """
        Run a script from the project
        
        Args:
            script_path: Path to script
            args: Script arguments
        
        Returns:
            Script output
        """
        if args is None:
            args = []
        
        full_path = self.project_root / script_path
        
        if not full_path.exists():
            return f"Script not found: {script_path}"
        
        # Determine how to run the script
        if script_path.endswith('.py'):
            command = ["python", str(full_path)] + args
        elif script_path.endswith('.sh'):
            command = ["bash", str(full_path)] + args
        elif script_path.endswith('.ps1'):
            command = ["powershell", "-File", str(full_path)] + args
        elif script_path.endswith('.cmd') or script_path.endswith('.bat'):
            command = [str(full_path)] + args
        else:
            return f"Unknown script type: {script_path}"
        
        result = await self._execute_command(command, timeout=120)
        
        if result["success"]:
            return result["stdout"]
        return f"Script failed:\n{result['stderr']}"
    
    # ========================================
    # DOCKER OPERATIONS
    # ========================================
    
    async def docker_ps(self) -> str:
        """List running Docker containers"""
        result = await self._execute_command(["docker", "ps", "--format", "table {{.Names}}\t{{.Status}}"])
        return result["stdout"] if result["success"] else f"Error: {result['stderr']}"
    
    async def docker_logs(self, container: str, lines: int = 20) -> str:
        """Get container logs"""
        result = await self._execute_command([
            "docker", "logs", "--tail", str(lines), container
        ])
        return result["stdout"] if result["success"] else f"Error: {result['stderr']}"
    
    async def docker_restart(self, container: str) -> str:
        """Restart Docker container"""
        result = await self._execute_command(["docker", "restart", container], timeout=60)
        return f"Restarted {container}" if result["success"] else f"Error: {result['stderr']}"
    
    # ========================================
    # PROJECT INFO
    # ========================================
    
    async def get_project_info(self) -> Dict:
        """Get project information"""
        info = {
            "root": str(self.project_root),
            "exists": self.project_root.exists(),
            "is_git": (self.project_root / ".git").exists(),
            "has_gradle": (self.project_root / "build.gradle.kts").exists(),
            "has_docker": (self.project_root / "docker-compose.yml").exists()
        }
        return info
    
    def get_stats(self) -> Dict:
        """Get controller statistics"""
        return {
            **self.stats,
            "success_rate": (
                self.stats["successful_commands"] / self.stats["total_commands"]
                if self.stats["total_commands"] > 0 else 0
            )
        }


# Testing
async def test_project_controller():
    """Test project controller"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv(".env.grok")
    
    project_root = os.getenv("PROJECT_ROOT", ".")
    
    controller = ProjectController(project_root)
    
    print("=" * 60)
    print("🎯 Testing Project Controller")
    print("=" * 60)
    print(f"Project: {project_root}")
    print("=" * 60)
    print()
    
    # Test project info
    print("📊 Project Info:")
    info = await controller.get_project_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
    print()
    
    # Test git status
    print("🔧 Git Status:")
    status = await controller.git_status()
    print(f"  {status}")
    print()
    
    # Test file listing
    print("📁 Root Files:")
    files = await controller.list_files()
    for f in files[:10]:  # Show first 10
        print(f"  {f}")
    print()
    
    # Test Docker
    print("🐳 Docker Containers:")
    containers = await controller.docker_ps()
    print(f"  {containers}")
    print()
    
    # Show stats
    print("=" * 60)
    print("📊 Statistics")
    print("=" * 60)
    stats = controller.get_stats()
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"{key}: {value:.3f}")
        else:
            print(f"{key}: {value}")


if __name__ == "__main__":
    asyncio.run(test_project_controller())

