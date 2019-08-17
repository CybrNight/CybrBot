import discord
from discord.ext import commands
from discord.utils import get
import aiohttp
import youtube_dl
import os
import asyncio

from bot.reference import *


class Voice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.players = {}
        self.youtube_id = ""
        self.queue = []
        self.queue_index = 0

        self.bot.loop.create_task(self.initialize())

    async def initialize(self):
        await self.bot.wait_until_ready()
        if not discord.opus.is_loaded():
            discord.opus.load_opus('opus')

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            print(f"Disconnected from {channel}")
            await ctx.send(f"```Left {channel}```")
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
            await ctx.send(f"```Joined {channel}```")

    @commands.command(pass_context=True)
    async def play(self, ctx):
        server = ctx.guild

        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            print(f"Connected to {channel}\n")
            await ctx.send(f"```Joined {channel}```")

        file = self.queue[self.queue_index]
        full_file = f"{AUDIO_DIRECTORY}/{self.queue[self.queue_index]}.mp3"

        voice.play(discord.FFmpegPCMAudio(full_file), after=lambda e: os.remove(full_file))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07

        print(f"Playing {file}")
        await ctx.send(f"```Playing {file}```")


    @commands.command(pass_context=True, name="queue")
    async def queue_control(self, ctx, option="-v", url=None):
        print(option)
        ctx.message.delete()
        if option == "-c":
            self.queue.clear()
            for file in os.listdir(AUDIO_DIRECTORY):
                os.remove(f"{AUDIO_DIRECTORY}/{file}")
            await ctx.send("```Cleared Queue```")
            print("Cleared music queue")
            return
        elif option == "-v":
            i = 1
            queue_list = ""
            for song in self.queue:
                queue_list += f"{i}. {song}\n"
                i += 1
            await ctx.send(f"```{queue_list}```")
            return
        elif option == "-a":
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": f"{AUDIO_DIRECTORY}/%(title)s.%(ext)s",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }],
            }

            print(f"Adding {url} to song queue")
            adding_msg = await ctx.send(f"Adding {url} to queue!")
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    print("Download started")
                    result = ydl.extract_info(url, download=True)

                    if "entries" in result:  # Add playlist support
                            video = result[0]
                    else:
                            video = result  # Just Video

                print(f"Added {url}")
                await adding_msg.delete()
                self.queue.append(video["title"])
                embed_queue = discord.Embed(title=f"Added {video['title']}", color=0x00ff00)
                embed_queue.set_image(url=video["thumbnail"])
                queue_length = len(self.queue)
                embed_queue.add_field(name=f"{queue_length} song(s) in queue", value=f"/play to play queue")
                temp = await ctx.send(embed=embed_queue)
                print(f"Added {video['tile']} to song queue")
            except Exception as e:
                print(e)
                print("Error downloading file")
            return
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Voice(bot))
