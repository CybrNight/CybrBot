# Media Cog

from discord.ext import commands

from bot.mediascraper import *

hh = HentaiHaven()
ph = PornHub()
r34 = Rule34()
gb = Gelbooru()


class Media:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hentaihaven', aliases=['hh', 'hentai'], pass_context=True)
    async def hentai_haven(self, ctx, *args):
        video = await hh.category_search(str(" ").join(args))
        await self.bot.say(video)
        return

    @commands.command(name='pornhub', aliases=['ph', 'porn'], pass_context=True)
    async def porn_hub(self, ctx, *args):
        video = await ph.video_search(str(" ").join(args))
        await self.bot.say(video)

    @commands.command(name='r34', alias=['rule34'], pass_context=True)
    async def rule34(self, ctx, *args):
        video = await r34.image_search(str(" ").join(args))
        await self.bot.say(video)

    @commands.command(name='gb', aliases=['gbooru', 'gelbooru'], pass_context=True)
    async def gelbooru(self, ctx, *args):
        video = await gb.image_search(str(" ").join(args))
        await self.bot.say(video)


def setup(bot):
    bot.add_cog(Media(bot))
