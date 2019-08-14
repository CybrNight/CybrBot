import os

import aiofiles, aiohttp
import discord
from PIL import Image, ImageEnhance

from bot import reference as ref
from discord.ext import commands
import shutil, imageio
from os import listdir
from os.path import isfile, join

class Context(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def embed_json(data, key="message"):
        em = discord.Embed(color=0xe09d00)
        em.set_image(url=data[key])
        return em

    @staticmethod
    def embed_image(img):
        em = discord.Embed(color=0xe09d00)
        em.set_image(url=img)
        return em

    @commands.Cog.listener()
    async def on_message(self, message):
        # we do not want the self.bot to reply to itself
        if message.author == self.bot.user:
            return

        content = str(message.content).lower()
        channel = message.channel

        if content.startswith('.'):
            return

        # Autism picture command
        if content.startswith("autism"):
            msg = content.split(" ")
            if len(msg) > 1:
                msg.pop(0)
                await channel.send(">literally " + str(" ").join(msg),
                                    embed=self.embed_image("http://i.imgur.com/g9O5snh.png"))

        if content.startswith("mechanized autism"):
            await channel.send("Mechanzied Autism", embed=self.embed_image("https://i.imgur.com/HlvFNXW.gif"))

        # Sends current prefix to chat
        if content.startswith("prefix?"):
            await channel.send("```The current prefix is " + "'" + ref.BOT_PREFIX + "'```")
            await message.delete()

        # Sends eye=patch picture to chat
        if content.__contains__("fuck you"):
            await channel.send(embed=self.embed_image("https://i.imgur.com/9hZyYly.jpg"))

        # Sends lewd gif
        if content.__contains__("lewd"):
            await channel.send(embed=self.embed_image("[img]https://i.imgur.com/3geE8aq.gif"))

        # Sends nyanpasu picture
        if content.startswith("nyanpasu"):
            await channel.send("@everyone", embed=self.embed_image("https://i.imgur.com/Ca6EuUP.png"))
            await message.delete()

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
                            img = x.attachments[0].url
                        else:
                            img = x.content

                # Download image locally to server

                ext = os.path.splitext(img)[1]

                if ext != ".gif":
                    try:
                        async with aiohttp.ClientSession() as session:
                            async with session.get(img) as resp:
                                if resp.status == 200:
                                    file = await aiofiles.open("morejpeg.jpeg", mode="wb")
                                    await file.write(await resp.read())
                                    await file.close()

                                    # Save as JPEG in lowest quality and send it
                                    im = Image.open("morejpeg.jpeg")
                                    im = im.convert("RGB")
                                    im.save("morejpeg.jpeg", format="jpeg", quality=1)
                                    await channel.send(file=discord.File("morejpeg.jpeg"))

                            # Delete off server
                            os.remove("morejpeg.jpeg")
                    except Exception as e:
                        print(e)

                        error = "No image found in message"

                        await channel.send("```" + error + "```")
                else:
                    try:
                        async with aiohttp.ClientSession() as session:
                            async with session.get(img) as resp:
                                if resp.status == 200:
                                    file = await aiofiles.open("morejpeg.gif", mode="wb")
                                    await file.write(await resp.read())
                                    await file.close()

                        if not os.path.isdir(os.getcwd() + "/download/gif"): os.mkdir(os.getcwd() + "/download/gif")
                        await channel.send(file=discord.File(
                            await self.assemble_gif("morejpeg.gif", os.getcwd() + "/download/gif")))
                        # Delete off server
                        shutil.rmtree(os.getcwd() + "/download/gif")
                        os.remove("jpeg.gif")
                        os.remove("morejpeg.gif")
                    except Exception as e:
                        print(e)

                        error = "No image found in message"

                        await channel.send("```" + error + "```")

    async def assemble_gif(self, inGif, outFolder):
        frame = Image.open(inGif)
        nframes = 0
        while frame:
            frame.save('%s/%s-%s.gif' % (outFolder, os.path.basename(inGif), nframes), 'GIF', quality=1)
            nframes += 1
            try:
                frame.seek(nframes)
            except EOFError:
                break
        files = [f for f in listdir(outFolder) if isfile(join(outFolder, f))]
        images = []

        for file in files:
            img = os.getcwd() + "/download/gif/" + file
            im = Image.open(img)
            im = im.convert("RGB")
            im.save(img + ".jpeg", format="jpeg", quality=1)
            images.append(imageio.imread(os.getcwd() + "/download/gif/" + file + ".jpeg"))
        imageio.mimsave('jpeg.gif', images)

        return "jpeg.gif"

def setup(bot):
    bot.add_cog(Context(bot))
