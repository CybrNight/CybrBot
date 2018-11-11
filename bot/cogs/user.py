import json

from discord.ext import commands

from bot import reference as ref
from asyncio import sleep as sleepasync

import random
import os


class User:
    def __init__(self, bot):
        self.bot = bot

        self.shake_a = self.shake_b = self.shake_c = []
        self.haikuLines = []

        with open(os.getcwd()+"/resources/insults.csv", mode='r') as file:
            for line in file:
                words = line.split(",")
                self.shake_a.append(words[0])
                self.shake_b.append(words[1])
                self.shake_c.append(words[2].strip())
            file.close()

        with open(os.getcwd()+"/resources/haiku.csv", mode='r') as file:
            for line in file:
                self.haikuLines.append(line)
            file.close()

        with open("commands.json", "r") as cmds:
            self.data = json.load(cmds)

    # Haiku Generator
    @commands.command(name="haiku", pass_context=True)
    async def haiku(self, ctx):
        haiku = random.choice(self.haikuLines[0].split(",")).strip() + " " + random.choice(self.haikuLines[1].split(",")).strip()+"\n"
        haiku += random.choice(self.haikuLines[2].split(",")).strip() + " " + random.choice(self.haikuLines[3].split(",")).strip()+" "+random.choice(self.haikuLines[4].split(",")).strip()+"\n"
        haiku += random.choice(self.haikuLines[5].split(",")).strip() + " " + random.choice(self.haikuLines[6].split(",")).strip()+"\n"

        await self.bot.say(haiku)

    # Help Command
    @commands.command(name="help", pass_context=True)
    async def help(self, ctx, *args):
        # Open commands.json for reading
        if args.__len__() == 0:
            # Send message to channel where message was sent
            bot_message = await self.bot.say("{0} I DM'd you the command list".format(ctx.message.author.mention))
            help_message = "Here's the command list for ya! The current command prefix is " + "'" + ref.BOT_PREFIX + "'"

            # Iterate through json file and add all commands to help string

            for index, item in enumerate(self.data["commands"]):

                aliases = []
                for index2, alias in enumerate(item["aliases"]):
                    aliases.append(alias["id"])
                help_message += "\n{0}\n-Description: {1}\n-Usage: {2}\n-Aliases: {3}\n".format(item["name"],
                                                                                                item["desc"],
                                                                                                item["usage"],
                                                                                                str(", ").join(aliases))
            # Send author help text in direct message
            await self.bot.send_message(ctx.message.author, "```html\n" + help_message + "```")

            await sleepasync(1.5)
            await self.bot.delete_message(bot_message)
            await self.bot.delete_message(ctx.message)
        else:
            help_message = ""

            # Check if commands exist
            for arg in args:
                aliases = []

                for index, item in enumerate(self.data["commands"]):

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
            bot_message = await self.bot.send_message(ctx.message.channel, "```html\n" + help_message + "```")

            await sleepasync(5)
            await self.bot.delete_message(bot_message)
            await self.bot.delete_message(ctx.message)

    # Shakespeare Insults
    @commands.command(name="insult", pass_context=True)
    async def insult(self, ctx, user=None):
        if user is None:
            await self.bot.say("```Thy did not specify whom I shall insult!```")
            return

        word_a = random.choice(self.shake_a)
        word_b = random.choice(self.shake_b)
        word_c = random.choice(self.shake_c)

        insult = "Thou" + word_a+" "+word_b+word_c
        await self.bot.say(user+" "+insult)

    @commands.command(name='lolicon', aliases=['loli'], pass_context=True)
    async def lolicon(self, ctx, *args):
        if args.__len__() == 0:
            await self.bot.send_message(ctx.message.channel, ctx.message.author.mention + " " +
                                        "https://www.youtube.com/watch?v=-mzR1jcZ_OI")
        else:
            await self.bot.send_message(ctx.message.channel, str(" ").join(args) + " " +
                                        "https://www.youtube.com/watch?v=-mzR1jcZ_OI")

    # Pat user command
    @commands.command(name='pat', aliases=['pats', 'pets', 'pet'], pass_context=True)
    async def pat(self, ctx, *args):
        if args.__len__() == 0:
            await self.bot.say(ctx.message.author.mention + " \*pats* themselves")
        else:
            await self.bot.say(ctx.message.author.mention + " \*pats* " + str(" ").join(args))

    @commands.command(name='ping', pass_context=True)
    async def ping(self, ctx, *args):
        await self.bot.say(":ping_pong: Ping! " + str(" ").join(args))

    @commands.command(name='police', aliases=['lolice', '911', 'swat'], pass_context=True)
    async def police(self, ctx, *args):
        await self.bot.send_message(ctx.message.channel, str(" ").join(args) + " " + "https://i.imgur.com/xAQw8pK.gif"
                                                                                     "https://i.imgur.com/q2pN9g3.jpg"
                                                                                     "https://imgur.com/PlJT8v1")

    @commands.command(name="purge", aliases=["PURGE"], pass_context=True)
    async def purge(self, ctx, number=2):
        mgs = []  # Empty list to put all the messages in the log
        number = int(number)  # Converting the amount of messages to delete to an integer
        if number <= 1:
            number = 2

        async for x in self.bot.logs_from(ctx.message.channel, limit=number):
            mgs.append(x)
        await self.bot.delete_messages(mgs)

    # Spanks User
    @commands.command(pass_context=True)
    async def spank(self, ctx, *args):
        if args.__len__() == 0:
            await self.bot.say(ctx.message.author.mention + " \*spanks* themselves")
        else:
            await self.bot.say(ctx.message.author.mention + " \*spanks* " + str(" ").join(args))


def setup(bot):
    bot.add_cog(User(bot))
