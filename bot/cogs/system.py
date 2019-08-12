import asyncio

from discord.ext import commands


class System(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.initialize())
        self.reference = Reference()

    async def initialize(self):
        await self.bot.wait_until_ready()

        self.reference.set_guild(self.bot.get_guild(241338870208266250))

        for role in self.reference.guild.roles:
            if role.name == "Beta Tester":
                self.reference.set_beta_role(role)
        for channel in self.reference.guild.channels:
            if channel.name == "general":
                self.reference.set_general_chat(channel)
            if channel.name == "beta-testers":
                self.reference.set_beta_chat(channel)

    @commands.command(name="switch_server", pass_context=True)
    async def debug(self, ctx, *args):
        if ctx.author.id != 229773126936821760:
            print(self.reference.guild.id)
            return
        if args.__len__() <= 0:
            guild = ctx.guild
        else:
            guild = self.bot.get_guild(int(args[0]))

        if guild == self.reference.guild.id:
            return

        self.reference.set_guild(guild)

        for role in guild.roles:
            if role.name == "Beta Tester":
                self.reference.set_beta_role(role)
        for channel in guild.channels:
            if channel.name == "general":
                self.reference.set_general_chat(channel)
            if channel.name == "beta-testers":
                self.reference.set_beta_chat(channel)

        msg = await ctx.channel.send("SWITCHING TO SERVER {0}".format(guild))
        print("Running on {0}".format(guild))
        await asyncio.sleep(2.5)
        await msg.delete()


class Reference:
    _guild = None
    _beta_role = None
    _general_chat = None
    _beta_chat = None

    @property
    def guild(self):
        return self._guild

    @classmethod
    def set_guild(self, value):
        self._guild = value

    @property
    def general_chat(self):
        return self._general_chat

    @classmethod
    def set_general_chat(self, value):
        self._general_chat = value

    @property
    def beta_chat(self):
        return self._beta_chat

    @classmethod
    def set_beta_chat(self, value):
        self._beta_chat = value

    @property
    def beta_role(self):
        return self._beta_role

    @classmethod
    def set_beta_role(self, value):
        self._beta_role = value


def setup(bot):
    bot.add_cog(System(bot))
