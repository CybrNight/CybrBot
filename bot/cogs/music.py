import discord
from discord.ext import commands
from discord.utils import get
import aiohttp
import youtube_dl
import datetime
import os
import asyncio

from bot.reference import *


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.queue = {}
        self.queue_index = 0
        self.ydl_opts = None

        self.bot.loop.create_task(self.initialize())

    async def initialize(self):
        await self.bot.wait_until_ready()
        if not discord.opus.is_loaded():
            discord.opus.load_opus('opus')

        self.ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "outtmpl": f"{AUDIO_DIRECTORY}/%(title)s.%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            }],
        }

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            print(f"Disconnected from {channel}")
        else:
            print("Told to leave channel, but not connected to one")

    @commands.command(pass_context=True)
    async def join(self, ctx):
        try:
            global voice
            channel = ctx.message.author.voice.channel
            voice = get(self.bot.voice_clients, guild=ctx.guild)

            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()
                print(f"Connected to {channel}\n")
        except Exception as e:
            print(e)
            msg = await ctx.send("```Must be in voice channel to use this command```")
            await asyncio.sleep(1.5)
            await ctx.message.delete()
            await msg.delete()

    @commands.command(pass_context=True)
    async def play(self, ctx, url=None):
        global voice
        if url is None and len(self.queue) > 0:
            try:
                server = ctx.guild
                channel = ctx.message.author.voice.channel
                voice = get(self.bot.voice_clients, guild=ctx.guild)
            except Exception as e:
                print(e)
                await ctx.send("```Must be in voice channel to use this command```")
                return

            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()
                print(f"Connected to {channel}\n")

            self.queue_index = 0
            self.play_queue(ctx)
            return
        else:
            try:
                server = ctx.guild
                channel = ctx.message.author.voice.channel
                voice = get(self.bot.voice_clients, guild=ctx.guild)
            except Exception as e:
                print(e)
                msg = await ctx.send("```Must be in voice channel to use this command```")
                await asyncio.sleep(1.5)
                await ctx.message.delete()
                await msg.delete()
                return

            await ctx.send(f"**Downloading**: `{url}`")
            song = await self.download_audio(url)
            title = song['title']
            duration = str(datetime.timedelta(seconds=int(song['duration'])))
            thumbnail = song['thumbnail']
            full_file = f"{AUDIO_DIRECTORY}/{title}.mp3"

            try:
                if voice and voice.is_connected():
                    await voice.move_to(channel)
                else:
                    voice = await channel.connect()
                    print(f"Connected to {channel}\n")

                embed_playing = await self.embed_playing(song, url)

                print(f"Playing {title}")
                await ctx.send(embed=embed_playing)

                voice.play(discord.FFmpegPCMAudio(full_file), after=lambda e: os.remove(full_file))
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = float(os.environ["BOT_VOLUME"])
            except Exception as e:
                print(e)
                await ctx.send("`Must be in voice channel to use this command`")
                return

    @commands.command(pass_context=True, name="volume")
    async def volume(self, ctx, volume=None):
        if volume is None:
            await ctx.send(f":speaker:  **Volume is: {os.environ['BOT_VOLUME']}**")
        else:
            os.environ["BOT_VOLUME"] = volume
            await ctx.send(f":speaker:  **Volume set to: {volume}**")

    # Pause music command
    @commands.command(pass_context=True, name="pause")
    async def pause(self, ctx):
        if voice and voice.is_playing():
            await ctx.send("`Paused :pause_button:")
            print("Music paused")
            voice.pause()
        else:
            await ctx.send(":x: **Music not playing**")
            print("Trying to pause music that does not exist")

    @commands.command(pass_context=True, name='resume')
    async def resume(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            await ctx.send("```Music resumed```")
            print("Music paused")
            voice.resume()
        else:
            await ctx.send("```No music to resume```")
            print("Trying to resume music that is not paused")

    @commands.command(pass_context=True, name="stop")
    async def stop(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            await ctx.send("```Music stopped```")
            print("Music stopped")
            voice.stop()
        else:
            msg = await ctx.send(":x: **Music not playing**")
            print("No music to stop!")
        await asyncio.sleep(1.5)

    @commands.command(pass_context=True, name="queue")
    async def queue_control(self, ctx, option=None):
        print(option)
        if option == "clear" or option == "-c":
            self.clear_queue()
            msg = await ctx.send("```Cleared Queue```")
            await asyncio.sleep(2.5)
            await msg.delete()
            print("Cleared music queue")
            return
        elif option is None:
            await ctx.send(embed=await self.build_queue_embed())
            return
        elif option is not None and option is not "clear":
            await asyncio.sleep(0.5)
            print(f"Downloading: `{option}`")
            await ctx.send(f"**Queueing:`{option}`**")
            song = await self.download_audio(option)

            title = song['title']
            duration = str(datetime.timedelta(seconds=int(song['duration'])))
            thumbnail = song["thumbnail"]

            self.queue.update({title: duration})

            embed_queue = await self.embed_queued(song, option)

            user = ctx.message.author
            embed_queue.set_author(name="Added to queue", icon_url=f"https://cdn.discordapp.com/avatars/"
                                                                   f"{user.id}/{user.avatar}.png?size=1024")

            await ctx.send(embed=embed_queue)
            print(f"Added {title} to song queue")
            return
        await ctx.message.delete()

    def play_queue(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if len(self.queue) == 0:
            self.queue_finished(ctx)
        else:
            file = list(self.queue)[self.queue_index]
            full_file = f"{AUDIO_DIRECTORY}/{file}.mp3"

            voice.play(discord.FFmpegPCMAudio(full_file), after=lambda e: self.play_queue(ctx))
            print(self.queue[file])
            del self.queue[file]

        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = float(os.environ["BOT_VOLUME"])

    @commands.command(name="skip", pass_context=True)
    async def skip(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print("Music stopped")
            await ctx.send(":track_next: **Skipped**")
            voice.stop()

            if len(self.queue) > 0:
                await self.play_queue(ctx)
            else:
                self.queue_finished(ctx)
        else:
            msg = await ctx.send(":x: **Music not playing**")
            print("No music to stop!")

    def queue_finished(self, ctx):
        print("Queue done")
        self.clear_queue()

    async def embed_queued(self, song, url):
        title = song['title']
        duration = str(datetime.timedelta(seconds=int(song['duration'])))
        thumbnail = song["thumbnail"]

        print(f"Added {url}")

        embed = discord.Embed(title=f"**{title}**", url=url, color=0x00ff00)
        embed.set_thumbnail(url=thumbnail)
        queue_length = len(self.queue)
        embed.add_field(name="Duration:", value=f"{duration}", inline=False)
        embed.add_field(name=f"{queue_length} song(s) in queue", value=f"/play to play queue\n"
                                                                             f"/queue to view queue", inline=False)

        return embed

    @staticmethod
    async def embed_playing(song, url):
        title = song['title']
        duration = str(datetime.timedelta(seconds=int(song['duration'])))
        thumbnail = song["thumbnail"]

        embed = discord.Embed(title=f"**Playing {title}**", url=url, color=0x00ff00)
        embed.add_field(name=f"Duration:", value=f"{duration}", inline=True)
        embed.set_thumbnail(url=thumbnail)

        return embed

    async def download_audio(self, url):
        try:
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                print("Download started")
                result = ydl.extract_info(url, download=True)

                if "entries" in result:  # Add playlist support
                    video = result[0]
                else:
                    video = result  # Just Video

            return video
        except Exception as e:
            print(e)

    async def build_queue_embed(self):
        i = 1
        queue_embed = discord.Embed(title="Queue", description=f"Song Count:{str(len(self.queue))}", color=0xFFA200)
        if len(self.queue) > 0:
            for song, duration in self.queue.items():
                if i == 1:
                    queue_embed.add_field(name=f"{i}. {song}\n", value=f"-Duration-\n{duration}", inline=True)
                else:
                    queue_embed.add_field(name=f"{i}. {song}\n", value=f"-Duration-\n{duration}", inline=False)
                i += 1
            return queue_embed
        else:
            queue_embed.add_field(name="No songs in queue", value="-")
            return queue_embed

    def clear_queue(self):
        self.queue.clear()
        for file in os.listdir(AUDIO_DIRECTORY):
            print(f"Removeed {file}")
            os.remove(f"{AUDIO_DIRECTORY}/{file}")


def setup(bot):
    bot.add_cog(Music(bot))
