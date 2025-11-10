#!/usr/bin/env python3
"""
Grok Console Chat System - Integration Tests
Test all components and verify <1 second response times

Tests:
1. Grok API connectivity and response time
2. RCON command execution
3. Project controller operations
4. Console chat commands
5. API server endpoints
"""

import asyncio
import time
import os
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Import our modules
try:
    from grok_client import GrokClient
    from rcon_client import RconClient
    from project_controller import ProjectController
except ImportError as e:
    print(f"{Fore.RED}✗ Import error: {e}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Make sure all files are in the correct location{Style.RESET_ALL}")
    exit(1)


class SystemTester:
    """Integration tester for Grok console chat system"""
    
    def __init__(self):
        """Initialize tester"""
        load_dotenv(".env.grok")
        
        self.results = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "warnings": 0
        }
        
        self.grok_client = None
        self.rcon_client = None
        self.project_controller = None
    
    def print_header(self, text):
        """Print test section header"""
        print(f"\n{Fore.CYAN}{'=' * 60}")
        print(f"  {text}")
        print(f"{'=' * 60}{Style.RESET_ALL}\n")
    
    def print_test(self, name):
        """Print test name"""
        print(f"{Fore.YELLOW}📝 Test: {name}{Style.RESET_ALL}")
    
    def print_pass(self, message, time_ms=None):
        """Print test pass"""
        time_str = f" ({time_ms:.0f}ms)" if time_ms else ""
        print(f"{Fore.GREEN}✓ PASS: {message}{time_str}{Style.RESET_ALL}")
        self.results["passed"] += 1
    
    def print_fail(self, message):
        """Print test failure"""
        print(f"{Fore.RED}✗ FAIL: {message}{Style.RESET_ALL}")
        self.results["failed"] += 1
    
    def print_warning(self, message):
        """Print test warning"""
        print(f"{Fore.YELLOW}⚠ WARNING: {message}{Style.RESET_ALL}")
        self.results["warnings"] += 1
    
    async def test_environment(self):
        """Test environment configuration"""
        self.print_header("Environment Configuration")
        self.results["total_tests"] += 1
        
        self.print_test("Check .env.grok file")
        if os.path.exists(".env.grok"):
            self.print_pass(".env.grok file exists")
        else:
            self.print_fail(".env.grok file not found")
            return False
        
        # Check API key
        api_key = os.getenv("XAI_API_KEY", "")
        if api_key and api_key != "your-xai-api-key-here":
            self.print_pass("XAI_API_KEY is set")
        else:
            self.print_warning("XAI_API_KEY not configured")
            print(f"  Get your API key from: https://console.x.ai/")
            return False
        
        return True
    
    async def test_grok_client(self):
        """Test Grok API client"""
        self.print_header("Grok API Client Tests")
        
        # Test 1: Client initialization
        self.results["total_tests"] += 1
        self.print_test("Initialize Grok client")
        try:
            api_key = os.getenv("XAI_API_KEY", "")
            self.grok_client = GrokClient(api_key=api_key)
            self.print_pass("Grok client initialized")
        except Exception as e:
            self.print_fail(f"Client initialization failed: {e}")
            return False
        
        # Test 2: Simple query (response time)
        self.results["total_tests"] += 1
        self.print_test("Simple AI query (target: <1s)")
        try:
            start = time.time()
            response = await self.grok_client.ask("What is 2+2? Answer in one word.")
            elapsed = (time.time() - start) * 1000  # Convert to ms
            
            if elapsed < 1000:
                self.print_pass(f"Response received", elapsed)
                print(f"  Response: {response[:50]}...")
            else:
                self.print_warning(f"Response slower than target (>{elapsed:.0f}ms)")
                print(f"  Response: {response[:50]}...")
        except Exception as e:
            self.print_fail(f"Query failed: {e}")
            return False
        
        # Test 3: Cache functionality
        self.results["total_tests"] += 1
        self.print_test("Response caching (should be instant)")
        try:
            start = time.time()
            response = await self.grok_client.ask("What is 2+2? Answer in one word.")
            elapsed = (time.time() - start) * 1000
            
            if elapsed < 50:  # Cache hit should be <50ms
                self.print_pass(f"Cache working", elapsed)
            else:
                self.print_warning(f"Cache may not be working ({elapsed:.0f}ms)")
        except Exception as e:
            self.print_fail(f"Cache test failed: {e}")
        
        # Test 4: Minecraft-specific query
        self.results["total_tests"] += 1
        self.print_test("Minecraft-specific query")
        try:
            start = time.time()
            response = await self.grok_client.ask_minecraft("What is redstone?", "TestPlayer")
            elapsed = (time.time() - start) * 1000
            
            self.print_pass(f"Minecraft query success", elapsed)
            print(f"  Response: {response[:80]}...")
        except Exception as e:
            self.print_fail(f"Minecraft query failed: {e}")
        
        return True
    
    async def test_rcon_client(self):
        """Test RCON client"""
        self.print_header("RCON Client Tests")
        
        # Test 1: Client initialization
        self.results["total_tests"] += 1
        self.print_test("Initialize RCON client")
        try:
            host = os.getenv("MINECRAFT_RCON_HOST", "localhost")
            port = int(os.getenv("MINECRAFT_RCON_PORT", 25575))
            password = os.getenv("MINECRAFT_RCON_PASSWORD", "titan123")
            container = os.getenv("MINECRAFT_DOCKER_CONTAINER", "titan-hub")
            
            self.rcon_client = RconClient(
                host=host,
                port=port,
                password=password,
                docker_container=container
            )
            self.print_pass("RCON client initialized")
        except Exception as e:
            self.print_fail(f"RCON initialization failed: {e}")
            return False
        
        # Test 2: Simple command
        self.results["total_tests"] += 1
        self.print_test("Execute simple command (target: <100ms)")
        try:
            start = time.time()
            response = await self.rcon_client.send_command("list")
            elapsed = (time.time() - start) * 1000
            
            if elapsed < 100:
                self.print_pass(f"Command executed", elapsed)
            else:
                self.print_warning(f"Command slower than target ({elapsed:.0f}ms)")
            print(f"  Response: {response[:80]}...")
        except Exception as e:
            self.print_warning(f"RCON command failed (server may be offline): {e}")
            print(f"  This is OK if Minecraft server is not running")
            return False
        
        # Test 3: Say command
        self.results["total_tests"] += 1
        self.print_test("Say command")
        try:
            response = await self.rcon_client.say("Test message from integration test")
            self.print_pass("Say command executed")
        except Exception as e:
            self.print_warning(f"Say command failed: {e}")
        
        return True
    
    async def test_project_controller(self):
        """Test project controller"""
        self.print_header("Project Controller Tests")
        
        # Test 1: Initialize controller
        self.results["total_tests"] += 1
        self.print_test("Initialize project controller")
        try:
            project_root = os.getenv("PROJECT_ROOT", ".")
            self.project_controller = ProjectController(project_root)
            self.print_pass("Project controller initialized")
        except Exception as e:
            self.print_fail(f"Controller initialization failed: {e}")
            return False
        
        # Test 2: Project info
        self.results["total_tests"] += 1
        self.print_test("Get project info")
        try:
            info = await self.project_controller.get_project_info()
            self.print_pass("Project info retrieved")
            for key, value in info.items():
                print(f"    {key}: {value}")
        except Exception as e:
            self.print_fail(f"Project info failed: {e}")
        
        # Test 3: Git status
        self.results["total_tests"] += 1
        self.print_test("Git status")
        try:
            status = await self.project_controller.git_status()
            self.print_pass("Git status retrieved")
            print(f"  Status: {status[:80]}...")
        except Exception as e:
            self.print_warning(f"Git status failed: {e}")
        
        # Test 4: List files
        self.results["total_tests"] += 1
        self.print_test("List files")
        try:
            files = await self.project_controller.list_files()
            self.print_pass(f"Listed {len(files)} files/directories")
        except Exception as e:
            self.print_fail(f"List files failed: {e}")
        
        return True
    
    async def test_integration(self):
        """Test complete integration"""
        self.print_header("Integration Tests")
        
        # Test 1: Full workflow
        self.results["total_tests"] += 1
        self.print_test("Complete workflow (AI + RCON)")
        
        if not self.grok_client or not self.rcon_client:
            self.print_warning("Skipping (components not available)")
            return
        
        try:
            # Ask AI
            start = time.time()
            ai_response = await self.grok_client.ask_minecraft("Say hello in 3 words", "Test")
            ai_time = (time.time() - start) * 1000
            
            # Send to Minecraft
            start = time.time()
            await self.rcon_client.say(ai_response)
            rcon_time = (time.time() - start) * 1000
            
            total_time = ai_time + rcon_time
            
            if total_time < 1000:
                self.print_pass(f"Complete workflow", total_time)
            else:
                self.print_warning(f"Workflow slower than target ({total_time:.0f}ms)")
            
            print(f"  AI time: {ai_time:.0f}ms")
            print(f"  RCON time: {rcon_time:.0f}ms")
            print(f"  Total: {total_time:.0f}ms")
        except Exception as e:
            self.print_fail(f"Integration test failed: {e}")
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.grok_client:
            await self.grok_client.close()
    
    def print_summary(self):
        """Print test summary"""
        self.print_header("Test Summary")
        
        print(f"Total Tests: {self.results['total_tests']}")
        print(f"{Fore.GREEN}Passed: {self.results['passed']}{Style.RESET_ALL}")
        print(f"{Fore.RED}Failed: {self.results['failed']}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Warnings: {self.results['warnings']}{Style.RESET_ALL}")
        print()
        
        # Calculate success rate
        if self.results['total_tests'] > 0:
            success_rate = (self.results['passed'] / self.results['total_tests']) * 100
            
            if success_rate >= 80:
                print(f"{Fore.GREEN}✓ System Status: READY ({success_rate:.0f}% passed){Style.RESET_ALL}")
            elif success_rate >= 50:
                print(f"{Fore.YELLOW}⚠ System Status: PARTIALLY READY ({success_rate:.0f}% passed){Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}✗ System Status: NOT READY ({success_rate:.0f}% passed){Style.RESET_ALL}")
        
        print()
    
    async def run_all_tests(self):
        """Run all tests"""
        print(f"\n{Fore.CYAN}{'=' * 60}")
        print(f"  🚀 GROK CONSOLE CHAT - INTEGRATION TESTS")
        print(f"{'=' * 60}{Style.RESET_ALL}\n")
        
        try:
            # Environment tests
            env_ok = await self.test_environment()
            
            if env_ok:
                # Component tests
                await self.test_grok_client()
                await self.test_rcon_client()
                await self.test_project_controller()
                
                # Integration tests
                await self.test_integration()
            
        finally:
            await self.cleanup()
            self.print_summary()


async def main():
    """Main test entry point"""
    tester = SystemTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Tests interrupted{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Test error: {e}{Style.RESET_ALL}")

