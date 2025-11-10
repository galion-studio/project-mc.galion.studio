#!/usr/bin/env python3
"""
GALION Web Control Panel Backend
Simple, fast, works.
"""

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

app = FastAPI(title="GALION Control Panel API")

# CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import Grok client (if available)
try:
    from grok_client import GrokClient
    import os
    
    # Load API key
    env_file = PROJECT_ROOT / ".env.grok"
    api_key = None
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith("OPENROUTER_API_KEY="):
                    api_key = line.split('=', 1)[1].strip()
                    break
    
    grok_client = GrokClient(api_key=api_key) if api_key else None
except Exception as e:
    print(f"[WARN] Grok client not available: {e}")
    grok_client = None


@app.get("/")
async def root():
    """Serve the main control panel"""
    return FileResponse("web-control-panel/index.html")


@app.get("/api/status")
async def get_status():
    """Get server status"""
    # TODO: Implement real server status check
    return {
        "online": True,
        "players": 0,
        "max_players": 100,
        "tps": 20.0,
        "version": "1.21.1",
        "uptime": "99.9%"
    }


@app.get("/api/players")
async def get_players():
    """Get online players list"""
    # TODO: Implement real player list
    return {
        "count": 0,
        "players": []
    }


@app.post("/api/chat")
async def chat(message: dict):
    """AI chat endpoint"""
    user_message = message.get("message", "")
    
    if not grok_client:
        return {
            "response": "AI is not configured. Add your OpenRouter API key to .env.grok"
        }
    
    try:
        response = await grok_client.ask_minecraft(user_message)
        return {"response": response}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time updates"""
    await websocket.accept()
    try:
        while True:
            # Send status updates every 2 seconds
            status = {
                "type": "status_update",
                "data": {
                    "tps": 20.0,
                    "players": 0
                }
            }
            await websocket.send_json(status)
            await asyncio.sleep(2)
    except Exception as e:
        print(f"WebSocket error: {e}")


if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("GALION Control Panel")
    print("=" * 60)
    print()
    print("Starting server...")
    print("Access at: http://localhost:8080")
    print()
    print("Press Ctrl+C to stop")
    print()
    
    # Suppress default uvicorn startup message to avoid encoding issues
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="warning")

