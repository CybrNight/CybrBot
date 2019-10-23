import asyncio
import random

from discord.ext import commands
import bot.reference as ref


class RNG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Magic 8-Ball Command
    @commands.command(name='8ball',
                      aliases=['eight_ball', 'eightball', '8-ball'],
                      pass_context=True)
    async def eight_ball(self, ctx):
        can_send = await ref.check_can_use(ctx, "8ball")
        if not can_send:
            return

        possible_responses = [
            'That is a resounding no',
            'It is not looking likely',
            'Too hard to tell',
            'It is quite possible',
            'Definitely',
        ]
        response = random.choice(possible_responses)
        await ctx.send(f"**{response}, {ctx.message.author.mention}**")
        
    # Coin Flip Command
    @commands.command(name="coinflip", aliases=['flipacoin', 'flipcoin'], pass_context=True)
    async def coin_flip(self, ctx):
        can_send = await ref.check_can_use(ctx, "coinflip")
        if not can_send:
            return

        await ctx.send("**Flipping coin...**")
        await asyncio.sleep(0.5)
        possible_outcomes = ['Heads', 'Tails']
        outcome = random.choice(possible_outcomes)
        await ctx.send(f"**It's {outcome}**")

    # Dice Roll Command
    @commands.command(name="diceroll", aliases=['rolldie', 'rolladie'], pass_context=True)
    async def dice_roll(self, ctx):
        can_send = await ref.check_can_use(ctx, "diceroll")
        if not can_send:
            return

        await ctx.send("**:game_die: Rolling die...**")
        await asyncio.sleep(0.5)
        number = random.randint(1, 6)
        await ctx.send(f"**It's {number}**")


def setup(bot):
    bot.add_cog(RNG(bot))
