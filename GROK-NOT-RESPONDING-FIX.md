# Grok Not Responding - Quick Fix Guide

## Problem
Your AI chat shows "Connected" but Grok is not responding to messages.

## Root Cause
**Invalid API Key** - The API key in `.env.grok` is incorrect or expired.

Error from OpenRouter API: `"User not found" (401)`

## Solution

### Quick Fix (Recommended)
Run this command to get step-by-step help:
```cmd
FIX-GROK-API-KEY.cmd
```

### Manual Fix

#### Step 1: Get FREE OpenRouter API Key
1. Go to: https://openrouter.ai/keys
2. Sign in (free, no credit card needed)
3. Click "Create Key"
4. Copy the key (should start with `sk-or-v1-`)

#### Step 2: Update .env.grok File
1. Open `.env.grok` in your project folder
2. Find line: `OPENROUTER_API_KEY=...`
3. Replace with your new key from OpenRouter
4. Save the file

Example:
```
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxx
```

#### Step 3: Test Connection
Run the test script:
```cmd
py test-grok-connection-debug.py
```

If you see `[OK] SUCCESS!` - you're done!

#### Step 4: Restart AI Console
1. Close your AI Control Center
2. Restart it
3. Try sending a message again

## How to Verify It's Working

### Test Command Line
```cmd
py test-grok-connection-debug.py
```

Expected output:
```
[OK] SUCCESS! Grok is responding!
Response: Hello! How can I help you today?
```

### Test in GUI
1. Open AI Control Center
2. Click "Connect" button
3. Send message: "hi"
4. You should get a response within 1-2 seconds

## Common Issues

### Issue: Still getting "User not found" error
**Cause**: Wrong API key or not saved properly

**Fix**:
- Make sure you copied the ENTIRE key from OpenRouter
- Check that key starts with `sk-or-v1-`
- Make sure you saved the `.env.grok` file
- Try creating a new key on OpenRouter

### Issue: "Timeout" error
**Cause**: Network or OpenRouter is slow

**Fix**:
- Check internet connection
- Wait a minute and try again
- OpenRouter might be experiencing high load

### Issue: "Network error"
**Cause**: Cannot reach OpenRouter

**Fix**:
- Check internet connection
- Check firewall settings
- Try disabling VPN temporarily

## Notes

### Why OpenRouter instead of xAI directly?
- OpenRouter provides unified API for multiple models
- Better uptime and reliability
- Free tier with $1 credit to start
- Easy to switch between models

### API Key Security
- Never share your API key
- The `.env.grok` file is in `.gitignore` so it won't be committed
- If key is leaked, delete it on OpenRouter and create new one

## Support

If you still have issues:
1. Check the error message in the chat window
2. Run the debug test: `py test-grok-connection-debug.py`
3. Check OpenRouter status: https://status.openrouter.ai

## Files Changed to Fix This Issue

### 1. Better Error Messages
`dev-console/ai/grok_chat.py` - Now shows clear error messages when API key is invalid

### 2. Debug Test Script
`test-grok-connection-debug.py` - Tests your Grok connection and shows detailed info

### 3. Fix Helper Script
`FIX-GROK-API-KEY.cmd` - Guides you through fixing the API key step-by-step

---

**Quick Summary**: Your API key is wrong. Get a free one from OpenRouter, update `.env.grok`, and restart.

