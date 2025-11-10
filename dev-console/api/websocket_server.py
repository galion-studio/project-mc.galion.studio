"""
WebSocket Server for Real-time Updates
Provides real-time notifications and log streaming
"""

import asyncio
import json
from typing import Set
import websockets
from websockets.server import WebSocketServerProtocol


class WebSocketServer:
    """
    WebSocket server for real-time communication.
    Simple, efficient, scalable.
    """
    
    def __init__(self, host: str = "localhost", port: int = 8081):
        self.host = host
        self.port = port
        self.clients: Set[WebSocketServerProtocol] = set()
    
    async def register(self, websocket: WebSocketServerProtocol):
        """Register new client"""
        self.clients.add(websocket)
        print(f"Client connected. Total clients: {len(self.clients)}")
    
    async def unregister(self, websocket: WebSocketServerProtocol):
        """Unregister client"""
        self.clients.remove(websocket)
        print(f"Client disconnected. Total clients: {len(self.clients)}")
    
    async def handler(self, websocket: WebSocketServerProtocol, path: str):
        """Handle WebSocket connection"""
        await self.register(websocket)
        
        try:
            async for message in websocket:
                # Echo message back for now
                await websocket.send(message)
        finally:
            await self.unregister(websocket)
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        if self.clients:
            message_json = json.dumps(message)
            await asyncio.gather(
                *[client.send(message_json) for client in self.clients],
                return_exceptions=True
            )
    
    async def start(self):
        """Start WebSocket server"""
        async with websockets.serve(self.handler, self.host, self.port):
            print(f"WebSocket server started on ws://{self.host}:{self.port}")
            await asyncio.Future()  # Run forever
    
    def run(self):
        """Run WebSocket server"""
        asyncio.run(self.start())


if __name__ == "__main__":
    server = WebSocketServer()
    server.run()

