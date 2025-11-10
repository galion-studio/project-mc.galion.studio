#!/usr/bin/env python3
"""
Console Chat Interface for Minecraft Server
Interactive terminal for instant AI chat and server control

Features:
- Interactive console with rich UI
- Grok-4 Fast AI integration
- Instant Minecraft RCON commands
- Project control operations
- Color-coded output
- Command history
- Real-time responses (<1 second)

Commands:
  /say <message>        - Send to Minecraft chat
  /cmd <minecraft-cmd>  - Execute Minecraft command
  @ai <question>        - Ask AI assistant
  @project <action>     - Control project
  /status               - System status
  /help                 - Show help
  /quit                 - Exit
"""

import asyncio
import os
import sys
from typing import Optional
from dotenv import load_dotenv
from colorama import init, Fore, Back, Style
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
import time

# Import our custom modules
try:
    from grok_client import GrokClient
except ImportError:
    # Try importing from current directory
    import sys
    sys.path.insert(0, '.')
    from grok_client import GrokClient

try:
    from rcon_client import RconClient
except ImportError:
    import sys
    sys.path.insert(0, '.')
    from rcon_client import RconClient

try:
    from project_controller import ProjectController
except ImportError:
    import sys
    sys.path.insert(0, '.')
    from project_controller import ProjectController


# Initialize colorama for Windows color support
init(autoreset=True)


