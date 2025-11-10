"""
Development API Server
Extended API for development console with mod upload, deployment, and server control
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import hashlib
import shutil
import sys
import socket
import subprocess
from typing import Optional, Dict, List
from datetime import datetime
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import SERVER_MODS_DIR, PROJECT_ROOT, MINECRAFT_SERVER_PORT
from database.db_manager import get_db

# Create FastAPI app
app = FastAPI(
    title="Development Console API",
    version="1.0.0",
    description="API for Galion.Studio Development Console"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get database
db = get_db()


# === Utility Functions ===

def calculate_checksum(file_path: Path) -> str:
    """Calculate SHA256 checksum"""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def check_server_online() -> bool:
    """Check if Minecraft server is online"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', MINECRAFT_SERVER_PORT))
        sock.close()
        return result == 0
    except:
        return False


# === Root & Health Endpoints ===

@app.get("/")
async def root():
    """API root"""
    return {
        "name": "Development Console API",
        "version": "1.0.0",
        "status": "online",
        "endpoints": {
            "mods": "/api/dev/mods",
            "server": "/api/dev/server",
            "logs": "/api/dev/logs",
            "deployments": "/api/dev/deployments"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    server_online = check_server_online()
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "server_online": server_online,
        "database": "connected"
    }


# === Mod Endpoints ===

@app.get("/api/dev/mods")
async def get_mods(environment: str = "dev"):
    """
    Get all mods for an environment.
    """
    mods = db.get_mods_by_environment(environment)
    return {
        "success": True,
        "environment": environment,
        "count": len(mods),
        "mods": mods
    }


@app.get("/api/dev/mods/{mod_id}")
async def get_mod(mod_id: int):
    """Get specific mod by ID"""
    mod = db.get_mod_by_id(mod_id)
    
    if not mod:
        raise HTTPException(status_code=404, detail="Mod not found")
    
    return {
        "success": True,
        "mod": mod
    }


@app.post("/api/dev/mods/upload")
async def upload_mod(
    file: UploadFile = File(...),
    environment: str = Form("dev"),
    user_id: int = Form(1)
):
    """
    Upload a new mod file.
    
    This endpoint handles mod file uploads to the server.
    """
    try:
        # Validate file type
        if not file.filename.endswith('.jar'):
            raise HTTPException(status_code=400, detail="Only .jar files allowed")
        
        # Save file to server-mods directory
        file_path = SERVER_MODS_DIR / file.filename
        
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(file.file, f)
        
        # Calculate checksum
        checksum = calculate_checksum(file_path)
        file_size = file_path.stat().st_size
        
        # Parse mod name and version from filename
        # Simple parsing: filename-version.jar
        name_parts = file.filename.replace('.jar', '').split('-')
        mod_name = name_parts[0] if name_parts else file.filename
        mod_version = name_parts[1] if len(name_parts) > 1 else "1.0.0"
        
        # Save to database
        mod_id = db.create_mod(
            name=mod_name,
            version=mod_version,
            file_name=file.filename,
            file_path=str(file_path),
            file_size=file_size,
            checksum=checksum,
            author_id=user_id,
            environment=environment
        )
        
        # Create deployment record
        deployment_id = db.create_deployment(
            mod_id=mod_id,
            environment=environment,
            user_id=user_id,
            status="success",
            deployment_type="upload"
        )
        
        # Log activity
        db.log_activity(
            user_id,
            "upload_mod",
            {
                "mod_id": mod_id,
                "mod_name": mod_name,
                "environment": environment
            }
        )
        
        return {
            "success": True,
            "message": "Mod uploaded successfully",
            "mod_id": mod_id,
            "deployment_id": deployment_id,
            "checksum": checksum
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/dev/mods/{mod_id}")
async def delete_mod(mod_id: int, user_id: int = 1):
    """Delete a mod"""
    mod = db.get_mod_by_id(mod_id)
    
    if not mod:
        raise HTTPException(status_code=404, detail="Mod not found")
    
    # Delete file
    try:
        file_path = Path(mod['file_path'])
        if file_path.exists():
            file_path.unlink()
    except:
        pass
    
    # Delete from database
    db.delete_mod(mod_id)
    
    # Log activity
    db.log_activity(
        user_id,
        "delete_mod",
        {"mod_id": mod_id, "mod_name": mod['name']}
    )
    
    return {
        "success": True,
        "message": "Mod deleted successfully"
    }


@app.get("/api/dev/mods/download/{filename}")
async def download_mod(filename: str):
    """Download a mod file"""
    file_path = SERVER_MODS_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Mod file not found")
    
    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type="application/java-archive"
    )


# === Server Control Endpoints ===

@app.get("/api/dev/server/status")
async def get_server_status():
    """Get server status"""
    is_online = check_server_online()
    
    status = {
        "online": is_online,
        "port": MINECRAFT_SERVER_PORT,
        "timestamp": datetime.now().isoformat()
    }
    
    # Record status in database
    db.record_server_status(
        environment="dev",
        status="online" if is_online else "offline",
        player_count=0  # TODO: Get actual player count via RCON
    )
    
    return {
        "success": True,
        "status": status
    }


@app.post("/api/dev/server/start")
async def start_server():
    """Start Minecraft server"""
    try:
        # Check if already running
        if check_server_online():
            return {
                "success": False,
                "message": "Server is already running"
            }
        
        # Look for start script
        start_script = PROJECT_ROOT / "START-SERVER.cmd"
        
        if not start_script.exists():
            raise HTTPException(
                status_code=404,
                detail="START-SERVER.cmd not found"
            )
        
        # Start server
        subprocess.Popen(
            [str(start_script)],
            cwd=str(PROJECT_ROOT),
            shell=True
        )
        
        return {
            "success": True,
            "message": "Server start command executed"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/dev/server/stop")
async def stop_server():
    """Stop Minecraft server"""
    try:
        # Look for stop script
        stop_script = PROJECT_ROOT / "STOP-SERVER.cmd"
        
        if not stop_script.exists():
            raise HTTPException(
                status_code=404,
                detail="STOP-SERVER.cmd not found"
            )
        
        # Stop server
        subprocess.run(
            [str(stop_script)],
            cwd=str(PROJECT_ROOT),
            shell=True
        )
        
        return {
            "success": True,
            "message": "Server stop command executed"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/dev/server/restart")
async def restart_server():
    """Restart Minecraft server"""
    try:
        # Stop then start
        await stop_server()
        await start_server()
        
        return {
            "success": True,
            "message": "Server restart initiated"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === Deployment Endpoints ===

@app.get("/api/dev/deployments")
async def get_deployments(environment: Optional[str] = None, limit: int = 50):
    """Get deployment history"""
    if environment:
        deployments = db.get_deployments_by_environment(environment, limit)
    else:
        deployments = db.get_recent_deployments(limit)
    
    return {
        "success": True,
        "count": len(deployments),
        "deployments": deployments
    }


@app.post("/api/dev/deployments")
async def create_deployment(
    mod_id: int,
    environment: str,
    user_id: int = 1,
    deployment_type: str = "manual"
):
    """Create a new deployment record"""
    deployment_id = db.create_deployment(
        mod_id=mod_id,
        environment=environment,
        user_id=user_id,
        status="pending",
        deployment_type=deployment_type
    )
    
    return {
        "success": True,
        "deployment_id": deployment_id
    }


# === Activity Logs Endpoints ===

@app.get("/api/dev/activity")
async def get_activity(limit: int = 100):
    """Get recent activity logs"""
    activities = db.get_recent_activity(limit)
    
    return {
        "success": True,
        "count": len(activities),
        "activities": activities
    }


@app.get("/api/dev/activity/user/{user_id}")
async def get_user_activity(user_id: int, limit: int = 50):
    """Get activity for specific user"""
    activities = db.get_user_activity(user_id, limit)
    
    return {
        "success": True,
        "user_id": user_id,
        "count": len(activities),
        "activities": activities
    }


# === Logs Endpoint ===

@app.get("/api/dev/logs/latest")
async def get_latest_logs(lines: int = 100):
    """Get latest log lines"""
    log_file = PROJECT_ROOT / "logs" / "latest.log"
    
    if not log_file.exists():
        return {
            "success": False,
            "message": "Log file not found"
        }
    
    try:
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            all_lines = f.readlines()
            latest_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
        
        return {
            "success": True,
            "lines": len(latest_lines),
            "logs": latest_lines
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === Main ===

if __name__ == "__main__":
    import uvicorn
    
    print("="*50)
    print("  DEVELOPMENT CONSOLE API")
    print("  Galion.Studio")
    print("="*50)
    print()
    print("Starting API server...")
    print(f"API available at: http://localhost:8080")
    print(f"API docs at: http://localhost:8080/docs")
    print()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info"
    )

