import asyncio
import datetime
import json

from discord.ext import commands

from bot import reference as ref


class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True,name="clear")
    async def clear(self, ctx, number=5):
        number = int(number)  # Converting the amount of messages to delete to an integer
        counter = 0
        async for x in ctx.message.channel.history(limit=number):
            if counter < number:
                await x.delete()
                counter += 1

        clear_message = await ctx.message.channel.send("Cleared Messages :white_check_mark:")
        await asyncio.sleep(2.5)
        await clear_message.delete()

    @commands.command(pass_context=True, name="prefix")
    async def prefix(self, ctx, prefix):
        with open("json/config.json", "r") as config:
            data = json.load(config)

        data["prefix"] = prefix
        ref.BOT_PREFIX = prefix

        with open("conjfig.json", "w") as config:
            json.dump(data, config)
        await ctx.message.channel("Command Prefix is now {0}".format(prefix))
        self.bot.command_prefix = prefix

    @commands.command(name="info", pass_context=True, alias=['status'])
    async def info(self, ctx):
        current_datetime = datetime.datetime.now()
        time = current_datetime.time()
        date = current_datetime.date()
        info = await ctx.message.channel.send("```{0} {3}\n(C) Nathan Estrada 2018"
                                  "\nServer time: {1} Server date: {2}```".format(self.bot.user.display_name,
                                                                                  time, date, ref.RELEASE_VERSION))

        await asyncio.sleep(5)
        await info.delete()
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Util(bot))
