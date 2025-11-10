# 🚀 Quick Start - Client Console

Get started with the Client Console in 3 easy steps!

---

## Step 1: Start the Console

### Option A: From Dev Console (Recommended)

1. Open terminal/command prompt
2. Run:
   ```cmd
   cd dev-console
   DEV-CONSOLE.cmd
   ```
3. Click **"💬 Client Console"** in the left sidebar

### Option B: Standalone Mode

1. Open terminal/command prompt
2. Run:
   ```cmd
   START-CLIENT-CONSOLE.cmd
   ```

### Option C: Direct to Client Console

1. Open terminal/command prompt  
2. Run:
   ```cmd
   cd dev-console
   START-WITH-CLIENT-CONSOLE.cmd
   ```

---

## Step 2: Configure (First Time Only)

1. Open `.env.grok` file in root directory
2. Add your OpenRouter API key:
   ```env
   OPENROUTER_API_KEY=your-key-here
   ```
3. Get free API key at: https://openrouter.ai/keys ($1 free credit!)

**Optional:** Configure RCON settings if different:
```env
MINECRAFT_RCON_HOST=localhost
MINECRAFT_RCON_PORT=25575
MINECRAFT_RCON_PASSWORD=titan123
```

---

## Step 3: Start Using!

### Try These Commands

#### Ask AI:
```
@ai how do I make a farm?
what is redstone?
```

#### Control Server:
```
/list
/time set day
/say Hello players!
```

#### Manage Project:
```
@project status
@project docker
@project build
```

#### Get Help:
```
/help
/status
```

---

## Visual Guide

### In Dev Console:

```
┌──────────────────────────────────────────────────┐
│  DEV CONSOLE - mc.galion.studio                  │
├────────────┬─────────────────────────────────────┤
│ Sidebar    │  Content Area                       │
│            │                                      │
│ Dashboard  │  ┌────────────────────────────────┐ │
│ Console ◀──┼──│ 💬 Client Console              │ │
│ Mods       │  │                                │ │
│ Server     │  │  Chat Output Window            │ │
│ Logs       │  │  (Responses appear here)       │ │
│ Repository │  │                                │ │
│ ...        │  │  Command Input: ____________   │ │
│            │  │                  [Send] [Help] │ │
│            │  └────────────────────────────────┘ │
│            │                                      │
│ Settings   │  Status: 🤖 AI: Online 🎮 RCON: Online│
└────────────┴─────────────────────────────────────┘
```

### Standalone Mode:

```
═══════════════════════════════════════════════════════
  ⚡ CLIENT CONSOLE - mc.galion.studio
  Ultra-fast AI chat + Minecraft server control
═══════════════════════════════════════════════════════

Welcome! Use these commands:
  @ai <question>      - Ask AI
  /cmd <command>      - Minecraft command
  /say <message>      - Send to chat
  @project <action>   - Project tools

[12:34:56] ✓ Grok AI connected
[12:34:56] ✓ Minecraft RCON connected
[12:34:57] ✓ Console ready!

> _
```

---

## Common Commands

### AI Assistance
| Command | What It Does |
|---------|-------------|
| `@ai <question>` | Ask Grok AI anything |
| `<plain text>` | Defaults to AI question |
| `/help` | Show all commands |
| `/status` | Show system status |

### Minecraft Control
| Command | What It Does |
|---------|-------------|
| `/list` | List online players |
| `/time set day` | Change time to day |
| `/say <message>` | Broadcast message |
| `/cmd <any>` | Execute any command |

### Project Management
| Command | What It Does |
|---------|-------------|
| `@project status` | Show git status |
| `@project docker` | List containers |
| `@project logs` | View logs |
| `@project build` | Build project |

---

## Keyboard Shortcuts

| Key | Function |
|-----|----------|
| **Enter** | Send command |
| **↑ Up Arrow** | Previous command |
| **↓ Down Arrow** | Next command |
| **Ctrl+L** | Clear console (standalone) |

---

## Troubleshooting

### ❌ "Grok AI not configured"

**Solution:**
1. Check `.env.grok` file exists
2. Verify `OPENROUTER_API_KEY` is set
3. Test at https://openrouter.ai

### ❌ "RCON not connected"

**Solution:**
1. Ensure Minecraft server is running
2. Check server has RCON enabled
3. Verify password matches

### ❌ Commands not working

**Solution:**
1. Check command syntax with `/help`
2. Ensure correct prefix (`@ai`, `/`, `@project`)
3. Look for error messages in output

---

## Examples

### Example Session 1: Getting Help

```
> @ai how do I build a portal?

[12:35:01] 💬 You: @ai how do I build a portal?
[12:35:01] 🤔 Asking Grok...
[12:35:02] 🤖 Grok: To build a Nether portal, you need:
1. At least 10 obsidian blocks
2. Flint and steel or fire charge
3. Arrange in 4x5 frame (corners optional)
4. Light with flint and steel
⏱️ 0.85s
```

### Example Session 2: Server Control

```
> /list

[12:36:15] 💬 You: /list
[12:36:15] ⚙️ Executing: list
[12:36:15] ✓ There are 5 of a max of 100 players online
⏱️ 0.05s

> /say Welcome to mc.galion.studio!

[12:36:30] 💬 You: /say Welcome to mc.galion.studio!
[12:36:30] ✓ Message sent to Minecraft
```

### Example Session 3: Project Status

```
> @project status

[12:37:00] 💬 You: @project status
[12:37:00] On branch main
Your branch is up to date with 'origin/main'
nothing to commit, working tree clean
```

---

## Tips & Tricks

### 💡 Tip 1: Command History
Use ↑ and ↓ arrows to navigate through previous commands. No need to retype!

### 💡 Tip 2: Default to AI
Don't want to type `@ai` every time? Just type your question directly!

```
> how do I make concrete?
```

Auto-routes to AI!

### 💡 Tip 3: Quick Commands
Use short aliases for common commands:

```
/l        → /list
/t d      → /time set day
/gmc      → /gamemode creative
```

### 💡 Tip 4: Check Status
Use `/status` to see performance stats:
- Request counts
- Cache hit rates
- Average response times

---

## Next Steps

### Learn More
- Read full docs: `dev-console/client/README.md`
- Check commands: Type `/help` in console
- View examples: `CLIENT-CONSOLE-ADDED.md`

### Get Advanced
- Set up command aliases
- Create custom macros
- Explore API integration

### Need Help?
- Type `/help` in console
- Check troubleshooting section above
- Visit: https://galion.studio

---

## Summary

The Client Console gives you:
- ✅ **Instant AI help** - <1 second responses
- ✅ **Full server control** - RCON commands
- ✅ **Project management** - Git, Docker, builds
- ✅ **Easy to use** - Simple, clean interface

**Start now:** Just run `DEV-CONSOLE.cmd` and click **💬 Client Console**!

---

**Made with ❤️ by [galion.studio](https://galion.studio)**  
**Get started in under 2 minutes!**

