import asyncio
import random

import discord
from discord.ext import commands

from bot.reference import *


class BotPresence(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.update_presence())
        self.data = ""

        # Load JSON of statuses
        with open(PRESENCE_JSON, "r", encoding="utf8", errors="ignore") as cfg:
            self.data = json.load(cfg)

    async def update_presence(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():

            # Pick random game/show to be watching
            presence = random.choice(self.data["presence"])
            status = presence["status_type"]
            name = presence["name"]
            activity = discord.Activity(name="N/A",type=discord.ActivityType.unknown)

            print(f"{status} {name}")

            # Generate Discord activity object based on status_type
            if status == "listening":
                activity = discord.Activity(name=name, type=discord.ActivityType.listening)
            elif status == "watching":
                activity = discord.Activity(name=name, type=discord.ActivityType.watching)
            elif status == "playing":
                activity = discord.Activity(name=name, type=discord.ActivityType.playing)

            # Set presence of bot
            await self.bot.change_presence(activity=activity)

            # Sleep for 30 minutes and upate again
            await asyncio.sleep(60*30)


def setup(bot):
    bot.add_cog(BotPresence(bot))
