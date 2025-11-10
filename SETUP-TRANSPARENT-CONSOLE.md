# 🚀 Quick Setup Guide - Transparent Developer Console

**Get up and running in 5 minutes!**

## Step 1: Install Python (if not already installed)

### Windows
1. Download Python 3.8+ from [python.org](https://www.python.org/downloads/)
2. **Important:** Check "Add Python to PATH" during installation
3. Verify installation:
```bash
python --version
```

## Step 2: Install Dependencies

Open PowerShell or Command Prompt in the project directory:

```bash
pip install -r requirements.txt
```

This installs:
- `customtkinter` - Modern GUI framework
- `python-dotenv` - Configuration management
- `colorama` - Colored console output
- `aiohttp` - AI API client
- `fastapi` - Chat server
- And more...

## Step 3: Configure Your API Keys

### Get OpenRouter API Key (for AI features)

1. Go to [OpenRouter.ai](https://openrouter.ai/)
2. Sign up for a free account
3. Go to [Keys page](https://openrouter.ai/keys)
4. Create a new API key
5. Copy your API key

### Add to Configuration

Open `.env.grok` file and add your API key:

```bash
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

That's it! All other settings have defaults.

## Step 4: Launch the Console

Double-click:
```
START-TRANSPARENT-CONSOLE.cmd
```

Or run manually:
```bash
cd dev-console
python transparent_console.py
```

## Step 5: Explore Features

### Configuration Tab 📋
- View all settings
- Copy configuration
- Export full config

### Console Tab 💻
- Interactive command line
- Easy text copying
- Real-time output

### Server Control Tab 🎮
- Start/Stop server
- Execute commands
- Quick actions

### Secrets & API Keys Tab 🔑
- All secrets visible
- Edit any value
- Save changes instantly

## 🎯 Quick Configuration

### Minimum Setup (AI Features Only)
Just need one thing:
```bash
OPENROUTER_API_KEY=your-key-here
```

### Full Setup (All Features)
Edit `.env.grok` and `.env` files with your values:

**AI Configuration** (`.env.grok`):
- `OPENROUTER_API_KEY` - Required for AI
- `GROK_MODEL` - Which AI model to use
- `MINECRAFT_RCON_PASSWORD` - Server control

**Server Configuration** (`.env`):
- `MC_VERSION` - Minecraft version
- `SERVER_PORT` - Server port
- `POSTGRES_PASSWORD` - Database (if using)
- `REDIS_PASSWORD` - Cache (if using)
- `VELOCITY_SECRET` - Proxy (if using)

## 💡 Pro Tips

### 1. Copy Any Configuration Value
- Go to "Secrets & API Keys" tab
- Click 📋 button next to any value
- Paste anywhere (Ctrl+V)

### 2. Export Everything
- Go to "Configuration" tab
- Click "Export Full Config"
- Save backup of all settings

### 3. Quick Command Execution
- Go to "Console" tab
- Type command and press Enter
- All text is copyable!

### 4. Validate Configuration
- Go to "Configuration" tab
- Click "Refresh"
- See any missing or invalid values

## 🔧 Troubleshooting

### "Python is not recognized"
Add Python to your PATH:
1. Search "Environment Variables" in Windows
2. Edit System Variables
3. Add Python installation path

### "Module not found: customtkinter"
Install manually:
```bash
pip install customtkinter
```

### "Cannot connect to AI"
Check your API key:
1. Verify key is correct in `.env.grok`
2. Check credits at [OpenRouter Credits](https://openrouter.ai/credits)
3. Try the test:
```bash
python test-openrouter-connection.py
```

### "Configuration not loading"
1. Check `.env.grok` exists in project root
2. Check `.env` exists in project root
3. Run config test:
```bash
cd dev-console
python config_manager.py
```

## 🎮 Example Commands

### In Console Tab

**Minecraft Commands:**
```
/list
/time set day
/gamemode creative @a
/weather clear
```

**AI Questions:**
```
@ai How do I create a custom mod?
@ai What's the best way to optimize server performance?
@ai Explain how RCON works
```

## 📚 Next Steps

1. ✅ Setup complete!
2. Explore the Configuration tab
3. Set your API keys in Secrets tab
4. Try the Server Control features
5. Use the Console for commands

## 🤝 Need Help?

- Check [Transparent Console README](dev-console/TRANSPARENT-CONSOLE-README.md)
- Read [Main Project README](README.md)
- Check [AI Features Guide](AI-FEATURES-COMPLETE.md)

## 🔐 Security Reminder

This console shows all secrets for transparency:
- Keep the window secure
- Don't share screenshots with secrets visible
- Use "Export Full Config" carefully
- Close when not in use

---

**Ready to go!** 🚀

Launch with: `START-TRANSPARENT-CONSOLE.cmd`

*Built with ❤️ for mc.galion.studio*

