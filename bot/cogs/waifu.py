import discord
from discord.ext import commands
from bot.reference import *
import os
from os import path
import random
import json


class Waifu(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.waifu_json = None

    @commands.command(name="wish")
    async def wish(self, ctx):
        author_name = str(ctx.message.author.id)

        if path.isfile(WISHLIST_DIRECTORY+"/"+author_name+".csv"):
            print("You have a wishlist")
        else:
            f = open(WISHLIST_DIRECTORY+"/"+author_name+".csv", "w+")
            f.close()

    @commands.command(name="wishlist", aliases=["wl"])
    async def wishlist(self, ctx):
        author_name = str(ctx.message.author.id)

        if path.isfile(WISHLIST_DIRECTORY+"/"+author_name+".csv"):
            print("You have a wishlist")
        else:
            f = open(WISHLIST_DIRECTORY+"/"+author_name+".csv", "w+")
            f.close()

    @commands.command(name="w")
    async def waifu(self, ctx):
        files = os.listdir(WAIFU_DIRECTORY)
        name = random.choice(files)

        file = f"{WAIFU_DIRECTORY}/{name}"

        try:
            with open(file, "r", encoding="utf8",
                      errors="ignore") as json_file:
                self.waifu_json = json.load(json_file)
        except FileNotFoundError:
            print("No Such File")

        waifu = random.choice(self.waifu_json["characters"])
        name = waifu["name"]
        image = waifu["image"]

        embed = discord.Embed(title=f"**{name}**", color=0xffdd00)
        embed.add_field(name=f"{self.waifu_json['name']}", value="\u200b")
        embed.set_image(url=image)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Waifu(bot))
