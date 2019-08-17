import discord
from discord.ext import commands
from discord.utils import get
import aiohttp
import youtube_dl
import os
import asyncio


class Voice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.players = {}
        self.song_queue = {}
        self.youtube_id = ""

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            print(f"Disconnected from {channel}")
            await ctx.send(f"```Left {channel}")
        else:
            print("Told to leave channel, but not connected to one")

    @commands.command(pass_context=True)
    async def join(self, ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            print(f"Connected to {channel}\n")
            await ctx.send(f"```Joined {channel}")

    @commands.command(pass_context=True)
    async def play(self, ctx, url: str):
        server = ctx.guild

        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            print(f"Connected to {channel}\n")
            await ctx.send(f"```Joined {channel}```")

    @commands.command(pass_context=True, name="queue")
    async def queue_control(self, ctx, option="-v", url=""):
        if option == "-c":
            self.song_queue.clear()
            await ctx.send("```Cleared Queue```")
        elif option == "-v":
            i = 1
            queue_list = ""
            for url in self.song_queue:
                queue_list += f"{i} {url}\n"
                i += 1
            await ctx.send(f"```{queue_list}```")
        elif option == "-a":
            ydl_opts = {
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }],
            }

            if "https://www.youtube.com" in url:
                try:
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        print("Download started")
                        result = ydl.extract_info(url, download=True)

                        print(result)
                        if "entries" in result:  # Add playlist support
                            video = result[0]
                        else:
                            video = result  # Just Video

                    '''print(f"Added {url}")
                    temp = await ctx.send(f"Added {url} to queue!\n/play to play queue")
                    await ctx.message.delete()
                    await asyncio.sleep(5)
                    await temp.delete()'''
                    self.song_queue.update({video["id"]: video["title"]})
                    print(f"Added {video['tile']} to song queue")
                except Exception as e:
                    print(e)
                    print("Error downloading file")


def setup(bot):
    bot.add_cog(Voice(bot))
