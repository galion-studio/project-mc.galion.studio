#!/usr/bin/env python3
"""
Fun Commands Plugin
Add fun and entertaining commands

Features:
- Random jokes
- Fun facts
- ASCII art
- Magic 8-ball
- Dice rolls
"""

from plugins.plugin_base import PluginBase
import random


class FunCommandsPlugin(PluginBase):
    """Fun commands and entertainment"""
    
    def get_name(self) -> str:
        return "FunCommands"
    
    def get_description(self) -> str:
        return "Fun and entertaining commands"
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def get_commands(self) -> dict:
        return {
            "/joke": {
                "description": "Get a random joke",
                "usage": "/joke",
                "handler": self.handle_joke
            },
            "/8ball": {
                "description": "Ask the magic 8-ball",
                "usage": "/8ball <question>",
                "handler": self.handle_8ball
            },
            "/roll": {
                "description": "Roll dice",
                "usage": "/roll [NdN]",
                "handler": self.handle_roll
            },
            "/flip": {
                "description": "Flip a coin",
                "usage": "/flip",
                "handler": self.handle_flip
            }
        }
    
    def __init__(self, console_instance):
        super().__init__(console_instance)
        
        self.jokes = [
            "Why did the creeper cross the road? To get to the other SSSS-side!",
            "What's a Minecraft player's favorite vegetable? Beetroot!",
            "Why can't you trust an enderman? They're always taking blocks!",
            "What do you call a Minecraft player who builds houses? A blockbuster!",
            "Why did the zombie go to school? To improve his brain food!",
        ]
        
        self.ball_responses = [
            "🔮 It is certain",
            "🔮 Without a doubt",
            "🔮 Yes definitely",
            "🔮 You may rely on it",
            "🔮 As I see it, yes",
            "🔮 Most likely",
            "🔮 Outlook good",
            "🔮 Signs point to yes",
            "🔮 Reply hazy, try again",
            "🔮 Ask again later",
            "🔮 Cannot predict now",
            "🔮 Concentrate and ask again",
            "🔮 Don't count on it",
            "🔮 My reply is no",
            "🔮 Outlook not so good",
            "🔮 Very doubtful",
        ]
    
    async def handle_joke(self):
        """Tell a random joke"""
        joke = random.choice(self.jokes)
        return f"😄 {joke}"
    
    async def handle_8ball(self):
        """Magic 8-ball"""
        response = random.choice(self.ball_responses)
        return response
    
    async def handle_roll(self):
        """Roll dice (default 1d6)"""
        result = random.randint(1, 6)
        return f"🎲 You rolled: {result}"
    
    async def handle_flip(self):
        """Flip a coin"""
        result = random.choice(["Heads", "Tails"])
        return f"🪙 Coin flip: {result}"

