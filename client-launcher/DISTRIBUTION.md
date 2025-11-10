# Distribution Guide - Galion Studio Launcher

How to package and distribute the launcher to your players.

## Building for Distribution

### Step 1: Build the Executable

Run the build script:

```bash
# Windows or Linux
python build.py
```

This creates a standalone executable that players can use without installing Python.

### Step 2: Test the Executable

Before distributing, test the built executable:

**Windows:**
```
dist\GalionLauncher.exe
```

**Linux:**
```
chmod +x dist/GalionLauncher
./dist/GalionLauncher
```

### Step 3: Package for Distribution

Create a distribution package:

#### Windows Package

Create a folder with:
```
GalionLauncher-Windows/
├── GalionLauncher.exe
└── README.txt          # Simple instructions for players
```

Zip this folder: `GalionLauncher-Windows.zip`

#### Linux Package

Create a folder with:
```
GalionLauncher-Linux/
├── GalionLauncher
├── install.sh          # Optional: helper script
└── README.txt          # Simple instructions for players
```

Create tar.gz: `tar -czf GalionLauncher-Linux.tar.gz GalionLauncher-Linux/`

## Player Instructions Template

Create a simple `README.txt` for players:

```
GALION STUDIO MINECRAFT LAUNCHER
=================================

REQUIREMENTS:
- Minecraft Java Edition installed
- Internet connection

WINDOWS INSTRUCTIONS:
1. Extract this zip file
2. Double-click GalionLauncher.exe
3. Enter your Minecraft username
4. Click PLAY
5. Once Minecraft opens, go to Multiplayer
6. The server mc.galion.studio should be listed
7. Join and have fun!

LINUX INSTRUCTIONS:
1. Extract this archive
2. Open terminal in this folder
3. Run: chmod +x GalionLauncher
4. Run: ./GalionLauncher
5. Enter your Minecraft username
6. Click PLAY
7. Once Minecraft opens, go to Multiplayer
8. Add server: mc.galion.studio
9. Join and have fun!

TROUBLESHOOTING:
- Make sure Minecraft is installed first
- Make sure you can launch Minecraft normally
- Contact server admins for help

Server: mc.galion.studio
```

## Distribution Channels

### Option 1: Direct Download
- Upload to your server's website
- Provide download links in Discord/Forums
- Host on Google Drive, Dropbox, etc.

### Option 2: GitHub Releases
1. Create a GitHub repository for the launcher
2. Use GitHub Releases to host the binaries
3. Players can download from the Releases page

### Option 3: Server Integration
- Host on your server's CDN
- Add download link to your server website
- Include in welcome messages

## File Sizes

Typical executable sizes:
- Windows: ~8-12 MB
- Linux: ~10-15 MB

These are small enough to distribute easily.

## Version Updates

When you update the launcher:

1. Update version in `launcher.py` (line 18)
2. Rebuild: `python build.py`
3. Test the new executable
4. Package and redistribute
5. Notify players of the update

## Auto-Update (Future Feature)

To add auto-update capability:
1. Host a `version.json` file on your server
2. Add version check in launcher
3. Download and replace executable if needed

Example `version.json`:
```json
{
  "version": "1.0.1",
  "download_url": "https://mc.galion.studio/launcher/download",
  "changelog": "Fixed connection issues"
}
```

## Security Notes

- Build executables on a clean, secure machine
- Scan with antivirus before distributing
- Use HTTPS for download links
- Sign executables (optional but recommended)

### Code Signing (Optional)

**Windows:**
- Get a code signing certificate
- Sign with `signtool.exe`
- Prevents Windows SmartScreen warnings

**Linux:**
- Not typically required
- Can use GPG signatures

## Branding

To customize the launcher appearance:

1. **Add an icon**: 
   - Create `icon.ico` (Windows) or `icon.png` (Linux)
   - Add to PyInstaller command: `--icon=icon.ico`

2. **Change colors**:
   - Edit `launcher.py` color codes
   - Update header background color (line 51)

3. **Add logo**:
   - Place logo image in launcher folder
   - Update code to display it

## Monitoring

Track launcher usage:
- Add analytics (optional)
- Log launcher errors to server
- Monitor download counts

## Support

Prepare support resources:
- FAQ document
- Video tutorial
- Discord support channel
- Troubleshooting guide

## Legal

Include appropriate notices:
- Minecraft is property of Mojang/Microsoft
- This is a launcher, not the game
- Use in compliance with Minecraft EULA
- Server terms of service

---

**You're all set!** Build, test, package, and share your custom launcher with your community!

