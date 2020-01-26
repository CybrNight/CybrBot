import discord
from discord.ext import commands
from bot.reference import *
import os
from random import randint


class Waifu(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="w")
    async def waifu(self, ctx):
        files = os.listdir(WAIFU_DIRECTORY)
        r = randint(0, len(files)+1)

        print(r.name)


def setup(bot):
    bot.add_cog(Waifu(bot))
