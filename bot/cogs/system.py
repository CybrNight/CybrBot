import asyncio
import datetime
import csv

from discord.ext import commands

from bot.reference import *
import bot.reference as ref


class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.roles = None

    @commands.command(name="list_roles")
    async def list_roles(self, ctx):
        guild_roles = ctx.guild.roles
        with open(ROLES_CSV, 'r') as roles_csv:
            reg_roles = roles_csv.readlines()
        embed = discord.Embed(title=f"**Registered Roles For {ctx.guild}**")
        i = 0
        for role in guild_roles:
            for reg_role in reg_roles:
                r = reg_role.split(",")
                reg_name = r[0]
                reg_id = int(r[1])
                if reg_name == role.name and reg_id == int(role.id):
                    reg_name = r[0].strip()
                    perm = r[2].strip()
                    if i == 0:
                        embed.add_field(name=f"{reg_name}",
                                        value=f"Permission Level: "f"{perm}",
                                        inline=False)
                    else:
                        embed.add_field(name=f"{reg_name}",
                                        value=f"Permission Level: "f"{perm}",
                                        inline=True)
        await ctx.send(embed=embed)

    @commands.command(name="register_role")
    async def register_role(self, ctx, role=None, permission_level=5):
        guild_roles = ctx.guild.roles
        guild = ctx.guild
        global valid_role
        valid_role = False
        if role is not None:
            for r in guild_roles:
                if r.name == role:
                    fields = [r.name, r.id, permission_level]
                    with open(ROLES_CSV, 'a') as roles_csv:
                        valid_role = True
                        writer = csv.writer(roles_csv, lineterminator="\n")
                        writer.writerow(fields)
                        print(f"Registered new role {role} successfully")
                        await ctx.send(f"**Registered new role {role} with "
                                       f"permission level {permission_level}"
                                       f" successfully **")

            if not valid_role:
                print(f"No such role {role} on server {guild}")
                await ctx.send(f"**No role {role} on {guild}**")

    @commands.command(name="remove_role")
    async def remove_role(self, ctx, role=None):
        guild_roles = ctx.guild.roles
        if role is not None:
            for guild_role in guild_roles:
                if guild_role.name == role:
                    current_role = guild_role
                    with open(ROLES_CSV, 'r') as roles_csv:
                        role_list = list(csv.reader(roles_csv,
                                                    lineterminator='\n'))
                    with open(ROLES_CSV, "w") as roles_csv:
                        writer = csv.writer(roles_csv, lineterminator='\n')
                        for r in role_list:
                            print(r)
                            name = r[0]
                            id = int(r[1])
                            if name != current_role.name \
                                    or id != int(current_role.id):
                                writer.writerow(r)
                            else:
                                print(f"Removed role {r[0]} from registry")
                                await ctx.send(f"**Removed role {r[0]} "
                                               f"from registry**")

    @commands.command(name="list_channels")
    async def list_channels(self, ctx):
        guild = ctx.guild
        guild_channels = ctx.guild.channels
        with open(CHANNELS_CSV, 'r') as channels_csv:
            reg_channels = channels_csv.readlines()
        embed = discord.Embed(title=f"**Registered Channels For {guild}**")
        i = 0
        for reg_channel in reg_channels:
            for channel in guild_channels:
                c = channel.split(",")
                name = c[0]
                channel_id = c[1]
                nsfw = c[2]
                if name == channel.name and channel_id == int(channel.id):
                    print(c)
                    if i == 0:
                        embed.add_field(name=f"{name.strip()}",
                                        value=f"NSFW: {nsfw.strip().upper()}",
                                        inline=False)
                    else:
                        embed.add_field(name=f"{name.strip()}",
                                        value=f"NSFW: {nsfw.strip().upper()}",
                                        inline=True)

        await ctx.send(embed=embed)

    @commands.command(name="register_channel")
    async def register_channel(self, ctx, channel=None, nsfw="no"):
        global valid_channel
        valid_channel = False
        if channel is None:
            channel = ctx.channel.name

        if "nsfw" in channel:
            nsfw = "yes"

        for c in ctx.guild.channels:
            if c.name == channel:
                fields = [c.name, c.id, nsfw]
                with open(CHANNELS_CSV, 'a') as roles_csv:
                    valid_channel = True
                    writer = csv.writer(roles_csv, lineterminator="\n")
                    writer.writerow(fields)
                    print(f"Registered new channel {channel} successfully")
                    await ctx.send(f"**Registered new channel {channel} "
                                   f"successfully **")

        if not valid_channel:
            print(f"No channel {channel} on {ctx.guild}")
            await ctx.send(f"**No channel {channel} on {ctx.guild}**")

    @commands.command(name="remove_channel")
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
                if _channel[0] != current_channel.name \
                        or int(_channel[1]) != int(current_channel.id):
                    writer.writerow(_channel)
                else:
                    print(f"Removed channel {_channel[0]} from registry")
                    await ctx.send(f"**Removed channel {_channel[0]} "
                                   f"from registry**")

    @commands.command(name="clear")
    async def clear(self, ctx, number=5):
        channel = ctx.message.channel
        author = ctx.author
        can_send = await ref.check_can_use(ctx, "clear")
        if not can_send:
            return

        if can_send:
            number = int(number)
            await ctx.channel.purge(limit=number)
            temp = await ctx.send(f"**{author.mention} :white_check_mark: "
                                  f"{number} message(s) Cleared!**")
            print(f"Cleared {number} messages from channel: {channel}")
            await asyncio.sleep(2.5)
            await temp.delete()
        else:
            print("User unable to use this command")
            await ctx.channel.send(f"**{author.mention} "
                                   f"You do not have permission to use this!**")

    @commands.command(name="prefix")
    async def prefix(self, ctx, prefix=None):
        can_send = ref.check_can_use(ctx, "prefix")
        if not can_send:
            return

        if ctx.channel.name != "bot_commands" \
                and "Sauce Creators" not in ctx.author.roles:
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

    @commands.command(name="info", alias=['status'])
    async def info(self, ctx):
        can_send = await ref.check_can_use(ctx, "info")
        if not can_send:
            return

        current_datetime = datetime.datetime.now()
        time = current_datetime.time()
        date = current_datetime.date()
        user = self.bot.user.display_name
        info = await ctx.send(f"```{user} {RELEASE_VERSION}\n"
                              f"(C Nathan Estrada 2019\nServer Time: {time}\n"
                              f"Server Date: {date}```")

        await asyncio.sleep(5)
        await info.delete()
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Util(bot))
