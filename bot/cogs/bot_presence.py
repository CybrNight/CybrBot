import discord
from discord.ext import commands
from bot import reference as ref
import os, json

import asyncio, random

class BotPresence(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.update_presence())
        self.data = ""
        self.presences = []

        with open(os.getcwd() + "/resources/presence.json", "r", encoding="utf8", errors="ignore") as config:
            self.data = json.load(config)

    async def update_presence(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():

            # Pick random game/show to be watching
            presence = random.choice(self.data["presence"])
            status = presence["status_type"]
            name = presence["name"]
            activity = discord.Activity(name="N/A",type=discord.ActivityType.unknown)

            print(f"{status} {name}")

            if status == "listening": activity = discord.Activity(name=name,type=discord.ActivityType.listening)
            elif status == "watching": activity = discord.Activity(name=name,type=discord.ActivityType.watching)
            elif status == "playing": activity = discord.Activity(name=name,type=discord.ActivityType.playing)

            await self.bot.change_presence(activity=activity)

            await asyncio.sleep(60*30)

def setup(bot):
    bot.add_cog(BotPresence(bot))