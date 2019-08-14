import discord
from discord.ext import commands
from bot import reference as ref
import os, json

import asyncio, random

class DeepFry(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(DeepFry(bot))