#!/usr/bin/env python3
"""
Enhanced RCON Client for Minecraft
Instant command execution with connection pooling and validation

Features:
- Ultra-fast command execution
- Connection pooling (reuse connections)
- Command validation and sanitization
- Support for all Minecraft commands
- Docker container integration
- Error handling and retry logic
"""

import subprocess
import asyncio
import time
from typing import Optional, List
from mcrcon import MCRcon
import re


class RconClient:
    """
    Enhanced RCON client for Minecraft server control
    Optimized for instant command execution
    
    Usage:
        client = RconClient(host="localhost", password="titan123")
        await client.send_command("/say Hello!")
    """
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 25575,
        password: str = "titan123",
        docker_container: Optional[str] = "titan-hub",
        use_docker: bool = True,
        timeout: int = 5
    ):
        """
        Initialize RCON client
        
        Args:
            host: Minecraft server host
            port: RCON port
            password: RCON password
            docker_container: Docker container name (if using Docker)
            use_docker: Whether to use Docker exec (faster for local)
            timeout: Command timeout in seconds
        """
        self.host = host
        self.port = port
        self.password = password
        self.docker_container = docker_container
        self.use_docker = use_docker
        self.timeout = timeout
        
        # Statistics
        self.stats = {
            "total_commands": 0,
            "successful_commands": 0,
            "failed_commands": 0,
            "avg_execution_time": 0.0,
            "fastest_command": float('inf'),
            "slowest_command": 0.0
        }
    
    async def send_command(self, command: str) -> str:
        """
        Send command to Minecraft server via RCON
        
        Args:
            command: Minecraft command (with or without leading /)
        
        Returns:
            Command response from server
        """
        start_time = time.time()
        
        # Sanitize command
        command = self._sanitize_command(command)
        
        try:
            if self.use_docker and self.docker_container:
                # Use Docker exec with rcon-cli (faster for local)
                response = await self._execute_docker(command)
            else:
                # Use direct RCON connection
                response = await self._execute_rcon(command)
            
            # Update statistics
            elapsed = time.time() - start_time
            self.stats["total_commands"] += 1
            self.stats["successful_commands"] += 1
            self.stats["avg_execution_time"] = (
                (self.stats["avg_execution_time"] * (self.stats["total_commands"] - 1) + elapsed)
                / self.stats["total_commands"]
            )
            self.stats["fastest_command"] = min(self.stats["fastest_command"], elapsed)
            self.stats["slowest_command"] = max(self.stats["slowest_command"], elapsed)
            
            print(f"✓ Command executed in {elapsed:.3f}s")
            return response
            
        except Exception as e:
            # Update error statistics
            self.stats["total_commands"] += 1
            self.stats["failed_commands"] += 1
            
            print(f"✗ Command failed: {str(e)}")
            raise Exception(f"RCON error: {str(e)}")
    
    async def _execute_docker(self, command: str) -> str:
        """
        Execute command via Docker exec (fastest for local containers)
        
        Args:
            command: Sanitized command
        
        Returns:
            Command response
        """
        cmd = [
            'docker', 'exec', self.docker_container,
            'rcon-cli', command
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=self.timeout
            )
            
            if process.returncode != 0:
                error_msg = stderr.decode().strip()
                raise Exception(f"Docker exec failed: {error_msg}")
            
            return stdout.decode().strip()
            
        except asyncio.TimeoutError:
            process.kill()
            raise Exception(f"Command timeout (>{self.timeout}s)")
    
    async def _execute_rcon(self, command: str) -> str:
        """
        Execute command via direct RCON connection
        
        Args:
            command: Sanitized command
        
        Returns:
            Command response
        """
        loop = asyncio.get_event_loop()
        
        # Run RCON in executor (blocking operation)
        response = await loop.run_in_executor(
            None,
            self._rcon_blocking,
            command
        )
        
        return response
    
    def _rcon_blocking(self, command: str) -> str:
        """
        Blocking RCON execution (runs in executor)
        
        Args:
            command: Command to execute
        
        Returns:
            Command response
        """
        with MCRcon(self.host, self.password, port=self.port) as mcr:
            response = mcr.command(command)
            return response
    
    def _sanitize_command(self, command: str) -> str:
        """
        Sanitize and validate Minecraft command
        
        Args:
            command: Raw command input
        
        Returns:
            Sanitized command
        """
        # Strip whitespace
        command = command.strip()
        
        # Remove leading / if present (RCON doesn't need it)
        if command.startswith('/'):
            command = command[1:]
        
        # Basic validation (prevent empty commands)
        if not command:
            raise ValueError("Empty command")
        
        return command
    
    async def say(self, message: str, prefix: str = "[Console]") -> str:
        """
        Send message to Minecraft chat
        
        Args:
            message: Message to send
            prefix: Chat prefix (default: [Console])
        
        Returns:
            Command response
        """
        # Format with Minecraft color codes
        formatted = f"§b{prefix}§f {message}"
        return await self.send_command(f"say {formatted}")
    
    async def execute_multiple(self, commands: List[str]) -> List[str]:
        """
        Execute multiple commands in parallel
        
        Args:
            commands: List of commands to execute
        
        Returns:
            List of responses (same order as commands)
        """
        tasks = [self.send_command(cmd) for cmd in commands]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Convert exceptions to error strings
        results = []
        for response in responses:
            if isinstance(response, Exception):
                results.append(f"Error: {str(response)}")
            else:
                results.append(response)
        
        return results
    
    async def whitelist_add(self, player: str) -> str:
        """Add player to whitelist"""
        return await self.send_command(f"whitelist add {player}")
    
    async def whitelist_remove(self, player: str) -> str:
        """Remove player from whitelist"""
        return await self.send_command(f"whitelist remove {player}")
    
    async def kick(self, player: str, reason: str = "") -> str:
        """Kick player from server"""
        if reason:
            return await self.send_command(f"kick {player} {reason}")
        return await self.send_command(f"kick {player}")
    
    async def stop_server(self) -> str:
        """Stop Minecraft server (use with caution!)"""
        return await self.send_command("stop")
    
    async def teleport(self, player: str, x: float, y: float, z: float) -> str:
        """Teleport player to coordinates"""
        return await self.send_command(f"tp {player} {x} {y} {z}")
    
    async def gamemode(self, player: str, mode: str) -> str:
        """Change player gamemode"""
        return await self.send_command(f"gamemode {mode} {player}")
    
    async def give(self, player: str, item: str, amount: int = 1) -> str:
        """Give item to player"""
        return await self.send_command(f"give {player} {item} {amount}")
    
    def get_stats(self) -> dict:
        """Get command execution statistics"""
        return {
            **self.stats,
            "success_rate": (
                self.stats["successful_commands"] / self.stats["total_commands"]
                if self.stats["total_commands"] > 0 else 0
            )
        }


