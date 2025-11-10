# 🔧 Transparent Developer Console

**Full Configuration Visibility & Control for mc.galion.studio**

## ✨ Features

### 1. **Easy Text Copying**
- All text is selectable and copyable
- Click and drag to select any text
- `Ctrl+C` to copy
- Perfect for sharing configuration or debugging

### 2. **Full Configuration Transparency**
- All settings visible in one place
- No hidden configuration
- Easy-to-read format
- Export functionality

### 3. **Secrets & API Keys Management**
- OpenRouter AI API Key
- VPN credentials
- Database passwords
- RCON passwords
- Velocity secrets
- All editable in the UI

### 4. **Server Control Panel**
- Start/Stop/Restart server
- Execute Minecraft commands
- Quick actions (List players, Set time, etc.)
- Real-time status monitoring

### 5. **Interactive Console**
- Type commands directly
- AI integration (coming soon)
- Minecraft RCON commands
- Command history

## 🚀 Quick Start

### Windows
```bash
START-TRANSPARENT-CONSOLE.cmd
```

### Manual Launch
```bash
cd dev-console
python transparent_console.py
```

## 📋 Configuration Files

The console reads from:
- `.env.grok` - AI and chat configuration
- `.env` - Server and database configuration
- `launcher_config.json` - Launcher settings

## 🔑 Secrets Management

All secrets are visible and editable:

### AI Configuration
- `OPENROUTER_API_KEY` - Get from https://openrouter.ai/keys
- `GROK_MODEL` - AI model selection
- Performance settings

### Minecraft Server
- `MINECRAFT_RCON_PASSWORD` - Server control password
- `MINECRAFT_DOCKER_CONTAINER` - Container name
- Server port and settings

### Database
- `POSTGRES_PASSWORD` - Database password
- `REDIS_PASSWORD` - Redis cache password
- Connection details

### Network & VPN
- `VELOCITY_SECRET` - Proxy security key
- `VPN_PASSWORD` - VPN credentials
- Domain configuration

### Monitoring
- `GRAFANA_ADMIN_PASSWORD` - Dashboard access

## 💡 How to Use

### Configuration Tab
1. View all configuration in one place
2. Copy entire config with one click
3. Export full config (including secrets) to file
4. Validate configuration for missing values

### Console Tab
1. Type commands in the input box
2. Press Enter or click Send
3. All output is selectable
4. Use Ctrl+C to copy any text

### Server Control Tab
1. Quick action buttons for common tasks
2. Start/Stop/Restart server
3. Execute Minecraft commands
4. View logs and backups

### Secrets & API Keys Tab
1. All secrets visible in editable fields
2. Click the 📋 button to copy individual values
3. Edit any value directly
4. Click "Save All Changes" to persist

## 🔒 Security Note

This console shows all secrets for transparency. Keep this window secure:
- Don't share screenshots with visible secrets
- Close the window when not in use
- Use the "Export Full Config" feature carefully

## 🎯 Philosophy

**Open Source Transparency**
- No hidden configuration
- Everything is visible
- Everything is editable
- Full control to developers

## 📝 Examples

### Copy API Key
1. Go to "Secrets & API Keys" tab
2. Find `openrouter_api_key`
3. Click the 📋 button next to it
4. Paste anywhere (Ctrl+V)

### Export Full Configuration
1. Go to "Configuration" tab
2. Click "Export Full Config"
3. File saved as `CONFIG_EXPORT_FULL.txt`
4. Contains all secrets - keep secure!

### Execute Minecraft Command
1. Go to "Console" tab
2. Type: `/list`
3. Press Enter
4. See results in console output

### Update a Secret
1. Go to "Secrets & API Keys" tab
2. Find the setting you want to change
3. Edit the value in the text field
4. Click "Save All Changes"
5. Configuration files are updated

## 🛠 Troubleshooting

### Console Won't Start
```bash
# Install dependencies
pip install -r requirements.txt

# Or install specific packages
pip install customtkinter python-dotenv
```

### Configuration Not Loading
- Check that `.env.grok` exists in project root
- Check that `.env` exists in project root
- Run the config test:
```bash
cd dev-console
python config_manager.py
```

### Can't Copy Text
- Make sure you're clicking and dragging to select text
- Use Ctrl+C after selecting
- Try the "Copy All" button in Configuration tab

## 🚀 Advanced Features

### Command Aliases
- `/list` - List players
- `/time set day` - Set time to day
- `@ai <question>` - Ask AI assistant
- `/status` - Show server status

### Keyboard Shortcuts
- `Ctrl+C` - Copy selected text
- `Enter` - Execute command
- `Ctrl+A` - Select all text in field

## 📚 Related Documentation

- [Main Project README](../README.md)
- [Server Modes Guide](../SERVER-MODES-GUIDE.md)
- [AI Features Complete](../AI-FEATURES-COMPLETE.md)
- [Grok Quick Start](../QUICK-START-GROK.md)

## 🤝 Contributing

This is open source! Feel free to:
- Add new features
- Improve the UI
- Add more command shortcuts
- Enhance the configuration system

## 📄 License

Same as main project - fully open source

---

**Built with ❤️ for mc.galion.studio**

*Full Transparency • Complete Control • Developer First*

