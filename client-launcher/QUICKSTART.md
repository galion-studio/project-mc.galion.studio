# Quick Start Guide - Galion Studio Launcher

Simple instructions to get started with the custom Minecraft launcher.

## For Users (Quick Test)

### Windows
1. Double-click `LAUNCH-WINDOWS.bat`
2. Enter your Minecraft username
3. Click PLAY

### Linux
1. Open terminal in this folder
2. Run: `./launch-linux.sh`
3. Enter your Minecraft username
4. Click PLAY

## For Developers (Build Executable)

### Build Standalone Executable

To create a distributable .exe or binary file:

```bash
python build.py
```

This will:
- Install PyInstaller if needed
- Build a standalone executable
- Save it to the `dist/` folder

### Windows Executable
After building, you'll get:
- `dist/GalionLauncher.exe` - Ready to distribute!

Users can simply double-click this file. No Python installation required!

### Linux Binary
After building, you'll get:
- `dist/GalionLauncher` - Ready to distribute!

Users need to:
1. Make it executable: `chmod +x GalionLauncher`
2. Run it: `./GalionLauncher`

## Testing the Launcher

Test it now (requires Python):

**Windows:**
```
python launcher.py
```

**Linux:**
```
python3 launcher.py
```

## File Structure

```
client-launcher/
├── launcher.py              # Main launcher code
├── build.py                 # Build script for executables
├── requirements.txt         # Python dependencies
├── LAUNCH-WINDOWS.bat       # Windows quick launch
├── launch-linux.sh          # Linux quick launch
├── README.md                # Full documentation
└── QUICKSTART.md            # This file
```

## Features

✅ Clean, simple interface  
✅ Remembers your username  
✅ Auto-detects Minecraft installation  
✅ Cross-platform (Windows & Linux)  
✅ Lightweight (~5MB executable)  

## Customization

Edit `launcher.py` to customize:
- Server address (line 16: `SERVER_ADDRESS`)
- Server name (line 17: `SERVER_NAME`)
- Launcher colors (lines 51-60: color codes)
- Window size (line 32: geometry)

## Next Steps

1. **Test the launcher**: Run `python launcher.py`
2. **Build executable**: Run `python build.py`
3. **Distribute**: Share the exe/binary with your players!

## Need Help?

- Check `README.md` for detailed documentation
- Make sure Minecraft is installed
- Ensure Python 3.7+ is installed for development

---
*Created for the Galion Studio Minecraft Server*

