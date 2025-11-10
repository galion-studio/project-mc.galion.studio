# 🚀 Quick Start Guide

Get the Development Minecraft Console running in **5 minutes**.

---

## Step 1: Install Dependencies (2 minutes)

```bash
cd dev-console
pip install -r requirements-dev-console.txt
```

**What gets installed**:
- CustomTkinter (Modern UI)
- FastAPI (Backend API)
- SQLite (Database)
- Git integration
- RCON client
- And more...

---

## Step 2: Start the Console (30 seconds)

### Windows

Double-click `DEV-CONSOLE.cmd` or run:

```cmd
DEV-CONSOLE.cmd
```

### Linux/Mac

```bash
python console_main.py
```

---

## Step 3: Login (10 seconds)

The console starts with a default admin account:

**Username**: `admin`  
**Password**: `admin123`

⚠️ **Important**: Change this password after first login!

---

## Step 4: Upload Your First Mod (1 minute)

1. Click **📦 Mods** in the sidebar
2. Drag and drop a `.jar` file into the upload zone
3. Or click the zone to browse for a file
4. Click **Upload Mod**
5. ✅ Done! Mod is deployed to Dev environment

---

## Step 5: Check Server Status (30 seconds)

1. Click **🖥️ Server** in the sidebar
2. See real-time server status
3. Click **▶️ START SERVER** if offline
4. Monitor player count and status

---

## Step 6: View Live Logs (30 seconds)

1. Click **📜 Logs** in the sidebar
2. See real-time log streaming
3. Use search bar to find specific entries
4. Filter by log level (INFO, WARN, ERROR)

---

## 🎉 You're Ready!

That's it! You now have a fully functional development console.

---

## Next Steps

### Enable Hot Reload

For instant mod updates without server restart:

1. Enable RCON in `server.properties`:
   ```properties
   enable-rcon=true
   rcon.port=25575
   rcon.password=your_password
   ```

2. Update `dev-console/config.py`:
   ```python
   RCON_PASSWORD = "your_password"
   ```

3. Install PlugManX on your server

4. Upload a mod → It auto-reloads!

### Explore Other Features

- **🗄️ Repository** - Version control and CDN
- **🌍 Environments** - Dev/Staging/Prod
- **👥 Team** - Activity feed and approvals
- **💡 Snippets** - Copy Minecraft code patterns
- **🔨 Builder** - Build mods with Gradle
- **🐛 Debugger** - Run RCON commands
- **📈 Profiler** - Monitor performance

---

## Common Tasks

### Upload a Mod

Navigate to **Mods** → Drag & drop `.jar` file → Click Upload

### Start Server

Navigate to **Server** → Click **▶️ START SERVER**

### View Logs

Navigate to **Logs** → Logs stream automatically

### Build a Mod

Navigate to **Builder** → Select project → Click **🔨 BUILD**

### Check Performance

Navigate to **Profiler** → Click **▶️ Start Profiling**

### Copy Code Snippet

Navigate to **Snippets** → Find pattern → Click **📋 Copy**

---

## Troubleshooting

### "Python not found"

Install Python 3.8+ from python.org

### "Dependencies failed to install"

Try upgrading pip first:
```bash
python -m pip install --upgrade pip
```

### "Database error"

Delete `dev-console/database/dev_console.db` and restart

### "Server won't start"

Check that `START-SERVER.cmd` exists in project root

### "Hot reload not working"

1. Check RCON is enabled
2. Verify password in config
3. Install PlugManX plugin
4. Restart server once

---

## Help & Support

- **Full docs**: Read `README.md`
- **Project status**: See `PROJECT-COMPLETE.md`
- **Configuration**: Edit `config.py`
- **Issues**: Check code comments (heavily documented)

---

## Default Credentials

**⚠️ CHANGE AFTER FIRST LOGIN**

Username: `admin`  
Password: `admin123`

---

## Quick Tips

✅ Use hot reload for instant testing  
✅ Check logs for debugging  
✅ Profile regularly to catch performance issues  
✅ Use snippets to speed up development  
✅ Commit mods with Git for version tracking  
✅ Promote Dev → Staging → Prod for safety  

---

**That's it! Now go build something amazing! 🚀**

