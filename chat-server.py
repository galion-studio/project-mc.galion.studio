#!/usr/bin/env python3
"""
Chat Server - FastAPI Communication Layer
REST API for Grok Console Chat System

Features:
- REST API endpoints for chat, commands, and status
- Async request handling
- CORS support
- Request validation
- Error handling

Endpoints:
  POST /chat          - Send AI chat message
  POST /command       - Execute Minecraft command
  POST /project/cmd   - Execute project command
  GET /status         - Get system status
  GET /stats          - Get usage statistics
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import asyncio
import os
from dotenv import load_dotenv
import uvicorn

# Import our modules
try:
    from grok_client import GrokClient
    from rcon_client import RconClient
    from project_controller import ProjectController
except ImportError:
    # Try importing from current directory
    import sys
    sys.path.insert(0, '.')
    from grok_client import GrokClient
    from rcon_client import RconClient
    from project_controller import ProjectController


# Load environment
load_dotenv(".env.grok")


# ========================================
# REQUEST/RESPONSE MODELS
# ========================================

class ChatRequest(BaseModel):
    """Request model for AI chat"""
    message: str
    player_name: Optional[str] = "Console"
    system_prompt: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for AI chat"""
    response: str
    execution_time: float


class CommandRequest(BaseModel):
    """Request model for Minecraft commands"""
    command: str


class CommandResponse(BaseModel):
    """Response model for Minecraft commands"""
    response: str
    success: bool
    execution_time: float


class ProjectCommandRequest(BaseModel):
    """Request model for project commands"""
    action: str
    args: Optional[List[str]] = []


class ProjectCommandResponse(BaseModel):
    """Response model for project commands"""
    result: str
    success: bool


class StatusResponse(BaseModel):
    """Response model for system status"""
    grok_available: bool
    rcon_available: bool
    project_available: bool
    stats: Dict[str, Any]


# ========================================
# API APPLICATION
# ========================================

app = FastAPI(
    title="Grok Console Chat API",
    description="REST API for ultra-fast AI chat and Minecraft server control",
    version="1.0.0"
)

# Enable CORS for web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (restrict in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========================================
# GLOBAL CLIENTS (initialized on startup)
# ========================================

grok_client: Optional[GrokClient] = None
rcon_client: Optional[RconClient] = None
project_controller: Optional[ProjectController] = None


# ========================================
# STARTUP/SHUTDOWN
# ========================================

@app.on_event("startup")
async def startup_event():
    """Initialize clients on startup"""
    global grok_client, rcon_client, project_controller
    
    print("🚀 Starting Chat Server...")
    
    # Initialize Grok AI via OpenRouter
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "")
    if openrouter_api_key and openrouter_api_key != "your-openrouter-api-key-here":
        try:
            grok_client = GrokClient(api_key=openrouter_api_key)
            print("✓ Grok AI initialized (via OpenRouter)")
        except Exception as e:
            print(f"⚠ Grok AI failed: {e}")
    else:
        print("⚠ Grok AI not configured (set OPENROUTER_API_KEY)")
    
    # Initialize RCON
    try:
        rcon_client = RconClient(
            host=os.getenv("MINECRAFT_RCON_HOST", "localhost"),
            port=int(os.getenv("MINECRAFT_RCON_PORT", 25575)),
            password=os.getenv("MINECRAFT_RCON_PASSWORD", "titan123"),
            docker_container=os.getenv("MINECRAFT_DOCKER_CONTAINER", "titan-hub")
        )
        # Test connection
        await rcon_client.send_command("list")
        print("✓ RCON initialized")
    except Exception as e:
        print(f"⚠ RCON failed: {e}")
        rcon_client = None
    
    # Initialize project controller
    try:
        project_root = os.getenv("PROJECT_ROOT", ".")
        project_controller = ProjectController(project_root)
        print("✓ Project controller initialized")
    except Exception as e:
        print(f"⚠ Project controller failed: {e}")
        project_controller = None
    
    print("✓ Chat Server ready!")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    if grok_client:
        await grok_client.close()
    print("✓ Chat Server stopped")


# ========================================
# API ENDPOINTS
# ========================================

