#!/usr/bin/env python3
"""
TITAN LOG VIEWER
Real-time web dashboard for VPS and Minecraft server logs
Access: http://54.37.223.40:8080
"""

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import subprocess
import threading
import time
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'titan-logs-2025'
socketio = SocketIO(app, cors_allowed_origins="*")

# Log file paths
MC_LOG_PATH = "/opt/mc/data/logs/latest.log"
SYSTEM_LOG_PATH = "/var/log/syslog"

def tail_file(filepath, callback, prefix=""):
    """Tail a file and send new lines via callback"""
    try:
        # Use tail -f to follow file
        process = subprocess.Popen(
            ['tail', '-f', '-n', '50', filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        for line in iter(process.stdout.readline, ''):
            if line:
                callback(f"{prefix}{line.strip()}")
    except Exception as e:
        callback(f"{prefix}ERROR: {str(e)}")

def get_docker_logs():
    """Get live Docker logs"""
    try:
        process = subprocess.Popen(
            ['docker', 'logs', '-f', '--tail', '50', 'mc'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            cwd='/opt/mc'
        )
        
        for line in iter(process.stdout.readline, ''):
            if line:
                socketio.emit('minecraft_log', {'data': line.strip()})
    except Exception as e:
        socketio.emit('minecraft_log', {'data': f'ERROR: {str(e)}'})

def monitor_system():
    """Monitor system resources and logs"""
    while True:
        try:
            # Get system stats
            cpu = subprocess.check_output(['top', '-bn1']).decode('utf-8').split('\n')[2]
            memory = subprocess.check_output(['free', '-h']).decode('utf-8').split('\n')[1]
            
            socketio.emit('system_stats', {
                'cpu': cpu,
                'memory': memory,
                'time': time.strftime('%Y-%m-%d %H:%M:%S')
            })
            
            time.sleep(2)
        except Exception as e:
            socketio.emit('system_log', {'data': f'ERROR: {str(e)}'})
            time.sleep(5)

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/status')
def status():
    """Get current server status"""
    try:
        # Check if Minecraft container is running
        result = subprocess.run(
            ['docker', 'ps', '--filter', 'name=mc', '--format', '{{.Status}}'],
            capture_output=True,
            text=True,
            cwd='/opt/mc'
        )
        
        mc_status = result.stdout.strip() if result.stdout else "Not Running"
        
        # Get player count from logs
        players = "0"
        try:
            player_line = subprocess.check_output(
                ['docker', 'exec', 'mc', 'rcon-cli', 'list'],
                stderr=subprocess.DEVNULL
            ).decode('utf-8')
            players = player_line.split()[2] if len(player_line.split()) > 2 else "0"
        except:
            pass
        
        return jsonify({
            'minecraft': mc_status,
            'players': players,
            'ip': '54.37.223.40:25565',
            'domain': 'mc.galion.studio'
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected')
    socketio.emit('message', {'data': 'Connected to Titan Log Viewer'})
    
    # Start log streaming threads
    threading.Thread(target=get_docker_logs, daemon=True).start()

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

@socketio.on('restart_server')
def handle_restart():
    """Restart Minecraft server"""
    try:
        subprocess.run(['docker-compose', 'restart'], cwd='/opt/mc')
        socketio.emit('message', {'data': 'Server restart initiated...'})
    except Exception as e:
        socketio.emit('message', {'data': f'Restart failed: {str(e)}'})

if __name__ == '__main__':
    # Start system monitoring thread
    threading.Thread(target=monitor_system, daemon=True).start()
    
    print("=" * 50)
    print("🚀 TITAN LOG VIEWER STARTING")
    print("=" * 50)
    print(f"📊 Dashboard: http://54.37.223.40:8080")
    print(f"🔒 Local: http://localhost:8080")
    print("=" * 50)
    
    socketio.run(app, host='0.0.0.0', port=8080, debug=False)

