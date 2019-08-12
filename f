import discord
from discord.ext import commands
import aiofiles, aiohttp
from PIL import Image
import os, shutil
from os import listdir
from os.path import isfile, join
import imageio
import asyncio

class JPEG(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self,message):
        channel = message.channel
        content = str(message.content).lower()
        print(content)

        # Takes previous image in chat and compresses it
        if content.lower().startswith("needsmorejpeg") or content.lower().startswith("needs more jpeg") \
                or content.lower().startswith("morejpeg") or content.lower().startswith("more jpeg"):
            number = 2
            img = ""

            # Get link to previous image in chat
            async for x in channel.history(limit=number):
                if x.content != "needsmorejpeg" or x.content != "needs more jpeg" or x.content != "morejpeg" \
                        or x.content != "more jpeg":
                    if x.content == "":
                        img = x.attachments[0]["url"]
                    else:
                        img = x.content

            async with aiohttp.ClientSession() as session:
                async with session.get(img) as resp:
                    if resp.status == 200:
                        file = await aiofiles.open("morejpeg.gif", mode="wb")
                        await file.write(await resp.read())
                        await file.close()

                        os.mkdir(os.getcwd() + "/download/gif/")
                        await self.assemble_gif("morejpeg.gif", os.getcwd() + "/download/gif/")

                        await channel.send(file=discord.File("jpeg.gif"))
                        os.remove("jpeg.gif")
                        os.remove("morejpeg.gif")


                        # Save as JPEG in lowest quality and send it

                        '''
                        im = Image.open("morejpeg.jpeg")
                        im = im.convert("RGB")
                        im.save("morejpeg.jpeg", format="jpeg", quality=1)
                        await channel.send(file=discord.File("morejpeg.jpeg"))'''


    async def assemble_gif(self, inGif, outFolder):
        print(outFolder)
        frame = Image.open(inGif)
        nframes = 0
        frame.save("test.png")
        while frame:
            frame.save( '%s/%s-%s.png' % (outFolder, os.path.basename(inGif), nframes ))
            nframes += 1
            try:
                frame.seek( nframes )
            except EOFError:
                break
        files = [f for f in listdir(outFolder) if isfile(join(outFolder, f))]
        images = []

        print(files)

        for file in files:
            if file == "morejpeg.gif-0.png":
                img = Image.open(outFolder+file)
                palette = img.palette
                img.close()
            else:
                img = Image.open(outFolder+file)
                img = img.convert(palette=palette)
                img.save(outFolder+file)

            images.append(imageio.imread(outFolder+file))
        imageio.mimsave('jpeg.gif', images)
        # shutil.rmtree(outFolder)
        return "jpeg.gif"


def setup(bot):
    bot.add_cog(JPEG(bot))