@app.get("/")
async def root():
    """API root - health check"""
    return {
        "status": "online",
        "api": "Grok Console Chat",
        "version": "1.0.0"
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send AI chat message
    
    Args:
        request: Chat request with message and optional player name
    
    Returns:
        AI response with execution time
    """
    if not grok_client:
        raise HTTPException(status_code=503, detail="Grok AI not available")
    
    import time
    start_time = time.time()
    
    try:
        # Ask Grok
        if request.system_prompt:
            response = await grok_client.ask(
                request.message,
                system=request.system_prompt
            )
        else:
            response = await grok_client.ask_minecraft(
                request.message,
                request.player_name
            )
        
        execution_time = time.time() - start_time
        
        return ChatResponse(
            response=response,
            execution_time=execution_time
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


@app.post("/command", response_model=CommandResponse)
async def execute_command(request: CommandRequest):
    """
    Execute Minecraft command via RCON
    
    Args:
        request: Command request
    
    Returns:
        Command response with success status
    """
    if not rcon_client:
        raise HTTPException(status_code=503, detail="RCON not available")
    
    import time
    start_time = time.time()
    
    try:
        response = await rcon_client.send_command(request.command)
        execution_time = time.time() - start_time
        
        return CommandResponse(
            response=response,
            success=True,
            execution_time=execution_time
        )
    
    except Exception as e:
        execution_time = time.time() - start_time
        return CommandResponse(
            response=str(e),
            success=False,
            execution_time=execution_time
        )


@app.post("/say")
async def say_message(message: str):
    """
    Send message to Minecraft chat
    
    Args:
        message: Message to send
    
    Returns:
        Success status
    """
    if not rcon_client:
        raise HTTPException(status_code=503, detail="RCON not available")
    
    try:
        await rcon_client.say(message)
        return {"success": True, "message": "Message sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/project/command", response_model=ProjectCommandResponse)
async def project_command(request: ProjectCommandRequest):
    """
    Execute project command
    
    Args:
        request: Project command request
    
    Returns:
        Command result
    """
    if not project_controller:
        raise HTTPException(status_code=503, detail="Project controller not available")
    
    try:
        action = request.action
        args = request.args or []
        
        # Route to appropriate method
        if action == "status":
            result = await project_controller.git_status()
        elif action == "log":
            result = await project_controller.git_log()
        elif action == "diff":
            result = await project_controller.git_diff()
        elif action == "docker":
            result = await project_controller.docker_ps()
        elif action == "logs":
            container = args[0] if args else "titan-hub"
            result = await project_controller.docker_logs(container)
        elif action == "ls":
            directory = args[0] if args else "."
            files = await project_controller.list_files(directory)
            result = "\n".join(files)
        elif action == "read":
            if not args:
                return ProjectCommandResponse(
                    result="Error: No file specified",
                    success=False
                )
            result = await project_controller.read_file(args[0])
        elif action == "build":
            result = await project_controller.gradle_build()
        elif action == "clean":
            result = await project_controller.gradle_clean()
        else:
            return ProjectCommandResponse(
                result=f"Unknown action: {action}",
                success=False
            )
        
        return ProjectCommandResponse(
            result=result,
            success=True
        )
    
    except Exception as e:
        return ProjectCommandResponse(
            result=str(e),
            success=False
        )


@app.get("/status", response_model=StatusResponse)
async def get_status():
    """
    Get system status
    
    Returns:
        System status with statistics
    """
    stats = {}
    
    # Collect stats from each client
    if grok_client:
        stats["grok"] = grok_client.get_stats()
    
    if rcon_client:
        stats["rcon"] = rcon_client.get_stats()
    
    if project_controller:
        stats["project"] = project_controller.get_stats()
    
    return StatusResponse(
        grok_available=grok_client is not None,
        rcon_available=rcon_client is not None,
        project_available=project_controller is not None,
        stats=stats
    )


@app.get("/stats")
async def get_stats():
    """Get detailed statistics"""
    stats = {
        "grok": grok_client.get_stats() if grok_client else None,
        "rcon": rcon_client.get_stats() if rcon_client else None,
        "project": project_controller.get_stats() if project_controller else None
    }
    return stats


@app.post("/cache/clear")
async def clear_cache():
    """Clear Grok response cache"""
    if not grok_client:
        raise HTTPException(status_code=503, detail="Grok AI not available")
    
    grok_client.clear_cache()
    return {"success": True, "message": "Cache cleared"}


# ========================================
# MAIN (for direct execution)
# ========================================

if __name__ == "__main__":
    # Get configuration
    host = os.getenv("CHAT_SERVER_HOST", "localhost")
    port = int(os.getenv("CHAT_SERVER_PORT", 8000))
    
    print(f"""
{'=' * 60}
  🚀 GROK CHAT SERVER
{'=' * 60}
  API: http://{host}:{port}
  Docs: http://{host}:{port}/docs
{'=' * 60}
""")
    
    # Run server
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )

