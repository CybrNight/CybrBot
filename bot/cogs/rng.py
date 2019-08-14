import asyncio
import random

from discord.ext import commands


class RNG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Magic 8-Ball Command
    @commands.command(name='8ball',
                      aliases=['eight_ball', 'eightball', '8-ball'],
                      pass_context=True)
    async def eight_ball(self, ctx):
        possible_responses = [
            'That is a resounding no',
            'It is not looking likely',
            'Too hard to tell',
            'It is quite possible',
            'Definitely',
        ]
        await ctx.channel.send(random.choice(possible_responses) + ", " + ctx.message.author.mention)

    # Coin Flip Command
    @commands.command(name="coinflip", aliases=['flipacoin', 'flipcoin'], pass_context=True)
    async def coin_flip(self, ctx):
        await ctx.channel.send("Flipping coin...")
        await asyncio.sleep(0.5)
        possible_outcomes = ['Heads', 'Tails']
        await ctx.channel.send("It's " + random.choice(possible_outcomes))

    # Dice Roll Command
    @commands.command(name="diceroll", aliases=['rolldie', 'rolladie'], pass_context=True)
    async def dice_roll(self, ctx):
        await ctx.channel.send(":game_die: Rolling die...")
        await asyncio.sleep(0.5)
        number = random.randint(1, 6)
        await ctx.channel.send("It's " + str(number))


def setup(bot):
    bot.add_cog(RNG(bot))
