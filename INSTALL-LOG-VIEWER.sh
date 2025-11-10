#!/bin/bash
# ONE-COMMAND INSTALL: Titan Log Viewer
# Run this on your VPS

set -e

echo "═══════════════════════════════════════"
echo "   ⚡ TITAN LOG VIEWER INSTALLER ⚡"
echo "═══════════════════════════════════════"
echo ""

# Install dependencies
echo "[1/4] Installing Python and dependencies..."
apt update -qq
apt install -y python3 python3-pip -qq

# Create directory structure
echo "[2/4] Creating directory structure..."
mkdir -p /opt/titan-logs/templates
cd /opt/titan-logs

# Install Python packages
echo "[3/4] Installing Flask and SocketIO..."
pip3 install flask flask-socketio python-socketio eventlet -q

# Create app.py
echo "[4/4] Creating log viewer application..."
cat > /opt/titan-logs/app.py << 'PYEOF'
#!/usr/bin/env python3
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import subprocess
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'titan-logs-2025'
socketio = SocketIO(app, cors_allowed_origins="*")

def get_docker_logs():
    try:
        process = subprocess.Popen(
            ['docker', 'logs', '-f', '--tail', '100', 'mc'],
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def status():
    try:
        result = subprocess.run(
            ['docker', 'ps', '--filter', 'name=mc', '--format', '{{.Status}}'],
            capture_output=True,
            text=True,
            cwd='/opt/mc'
        )
        mc_status = result.stdout.strip() if result.stdout else "Not Running"
        return jsonify({
            'minecraft': mc_status,
            'players': '0',
            'ip': '54.37.223.40:25565',
            'domain': 'mc.galion.studio'
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@socketio.on('connect')
def handle_connect():
    socketio.emit('message', {'data': 'Connected to Titan Log Viewer'})
    threading.Thread(target=get_docker_logs, daemon=True).start()

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 TITAN LOG VIEWER")
    print("=" * 60)
    print(f"📊 Dashboard: http://54.37.223.40:8080")
    print("=" * 60)
    socketio.run(app, host='0.0.0.0', port=8080, debug=False)
PYEOF

# Create HTML template (simplified version)
cat > /opt/titan-logs/templates/index.html << 'HTMLEOF'
<!DOCTYPE html>
<html>
<head>
    <title>⚡ Titan Logs</title>
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
    <style>
        body { background: #0a0e27; color: #00ff41; font-family: monospace; margin: 0; padding: 20px; }
        h1 { color: #ffd700; text-align: center; }
        #logs { background: #1a1e3a; padding: 20px; border-radius: 10px; height: 80vh; overflow-y: auto; }
        .log-line { padding: 5px; border-left: 3px solid #667eea; margin: 5px 0; padding-left: 10px; }
        .error { border-left-color: #f56565; color: #fc8181; }
        .success { border-left-color: #48bb78; color: #9ae6b4; }
        .status { text-align: center; padding: 10px; background: #667eea; color: white; border-radius: 5px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="status" id="status">🔄 Connecting...</div>
    <h1>⚡ TITAN SERVER LOGS ⚡</h1>
    <div id="logs"></div>
    <script>
        const socket = io();
        socket.on('connect', () => {
            document.getElementById('status').textContent = '🟢 Connected';
            addLog('Connected to server', 'success');
        });
        socket.on('minecraft_log', (msg) => addLog(msg.data));
        socket.on('message', (msg) => addLog(msg.data, 'success'));
        function addLog(text, type = '') {
            const logs = document.getElementById('logs');
            const line = document.createElement('div');
            line.className = 'log-line ' + type;
            line.textContent = '[' + new Date().toLocaleTimeString() + '] ' + text;
            logs.appendChild(line);
            logs.scrollTop = logs.scrollHeight;
        }
    </script>
</body>
</html>
HTMLEOF

chmod +x /opt/titan-logs/app.py

echo ""
echo "═══════════════════════════════════════"
echo "   ✅ INSTALLATION COMPLETE ✅"
echo "═══════════════════════════════════════"
echo ""
echo "🚀 TO START LOG VIEWER:"
echo "   python3 /opt/titan-logs/app.py"
echo ""
echo "🌐 ACCESS AT:"
echo "   http://54.37.223.40:8080"
echo ""
echo "💡 RUN IN BACKGROUND:"
echo "   nohup python3 /opt/titan-logs/app.py > /dev/null 2>&1 &"
echo ""
echo "═══════════════════════════════════════"

