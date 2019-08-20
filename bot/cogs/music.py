import discord
from discord.ext import commands
from discord.utils import get
import aiohttp
import youtube_dl
import datetime
import os
import asyncio

from bot.reference import *

from enum import Enum


class MusicState(Enum):
    PlayingNone = -1
    PlayingSingle = 0
    PlayingQueue = 1


class Music(commands.Cog):
    global voice

    def __init__(self, bot):
        self.bot = bot
        self.queue = {}
        self.queue_index = 0
        self.ydl_opts = None
        self.music_state = MusicState.PlayingNone

        self.bot.loop.create_task(self.initialize())

    async def initialize(self):
        await self.bot.wait_until_ready()

        # Load Opus library for voice
        if not discord.opus.is_loaded():
            discord.opus.load_opus('opus')
            print("Loaded OPUS lib")

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

        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send(f"**Successfully disconnected**")
            print(f"Disconnected from {channel}")
        else:
            print("Told to leave channel, but not connected to one")

    # Tells bot to join text channel in
    @commands.command(pass_context=True)
    async def join(self, ctx):
        global voice
        try:
            channel = ctx.message.author.voice.channel
            voice = get(self.bot.voice_clients, guild=ctx.guild)

            # Connect bot to voice channel
            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()
                print(f"Connected to {channel}\n")
            await ctx.send(f"**Connected to `{channel}**")
        except Exception as e:
            print(e)
            await ctx.send("**Must be in voice channel to use this command**")

    @commands.command(pass_context=True, aliases=['p'])
    async def play(self, ctx, url=None):
        if self.music_state is not MusicState.PlayingNone:
            await ctx.send("**Already playing music. Try /queue <url> or /stop**")
            print("Already playing music")
            return

        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if url is None and len(self.queue) > 0:
            try:
                channel = ctx.message.author.voice.channel
                if voice and voice.is_connected():
                    await voice.move_to(channel)
                else:
                    await channel.connect()
                    print(f"Connected to {channel}\n")
                self.queue_index = 0
                self.play_queue(ctx)
            except Exception as e:
                print(e)
                await ctx.send(f"{ctx.message.author.mention} **Must be in voice channel to use this command**")
                return
            return
        else:
            try:
                channel = ctx.message.author.voice.channel
            except Exception as e:
                print(e)
                await ctx.send(f"{ctx.message.author.mention} **Must be in voice channel to use this command**")
                return

            await ctx.send(f"**Downloading**: `{url}` for playback")
            song = await self.download_audio(url)
            title = song['title']
            full_file = f"{AUDIO_DIRECTORY}/{title}.mp3"

            try:
                if voice and voice.is_connected():
                    await voice.move_to(channel)
                else:
                    voice = await channel.connect()
                    print(f"Connected to {channel}\n")

                print(f"Playing {title}")

                await ctx.send(embed=await self.embed_song(song))

                voice.play(discord.FFmpegPCMAudio(full_file), after=lambda e: self.clear_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = float(os.environ["BOT_VOLUME"])
                self.music_state = MusicState.PlayingSingle
            except Exception as e:
                print(e)
                await ctx.send(f"{ctx.message.author.mention} **Must be in voice channel to use this command**")
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
            await ctx.send("**Music paused :pause_button:**")
            print("Music paused")
            voice.pause()
        else:
            await ctx.send(":x: **Music not playing**")
            print("Trying to pause music that does not exist")

    @commands.command(pass_context=True, name='resume')
    async def resume(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            await ctx.send("**Music resumed :play_pause:**")
            print("Music paused")
            voice.resume()
        else:
            await ctx.send("**:x: No music to resume**")
            print("Trying to resume music that is not paused")

    @commands.command(pass_context=True, name="stop")
    async def stop(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            await ctx.send("**Music stopped :octagonal_sign:**")
            print("Music stopped")
            voice.stop()
        else:
            msg = await ctx.send(":x: **Music not playing**")
            print("No music to stop!")
        self.music_state = MusicState.PlayingNone

    @commands.command(pass_context=True, name="queue", aliases=['q'])
    async def queue_control(self, ctx, option=None):
        if option == "clear" or option == "-c" and self.music_state is MusicState.PlayingNone:
            self.clear_queue()
            msg = await ctx.send("**Cleared Queue :wastebasket:**")
            print("Cleared music queue")
            return
        elif option is None:
            await ctx.send(embed=await self.build_queue_embed())
            return
        elif option is not None and option is not "clear":
            await ctx.send(f"**Queueing:`{option}`**")
            song = await self.download_audio(option)

            title = song['title']
            duration = str(datetime.timedelta(seconds=int(song['duration'])))
            thumbnail = song["thumbnail"]

            self.queue.update({title: duration})

            embed_queue = await self.embed_song(song, show_queue=True, ctx=ctx)

            await ctx.send(embed=embed_queue)
            print(f"Added {title} to song queue")
            return
        await ctx.message.delete()

    def play_queue(self, ctx):
        print(len(self.queue))

        if len(self.queue) == 0 and len(os.listdir(AUDIO_DIRECTORY)) > 0:
            print("Cleaing queue @ play_queue")
            self.clear_queue()
            return
        else:
            file = list(self.queue)[self.queue_index]
            full_file = f"{AUDIO_DIRECTORY}/{file}.mp3"
            self.music_state = MusicState.PlayingQueue

            voice.play(discord.FFmpegPCMAudio(full_file), after=lambda e: self.play_queue(ctx))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = float(os.environ["BOT_VOLUME"])
            print(self.queue[file])
            del self.queue[file]
            return

    @commands.command(name="skip", pass_context=True)
    async def skip(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print("Music stopped")
            await ctx.send(":track_next: **Skipped**")
            voice.stop()
        else:
            msg = await ctx.send(":x: **Music not playing**")
            print("No music to stop!")

    async def embed_song(self, song, show_queue=False, ctx=None):
        title = song['title']
        duration = str(datetime.timedelta(seconds=int(song['duration'])))
        thumbnail = song["thumbnail"]
        url = f"https://www.youtube.com/watch?v={song['id']}"
        queue_length = len(self.queue)

        embed = discord.Embed(title=f"**{title}**", url=url, color=0x00ff00)
        embed.set_thumbnail(url=thumbnail)

        if show_queue and ctx is not None:
            user = ctx.message.author
            embed.add_field(name=f"**Position in queue:** {queue_length}", value="\u200b", inline=True)
            embed.set_footer(text=f"{queue_length} song(s) in queue\n /play")
            embed.set_author(name="Added to queue", icon_url=f"https://cdn.discordapp.com/avatars/"
                                                             f"{user.id}/{user.avatar}.png?size=1024")
        else:
            embed.set_author(name="Now Playing")

        embed.add_field(name=f"**Duration:** {duration}", value=f"\u200b", inline=False)

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
        queue_embed = discord.Embed(title=f"**Songs in queue:** {len(self.queue)}", description="\u200b")
        if len(self.queue) > 0:
            for song, duration in self.queue.items():
                if i == 1:
                    queue_embed.add_field(name=f"{i}. {song}", value=f"Duration:{duration}", inline=True)
                else:
                    queue_embed.add_field(name=f"{i}. {song}", value=f"Duration:{duration}", inline=False)
                i += 1
            return queue_embed
        else:
            queue_embed.add_field(name="**No songs in queue**", value='\u200b')
            return queue_embed

    def clear_queue(self):
        self.queue.clear()
        for file in os.listdir(AUDIO_DIRECTORY):
            print(f"Removed {file}")
            os.remove(f"{AUDIO_DIRECTORY}/{file}")
        self.music_state = MusicState.PlayingNone


def setup(bot):
    bot.add_cog(Music(bot))
