import discord
from discord.ext import commands
from bot.reference import *


class Waifu(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        self.waifu_jsons = os.listdir(WAIFU_DIRECTORY)


def setup(bot):
    bot.add_cog(Waifu(bot))
