import asyncio
import random

from discord.ext import commands

from bot.reference import *
from .music import Music, MusicState


class BotPresence(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        self.bot.loop.create_task(self.initialize())
        self.presence_json = ""

    async def initialize(self):
        await self.bot.wait_until_ready()

        activity = discord.Activity(name="/help", type=discord.ActivityType.playing)
        await self.bot.change_presence(activity=activity)

        # Load JSON of statuses
        try:
            with open(PRESENCE_JSON, "r", encoding="utf8", errors="ignore") as cfg:
                self.presence_json = json.load(cfg)
                print("Loaded presence.json")
        except Exception as e:
            print("Failed to load presence.json")
            print(e)

        # self.bot.loop.create_task(self.update_presence())

    async def force_update_presence(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():

            if Music.music_state == MusicState.PlayingNone:
                # Pick random game/show to be watching
                presence = random.choice(self.presence_json["presence"])
                status = presence["status_type"]
                name = presence["name"]
                activity = discord.Activity(name="N/A", type=discord.ActivityType.unknown)

                # Generate Discord activity object based on status_type
                if status == "listening":
                    activity = discord.Activity(name=name, type=discord.ActivityType.listening)
                elif status == "watching":
                    activity = discord.Activity(name=name, type=discord.ActivityType.watching)
                elif status == "playing":
                    activity = discord.Activity(name=name, type=discord.ActivityType.playing)

                # Set presence of bot
                await self.bot.change_presence(activity=activity)

                # Sleep for 30 minutes and update again

    async def update_presence(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():

            if Music.music_state == MusicState.PlayingNone:
                # Pick random game/show to be watching
                presence = random.choice(self.presence_json["presence"])
                status = presence["status_type"]
                name = presence["name"]
                activity = discord.Activity(name="N/A", type=discord.ActivityType.unknown)

                # Generate Discord activity object based on status_type
                if status == "listening":
                    activity = discord.Activity(name=name, type=discord.ActivityType.listening)
                elif status == "watching":
                    activity = discord.Activity(name=name, type=discord.ActivityType.watching)
                elif status == "playing":
                    activity = discord.Activity(name=name, type=discord.ActivityType.playing)

                # Set presence of bot
                await self.bot.change_presence(activity=activity)

                # Sleep for 30 minutes and update again
                await asyncio.sleep(60*30)


def setup(bot):
    bot.add_cog(BotPresence(bot))
