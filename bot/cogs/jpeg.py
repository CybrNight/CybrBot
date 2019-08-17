import shutil
from os import listdir
from os.path import isfile, join

import aiofiles
import aiohttp
import discord
import imageio
from PIL import Image
from discord.ext import commands

from bot.reference import *


class JPEG(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self,message):
        channel = message.channel
        content = str(message.content).lower()

        # Takes previous image in chat and compresses it
        if content.lower().startswith("needsmorejpeg") or content.lower().startswith("needs more jpeg") \
                or content.lower().startswith("morejpeg") or content.lower().startswith("more jpeg"):
            number = 2
            img = ""

            # Get link to previous image in chat
            async for x in channel.history(limit=number):
                if x.content != "needsmorejpeg" or x.content != "needs more jpeg" or x.content != "morejpeg" \
                        or x.content != "more jpeg":
                    if not x.attachments:
                        img = x.content
                    else:
                        img = x.attachments[0].url

            ext = os.path.splitext(img)[1]

            if ext != ".gif":
                try:
                    # Download image locally to server
                    async with aiohttp.ClientSession() as session:
                        async with session.get(img) as resp:
                            if resp.status == 200:
                                img_path = f"{DOWNLOAD_DIRECTORY}/needsmore."+ext
                                file = await aiofiles.open(img_path, mode="wb")
                                await file.write(await resp.read())
                                await file.close()

                                # Save as JPEG in lowest quality and send it
                                im = Image.open(img_path)
                                im = im.convert("RGB")
                                im.save(f"{DOWNLOAD_DIRECTORY}/morejpeg.jpeg", format="jpeg", quality=1)
                                await channel.send(file=discord.File(f"{DOWNLOAD_DIRECTORY}/morejpeg.jpeg"))

                        # Delete off server
                        os.remove(img_path)
                        os.remove(f"{DOWNLOAD_DIRECTORY}/morejpeg.jpeg")
                except Exception as e:
                    print(e)

                    error = "No image found in message"

                    await channel.send("```" + error + "```")
            else:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(img) as resp:
                            if resp.status == 200:
                                img_path = f"{DOWNLOAD_DIRECTORY}/needsmore.gif"
                                file = await aiofiles.open(img_path, mode="wb")
                                await file.write(await resp.read())
                                await file.close()

                    if not os.path.isdir(JPEG_DIRECTORY):
                        os.mkdir(JPEG_DIRECTORY)

                    # Send modified GIF to server chat
                    await channel.send(file=await self.assemble_gif(img_path, JPEG_DIRECTORY))

                    # Remove files from server
                    shutil.rmtree(JPEG_DIRECTORY)
                    os.remove(img_path)
                    os.remove(f"{DOWNLOAD_DIRECTORY}/morejpeg.gif")
                except Exception as e:
                    print(e)

                    error = "No image found in message"

                    await channel.send("```" + error + "```")

    @staticmethod
    async def assemble_gif(in_gif, out_folder):
        frame = Image.open(in_gif)
        nframes = 0
        while frame:
            frame.save( '%s/%s-%s.gif' % (out_folder, os.path.basename(in_gif), nframes), 'GIF', quality=1)
            nframes += 1
            try:
                frame.seek(nframes)
            except EOFError:
                break
        files = [f for f in listdir(out_folder) if isfile(join(out_folder, f))]
        images = []

        for file in files:
            img = f"{JPEG_DIRECTORY}/{file}"
            im = Image.open(img)
            im = im.convert("RGB")
            im.save(f"{img}.jpeg", format="jpeg", quality=1)
            images.append(imageio.imread(f"{img}.jpeg"))
        imageio.mimsave(f"{DOWNLOAD_DIRECTORY}/morejpeg.gif", images)

        return discord.File(f"{DOWNLOAD_DIRECTORY}/morejpeg.gif")


def setup(bot):
    bot.add_cog(JPEG(bot))
