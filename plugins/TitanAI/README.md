# 🤖 Titan AI Assistant

**In-game AI assistant powered by Claude Sonnet 4.5**

Chat with Claude directly in Minecraft! Get code help, debug issues, and learn - all without leaving the game.

---

## 🎮 How to Use

### In Minecraft Chat:

```
@ai how do I create a plugin?
@ai what's the command for teleporting?
@ai help me debug this error: NullPointerException
@ai how do I set up auto-restart?
@ai show me code for a custom command
```

**The AI responds as [Console] in chat!**

---

## ⚙️ Setup

### 1. Get API Key

Visit: https://console.anthropic.com/settings/keys

Create a new API key.

### 2. Configure Plugin

Edit `plugins/TitanAI/config.yml`:

```yaml
claude-api-key: "sk-ant-api03-your-key-here"
```

### 3. Restart Server

```bash
docker-compose restart titan-hub
```

### 4. Test It!

In-game, type:
```
@ai hello!
```

You should get a response from [Console]!

---

## 💡 Use Cases

### Code Help
```
@ai how do I listen to player join events?
@ai show me a basic plugin structure
@ai what's the Bukkit API for setting blocks?
```

### Server Management
```
@ai how do I increase server RAM?
@ai what causes low TPS?
@ai how do I backup my world?
```

### Debugging
```
@ai this error: java.lang.NullPointerException at line 42
@ai players can't connect, what should I check?
@ai server is lagging, help me diagnose
```

### Learning
```
@ai explain how Minecraft servers work
@ai what's the difference between Spigot and Paper?
@ai how does cross-server chat work?
```

---

## 🔧 Configuration

### Command Prefix

Change the trigger word:

```yaml
command-prefix: "@console"  # Now use @console instead of @ai
```

### Response Length

Adjust how long responses can be:

```yaml
max-tokens: 2048  # Longer responses
```

### Access Control

Restrict who can use AI:

```yaml
access: "op"  # Only OPs can use
# or
access: "permission"
permission-node: "titan.ai.use"
```

---

## 📊 Features

- ✅ **Real-time responses** - Chat with Claude in Minecraft
- ✅ **Code help** - Get Java/Plugin code examples
- ✅ **Debugging** - Paste errors, get solutions
- ✅ **Multi-player** - Everyone can see AI responses
- ✅ **Rate limiting** - Prevents API abuse
- ✅ **Configurable** - Customize behavior
- ✅ **Async** - Doesn't lag server
- ✅ **Smart formatting** - Breaks long responses into chat lines

---

## 🎯 Example Conversations

```
[galion.studio] @ai how do I create a custom command?
[Console] 🤔 Thinking...
[Console] Create a class extending JavaPlugin, override onCommand(),
[Console] register in plugin.yml. Need code example?

[galion.studio] @ai yes show me code
[Console] 🤔 Thinking...
[Console] @Override public boolean onCommand(CommandSender sender,
[Console] Command cmd, String label, String[] args) { 
[Console] sender.sendMessage("Hello!"); return true; }
```

---

## 🔐 Security

- API key is stored server-side (not visible to players)
- Rate limiting prevents abuse
- Can restrict to OPs only
- All interactions are logged

---

## 💰 Cost

Claude API pricing (as of 2025):
- Input: ~$0.003 per 1K tokens
- Output: ~$0.015 per 1K tokens

**Typical question + answer**: ~$0.001 (less than 1 cent!)

**100 questions**: ~$0.10 (10 cents)

Very affordable for development and learning! 🎉

---

## 🆘 Troubleshooting

### "AI not configured" message

**Fix**: Add API key to `config.yml`

### No response from AI

**Fix**: Check server logs for errors:
```bash
docker-compose logs titan-hub | grep "TitanAI"
```

### API error

**Fix**: Verify API key is valid at https://console.anthropic.com/

---

## 🚀 Advanced Usage

### Ask About Your Project

```
@ai I'm building a 20k player server, what should I optimize?
@ai how do I implement cross-server teleportation?
@ai explain the Titan architecture
```

### Get Real Code

```
@ai write a plugin that tracks player playtime
@ai show me how to use Redis in a Bukkit plugin
@ai create a command that shows server TPS
```

### Learn Minecraft Development

```
@ai what are the most important Bukkit events?
@ai how does chunk loading work?
@ai explain the difference between sync and async tasks
```

---

**🤖 YOUR AI ASSISTANT IS READY TO HELP IN-GAME!** ⚡

