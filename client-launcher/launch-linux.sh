#!/bin/bash
# Galion Studio Launcher - Linux Launch Script
# This script launches the Minecraft launcher on Linux

echo "================================================"
echo "Galion Studio Minecraft Launcher"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo ""
    echo "Please install Python 3.7 or higher:"
    echo "  sudo apt install python3"
    echo ""
    exit 1
fi

# Check if tkinter is installed
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: tkinter is not installed"
    echo ""
    echo "Please install tkinter:"
    echo "  sudo apt install python3-tk"
    echo ""
    exit 1
fi

# Launch the launcher
echo "Starting launcher..."
echo ""
python3 launcher.py

# Check if there was an error
if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Launcher failed to start"
    echo ""
    exit 1
fi

echo ""
echo "Launcher closed."

