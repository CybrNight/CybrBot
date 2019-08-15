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

        # Generate default values
        self.saturation_val = 4
        self.brightness_val = 4
        self.contrast_val = 20
        self.sharpness_val = 300

        # Get saturation, brightness, contrast, and sharpness values from environ vars
        try:
            self.saturation_val = int(os.environ.get("FRY_SAT"))
            self.brightness_val = int(os.environ.get("FRY_BRIGHT"))
            self.contrast_val = int(os.environ.get("FRY_CONTRAST"))
            self.sharpness_val = int(os.environ.get("FRY_SHARPNESS"))
        # Use defaults when unable to get values from vars
        except Exception as e:
            print(e)
            print("Unable to access environment variables! Using default values!")

    @commands.Cog.listener()
    async def on_message(self, message):
        # Get channel and content of message for parsing
        channel = message.channel
        content = str(message.content).lower()

        # Check if message is deep fry or deepfry
        if content == "deepfry" or content == "deep fry":
            number = 2
            img = ""

            # Get image above message in chat
            async for x in channel.history(limit=number):
                if x.content != "deepfry" or x.content != "deep fry":
                    if not x.attachments:
                        img = x.content
                    else:
                        img = x.attachments[0].url

            # Grab the file extension
            ext = os.path.splitext(img)[1]

            if ext != ".gif":

                # Get file and save it locally
                async with aiohttp.ClientSession() as session:
                    async with session.get(img) as resp:
                        if resp.status == 200:

                            img_path = f"{DOWNLOAD_DIRECTORY}/deepfried." + ext
                            file = await aiofiles.open(img_path, mode="wb")
                            await file.write(await resp.read())
                            await file.close()

                # Open with PIL and "enhance" it
                img = Image.open(img_path)
                saturated = ImageEnhance.Color(img).enhance(self.saturation_val)
                brightness = ImageEnhance.Brightness(saturated).enhance(self.brightness_val)
                contrast = ImageEnhance.Contrast(brightness).enhance(self.contrast_val)
                final = ImageEnhance.Sharpness(contrast).enhance(self.sharpness_val)

                # Write editrd picture to disk
                final.save(img_path, format="png")
                await channel.send("Fresh from the fryer!", file=discord.File(img_path))

                # Delete file from disk
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

                # Send fried GIF to server chat
                await channel.send("Fresh from the fryer!", file=await self.assemble_gif(img_path, FRY_DIRECTORY))

                # Delete off server
                shutil.rmtree(FRY_DIRECTORY)
                os.remove(img_path)
                os.remove(f"{DOWNLOAD_DIRECTORY}/deepfried.gif")

    async def assemble_gif(self, in_gif, out_folder):
        # Open GIF
        frame = Image.open(in_gif)
        nframes = 0
        while frame:
            # Iterate through whole GIF and save each frame
            frame.save('%s/%s-%s.gif' % (out_folder, os.path.basename(in_gif), nframes), 'GIF', quality=1)
            nframes += 1
            try:
                frame.seek(nframes)
            except EOFError:
                break

        # Get list of all files in download directory
        files = [f for f in listdir(out_folder) if isfile(join(out_folder, f))]
        images = []

        # Modify each frame
        for file in files:
            img = f"{FRY_DIRECTORY}/{file}"
            im = Image.open(img)
            im = im.convert("RGB")
            saturated = ImageEnhance.Color(im).enhance(self.saturation_val)
            brightness = ImageEnhance.Brightness(saturated).enhance(self.brightness_val)
            contrast = ImageEnhance.Contrast(brightness).enhance(self.contrast_val)
            final = ImageEnhance.Sharpness(contrast).enhance(self.sharpness_val)

            # Save final image and append to images array
            final.save(img + ".jpeg", format="jpeg")
            images.append(imageio.imread(img + ".jpeg"))

        # Generate GIF from images array
        imageio.mimsave(f"{DOWNLOAD_DIRECTORY}/deepfried.gif", images)

        # Return Discord file object that can be sent to server
        return discord.File(f"{DOWNLOAD_DIRECTORY}/deepfried.gif")


def setup(bot):
    bot.add_cog(DeepFry(bot))
