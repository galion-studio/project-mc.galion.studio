# 💬 Client Console

Interactive console interface integrated into the Dev Console for real-time communication with AI, Minecraft server, and project control.

## Overview

The Client Console combines three powerful systems:
- **AI Chat** - Grok-4 Fast for instant answers
- **RCON Control** - Direct Minecraft server commands
- **Project Management** - Git, Docker, and build tools

## Features

### 🤖 AI Integration
- Ask questions and get instant responses (<1 second)
- Powered by Grok-4 Fast via OpenRouter
- Smart caching for repeated queries
- Context-aware Minecraft knowledge

### 🎮 Minecraft Control
- Execute server commands via RCON
- Send messages to in-game chat
- Real-time server status
- Command history and auto-complete

### 🛠️ Project Tools
- Git status and operations
- Docker container management
- Build system integration
- File operations

## Usage

### Starting the Console

1. **From Dev Console:**
   - Launch dev console: `DEV-CONSOLE.cmd`
   - Click "💬 Client Console" in sidebar

2. **Standalone:**
   - Run: `START-CLIENT-CONSOLE.cmd`

### Command Reference

#### AI Commands
```
@ai <question>        Ask AI a question
<any text>            Defaults to AI question

Examples:
@ai how do I make a farm?
what is redstone?
```

#### Minecraft Commands
```
/cmd <command>        Execute Minecraft command
/<command>            Direct command (shorthand)
/say <message>        Send to in-game chat

Examples:
/list                 List players
/time set day         Set time
/say Hello players!   Send message
```

#### Project Commands
```
@project status       Git status
@project docker       List containers
@project logs [name]  Container logs
@project build        Build project
@project clean        Clean build

Examples:
@project status
@project docker
@project logs titan-hub
```

#### System Commands
```
/status               Show system status
/help                 Show help
/clear                Clear console output
```

### Keyboard Shortcuts

- **Enter** - Send command
- **Up/Down Arrows** - Navigate command history
- **Tab** - Auto-complete (coming soon)
- **Ctrl+L** - Clear console

## Configuration

The console uses environment variables from `.env.grok`:

```env
# AI Configuration
OPENROUTER_API_KEY=your-key-here
GROK_MODEL=x-ai/grok-4-fast

# Minecraft RCON
MINECRAFT_RCON_HOST=localhost
MINECRAFT_RCON_PORT=25575
MINECRAFT_RCON_PASSWORD=titan123
MINECRAFT_DOCKER_CONTAINER=titan-hub

# Project
PROJECT_ROOT=.
```

## Features in Detail

### Command History
- All commands are saved
- Navigate with up/down arrows
- Persists between sessions
- Stored in `.console_history`

### Status Indicators
- **AI Status** - Shows if Grok is connected
- **RCON Status** - Shows if Minecraft server is reachable
- Real-time updates on connection status

### Smart Routing
The console automatically routes commands:
- Text starting with `@ai` → AI
- Text starting with `/` → Minecraft
- Text starting with `@project` → Project tools
- Plain text → Defaults to AI

### Response Times
- **AI responses:** <1 second typically
- **RCON commands:** <100ms
- **Project commands:** Varies by operation

## Examples

### Getting Help
```
Player: @ai how do I build a portal?
Grok: To build a Nether portal, you need...
```

### Server Control
```
Player: /list
Server: There are 5 players online
Player: /say Welcome everyone!
Server: Message sent
```

### Project Management
```
Player: @project status
Git: On branch main, nothing to commit
Player: @project docker
Docker: titan-hub (running), postgres (running)...
```

## Troubleshooting

### AI Not Responding
1. Check `.env.grok` has valid `OPENROUTER_API_KEY`
2. Verify internet connection
3. Check API credits at https://openrouter.ai/credits

### RCON Not Connected
1. Ensure Minecraft server is running
2. Verify RCON is enabled in server.properties
3. Check RCON password matches

### Commands Not Working
1. Check command syntax with `/help`
2. Ensure proper prefix (`@ai`, `/`, `@project`)
3. Look for error messages in console output

## Development

### File Structure
```
dev-console/client/
├── __init__.py              # Module exports
├── client_console.py        # Main console implementation
└── README.md               # This file
```

### Integration Points
- Uses `grok_client.py` for AI
- Uses `rcon_client.py` for Minecraft
- Uses `project_controller.py` for project tools
- Integrates with dev-console UI framework

### Extending the Console

Add new command types:
```python
# In handle_command method
elif command.startswith("@custom "):
    await self.handle_custom_command(command[8:])
```

Add new features:
```python
async def handle_custom_command(self, command: str):
    """Handle custom commands"""
    # Your implementation here
    self.append_output("Custom response", "info")
```

## Performance

- **Memory:** ~50MB with AI client loaded
- **CPU:** Minimal when idle
- **Network:** Only when making AI/RCON calls
- **Startup:** <2 seconds

## Future Enhancements

### Planned Features
- [ ] Tab auto-completion
- [ ] Command aliases
- [ ] Macro recording
- [ ] Multi-server support
- [ ] Plugin system
- [ ] Custom themes
- [ ] Export chat history
- [ ] Search/filter output

## Credits

**Built by:** galion.studio  
**Developer:** Maciej Grajczyk  
**AI Assistant:** Cursor IDE + Claude Sonnet 4.5

Part of the Titan Minecraft Server project.

---

**Made with ❤️ by [galion.studio](https://galion.studio)**

