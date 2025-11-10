# ⚡ GROK 4 FAST - QUICK START GUIDE

## 🎯 What You Get
- **Ultra-fast AI** responses (<1 second!)
- **Grok 4 Fast** via OpenRouter
- Access to **500+ AI models** through one API
- **Caching** for instant repeated queries
- Works in Minecraft chat and console

---

## 🚀 3-STEP SETUP (Takes 2 minutes!)

### Step 1: Get OpenRouter API Key
1. Go to: **https://openrouter.ai/keys**
2. Sign up (free $1 credit to start!)
3. Copy your API key (starts with `sk-or-v1-...`)

### Step 2: Create `.env.grok` File
Copy `env.grok.example` to `.env.grok`:
```bash
copy env.grok.example .env.grok
```

Then edit `.env.grok` and paste your API key:
```env
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
```

### Step 3: Test It!
```bash
python test-grok-system.py
```

**That's it!** ✅

---

## 🎮 HOW TO USE

### Option 1: Test Console Chat
```bash
START-GROK-BRIDGE.cmd
```
Then ask questions in console!

### Option 2: Use in Your Code
```python
from grok_client import GrokClient
import asyncio

async def main():
    client = GrokClient(api_key="sk-or-v1-...")
    response = await client.ask("What is Minecraft?")
    print(response)

asyncio.run(main())
```

### Option 3: Minecraft In-Game Chat
1. Start Grok bridge: `START-GROK-BRIDGE.cmd`
2. In Minecraft, type: `/ask What is redstone?`
3. Get instant AI response!

---

## ⚙️ CONFIGURATION OPTIONS

Edit `.env.grok` to customize:

```env
# Choose your model (Grok 4 Fast is default)
GROK_MODEL=x-ai/grok-beta

# Or try other models:
# GROK_MODEL=x-ai/grok-2-1212          # Grok 2 (cheaper)
# GROK_MODEL=anthropic/claude-haiku    # Claude Haiku (fastest!)
# GROK_MODEL=openai/gpt-4-turbo        # GPT-4 Turbo
# GROK_MODEL=google/gemini-pro         # Gemini Pro

# Speed settings
GROK_TIMEOUT=30              # Max wait time (seconds)
GROK_MAX_TOKENS=100          # Response length (100 = short chat)
RESPONSE_CACHE_SIZE=100      # Cache 100 responses for speed
```

---

## 💰 PRICING (OpenRouter)

**Grok 4 Fast:**
- Input: $2.00 per 1M tokens
- Output: $10.00 per 1M tokens
- **~$0.001 per Minecraft question** (very cheap!)

**Free Credit:**
- OpenRouter gives **$1 free** to start
- That's ~1000 questions!

---

## 🔧 TROUBLESHOOTING

### "OPENROUTER_API_KEY not set"
- Make sure you copied `env.grok.example` to `.env.grok`
- Make sure you pasted your actual API key
- Check for typos!

### "API Error 401"
- Invalid API key
- Get a new key from: https://openrouter.ai/keys

### "Timeout Error"
- Increase `GROK_TIMEOUT` in `.env.grok`
- Check your internet connection

### "Model not found"
- Check model name in `.env.grok`
- Valid names: `x-ai/grok-beta`, `x-ai/grok-2-1212`
- See all models: https://openrouter.ai/models

---

## 🎯 NEXT STEPS

1. **Test it**: Run `python test-grok-system.py`
2. **Use it**: Start `START-GROK-BRIDGE.cmd`
3. **Customize it**: Edit `.env.grok` settings
4. **Try other models**: Change `GROK_MODEL` to experiment!

---

## 📚 HELPFUL LINKS

- **OpenRouter Dashboard**: https://openrouter.ai/
- **Get API Key**: https://openrouter.ai/keys
- **Available Models**: https://openrouter.ai/models
- **Pricing**: https://openrouter.ai/docs#models

---

## ✅ SUCCESS!

If you see this after running the test:
```
⚡ Grok responded in 0.8s
Response: [AI response here]
✓ Cache cleared
```

**You're all set!** 🎉

Start using AI in your Minecraft server right now!

