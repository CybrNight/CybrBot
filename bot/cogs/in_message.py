import discord

from bot.reference import *
from discord.ext import commands
from random import randint
import os


class InMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.autism = f"{IMG_DIRECTORY}/autism.png"
        self.riding_mower = f"{IMG_DIRECTORY}/riding_mower.gif"
        self.eye_patch = f"{IMG_DIRECTORY}/eyepatch.jpg"
        self.nepeta = f"{IMG_DIRECTORY}/nepeta.gif"
        self.nyanpasu = f"{IMG_DIRECTORY}/nyanpasu.png"

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.id == 522095867407106079:
            if "poop" in message.content or "poo" in message.contnet:
                await message.remove()
                return

        if message.author == self.bot.user:
            return
        # we do not want the self.bot to reply to itself

        content = str(message.content).lower()
        channel = message.channel

        if content.startswith('.'):
            return

        # Autism picture command
        if content.startswith("autism"):
            msg = content.split(" ")
            if len(msg) > 1:
                msg.pop(0)
                await channel.send(f"**literally>** {msg}",
                                   file=discord.File(self.autism))

        if content.startswith("**mechanised autism**"):
            await channel.send("Mechanised Autism",
                               file=discord.File(self.riding_mower))

        # Sends current prefix to chat
        if content.startswith("prefix?"):
            await channel.send(f"**The current prefix is '{BOT_PREFIX}'")
            await message.delete()

        # Sends eye=patch picture to chat
        if content.startswith("fuck you"):
            await channel.send(file=discord.File(self.eye_patch))

        # Sends lewd gif
        if content.startswith("lewd"):
            await channel.send(file=discord.File(self.nepeta))

        # Sends nyanpasu picture
        if content.startswith("nyanpasu"):
            await channel.send("@everyone", file=discord.File(self.nyanpasu))
            await message.delete()


def setup(bot):
    bot.add_cog(InMessage(bot))
