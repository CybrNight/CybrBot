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
        self.saturation_val = 4
        self.brightness_val = 4
        self.contrast_val = 20
        self.sharpness_val = 300

        self.bot.loop.create_task(self.initialize())

    async def initialize(self):
        await self.bot.wait_until_ready()
        # Get saturation, brightness, contrast, and sharpness values from environ vars
        try:
            self.saturation_val = int(os.environ["FRY_SAT"])
            self.brightness_val = int(os.environ["FRY_BRIGHT"])
            self.contrast_val = int(os.environ["FRY_CONTRAST"])
            self.sharpness_val = int(os.environ["FRY_SHARPNESS"])
            print("Loaded fry values from os.environ")
        # Use defaults when unable to get values from vars
        except Exception as e:
            print(e)
            print("Unable to access environment variables for deep fry! Using default values!")
            self.saturation_val = 4
            self.brightness_val = 4
            self.contrast_val = 20
            self.sharpness_val = 300

    @commands.command(name="deepfry", pass_context=True)
    async def deepfry(self, ctx, url=None):
        channel = ctx.message.channel

        img = ""

        try:
            if url is None:
                # Get image above message in chat
                async for x in channel.history(limit=2):
                    if x.content != "deepfry" or x.content != "deep fry":
                        if not x.attachments:
                            img = x.content
                        else:
                            img = x.attachments[0].url
                            print("Found image in message")
            else:
                img = url
        except Exception as e:
            print(e)
            print("Unable to find image attachment in previous message")

        # Grab the file extension
        ext = os.path.splitext(img)[1]

        if ext != ".gif":

            # Get file and save it locally
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(img) as resp:
                        if resp.status == 200:
                            img_path = f"{DOWNLOAD_DIRECTORY}/deep_fried." + ext
                            file = await aiofiles.open(img_path, mode="wb")
                            await file.write(await resp.read())
                            await file.close()
                print("Downloaded image file from url")
            except Exception as e:
                print(e)
                print("Failed to download image file")

            # Open with PIL and modify
            try:
                img = Image.open(img_path)
                saturated = ImageEnhance.Color(img).enhance(self.saturation_val)
                brightness = ImageEnhance.Brightness(saturated).enhance(self.brightness_val)
                contrast = ImageEnhance.Contrast(brightness).enhance(self.contrast_val)
                final = ImageEnhance.Sharpness(contrast).enhance(self.sharpness_val)
                final.save(img_path, format="png")
                await channel.send("**Fresh from the fryer!**", file=discord.File(img_path))
                print("Successfully modifiied downloaded image")
            except Exception as e:
                print(e)
                print("Failed while modifiying image")

            # Delete file from disk
            os.remove(img_path)
            await ctx.message.delete()
        else:
            # Download GIF
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(img) as resp:
                        if resp.status == 200:
                            img_path = f"{DOWNLOAD_DIRECTORY}/deepfry." + ext
                            file = await aiofiles.open(img_path, mode="wb")
                            await file.write(await resp.read())
                            await file.close()
            except Exception as e:
                print(e)
                print("Failed to download GIF file from url")

            try:
                # Create exraction directory
                if not os.path.isdir(FRY_DIRECTORY):
                    os.mkdir(FRY_DIRECTORY)
            except Exception as e:
                print(e)
                print("Failed to create directory for extracting GIF")

            # Send fried GIF to server chat
            await channel.send("**Fresh from the fryer!**", file=await self.assemble_gif(img_path, FRY_DIRECTORY))

            # Delete off server
            shutil.rmtree(FRY_DIRECTORY)
            os.remove(img_path)
            os.remove(f"{DOWNLOAD_DIRECTORY}/deep_fried.gif")

    @commands.Cog.listener()
    async def on_message(self, message):
        # Get channel and content of message for parsing
        channel = message.channel
        content = str(message.content).lower()

    async def assemble_gif(self, in_gif, out_folder):
        # Open GIF

        try:
            frame = Image.open(in_gif)
            n_frames = 0
            while frame:
                # Iterate through whole GIF and save each frame
                frame.save('%s/%s-%s.gif' % (out_folder, os.path.basename(in_gif), n_frames), 'GIF', quality=1)
                n_frames += 1
                try:
                    frame.seek(n_frames)
                except EOFError:
                    break
        except Exception as e:
            print(e)
            print("Failed to extract GIF frames")

        # Get list of all files in download directory
        files = []
        try:
            files = [f for f in listdir(out_folder) if isfile(join(out_folder, f))]
        except Exception as e:
            print(e)
            print("Failed to load individual frames")

        images = []

        # Modify each frame
        try:
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
            imageio.mimsave(f"{DOWNLOAD_DIRECTORY}/deep_fried.gif", images)

            # Return Discord file object that can be sent to server
            return discord.File(f"{DOWNLOAD_DIRECTORY}/deep_fried.gif")
        except Exception as e:
            print(e)
            print("Failed to save modified GIF file and return file object")


def setup(bot):
    bot.add_cog(DeepFry(bot))
