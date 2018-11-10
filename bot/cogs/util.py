import asyncio
import json
import datetime

from discord.ext import commands

from bot import reference as ref


class Util:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def clear(self, ctx, number=5):
        number = int(number)  # Converting the amount of messages to delete to an integer
        counter = 0
        async for x in self.bot.logs_from(ctx.message.channel, limit=number):
            if counter < number:
                await self.bot.delete_message(x)
                counter += 1

    @commands.command(pass_context=True)
    async def prefix(self, ctx, prefix):
        with open("config.json", "r") as config:
            data = json.load(config)

        data["prefix"] = prefix
        ref.BOT_PREFIX = prefix

        with open("config.json", "w") as config:
            json.dump(data, config)
        await self.bot.say("Command Prefix is now {0}".format(prefix))
        self.bot.command_prefix = prefix

    @commands.command(name="info",pass_context=True, alias=['status'])
    async def info(self, ctx):
        current_datetime = datetime.datetime.now()
        time = current_datetime.time()
        date = current_datetime.date()
        await self.bot.say("```{0} v2.0"
                           "\n(C) Nathan Estrada 2018"
                           "\nServer time: {1}"
                           "\nServer date: {2}```".format(self.bot.user.display_name, time, date))


def setup(bot):
    bot.add_cog(Util(bot))
