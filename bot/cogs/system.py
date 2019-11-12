import asyncio
import datetime
import csv

from discord.ext import commands
from discord.utils import get

from bot.reference import *
import bot.reference as ref


class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name="register_role")
    async def register_role(self, ctx, role=None, permission_level=5):
        if role is not None:
            for r in ctx.guild.roles:
                if r.name == role:
                    fields = [r.name, r.id, permission_level]
                    with open(ROLES_CSV, 'a') as roles_csv:
                        writer = csv.writer(roles_csv, lineterminator="\n")
                        writer.writerow(fields)
                        print(f"Registered new role {role} successfully")
                        await ctx.send(f"**Registered new role {role} with permission level {permission_level}"
                                       f" successfully **")

    @commands.command(pass_context=True, name="remove_role")
    async def remove_role(self, ctx, role=None):
        if role is not None:
            for r in ctx.guild.roles:
                if r.name == role:
                    current_role = r
                    with open(ROLES_CSV, 'r') as roles_csv:
                        role_list = list(csv.reader(roles_csv, lineterminator='\n'))
                    with open(ROLES_CSV, "w") as roles_csv:
                        writer = csv.writer(roles_csv, lineterminator='\n')
                        for _role in role_list:
                            if _role[0] != current_role.name or int(_role[1]) != int(current_role.id):
                                writer.writerow(_role)
                            else:
                                print(f"Removed role {_role[0]} from registry")
                                await ctx.send(f"**Removed role {_role[0]} from registry**")

    @commands.command(pass_context=True, name="remove_channel")
    async def remove_channel(self, ctx, channel=None):
        current_channel = None
        if channel is None:
            current_channel = ctx.message.channel
        else:
            for c in ctx.guild.channels:
                if c.name == channel:
                    current_channel = c

        with open(CHANNELS_CSV, 'r') as channels_csv:
            channel_list = list(csv.reader(channels_csv, lineterminator='\n'))
        with open(CHANNELS_CSV, "w") as channels_csv:
            writer = csv.writer(channels_csv, lineterminator='\n')
            for _channel in channel_list:
                if _channel[0] != current_channel.name or int(_channel[1]) != int(current_channel.id):
                    writer.writerow(_channel)
                else:
                    print(f"Removed channel {_channel[0]} from registry")
                    await ctx.send(f"**Removed channel {_channel[0]} from registry**")

    @commands.command(pass_context=True, name="register_channel")
    async def register_channel(self, ctx, channel=None, nsfw="no"):
        if channel is None:
            channel = ctx.channel.name

        if "nsfw" in channel:
            nsfw = "yes"

        for c in ctx.guild.channels:
            if c.name == channel:
                fields = [c.name, c.id, nsfw]
                with open(CHANNELS_CSV, 'a') as roles_csv:
                    writer = csv.writer(roles_csv, lineterminator="\n")
                    writer.writerow(fields)
                    print(f"Registered new channel {channel} successfully")
                    await ctx.send(f"**Registered new channel {channel} successfully **")

    @commands.command(pass_context=True, name="clear")
    async def clear(self, ctx, number=5):
        can_send = await ref.check_can_use(ctx, "clear")
        if not can_send:
            return

        if can_send:
            number = int(number)  # Converting the amount of messages to delete to an integer
            await ctx.channel.purge(limit=number)
            temp = await ctx.send(f"**{ctx.author.mention} :white_check_mark: {number} message(s) Cleared!**")
            print(f"Cleared {number} messages from channel: {ctx.channel}")
            await asyncio.sleep(2.5)
            await temp.delete()
        else:
            print("User unable to use this command")
            await ctx.channel.send(f"**{ctx.author.mention} You do not have permission to use this!**")

    @commands.command(pass_context=True, name="prefix")
    async def prefix(self, ctx, prefix=None):
        can_send = ref.check_can_use(ctx, "prefix")
        if not can_send:
            return

        if ctx.channel.name is not "bot_commands" and "Sauce Creators" not in ctx.author.roles:
            return

        if prefix is None:
            await ctx.send(f"**Current prefix is '{os.environ['BOT_PREFIX']}'")
            return
        try:
            os.environ["BOT_PREFIX"] = prefix
            ref.BOT_PREFIX = prefix
            self.bot.command_prefix = prefix
            await ctx.send(f"**Set prefix to '{prefix}'**")
            print(f"**Command prefix is now '{prefix}'**")
        except Exception as e:
            print("Failed to set prefix")
            print(e)

    @commands.command(name="info", pass_context=True, alias=['status'])
    async def info(self, ctx):
        can_send = await ref.check_can_use(ctx, "info")
        if not can_send:
            return

        current_datetime = datetime.datetime.now()
        time = current_datetime.time()
        date = current_datetime.date()
        user = self.bot.user.display_name
        info = await ctx.send(f"```{user} {RELEASE_VERSION}\n(C Nathan Estrada 2019\nServer Time: {time}\n"
                              f"Server Date: {date}```")

        await asyncio.sleep(5)
        await info.delete()
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Util(bot))