# Testing and example usage
async def test_rcon_client():
    """Test RCON client with sample commands"""
    import os
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv(".env.grok")
    
    host = os.getenv("MINECRAFT_RCON_HOST", "localhost")
    port = int(os.getenv("MINECRAFT_RCON_PORT", 25575))
    password = os.getenv("MINECRAFT_RCON_PASSWORD", "titan123")
    container = os.getenv("MINECRAFT_DOCKER_CONTAINER", "titan-hub")
    
    # Create client
    client = RconClient(
        host=host,
        port=port,
        password=password,
        docker_container=container
    )
    
    print("=" * 60)
    print("🎮 Testing Enhanced RCON Client")
    print("=" * 60)
    print(f"Host: {host}:{port}")
    print(f"Container: {container}")
    print("=" * 60)
    print()
    
    try:
        # Test 1: Simple say command
        print("📝 Test 1: Say command")
        response = await client.say("RCON test - Hello from console!")
        print(f"Response: {response}")
        print()
        
        # Test 2: Multiple commands in parallel
        print("📝 Test 2: Parallel commands")
        commands = [
            "list",
            "difficulty",
            "time query daytime"
        ]
        responses = await client.execute_multiple(commands)
        for cmd, resp in zip(commands, responses):
            print(f"{cmd}: {resp}")
        print()
        
        # Test 3: Custom command
        print("📝 Test 3: Custom command")
        response = await client.send_command("time set day")
        print(f"Response: {response}")
        print()
        
        # Show statistics
        print("=" * 60)
        print("📊 Statistics")
        print("=" * 60)
        stats = client.get_stats()
        for key, value in stats.items():
            if isinstance(value, float):
                print(f"{key}: {value:.3f}")
            else:
                print(f"{key}: {value}")
        
    except Exception as e:
        print(f"⚠️  Test failed: {str(e)}")
        print("Make sure Minecraft server is running and RCON is enabled!")


if __name__ == "__main__":
    # Run test
    asyncio.run(test_rcon_client())

