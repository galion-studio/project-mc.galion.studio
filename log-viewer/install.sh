#!/bin/bash
# Install Titan Log Viewer on VPS

echo "⚡ INSTALLING TITAN LOG VIEWER ⚡"
echo ""

# Install Python and pip
apt update
apt install -y python3 python3-pip python3-venv

# Create directory
mkdir -p /opt/titan-logs
cd /opt/titan-logs

# Install dependencies
pip3 install flask flask-socketio python-socketio eventlet

# Download files (you'll need to copy them)
echo "✅ Dependencies installed"
echo ""
echo "📋 Next steps:"
echo "1. Copy app.py to /opt/titan-logs/"
echo "2. Create templates directory: mkdir -p /opt/titan-logs/templates"
echo "3. Copy index.html to /opt/titan-logs/templates/"
echo "4. Run: python3 /opt/titan-logs/app.py"
echo ""
echo "🌐 Access at: http://54.37.223.40:8080"

