import discord
from discord.ext import commands

from bot.reference import *
from asyncio import sleep as sleepasync
import bot.reference as ref

import random


class User(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        self.shake_a = self.shake_b = self.shake_c = []
        self.haikuLines = []
        self.command_json = ""

        self.bot.loop.create_task(self.initialize())

    async def initialize(self):
        try:
            with open(INSULT_CSV, mode='r') as file:
                for line in file:
                    words = line.split(",")
                    self.shake_a.append(words[0])
                    self.shake_b.append(words[1])
                    self.shake_c.append(words[2].strip())
                file.close()
            print("Loaded insult.csv")
        except Exception as e:
            print("Failed to load insult.csv")
            print(e)

        try:
            with open(HAIKU_CSV, mode='r') as file:
                for line in file:
                    self.haikuLines.append(line)
                file.close()
        except Exception as e:
            print("Failed to load haiku.csv")
            print(e)

        try:
            with open(COMMAND_JSON, "r") as cmds:
                self.command_json = json.load(cmds)
                cmds.close()
            print("Loaded command.json")
        except Exception as e:
            print("Failed to load command.json")
            print(e)

    # Haiku Generator
    @commands.command(name="haiku", pass_context=True)
    async def haiku(self, ctx):
        can_send = await ref.check_can_use(ctx, "haiku")
        if not can_send:
            return

        haiku = random.choice(self.haikuLines[0].split(",")).strip() + " " + random.choice(
            self.haikuLines[1].split(",")).strip() + "\n"
        haiku += random.choice(self.haikuLines[2].split(",")).strip() + " " + random.choice(
            self.haikuLines[3].split(",")).strip() + " " + random.choice(self.haikuLines[4].split(",")).strip() + "\n"
        haiku += random.choice(self.haikuLines[5].split(",")).strip() + " " + random.choice(
            self.haikuLines[6].split(",")).strip() + "\n"

        await ctx.send(haiku)

    # Help Command
    @commands.command(name="help", pass_context=True)
    async def help(self, ctx, *args):
        can_send = await ref.check_can_use(ctx, "help")
        if not can_send:
            return

        # Open commands.json for reading
        if args.__len__() == 0:
            # Send message to channel where message was sent
            bot_message = await ctx.send(f"**{ctx.author.mention} I DM'd you the command list!**")
            help_message = f"Here's the command list! The current prefix is '{BOT_PREFIX}'\n"

            user_role = "Sauce"

            if not isinstance(ctx.message.channel, discord.DMChannel):
                for role in ctx.author.roles:
                    for line in roles:
                        r = line.split(",")
                        if role.name == r[0]:
                            user_role = r

            # Iterate through json file and add all commands to help string
            for index, item in enumerate(self.command_json["commands"]):
                if int(user_role[2]) >= int(item["permission-level"]):
                    aliases = []
                    for index2, alias in enumerate(item["aliases"]):
                        aliases.append(alias["id"])

                    name = item["name"]
                    desc = item["desc"]
                    usage = item["usage"]
                    help_message += f"\n{name}\n-Description: {desc}\n-Usage: {BOT_PREFIX}{usage}\n-Aliases: {aliases}\n"

                    if len(help_message) >= 1750:
                        print(len(help_message))
                        await ctx.message.author.send(f"```html\n{help_message} ```")
                        help_message = ""

            # Send author help text in direct message
            await ctx.message.author.send(f"```html\n{help_message} ```")
            print(f"Sent help message to {ctx.message.author}")

            await sleepasync(5)
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
                        name = item["name"]
                        desc = item["desc"]
                        usage = item["usage"]
                        help_message += f"\n{name}\n-Description: {desc}\n-Usage: {BOT_PREFIX}{usage}\n-Aliases: {alias_str}"
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
            await ctx.send(f"```html\n{help_message} ```")

    # Shakespeare Insults
    @commands.command(name="insult", pass_context=True)
    async def insult(self, ctx, user=None):
        can_send = await ref.check_can_use(ctx, "insult")
        if not can_send:
            return

        if user is None:
            await ctx.send("**Thy did not specify whom I shall insult!**")
            return

        word_a = random.choice(self.shake_a)
        word_b = random.choice(self.shake_b)
        word_c = random.choice(self.shake_c)

        insult = f"Thou {word_a} {word_b} {word_c}"
        await ctx.send(f"**{user} {insult}**")

    @commands.command(name='lolicon', aliases=['loli'], pass_context=True)
    async def lolicon(self, ctx, *args):
        can_send = await ref.check_can_use(ctx, "lolicon")
        if not can_send:
            return

        if args.__len__() == 0:
            await ctx.send(f"{ctx.message.author.mention} "
                                           f"https://www.youtube.com/watch?v=-mzR1jcZ_OI")
        else:
            await ctx.send(f"{str(' ').join(args)}"
                                           f"https://www.youtube.com/watch?v=-mzR1jcZ_OI")

    # Pat user command
    @commands.command(name='pat', aliases=['pats', 'pets', 'pet'], pass_context=True)
    async def pat(self, ctx, *args):
        can_send = await ref.check_can_use(ctx, "pat")
        if not can_send:
            return

        if args.__len__() == 0:
            await ctx.send(f"**{ctx.message.author.mention} \*pats\* themselves**")
        else:
            await ctx.send(f"**{ctx.message.author.mention} \*pats\* {str(' ').join(args)}**")

    @commands.command(name='ping', pass_context=True)
    async def ping(self, ctx, *args):
        can_send = await ref.check_can_use(ctx, "ping")
        if not can_send:
            return

        await ctx.send(f"**:ping_pong: Pong! {str(' ').join(args)}**")

    @commands.command(name='police', aliases=['lolice', '911', 'swat'], pass_context=True)
    async def police(self, ctx, *args):
        can_send = await ref.check_can_use(ctx, "police")
        if not can_send:
            return

        await ctx.send(str(" ").join(args), file=discord.File(f"{IMG_DIRECTORY}/police.jpg"))

    @commands.command(name="purge", aliases=["PURGE"], pass_context=True)
    async def purge(self, ctx):
        can_send = await ref.check_can_use(ctx, "purge")
        if not can_send:
            return

        await ctx.channel.purge(limit=2)

    # Spanks User
    @commands.command(pass_context=True)
    async def spank(self, ctx, *args):
        can_send = await ref.check_can_use(ctx, "spank")
        if not can_send:
            return

        if args.__len__() == 0:
            await ctx.send(ctx.message.author.mention + "** \*spanks* themselves**")
        else:
            await ctx.send(ctx.message.author.mention + "** \*spanks* **" + str(" ").join(args))


def setup(bot):
    bot.add_cog(User(bot))
