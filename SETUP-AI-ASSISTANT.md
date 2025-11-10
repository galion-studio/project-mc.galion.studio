# 🤖 SETUP AI ASSISTANT - QUICK GUIDE

**Get Claude AI inside your Minecraft server!**

---

## ⚡ STEP 1: GET API KEY (2 minutes)

### Visit Anthropic Console:
https://console.anthropic.com/settings/keys

1. **Sign up** or **Log in** to Anthropic
2. **Go to API Keys** section
3. **Create Key** → Name it "Titan Minecraft"
4. **Copy the key** (starts with `sk-ant-api03-...`)

**Free tier**: $5 credit (enough for ~5,000 questions!)

---

## ⚡ STEP 2: CONFIGURE PLUGIN (30 seconds)

### Edit config file:

```bash
# Open config
nano plugins/TitanAI/src/main/resources/config.yml

# Or on Windows:
notepad plugins\TitanAI\src\main\resources\config.yml
```

### Replace this line:
```yaml
claude-api-key: "YOUR_API_KEY_HERE"
```

### With your actual key:
```yaml
claude-api-key: "sk-ant-api03-your-actual-key-here"
```

**Save and close!**

---

## ⚡ STEP 3: BUILD & DEPLOY (1 minute)

### Build the plugin:

```powershell
# Windows
.\gradlew :plugins:TitanAI:build

# The plugin JAR will be in:
# plugins\TitanAI\build\libs\TitanAI-1.0.0.jar
```

### Copy to server:

```powershell
# Copy built plugin to server plugins folder
copy plugins\TitanAI\build\libs\TitanAI-1.0.0.jar worlds\hub\plugins\
```

### Restart server:

```powershell
docker-compose restart titan-hub
```

---

## ⚡ STEP 4: TEST IN-GAME! (30 seconds)

### Connect to server:
- `localhost:25565`

### In Minecraft chat, type:
```
@ai hello!
```

### You should see:
```
[galion.studio] @ai hello!
[Console] 🤔 Thinking...
[Console] Hello! I'm Console, your AI assistant in Titan server.
[Console] Ask me anything about Minecraft, plugins, or coding!
```

**IT WORKS!** ✅

---

## 🎯 EXAMPLE QUESTIONS:

```
@ai how do I create a custom command?
@ai what's causing server lag?
@ai show me code for a teleport plugin
@ai explain how Redis works
@ai help me debug this error: NullPointerException
@ai what's the best way to store player data?
@ai how do I make a minigame?
@ai optimize my server for 100 players
```

---

## 🔧 ADVANCED CONFIGURATION:

### Change Command Prefix:

```yaml
command-prefix: "@console"  # Now use @console instead
```

### Restrict Access (OP Only):

```yaml
access: "op"  # Only operators can use AI
```

### Increase Response Length:

```yaml
max-tokens: 2048  # Longer, more detailed responses
```

---

## 💰 API COST:

**Very cheap!**
- Each question: ~$0.001 (1/10th of a cent)
- 100 questions: ~$0.10 (10 cents)
- 1000 questions: ~$1.00

**Free tier**: $5 credit = ~5,000 questions!

---

## 🎊 YOU NOW HAVE:

✅ AI assistant in Minecraft  
✅ Code help in-game  
✅ Debugging support  
✅ Learning tool  
✅ Development assistant  
✅ Available to all players  

---

## 📝 QUICK SETUP SUMMARY:

```bash
# 1. Get API key from: https://console.anthropic.com/
# 2. Edit: plugins/TitanAI/src/main/resources/config.yml
# 3. Add your API key
# 4. Build: .\gradlew :plugins:TitanAI:build
# 5. Copy to: worlds\hub\plugins\
# 6. Restart: docker-compose restart titan-hub
# 7. Test: @ai hello!
```

---

**🤖 YOUR IN-GAME AI ASSISTANT IS READY!** ⚡

**Get your API key and let's activate it!** 🚀

