# Grok Console Chat System

Ultra-fast AI chat interface with Minecraft server control powered by Grok-4 Fast.

## Features

✨ **Core Features:**
- ⚡ Ultra-fast AI responses (<1 second typical)
- 🎮 Instant Minecraft RCON commands
- 💻 Project control operations (git, build, docker)
- 🖥️ Interactive terminal console
- 🌐 REST API server (FastAPI)
- 📊 Real-time status monitoring
- 💾 Response caching for speed

## Quick Start

### 1. Setup

1. **Copy environment configuration:**
   ```bash
   copy .env.grok.example .env.grok
   ```

2. **Edit `.env.grok` and set your API key:**
   ```bash
   XAI_API_KEY=your-xai-api-key-here
   ```
   Get your API key from: https://console.x.ai/

3. **Install dependencies:**
   ```bash
   pip install -r requirements-grok.txt
   ```

### 2. Run Console Chat (Interactive Terminal)

**Windows:**
```cmd
START-CONSOLE-CHAT.cmd
```

**Linux/Mac:**
```bash
python console-chat.py
```

### 3. Run In-Game AI Bridge (Minecraft Chat)

**Windows:**
```cmd
START-GROK-BRIDGE.cmd
```

Choose from:
- **NANO Bridge** - Minimal and fast
- **INSTANT Bridge** - Ultra-fast
- **FAST Bridge** - Full-featured with streaming

### 4. Run API Server (REST API)

**Windows:**
```cmd
START-CHAT-SERVER.cmd
```

**Linux/Mac:**
```bash
python chat-server.py
```

API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

## Usage

### Console Chat Commands

**AI Chat:**
```
@ai What is redstone?
@ai How do I create a plugin?
What is Minecraft?  (defaults to AI)
```

**Minecraft Commands:**
```
/say Hello players!
/cmd list
/list
/time set day
/gamemode creative
```

**Project Commands:**
```
@project status              - Git status
@project log                 - Recent commits
@project diff                - Git diff
@project docker              - List containers
@project logs titan-hub      - Container logs
@project ls                  - List files
@project read README.md      - Read file
@project build               - Build project
```

**System Commands:**
```
/status    - Show system status
/help      - Show help
/quit      - Exit console
```

### API Endpoints

**POST /chat**
```json
{
  "message": "What is redstone?",
  "player_name": "Console"
}
```

**POST /command**
```json
{
  "command": "list"
}
```

**POST /say**
```
?message=Hello from API
```

**POST /project/command**
```json
{
  "action": "status",
  "args": []
}
```

**GET /status**
- Get system status and statistics

**GET /stats**
- Get detailed statistics

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│             CONSOLE CHAT (console-chat.py)              │
│         Interactive Terminal Interface                  │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│  GROK CLIENT  │  │  RCON CLIENT  │  │   PROJECT     │
│  (grok-       │  │  (rcon-       │  │  CONTROLLER   │
│   client.py)  │  │   client.py)  │  │  (project-    │
│               │  │               │  │   controller  │
│  - Grok API   │  │  - RCON       │  │   .py)        │
│  - Caching    │  │  - Docker     │  │  - Git ops    │
│  - <1s resp   │  │  - Commands   │  │  - Build ops  │
└───────────────┘  └───────────────┘  └───────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│         CHAT SERVER (chat-server.py)                    │
│         FastAPI REST API (Optional)                     │
│         Endpoints: /chat, /command, /status             │
└─────────────────────────────────────────────────────────┘
```

## Components

### 1. Console Chat (`console-chat.py`)
Interactive terminal interface with:
- Color-coded output
- Command history
- Auto-suggestions
- Real-time responses

### 2. Grok Client (`grok-client.py`)
Ultra-fast Grok API client with:
- Connection pooling
- Response caching
- Timeout optimization
- Statistics tracking

### 3. RCON Client (`rcon-client.py`)
Minecraft command execution with:
- Docker integration
- Command validation
- Connection pooling
- Error handling

### 4. Project Controller (`project-controller.py`)
Project operations with:
- Git commands
- Build automation
- Docker control
- File operations

### 5. Chat Server (`chat-server.py`)
FastAPI REST API with:
- Async request handling
- CORS support
- Request validation
- Auto-generated docs

### 6. AI Bridges
In-game AI chat bridges:
- **instant.py** - Ultra-fast (minimal code)
- **nano-bridge.py** - Minimal and fast
- **fast-ai-bridge.py** - Full-featured with streaming

## Configuration

All settings in `.env.grok`:

```bash
# xAI Grok API
XAI_API_KEY=your-xai-api-key-here

# Minecraft RCON
MINECRAFT_RCON_HOST=localhost
MINECRAFT_RCON_PORT=25575
MINECRAFT_RCON_PASSWORD=titan123
MINECRAFT_DOCKER_CONTAINER=titan-hub

# Project
PROJECT_ROOT=C:\Users\Gigabyte\Documents\project-mc-serv-mc.galion.studio

# API Server
CHAT_SERVER_HOST=localhost
CHAT_SERVER_PORT=8000

# Performance
GROK_TIMEOUT=2
GROK_MAX_TOKENS=100
RESPONSE_CACHE_SIZE=100
```

## Performance

Target metrics:
- AI response time: <1 second (typical 0.3-0.8s)
- RCON command execution: <0.1 second
- Cache hit response: <0.01 second
- Project operations: Varies by operation

## Troubleshooting

### API Key Not Set
```
⚠️ Grok AI not configured (set XAI_API_KEY)
```
**Solution:** Edit `.env.grok` and add your xAI API key

### RCON Not Connected
```
⚠ Minecraft RCON unavailable
```
**Solution:** 
- Ensure Minecraft server is running
- Check RCON is enabled in server.properties
- Verify RCON password matches

### Dependencies Missing
```
ModuleNotFoundError: No module named 'aiohttp'
```
**Solution:** Install dependencies:
```bash
pip install -r requirements-grok.txt
```

### Slow Responses
**Check:**
1. Internet connection speed
2. Grok API status
3. Clear response cache: `/cache/clear` endpoint

## Examples

### Example 1: Quick Question
```
> @ai What is redstone?
🤔 Asking Grok...
⚡ Grok responded in 0.487s
🤖 Grok: Redstone is Minecraft's electrical system. Use it for circuits,
doors, traps, and automation with redstone dust, repeaters, and comparators.
```

### Example 2: Minecraft Command
```
> /list
⚙️  Executing: list
✓ Command executed in 0.043s
There are 3 of a max of 20 players online: player1, player2, player3
```

### Example 3: Project Status
```
> @project status
 M README.md
 M console-chat.py
?? GROK-CONSOLE-README.md
```

## Testing

Run tests to verify <1 second response times:

```bash
# Test Grok client
python grok-client.py

# Test RCON client
python rcon-client.py

# Test project controller
python project-controller.py

# Test API server
python chat-server.py
# Then visit: http://localhost:8000/docs
```

## Security Notes

⚠️ **Important:**
- Never commit `.env.grok` with real API keys
- Keep API keys secure
- Use RCON password protection
- Validate all user inputs
- Restrict API access in production

## Support

For issues or questions:
- Check troubleshooting section
- Review API documentation at `/docs`
- Check Grok API status at https://x.ai/status

## Credits

Built for Project Titan (mc.galion.studio)
- Powered by xAI Grok-4 Fast
- FastAPI for REST API
- Colorama for terminal colors
- Prompt Toolkit for rich console

---

**Get your xAI API key:** https://console.x.ai/

**Project:** mc.galion.studio

