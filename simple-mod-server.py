#!/usr/bin/env python3
"""
ULTRA-SIMPLE Mod Server - Musk Style: Delete complexity, ship fast
Just serves mods from a directory. No fancy APIs.
"""
import http.server
import socketserver
import json
from pathlib import Path

PORT = 8080
MODS_DIR = Path("server-mods")
MODS_DIR.mkdir(exist_ok=True)

class ModHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve manifest
        if self.path == "/manifest.json":
            mods = []
            for mod_file in MODS_DIR.glob("*.jar"):
                mods.append({
                    "name": mod_file.name,
                    "url": f"/mods/{mod_file.name}",
                    "size": mod_file.stat().st_size
                })
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"mods": mods}).encode())
            return
        
        # Serve mod files
        if self.path.startswith("/mods/"):
            filename = self.path.replace("/mods/", "")
            filepath = MODS_DIR / filename
            if filepath.exists():
                self.send_response(200)
                self.send_header("Content-Type", "application/octet-stream")
                self.end_headers()
                with open(filepath, 'rb') as f:
                    self.wfile.write(f.read())
                return
        
        # Default response
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        html = f"""
        <h1>Titan Mod Server</h1>
        <p>Mods available: {len(list(MODS_DIR.glob('*.jar')))}</p>
        <p><a href="/manifest.json">View Manifest</a></p>
        """
        self.wfile.write(html.encode())

if __name__ == "__main__":
    print("=" * 60)
    print("TITAN MOD SERVER - SIMPLE & FAST")
    print("=" * 60)
    print(f"Serving mods from: {MODS_DIR.absolute()}")
    print(f"Mods found: {len(list(MODS_DIR.glob('*.jar')))}")
    print(f"\nServer: http://localhost:{PORT}")
    print(f"Manifest: http://localhost:{PORT}/manifest.json")
    print("=" * 60)
    
    with socketserver.TCPServer(("", PORT), ModHandler) as httpd:
        httpd.serve_forever()

