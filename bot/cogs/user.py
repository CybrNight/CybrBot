import discord
from discord.ext import commands

from bot.reference import *
from asyncio import sleep as sleepasync

import random


class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.shake_a = self.shake_b = self.shake_c = []
        self.haikuLines = []

        with open(INSULT_CSV, mode='r') as file:
            for line in file:
                words = line.split(",")
                self.shake_a.append(words[0])
                self.shake_b.append(words[1])
                self.shake_c.append(words[2].strip())
            file.close()

        with open(HAIKU_CSV, mode='r') as file:
            for line in file:
                self.haikuLines.append(line)
            file.close()

        with open(COMMAND_JSON, "r") as cmds:
            self.command_json = json.load(cmds)

    # Haiku Generator
    @commands.command(name="haiku", pass_context=True)
    async def haiku(self, ctx):
        haiku = random.choice(self.haikuLines[0].split(",")).strip() + " " + random.choice(
            self.haikuLines[1].split(",")).strip() + "\n"
        haiku += random.choice(self.haikuLines[2].split(",")).strip() + " " + random.choice(
            self.haikuLines[3].split(",")).strip() + " " + random.choice(self.haikuLines[4].split(",")).strip() + "\n"
        haiku += random.choice(self.haikuLines[5].split(",")).strip() + " " + random.choice(
            self.haikuLines[6].split(",")).strip() + "\n"

        await ctx.message.channel.send(haiku)

    # Help Command
    @commands.command(name="help", pass_context=True)
    async def help(self, ctx, *args):

        # Open commands.json for reading
        if args.__len__() == 0:
            # Send message to channel where message was sent
            bot_message = await ctx.message.channel.send(f"{ctx.author.mention} I DM'd you the command list!")
            help_message = f"Here's the command list! The current prefix is '{BOT_PREFIX}'"

            # Iterate through json file and add all commands to help string
            for index, item in enumerate(self.command_json["commands"]):
                aliases = []
                for index2, alias in enumerate(item["aliases"]):
                    aliases.append(alias["id"])
                help_message += "\n{0}\n-Description: {1}\n-Usage: {2}\n-Aliases: {3}\n".format(item["name"],
                                                                                                item["desc"],
                                                                                                item["usage"],
                                                                                                str(", ").join(aliases))
            # Send author help text in direct message
            msg = await ctx.message.author.send(f"```html\n{help_message} ```")

            await sleepasync(5)
            await msg.delete()
            await bot_message.delete()
        else:
            help_message = ""
            # Check if commands exist
            for arg in args:
                aliases = []

                for index, item in enumerate(self.command_json["commands"]):
                    if item["name"] == arg:
                        for index2, alias in enumerate(item["aliases"]):
                            aliases.append(alias["id"])

                        alias_str = str(" ").join(aliases)
                        help_message += "\n{0}\n-Description: {1}\n-Usage: {2}\n-Aliases: {3}\n".format(item["name"],
                                                                                                        item["desc"],
                                                                                                        item["usage"],
                                                                                                        alias_str)
                        continue

                    aliases = []
                    # Check if aliases exist
                    for index2, alias in enumerate(item["aliases"]):
                        if alias["id"] == arg:
                            alias_str = str(" ").join(aliases)
                            help_message += "\n{0}\n-Description: {1}\n-Usage: {2}\n-Aliases: {3}\n".format(
                                item["name"],
                                item["desc"],
                                item["usage"],
                                alias_str)
            # Send help info for inputed commands to channel
            bot_message = ctx.message.author.send(f"```html\n{help_message} ```")

            await sleepasync(5)
            await bot_message.delete()
            await ctx.message.delete()

    # Shakespeare Insults
    @commands.command(name="insult", pass_context=True)
    async def insult(self, ctx, user=None):
        if user is None:
            await ctx.message.channel.send("```Thy did not specify whom I shall insult!```")
            return

        word_a = random.choice(self.shake_a)
        word_b = random.choice(self.shake_b)
        word_c = random.choice(self.shake_c)

        insult = f"Thou {word_a} {word_b} {word_c}"
        await ctx.message.channel.send(f"{user} {insult}")

    @commands.command(name='lolicon', aliases=['loli'], pass_context=True)
    async def lolicon(self, ctx, *args):
        if args.__len__() == 0:
            await ctx.message.channel.send(f"{ctx.message.author.mention} "
                                           f"https://www.youtube.com/watch?v=-mzR1jcZ_OI")
        else:
            await ctx.message.channel.send(f"{str(' ').join(args)}"
                                           f"https://www.youtube.com/watch?v=-mzR1jcZ_OI")

    # Pat user command
    @commands.command(name='pat', aliases=['pats', 'pets', 'pet'], pass_context=True)
    async def pat(self, ctx, *args):
        if args.__len__() == 0:
            await ctx.message.channel.send(f"{ctx.message.author.mention} \*pats\* themselves")
        else:
            await ctx.message.channel.send(f"{ctx.message.author.mention} \*pats\* {str(' ').join(args)}")

    @commands.command(name='ping', pass_context=True)
    async def ping(self, ctx, *args):
        await ctx.message.channel.send(f":ping_pong: Pong! {str(' ').join(args)}")

    @commands.command(name='police', aliases=['lolice', '911', 'swat'], pass_context=True)
    async def police(self, ctx, *args):
        await ctx.message.channel.send(str(" ").join(args), file=discord.File(os.getcwd() + "/resources/police.jpg"))

    @commands.command(name="purge", aliases=["PURGE"], pass_context=True)
    async def purge(self, ctx, number=2):
        msg = []  # Empty list to put all the messages in the log
        number = int(number)  # Converting the amount of messages to delete to an integer
        if number <= 1:
            number = 2

        async for x in ctx.message.channel.history(limit=number):
            await x.delete()

    # Spanks User
    @commands.command(pass_context=True)
    async def spank(self, ctx, *args):
        if args.__len__() == 0:
            await ctx.message.channel.send(ctx.message.author.mention + " \*spanks* themselves")
        else:
            await ctx.message.channel.send(ctx.message.author.mention + " \*spanks* " + str(" ").join(args))


def setup(bot):
    bot.add_cog(User(bot))
