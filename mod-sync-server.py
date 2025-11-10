"""
Titan Mod Sync Server - PARALLEL ARCHITECTURE
Provides mod manifest API and high-speed parallel file downloads
for automatic client synchronization.

Built with First Principles:
- Multiple concurrent connections = faster downloads
- Streaming responses = lower memory usage
- Checksum verification = data integrity
- Auto-discovery = zero configuration
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json
import hashlib
from typing import List, Dict
import uvicorn
import aiofiles
import asyncio
from datetime import datetime

app = FastAPI(
    title="Titan Mod Sync API", 
    version="2.0.0",
    description="High-performance parallel mod distribution system"
)

# Enable CORS for parallel downloads from browser/client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
MODS_DIR = Path("server-mods")
PACKAGES_DIR = Path("minecraft-packages")
FORGE_VERSION = "1.21.1-52.0.29"
MC_VERSION = "1.21.1"

# Ensure directories exist
MODS_DIR.mkdir(exist_ok=True)
PACKAGES_DIR.mkdir(exist_ok=True)

def calculate_checksum(file_path: Path) -> str:
    """Calculate SHA256 checksum of a file"""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def scan_mods() -> List[Dict]:
    """Scan mods directory and generate manifest"""
    mods = []
    
    for mod_file in MODS_DIR.glob("*.jar"):
        # Parse mod filename (usually: modname-version.jar)
        name = mod_file.stem
        
        # Calculate checksum
        checksum = calculate_checksum(mod_file)
        size = mod_file.stat().st_size
        
        mods.append({
            "id": name.lower().replace(" ", "-"),
            "name": name,
            "file": mod_file.name,
            "url": f"/api/mods/download/{mod_file.name}",
            "checksum": f"sha256:{checksum}",
            "size": size,
            "required": True
        })
    
    return mods

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "Titan Mod Sync API",
        "version": "1.0.0",
        "endpoints": {
            "manifest": "/api/mods/manifest",
            "download": "/api/mods/download/{filename}"
        }
    }

@app.get("/api/mods/manifest")
async def get_mod_manifest():
    """
    Get list of all required mods for the server
    
    Returns:
        JSON manifest with mod information
    """
    mods = scan_mods()
    
    manifest = {
        "server": {
            "name": "Titan Server",
            "address": "localhost:25565",
            "version": MC_VERSION
        },
        "forge": {
            "version": FORGE_VERSION,
            "required": True
        },
        "mods": mods,
        "total_size": sum(m["size"] for m in mods),
        "mod_count": len(mods)
    }
    
    return manifest

@app.get("/api/mods/download/{filename}")
async def download_mod(filename: str, request: Request):
    """
    Download a specific mod file with streaming support for parallel downloads.
    Supports HTTP range requests for resume capability.
    
    Args:
        filename: Name of the mod JAR file
    
    Returns:
        Streaming file download
    """
    file_path = MODS_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Mod file '{filename}' not found")
    
    if not file_path.suffix == ".jar":
        raise HTTPException(status_code=400, detail="Only JAR files can be downloaded")
    
    # Log download start
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Downloading: {filename}")
    
    # Use FileResponse for simplicity (FastAPI handles streaming automatically)
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/java-archive",
        headers={
            "Accept-Ranges": "bytes",  # Enable range requests for parallel downloads
            "Cache-Control": "public, max-age=31536000",  # Cache for 1 year
        }
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    mods = scan_mods()
    total_size = sum(m["size"] for m in mods)
    return {
        "status": "healthy",
        "mods_available": len(mods),
        "total_size_mb": round(total_size / 1024 / 1024, 2),
        "mods_directory": str(MODS_DIR.absolute()),
        "supports_parallel": True,
        "supports_resume": True
    }

@app.get("/api/mods/verify/{filename}")
async def verify_mod(filename: str, checksum: str):
    """
    Verify if a mod file matches the expected checksum.
    Allows clients to skip re-downloading if they already have the file.
    
    Args:
        filename: Name of the mod JAR file
        checksum: Expected checksum (format: sha256:hash)
    
    Returns:
        Verification result
    """
    file_path = MODS_DIR / filename
    
    if not file_path.exists():
        return {"valid": False, "reason": "file_not_found"}
    
    actual_checksum = f"sha256:{calculate_checksum(file_path)}"
    
    if actual_checksum == checksum:
        return {"valid": True, "checksum": actual_checksum}
    else:
        return {"valid": False, "reason": "checksum_mismatch", "expected": checksum, "actual": actual_checksum}

@app.get("/api/packages/list")
async def list_packages():
    """
    List all available complete Minecraft packages.
    These are pre-configured .minecraft directories ready to extract and play.
    
    Returns:
        List of available packages
    """
    packages = []
    
    for package_file in PACKAGES_DIR.glob("*.zip"):
        # Look for accompanying manifest
        manifest_file = package_file.with_suffix('.json')
        
        if manifest_file.exists():
            with open(manifest_file, 'r') as f:
                manifest = json.load(f)
                packages.append(manifest)
        else:
            # Create basic info
            packages.append({
                "name": package_file.stem,
                "file": package_file.name,
                "size": package_file.stat().st_size,
                "checksum": f"sha256:{calculate_checksum(package_file)}"
            })
    
    return {
        "packages": packages,
        "count": len(packages),
        "description": "Complete Minecraft installations - extract and play!"
    }

@app.get("/api/packages/download/{filename}")
async def download_package(filename: str, request: Request):
    """
    Download a complete Minecraft package.
    Fast single-file download of entire pre-configured setup.
    
    Args:
        filename: Name of the package ZIP file
    
    Returns:
        Package file for download
    """
    file_path = PACKAGES_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Package '{filename}' not found")
    
    if not file_path.suffix == ".zip":
        raise HTTPException(status_code=400, detail="Only ZIP packages can be downloaded")
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Downloading package: {filename}")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/zip",
        headers={
            "Accept-Ranges": "bytes",
            "Cache-Control": "public, max-age=86400",
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )

@app.get("/api/packages/info/{package_name}")
async def get_package_info(package_name: str):
    """
    Get detailed information about a package.
    
    Args:
        package_name: Name of the package (without .zip extension)
    
    Returns:
        Package manifest with details
    """
    manifest_file = PACKAGES_DIR / f"{package_name}.json"
    
    if not manifest_file.exists():
        raise HTTPException(status_code=404, detail=f"Package info for '{package_name}' not found")
    
    with open(manifest_file, 'r') as f:
        manifest = json.load(f)
    
    return manifest

if __name__ == "__main__":
    print("=" * 60)
    print("  TITAN MOD SYNC SERVER")
    print("=" * 60)
    print()
    print(f"Minecraft Version: {MC_VERSION}")
    print(f"Forge Version: {FORGE_VERSION}")
    print(f"Mods Directory: {MODS_DIR.absolute()}")
    print()
    
    # Check for mods
    mods = scan_mods()
    print(f"Found {len(mods)} mods:")
    for mod in mods:
        size_mb = mod['size'] / 1024 / 1024
        print(f"  • {mod['name']} ({size_mb:.2f} MB)")
    print()
    
    if len(mods) == 0:
        print("[!] No mods found!")
        print(f"    Add JAR files to: {MODS_DIR.absolute()}")
        print()
    
    print("Starting server on http://localhost:8080")
    print("API Docs: http://localhost:8080/docs")
    print()
    
    uvicorn.run(app, host="0.0.0.0", port=8080)

