# Media Cog

from discord.ext import commands
import discord

from bot.mediascraper import *
from discord.ext import commands

hh = HentaiHaven()
ph = PornHub()
r34 = Rule34()
gb = Gelbooru()


class Media(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def embed_image(img):
        em = discord.Embed(color=0xe09d00)
        em.set_image(url=img)
        return em

    @commands.command(name='hentaihaven', aliases=['hh', 'hentai'], pass_context=True)
    async def hentai_haven(self, ctx, *args):
        video = await hh.category_search(str(" ").join(args))
        await ctx.channel.send(video)
        return

    @commands.command(name='pornhub', aliases=['ph', 'porn'], pass_context=True)
    async def porn_hub(self, ctx, *args):
        video = await ph.video_search(str(" ").join(args))
        await ctx.channel.send(video)

    @commands.command(name='r34', alias=['rule34'], pass_context=True)
    async def rule34(self, ctx, *args):
        image = await r34.image_search(str(" ").join(args))
        await ctx.channel.send(image)

    @commands.command(name='gb', aliases=['gbooru', 'gelbooru'], pass_context=True)
    async def gelbooru(self, ctx, *args):
        image = await gb.image_search(str(" ").join(args))
        await ctx.channel.send(image)


def setup(bot):
    bot.add_cog(Media(bot))
