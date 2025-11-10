# Galion Studio Minecraft Launcher

A simple, custom Minecraft launcher for the **mc.galion.studio** server.

## Features

- ✅ Simple and clean interface
- ✅ Cross-platform (Windows & Linux)
- ✅ Remembers your username
- ✅ Quick connect to Galion Studio server
- ✅ Lightweight and fast

## Requirements

- Python 3.7 or higher
- Minecraft installed on your system
- Internet connection

## Installation

### Windows

1. Make sure you have Python installed:
   ```
   python --version
   ```

2. Run the launcher:
   ```
   python launcher.py
   ```

### Linux

1. Make sure you have Python and tkinter installed:
   ```bash
   python3 --version
   sudo apt install python3-tk  # On Debian/Ubuntu
   ```

2. Run the launcher:
   ```bash
   python3 launcher.py
   ```

## Usage

1. **Launch the program**: Run `python launcher.py` (or `python3 launcher.py` on Linux)

2. **Enter your username**: Type your Minecraft player name

3. **Click PLAY**: The launcher will start Minecraft

4. **Connect to server**: 
   - Once in Minecraft, go to Multiplayer
   - Add server: `mc.galion.studio`
   - Join and play!

## Building Standalone Executable

To create a standalone .exe (Windows) or binary (Linux), use PyInstaller:

### Windows
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "GalionLauncher" launcher.py
```

### Linux
```bash
pip3 install pyinstaller
pyinstaller --onefile --windowed --name "GalionLauncher" launcher.py
```

The executable will be in the `dist/` folder.

## Configuration

The launcher saves your username in `launcher_config.json` for convenience.

## Troubleshooting

### Minecraft not found
- Make sure Minecraft is installed on your system
- The launcher looks in these locations:
  - Windows: `%APPDATA%\.minecraft`
  - Linux: `~/.minecraft`

### Can't launch Minecraft
- Make sure the official Minecraft Launcher is installed
- Try launching Minecraft manually first to verify it works

## Server Information

- **Server Address**: mc.galion.studio
- **Launcher Version**: 1.0.0

## License

This launcher is created for the Galion Studio Minecraft community.

## Support

For issues or questions, contact the server administrators.

