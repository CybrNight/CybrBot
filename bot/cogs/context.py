import os

import aiofiles, aiohttp
import discord
from PIL import Image, ImageEnhance

from bot import reference as ref
from discord.ext import commands

class Context(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def embed_json(data, key="message"):
        em = discord.Embed(color=0xe09d00)
        em.set_image(url=data[key])
        return em

    @staticmethod
    def embed_image(img):
        em = discord.Embed(color=0xe09d00)
        em.set_image(url=img)
        return em

    @commands.Cog.listener()
    async def on_message(self, message):
        # we do not want the self.bot to reply to itself
        if message.author == self.bot.user:
            return

        content = str(message.content).lower()
        channel = message.channel

        if content.startswith('.'):
            return

        # Autism picture command
        if content.startswith("autism"):
            msg = content.split(" ")
            if len(msg) > 1:
                msg.pop(0)
                await channel.send(">literally " + str(" ").join(msg),
                                    embed=self.embed_image("http://i.imgur.com/g9O5snh.png"))

        if content.startswith("mechanized autism"):
            await channel.send("Mechanzied Autism", embed=self.embed_image("https://i.imgur.com/HlvFNXW.gif"))

        # Sends current prefix to chat
        if content.startswith("prefix?"):
            await channel.send("```The current prefix is " + "'" + ref.BOT_PREFIX + "'```")
            await message.delete()

        # Sends eye=patch picture to chat
        if content.__contains__("fuck you"):
            await channel.send(embed=self.embed_image("https://i.imgur.com/9hZyYly.jpg"))

        # Sends lewd gif
        if content.__contains__("lewd"):
            await channel.send(embed=self.embed_image("[img]https://i.imgur.com/3geE8aq.gif"))

        # Sends nyanpasu picture
        if content.startswith("nyanpasu"):
            await channel.send("@everyone", embed=self.embed_image("https://i.imgur.com/Ca6EuUP.png"))
            await message.delete()



def setup(bot):
    bot.add_cog(Context(bot))
