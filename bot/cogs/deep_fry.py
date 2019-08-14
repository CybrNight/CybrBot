import shutil
from os import listdir
from os.path import isfile, join

import aiofiles
import aiohttp
import discord
import imageio
from PIL import Image, ImageEnhance
from discord.ext import commands

from bot.reference import *


class DeepFry(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel
        content = str(message.content).lower()

        # Check if message is deep fry or deepfry
        if content == "deepfry" or content == "deep fry":
            number = 2
            img = ""

            # Get previous image in chat
            async for x in channel.history(limit=number):
                if x.content != "deepfry" or x.content != "deep fry":
                    if not x.attachments:
                        img = x.content
                    else:
                        img = x.attachments[0].url

            ext = os.path.splitext(img)[1]

            if ext != ".gif":
                async with aiohttp.ClientSession() as session:
                    async with session.get(img) as resp:
                        if resp.status == 200:

                            # Get deep fry values
                            try:
                                saturation_val = int(os.environ.get("FRY_SAT"))
                                brightness_val = int(os.environ.get("FRY_BRIGHT"))
                                contrast_val = int(os.environ.get("FRY_CONTRAST"))
                                sharpness_val = int(os.environ.get("FRY_SHARPNESS"))
                            except Exception as e:
                                print(e)
                                saturation_val = 4
                                brightness_val = 4
                                contrast_val = 20
                                sharpness_val = 300

                            img_path = f"{DOWNLOAD_DIRECTORY}/deepfried." + ext
                            file = await aiofiles.open(img, mode="wb")
                            await file.write(await resp.read())
                            await file.close()

                # Open with PIL and "enhance" it
                img = Image.open(img_path)
                saturated = ImageEnhance.Color(img).enhance(saturation_val)
                brightness = ImageEnhance.Brightness(saturated).enhance(brightness_val)
                contrast = ImageEnhance.Contrast(brightness).enhance(contrast_val)
                final = ImageEnhance.Sharpness(contrast).enhance(sharpness_val)

                # Write editrd picture to disk
                final.save(img_path, format="png")
                await channel.send("Fresh from the fryer!", file=discord.File(img_path))

                # Delete temp picture file
                os.remove(img_path)
            else:
                # Download GIF
                async with aiohttp.ClientSession() as session:
                    async with session.get(img) as resp:
                        if resp.status == 200:

                            img_path = f"{DOWNLOAD_DIRECTORY}/deepfry." + ext
                            file = await aiofiles.open(img_path, mode="wb")
                            await file.write(await resp.read())
                            await file.close()

                # Create exraction directory
                if not os.path.isdir(FRY_DIRECTORY):
                    os.mkdir(FRY_DIRECTORY)

                await channel.send("Fresh from the fryer!", file=discord.File(
                    await self.assemble_gif(img_path, FRY_DIRECTORY)))
                # Delete off server
                shutil.rmtree(FRY_DIRECTORY)
                os.remove(img_path)
                os.remove(f"{DOWNLOAD_DIRECTORY}/deepfried.gif")

    @staticmethod
    async def assemble_gif(in_gif, out_folder):
        frame = Image.open(in_gif)
        nframes = 0
        while frame:
            frame.save('%s/%s-%s.gif' % (out_folder, os.path.basename(in_gif), nframes), 'GIF', quality=1)
            nframes += 1
            try:
                frame.seek(nframes)
            except EOFError:
                break

        # Get values for deep fry
        try:
            saturation_val = int(os.environ.get("FRY_SAT"))
            brightness_val = int(os.environ.get("FRY_BRIGHT"))
            contrast_val = int(os.environ.get("FRY_CONTRAST"))
            sharpness_val = int(os.environ.get("FRY_SHARPNESS"))
        except Exception as e:
            print(e)
            saturation_val = 4
            brightness_val = 4
            contrast_val = 20
            sharpness_val = 300

        files = [f for f in listdir(out_folder) if isfile(join(out_folder, f))]
        images = []

        for file in files:
            img = f"{FRY_DIRECTORY}/{file}"
            im = Image.open(img)
            im = im.convert("RGB")
            saturated = ImageEnhance.Color(im).enhance(saturation_val)
            brightness = ImageEnhance.Brightness(saturated).enhance(brightness_val)
            contrast = ImageEnhance.Contrast(brightness).enhance(contrast_val)
            final = ImageEnhance.Sharpness(contrast).enhance(sharpness_val)
            final.save(img + ".jpeg", format="jpeg")
            images.append(imageio.imread(img + ".jpeg"))
        imageio.mimsave(f"{DOWNLOAD_DIRECTORY}/deepfried.gif", images)

        return f"{DOWNLOAD_DIRECTORY}/deepfried.gif"


def setup(bot):
    bot.add_cog(DeepFry(bot))
