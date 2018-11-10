import os

import aiofiles
import aiohttp
import discord
from PIL import Image, ImageEnhance

from bot import reference as ref

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

class Context:
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

    async def on_message(self, message):
        # we do not want the self.bot to reply to itself
        if message.author == self.bot.user:
            return

        content = str(message.content).lower()

        if content.startswith('.'):
            return

        # Autism picture command
        if content.startswith("autism"):
            msg = content.split()
            if len(msg) <= 1:
                await self.bot.send_message(message.channel, ">literally(You)",
                                            embed=self.embed_image("http://i.imgur.com/g9O5snh.png"))
                await self.bot.delete_message(message)
            else:
                await self.bot.send_message(message.channel, ">literally " + str(" ").join(msg),
                                            embed=self.embed_image("http://i.imgur.com/g9O5snh.png"))
                await self.bot.delete_message(message)

        # Sends current prefix to chat
        if content.startswith("prefix?"):
            await self.bot.send_message(message.channel, "```The current prefix is " + "'" + ref.BOT_PREFIX + "'```")
            await self.bot.delete_message(message)

        # Sends eye=patch picture to chat
        if content.__contains__("fuck you"):
            await self.bot.send_message(message.channel, embed=self.embed_image("https://i.imgur.com/9hZyYly.jpg"))

        # Sends nyanpasu picture
        if content.startswith("nyanpasu"):
            await self.bot.send_message(message.channel, "@everyone",
                                        embed=self.embed_image("https://i.imgur.com/Ca6EuUP.png"))
            await self.bot.delete_message(message)

        # Takes previous image in chat and compresses it
        if content.lower().startswith("needsmorejpeg") or content.lower().startswith("needs more jpeg") \
                or content.lower().startswith("morejpeg") or content.lower().startswith("more jpeg"):
            number = 2
            img = ""

            # Get link to previous image in chat
            async for x in self.bot.logs_from(message.channel, limit=number):
                if x.content != "needsmorejpeg" or x.content != "needs more jpeg" or x.content != "morejpeg" \
                        or x.content != "more jpeg":
                    if x.content == "":
                        img = x.attachments[0]["url"]
                    else:
                        img = x.content

            # Download image locally to server
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
                            await self.bot.send_file(message.channel, "morejpeg.jpeg")

                    # Delete off server
                    os.remove("morejpeg.jpeg")
            except Exception as e:
                print(e)
                await self.bot.send_message(message.channel, "```Found no image :(```")

        # Deep fry previous image
        if content.lower().startswith("deepfry") or content.lower().startswith("deep fry"):
            number = 2
            img = ""

            # et previous image in chat
            async for x in self.bot.logs_from(message.channel, limit=number):
                if x.content != "deep fry" or x.content != "deep fry":
                    if x.content == "":
                        img = x.attachments[0]["url"]
                    else:
                        img = x.content

            # Download image from URL
            try:
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
                            await self.bot.send_file(message.channel, "deepfried.png")

                    # Delete temp picture file
                    os.remove("deepfried.png")
            except Exception as e:
                print(e)
                await self.bot.send_message(message.channel, "```Found no image```")


def setup(bot):
    bot.add_cog(Context(bot))
