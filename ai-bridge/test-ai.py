import os
import requests
import subprocess

API_KEY = os.getenv("ANTHROPIC_API_KEY")  # Set your API key in environment variable

# Test API
print("Testing Claude API...")
response = requests.post(
    'https://api.anthropic.com/v1/messages',
    headers={
        'x-api-key': API_KEY,
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json'
    },
    json={
        'model': 'claude-sonnet-4-20250514',
        'max_tokens': 100,
        'messages': [{'role': 'user', 'content': 'Say hi to galion.studio in Minecraft! Keep it under 10 words.'}]
    }
)

if response.status_code == 200:
    answer = response.json()['content'][0]['text']
    print(f"AI Response: {answer}")
    
    # Send to Minecraft
    subprocess.run(['docker', 'exec', 'titan-hub', 'rcon-cli', f'say §b[Console]§f {answer}'])
    print("✓ Sent to Minecraft!")
else:
    print(f"Error: {response.status_code}")
    print(response.text)