class ConsoleChat:
    """
    Main console chat interface
    Handles user input, routes commands, displays responses
    """
    
    def __init__(self):
        """Initialize console chat system"""
        
        # Load environment variables
        load_dotenv(".env.grok")
        
        # Configuration
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "")
        self.rcon_host = os.getenv("MINECRAFT_RCON_HOST", "localhost")
        self.rcon_port = int(os.getenv("MINECRAFT_RCON_PORT", 25575))
        self.rcon_password = os.getenv("MINECRAFT_RCON_PASSWORD", "titan123")
        self.docker_container = os.getenv("MINECRAFT_DOCKER_CONTAINER", "titan-hub")
        self.project_root = os.getenv("PROJECT_ROOT", ".")
        
        # Initialize clients
        self.grok: Optional[GrokClient] = None
        self.rcon: Optional[RconClient] = None
        self.project: Optional[ProjectController] = None
        
        # Prompt session with history
        self.session: Optional[PromptSession] = None
        
        # Running state
        self.running = False
    
    async def initialize(self):
        """Initialize all clients and connections"""
        
        print(self._banner())
        print(f"{Fore.CYAN}🚀 Initializing systems...{Style.RESET_ALL}\n")
        
        # Initialize Grok AI client via OpenRouter
        if self.openrouter_api_key and self.openrouter_api_key != "your-openrouter-api-key-here":
            try:
                self.grok = GrokClient(api_key=self.openrouter_api_key)
                print(f"{Fore.GREEN}✓ Grok AI connected (via OpenRouter){Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}✗ Grok AI failed: {e}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠ Grok AI not configured (set OPENROUTER_API_KEY){Style.RESET_ALL}")
        
        # Initialize RCON client
        try:
            self.rcon = RconClient(
                host=self.rcon_host,
                port=self.rcon_port,
                password=self.rcon_password,
                docker_container=self.docker_container
            )
            # Test connection
            await self.rcon.send_command("list")
            print(f"{Fore.GREEN}✓ Minecraft RCON connected{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.YELLOW}⚠ Minecraft RCON unavailable: {e}{Style.RESET_ALL}")
            self.rcon = None
        
        # Initialize project controller
        try:
            self.project = ProjectController(self.project_root)
            print(f"{Fore.GREEN}✓ Project controller ready{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}✗ Project controller failed: {e}{Style.RESET_ALL}")
        
        print()
        
        # Create prompt session
        self.session = PromptSession(
            history=FileHistory('.console_history'),
            auto_suggest=AutoSuggestFromHistory()
        )
    
    async def cleanup(self):
        """Cleanup connections"""
        if self.grok:
            await self.grok.close()
        print(f"\n{Fore.CYAN}✓ Console chat closed{Style.RESET_ALL}")
    
    def _banner(self) -> str:
        """Return banner text"""
        return f"""
{Fore.CYAN}{'=' * 70}
{Fore.GREEN}  ⚡ GROK CONSOLE CHAT - mc.galion.studio
{Fore.CYAN}  Ultra-fast AI chat + Minecraft server control
{'=' * 70}{Style.RESET_ALL}
"""
    
    async def handle_command(self, user_input: str):
        """
        Route and handle user commands
        
        Args:
            user_input: Raw user input from console
        """
        user_input = user_input.strip()
        
        if not user_input:
            return
        
        start_time = time.time()
        
        try:
            # Help command
            if user_input == "/help":
                self._show_help()
            
            # Status command
            elif user_input == "/status":
                await self._show_status()
            
            # Say command (send to Minecraft chat)
            elif user_input.startswith("/say "):
                message = user_input[5:]
                await self._handle_say(message)
            
            # Minecraft command
            elif user_input.startswith("/cmd "):
                command = user_input[5:]
                await self._handle_minecraft_command(command)
            
            # AI question
            elif user_input.startswith("@ai "):
                question = user_input[4:]
                await self._handle_ai_question(question)
            
            # Project command
            elif user_input.startswith("@project "):
                command = user_input[9:]
                await self._handle_project_command(command)
            
            # Direct Minecraft command (no prefix)
            elif user_input.startswith("/"):
                await self._handle_minecraft_command(user_input[1:])
            
            # Default: treat as AI question
            else:
                await self._handle_ai_question(user_input)
            
            # Show execution time
            elapsed = time.time() - start_time
            if elapsed > 0.1:  # Only show if meaningful
                print(f"{Fore.BLUE}⏱️  {elapsed:.2f}s{Style.RESET_ALL}")
        
        except Exception as e:
            print(f"{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")
    
    async def _handle_say(self, message: str):
        """Send message to Minecraft chat"""
        if not self.rcon:
            print(f"{Fore.RED}✗ RCON not connected{Style.RESET_ALL}")
            return
        
        try:
            response = await self.rcon.say(message)
            print(f"{Fore.GREEN}✓ Sent to Minecraft{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}✗ Failed: {e}{Style.RESET_ALL}")
    
    async def _handle_minecraft_command(self, command: str):
        """Execute Minecraft command via RCON"""
        if not self.rcon:
            print(f"{Fore.RED}✗ RCON not connected{Style.RESET_ALL}")
            return
        
        try:
            print(f"{Fore.CYAN}⚙️  Executing: {command}{Style.RESET_ALL}")
            response = await self.rcon.send_command(command)
            print(f"{Fore.GREEN}{response}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}✗ Command failed: {e}{Style.RESET_ALL}")
    
    async def _handle_ai_question(self, question: str):
        """Ask Grok AI a question"""
        if not self.grok:
            print(f"{Fore.RED}✗ Grok AI not configured{Style.RESET_ALL}")
            return
        
        try:
            print(f"{Fore.CYAN}🤔 Asking Grok...{Style.RESET_ALL}")
            response = await self.grok.ask_minecraft(question)
            print(f"{Fore.MAGENTA}🤖 Grok: {response}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}✗ AI error: {e}{Style.RESET_ALL}")
    
    async def _handle_project_command(self, command: str):
        """Handle project control commands"""
        if not self.project:
            print(f"{Fore.RED}✗ Project controller not available{Style.RESET_ALL}")
            return
        
        parts = command.split()
        if not parts:
            print(f"{Fore.YELLOW}Usage: @project <action> [args]{Style.RESET_ALL}")
            return
        
        action = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        try:
            # Git commands
            if action == "status":
                result = await self.project.git_status()
                print(f"{Fore.GREEN}{result}{Style.RESET_ALL}")
            
            elif action == "log":
                result = await self.project.git_log()
                print(f"{Fore.GREEN}{result}{Style.RESET_ALL}")
            
            elif action == "diff":
                result = await self.project.git_diff()
                print(f"{Fore.GREEN}{result}{Style.RESET_ALL}")
            
            # Docker commands
            elif action == "docker":
                result = await self.project.docker_ps()
                print(f"{Fore.GREEN}{result}{Style.RESET_ALL}")
            
            elif action == "logs":
                container = args[0] if args else self.docker_container
                result = await self.project.docker_logs(container)
                print(f"{Fore.GREEN}{result}{Style.RESET_ALL}")
            
            # File operations
            elif action == "ls":
                directory = args[0] if args else "."
                files = await self.project.list_files(directory)
                for f in files:
                    print(f"{Fore.GREEN}{f}{Style.RESET_ALL}")
            
            elif action == "read":
                if not args:
                    print(f"{Fore.YELLOW}Usage: @project read <filepath>{Style.RESET_ALL}")
                    return
                content = await self.project.read_file(args[0])
                print(f"{Fore.GREEN}{content}{Style.RESET_ALL}")
            
            # Build commands
            elif action == "build":
                print(f"{Fore.CYAN}⚙️  Building project...{Style.RESET_ALL}")
                result = await self.project.gradle_build()
                print(f"{Fore.GREEN}{result}{Style.RESET_ALL}")
            
            elif action == "clean":
                result = await self.project.gradle_clean()
                print(f"{Fore.GREEN}{result}{Style.RESET_ALL}")
            
            else:
                print(f"{Fore.YELLOW}Unknown action: {action}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Available: status, log, diff, docker, logs, ls, read, build, clean{Style.RESET_ALL}")
        
        except Exception as e:
            print(f"{Fore.RED}✗ Project error: {e}{Style.RESET_ALL}")
    
    async def _show_status(self):
        """Show system status"""
        print(f"\n{Fore.CYAN}{'=' * 60}")
        print(f"  SYSTEM STATUS")
        print(f"{'=' * 60}{Style.RESET_ALL}")
        
        # Grok AI status
        if self.grok:
            stats = self.grok.get_stats()
            print(f"\n{Fore.GREEN}✓ Grok AI:{Style.RESET_ALL}")
            print(f"  Requests: {stats['total_requests']}")
            print(f"  Cache hits: {stats['cache_hits']} ({stats['cache_hit_rate']:.1%})")
            if stats['total_requests'] > 0:
                print(f"  Avg response: {stats['avg_response_time']:.3f}s")
                print(f"  Fastest: {stats['fastest_response']:.3f}s")
        else:
            print(f"\n{Fore.RED}✗ Grok AI: Not configured{Style.RESET_ALL}")
        
        # RCON status
        if self.rcon:
            stats = self.rcon.get_stats()
            print(f"\n{Fore.GREEN}✓ Minecraft RCON:{Style.RESET_ALL}")
            print(f"  Commands: {stats['total_commands']}")
            print(f"  Success rate: {stats['success_rate']:.1%}")
            if stats['total_commands'] > 0:
                print(f"  Avg time: {stats['avg_execution_time']:.3f}s")
        else:
            print(f"\n{Fore.RED}✗ Minecraft RCON: Not connected{Style.RESET_ALL}")
        
        # Project controller status
        if self.project:
            stats = self.project.get_stats()
            print(f"\n{Fore.GREEN}✓ Project Controller:{Style.RESET_ALL}")
            print(f"  Commands: {stats['total_commands']}")
            print(f"  Success rate: {stats['success_rate']:.1%}")
        else:
            print(f"\n{Fore.RED}✗ Project Controller: Not available{Style.RESET_ALL}")
        
        print()
    
    def _show_help(self):
        """Show help message"""
        help_text = f"""
{Fore.CYAN}{'=' * 60}
  COMMAND REFERENCE
{'=' * 60}{Style.RESET_ALL}

{Fore.YELLOW}CHAT COMMANDS:{Style.RESET_ALL}
  /say <message>        Send message to Minecraft chat
  @ai <question>        Ask Grok AI a question
  <any text>            Defaults to AI question

{Fore.YELLOW}MINECRAFT COMMANDS:{Style.RESET_ALL}
  /cmd <command>        Execute Minecraft command
  /<command>            Direct Minecraft command
  
  Examples:
    /list                List online players
    /time set day        Set time to day
    /gamemode creative   Set gamemode

{Fore.YELLOW}PROJECT COMMANDS:{Style.RESET_ALL}
  @project status       Git status
  @project log          Recent commits
  @project diff         Git diff
  @project docker       List containers
  @project logs [name]  Container logs
  @project ls [dir]     List files
  @project read <file>  Read file
  @project build        Build project
  @project clean        Clean build

{Fore.YELLOW}SYSTEM COMMANDS:{Style.RESET_ALL}
  /status               Show system status
  /help                 Show this help
  /quit                 Exit console

{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}
"""
        print(help_text)
    
    async def run(self):
        """Main console loop"""
        await self.initialize()
        
        self._show_help()
        
        self.running = True
        
        print(f"{Fore.GREEN}✓ Console ready! Type /help for commands{Style.RESET_ALL}\n")
        
        try:
            while self.running:
                try:
                    # Get user input
                    user_input = await asyncio.get_event_loop().run_in_executor(
                        None,
                        self.session.prompt,
                        f"{Fore.CYAN}> {Style.RESET_ALL}"
                    )
                    
                    # Check for quit
                    if user_input.strip() in ["/quit", "/exit", "quit", "exit"]:
                        print(f"{Fore.YELLOW}Exiting...{Style.RESET_ALL}")
                        break
                    
                    # Handle command
                    await self.handle_command(user_input)
                    print()  # Blank line for readability
                
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}Use /quit to exit{Style.RESET_ALL}")
                except EOFError:
                    break
        
        finally:
            self.running = False
            await self.cleanup()


async def main():
    """Entry point"""
    console = ConsoleChat()
    await console.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nExiting...")

