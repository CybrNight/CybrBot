import discord
from discord.ext import commands
import aiofiles, aiohttp
from PIL import Image, ImageEnhance
import os, shutil
from os import listdir
from os.path import isfile, join
import imageio

class DeepFry(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.download_dir = os.getcwd()+"/download/deepfry"

def setup(bot):
    bot.add_cog(DeepFry(bot))