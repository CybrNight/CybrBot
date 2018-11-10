import json

from discord.ext import commands

from bot import reference as ref

import random
import os

class User:
    def __init__(self, bot):
        self.bot = bot

        self.list_a = self.list_b = self.list_c = []

        list_a = list_b = list_c = []
        with open(os.getcwd()+"/resources/insults.csv", mode='r') as file:
            for line in file:
                words = line.split(",")
                self.list_a.append(words[0])
                self.list_b.append(words[1])
                self.list_c.append(words[2].strip())

        with open("commands.json", "r") as cmds:
            self.data = json.load(cmds)

    # Help Command
    @commands.command(name="help", pass_context=True)
    async def help(self, ctx, *args):
        # Open commands.json for reading
        with open("commands.json", "r") as cmds:
            data = json.load(cmds)

        if args.__len__() == 0:
            # Send message to channel where message was sent
            await self.bot.say("{0} I DM'd you the command list".format(ctx.message.author.mention))
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
        else:
            help_message = ""

            # Check if commands exist
            for arg in args:
                aliases = []

                for index, item in enumerate(data["commands"]):

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
            await self.bot.send_message(ctx.message.channel, "```html\n" + help_message + "```")

    # Shakespeare Insults
    @commands.command(name="insult", pass_context=True)
    async def insult(self, ctx, user=None):
        if user is None:
            self.bot.say("```Thy did not specify whom I shall insult```")
            return

        word_a = random.choice(self.list_a)
        word_b = random.choice(self.list_b)
        word_c = random.choice(self.list_c)

        insult = "Thou" + word_a+" "+word_b+word_c
        print(insult)
        self.bot.send_message(ctx.message.channel, user+" "+insult)

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

    # Pats user
    @commands.command(pass_context=True)
    async def spank(self, ctx, *args):
        if args.__len__() == 0:
            await self.bot.say(ctx.message.author.mention + " \*spanks* themselves")
        else:
            await self.bot.say(ctx.message.author.mention + " \*spanks* " + str(" ").join(args))


def setup(bot):
    bot.add_cog(User(bot))
