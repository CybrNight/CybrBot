import discord
from discord.ext import commands
import aiofiles, aiohttp
from PIL import Image, ImageEnhance
import os, shutil
from os import listdir
from os.path import isfile, join
import imageio

class DeepFry(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.download_dir = os.getcwd()+"/download/deepfry"

    @commands.Cog.listener()
    async def on_message(self,message):
        channel = message.channel
        content = str(message.content).lower()

        # Deep fry previous image
        if content.lower().startswith("deepfry") or content.lower().startswith("deep fry"):
            number = 2
            img = ""

            # et previous image in chat
            async for x in channel.history(limit=number):
                if x.content != "deepfry" or x.content != "deep fry":
                    if x.content == "":
                        img = x.attachments[0].url
                    else:
                        img = x.content

            ext = os.path.splitext(img)[1]

            if ext != ".gif":
                async with aiohttp.ClientSession() as session:
                    async with session.get(img) as resp:
                        if resp.status == 200:

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

                            file = await aiofiles.open("deepfried.png", mode="wb")
                            await file.write(await resp.read())
                            await file.close()

                            # Open with PIL and "enhance" it
                            im = Image.open("deepfried.png")
                            saturated = ImageEnhance.Color(im).enhance(saturation_val)
                            brightness = ImageEnhance.Brightness(saturated).enhance(brightness_val)
                            contrast = ImageEnhance.Contrast(brightness).enhance(contrast_val)
                            final = ImageEnhance.Sharpness(contrast).enhance(sharpness_val)

                            final.save("deepfried.png", format="png")
                            await channel.send("Fresh from the fryer!", file=discord.File("deepfried.png"))

                    # Delete temp picture file
                    os.remove("deepfried.png")
                # Download image from URL
            else:
                print("GIF")
                '''async with aiohttp.ClientSession() as session:
                    async with session.get(img) as resp:
                        if resp.status == 200:

                            file = await aiofiles.open("deepfry.gif", mode="wb")
                            await file.write(await resp.read())
                            await file.close()

                            if not os.path.isdir(self.download_dir): os.mkdir(self.download_dir)
                            await channel.send("Fresh from the fryer!", file=discord.File(
                                await self.assemble_gif("deepfry.gif", self.download_dir)))
                            # Delete off server
                            shutil.rmtree(self.download_dir)
                            os.remove("deepfry.gif")
                            os.remove("deepfried.gif")'''

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

            files = [f for f in listdir(outFolder) if isfile(join(outFolder, f))]
            images = []

            for file in files:
                img = os.getcwd() + "/download/deepfry/" + file
                im = Image.open(img)
                im = im.convert("RGB")
                saturated = ImageEnhance.Color(im).enhance(saturation_val)
                brightness = ImageEnhance.Brightness(saturated).enhance(brightness_val)
                contrast = ImageEnhance.Contrast(brightness).enhance(contrast_val)
                final = ImageEnhance.Sharpness(contrast).enhance(sharpness_val)
                final.save(img+".jpeg", format="jpeg")
                images.append(imageio.imread(img+".jpeg"))
            imageio.mimsave('deepfried.gif', images)

            return "deepfried.gif"

def setup(bot):
    bot.add_cog(DeepFry(bot))