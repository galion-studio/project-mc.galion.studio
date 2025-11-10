#!/usr/bin/env python3
"""INSTANT AI BRIDGE - Real-time responses with Grok-4 Fast"""
import subprocess, requests, re, time, threading, os
from dotenv import load_dotenv

# Load Grok API key from environment
load_dotenv("../.env.grok")
API = os.getenv("OPENROUTER_API_KEY", "your-openrouter-api-key-here")
last_msg = {}

def say(msg):
    """Send message to Minecraft chat"""
    subprocess.run(['docker','exec','titan-hub','rcon-cli',f'say §b[Console]§f {msg}'], capture_output=True)

def ai(q):
    """Ask Grok-4 Fast for ultra-fast responses via OpenRouter"""
    r = requests.post('https://openrouter.ai/api/v1/chat/completions',
        headers={'Authorization':f'Bearer {API}','content-type':'application/json'},
        json={'model':'x-ai/grok-beta','max_tokens':80,'messages':[{'role':'user','content':f'Answer in MAX 15 words: {q}'}]},
        timeout=5)
    return r.json()['choices'][0]['message']['content'] if r.status_code==200 else "Error"

def handle(p,m):
    key=f"{p}:{m}"
    if key in last_msg: return
    last_msg[key]=time.time()
    say("🤔")
    ans=ai(m)
    for chunk in [ans[i:i+70] for i in range(0,len(ans),70)]: say(chunk)

print("⚡ INSTANT AI - RUNNING (Grok-4 Fast)\n")
say("⚡ Grok AI ready! Type to chat!")

proc=subprocess.Popen(['docker','logs','-f','titan-hub'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=True,bufsize=1)
for line in proc.stdout:
    m=re.search(r'<([^>]+)> (.+)',line)
    if m and any(t in m.group(2).lower() for t in ['console','@ai','hey']):
        threading.Thread(target=handle,args=(m.group(1),m.group(2))).start()

