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

    @commands.command(name="morejpeg",
                      aliases=["jpeg", "needsmorejpeg"],
                      pass_context=True)
    async def more_jpeg(self, ctx, url=None):
        can_send = await check_can_use(ctx, "jpeg")
        if not can_send:
            return

        channel = ctx.message.channel
        img = ""

        if url is None:
            # Get link to previous image in chat
            async for x in channel.history(limit=2):
                if x.content != "needsmorejpeg" \
                        or x.content != "needs more jpeg" \
                        or x.content != "morejpeg" \
                        or x.content != "more jpeg":
                    if not x.attachments:
                        img = x.content
                    else:
                        img = x.attachments[0].url
            print(f"Got URL {img} from message")
        else:
            img = url

        ext = os.path.splitext(img)[1]

        if ext != ".gif":
            try:
                # Download image locally to server
                async with aiohttp.ClientSession() as session:
                    async with session.get(img) as resp:
                        if resp.status == 200:
                            try:
                                img_path = f"{DOWNLOAD_DIRECTORY}" \
                                               f"/needs_more." + ext
                                file = await aiofiles.open(img_path, mode="wb")
                                await file.write(await resp.read())
                                await file.close()
                            except Exception as e:
                                print("Failed to download image from URL")
                                print(e)

                            try:
                                # Save as JPEG in lowest quality and send it
                                im = Image.open(img_path)
                                im = im.convert("RGB")
                                im.save(f"{DOWNLOAD_DIRECTORY}/more_jpeg.jpeg",
                                        format="jpeg",
                                        quality=1)
                                await channel.send(file=discord.File(
                                    f"{DOWNLOAD_DIRECTORY}"
                                    f"/more_jpeg.jpeg"))
                                print("Sent image to server successfully")
                            except Exception as e:
                                print(f"Failed to send image to sever")
                                print(e)

                    # Delete off server
                    try:
                        os.remove(img_path)
                        os.remove(f"{DOWNLOAD_DIRECTORY}/more_jpeg.jpeg")
                        print(f"Removed {img_path} and {DOWNLOAD_DIRECTORY}"
                              f"/more_jpeg.jpeg from disk")
                    except Exception as e:
                        print(f"Failed to remove {img_path} and "
                              f"{DOWNLOAD_DIRECTORY}"
                              f"/more_jpeg.jpeg from disk")
                        print(e)
            except Exception as e:
                print(e)

                error = "No image found in message"

                await channel.send("```" + error + "```")
        else:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(img) as resp:
                        if resp.status == 200:
                            try:
                                img_path = \
                                    f"{DOWNLOAD_DIRECTORY}/needs_more.gif"
                                file = await aiofiles.open(img_path, mode="wb")
                                await file.write(await resp.read())
                                await file.close()
                                print("Saved GIF image to disk")
                            except Exception as e:
                                print("Failed to Save GIF image to disk")
                                print(e)
                try:
                    if not os.path.isdir(JPEG_DIRECTORY):
                        os.mkdir(JPEG_DIRECTORY)
                except Exception as e:
                    print("Failed to create JPEG directory")
                    print(e)
                # Send modified GIF to server chat

                try:
                    await channel.send(file=await self.assemble_gif(
                        img_path, JPEG_DIRECTORY))

                    print("Sent converted GIF to server")
                except Exception as e:
                    print("Failed to convert GIF and send to server!")
                    print(e)

                # Remove files from server
                shutil.rmtree(JPEG_DIRECTORY)
                os.remove(img_path)
                os.remove(f"{DOWNLOAD_DIRECTORY}/more_jpeg.gif")
            except Exception as e:
                print(e)

                error = "No image found in message"

                await channel.send("```" + error + "```")

    @staticmethod
    async def assemble_gif(in_gif, out_folder):
        try:
            frame = Image.open(in_gif)
            nframes = 0
            while frame:
                frame.save( '%s/%s-%s.gif' % (out_folder,
                                              os.path.basename(in_gif),
                                              nframes),
                            'GIF', quality=1)
                nframes += 1
                try:
                    frame.seek(nframes)
                except EOFError:
                    break
        except Exception as e:
            print(f"Failed to extract {in_gif} file to directory {out_folder}")
            print(e)

        files = [f for f in listdir(out_folder) if isfile(join(out_folder, f))]
        images = []

        try:
            for file in files:
                img = f"{JPEG_DIRECTORY}/{file}"
                im = Image.open(img)
                im = im.convert("RGB")
                im.save(f"{img}.jpeg", format="jpeg", quality=1)
                images.append(imageio.imread(f"{img}.jpeg"))
            imageio.mimsave(f"{DOWNLOAD_DIRECTORY}/more_jpeg.gif", images)

            print("Converted image and returned file object!")
            return discord.File(f"{DOWNLOAD_DIRECTORY}/more_jpeg.gif")
        except Exception as e:
            print("Failed to convert GIF and return file object")
            print(e)


def setup(bot):
    bot.add_cog(JPEG(bot))
