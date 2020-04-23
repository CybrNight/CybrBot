import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import datetime
import asyncio

from bot.reference import *

from enum import Enum


class BotStatus(Enum):
    Connected = 0
    Playing = 1
    Disconnected = -1


ffmpeg_options = {
    'options': '-vn'
}

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '{AUDIO_DIRECTORY}/%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses
    # cause issues sometimes
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')
        self.thumbnail = data.get('thumbnail')
        self.duration = data.get('duration')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None,
                                          lambda: ytdl.extract_info(url,
                                                                    download=
                                                                    not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options),
                   data=data)


class Music(commands.Cog):
    global voice
    currentPlayingSong = ""
    bot_status = BotStatus.Disconnected

    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.queue_index = 0

        self.bot.loop.create_task(self.initialize())

    async def initialize(self):
        await self.bot.wait_until_ready()

    @commands.command(aliases=["disconnect"])
    async def leave(self, ctx):
        can_send = await check_can_use(ctx, "leave")
        if not can_send:
            return

        try:
            channel = ctx.message.author.voice.channel
            voice = get(self.bot.voice_clients, guild=ctx.guild)

            if voice and voice.is_connected():
                await voice.disconnect()
                print(f"Disconnected from {channel}")
                self.bot_status = BotStatus.Disconnected
            else:
                print("Told to leave channel, but not connected to one")
        except AttributeError:
            msg = await ctx.send(
                "**Must be in voice channel to use this command**")
            await asyncio.sleep(0.5)
            await msg.remove()

    # Tells bot to join text channel in
    @commands.command()
    async def join(self, ctx):
        self.bot_status = BotStatus.Connected
        can_send = await check_can_use(ctx, "join")
        if not can_send:
            return

    @commands.command()
    async def play(self, ctx, *, url=None):
        can_send = await check_can_use(ctx, "play")

        if not can_send:
            return

        if self.bot_status is BotStatus.Disconnected:
            await self.connect_to_voice_channel(ctx)

        if url is None and len(self.queue) > 0 \
                and self.bot_status is BotStatus.Connected:

            self.queue_index = 0
            await self.play_queue(ctx)
        elif url is not None:
            if self.bot_status is BotStatus.Connected:

                async with ctx.typing():
                    await self.queue_song(ctx, url)
                    await self.play_queue(ctx)
            elif self.bot_status is BotStatus.Playing:
                async with ctx.typing():
                    await self.queue_song(ctx, url)

    async def queue_song(self, ctx, source):
        song = await YTDLSource.from_url(source, loop=self.bot.loop,
                                         stream=True)

        title = song.title

        self.queue.append(song)

        embed_queue = await self.embed_song(song, show_queue=True, ctx=ctx)

        await ctx.send(embed=embed_queue)
        print(f"Added {title} to song queue")

    @commands.command()
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"**Changed volume to {volume}%**")

    # Pause music command
    @commands.command(name="pause")
    async def pause(self, ctx):
        can_send = await check_can_use(ctx, "pause")
        if not can_send:
            return

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            await ctx.send("**Music paused :pause_button:**")
            print("Music paused")
            voice.pause()
        else:
            await ctx.send(":x: **Music not playing**")
            print("Trying to pause music that does not exist")

    @commands.command(name='resume')
    async def resume(self, ctx):
        can_send = await check_can_use(ctx, "resume")
        if not can_send:
            return

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            await ctx.send("**Music resumed :play_pause:**")
            print("Music paused")
            voice.resume()
        else:
            await ctx.send("**:x: No music to resume**")
            print("Trying to resume music that is not paused")

    @commands.command(name="stop")
    async def stop(self, ctx):
        can_send = await check_can_use(ctx, "stop")
        if not can_send:
            return

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            await ctx.send("**Music stopped :octagonal_sign:**")
            print("Music stopped")
            voice.stop()
        else:
            await ctx.send(":x: **Music not playing**")
            print("No music to stop!")
        self.bot_status = BotStatus.Connected

    @commands.command(name="queue", aliases=['q'])
    async def queue_control(self, ctx, option=None):
        can_send = await check_can_use(ctx, "queue")
        if not can_send:
            return

        if option == "clear" or option == "-c" \
                and self.bot_status is BotStatus.Connected:

            await self.clear_queue()
            await ctx.send("**Cleared Queue :wastebasket:**")
            print("Cleared music queue")
            return
        elif option is None:
            await ctx.send(embed=await self.build_queue_embed())
            return
        elif option is not None and option != "clear":
            await self.queue_song(ctx, option)
            return
        await ctx.message.delete()

    async def update_presence(self):
        await self.bot.wait_until_ready()
        activity = discord.Activity(name=self.currentPlayingSong,
                                    type=discord.ActivityType.listening)
        # Set presence of bot
        await self.bot.change_presence(activity=activity)

    async def play_queue(self, ctx):
        print(len(self.queue))
        file = None

        try:
            if len(self.queue) == 0:
                print("Cleaing queue @ play_queue")
                await self.clear_queue()
                return
            else:
                if len(self.queue) > 0:
                    file = self.queue[0]

                self.bot_status = BotStatus.Playing
                player = await YTDLSource.from_url(file.url,
                                                   loop=self.bot.loop,
                                                   stream=True)

                ctx.voice_client.play(player, after=lambda e: self.bot.loop.
                                      create_task(self.play_queue(ctx)))

                self.currentPlayingSong = self.queue[self.queue_index].title
                self.bot.loop.create_task(self.update_presence())

                print(f"Now Playing: {self.currentPlayingSong}")
                if self.queue.__len__() > 0:
                    del self.queue[0]
                return
        except Exception as e:
            print("Error playing " + self.queue[0].title)
            print(e)

    @commands.command(name="skip")
    async def skip(self, ctx):
        can_send = await check_can_use(ctx, "skip")
        if not can_send:
            return

        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print("Music stopped")
            await ctx.send(":track_next: **Skipped**")
            voice.stop()
        else:
            await ctx.send(":x: **Music not playing**")
            print("No music to stop!")

    async def embed_song(self, song, show_queue=False, ctx=None):
        title = song.title
        duration = str(datetime.timedelta(seconds=int(song.duration)))
        thumbnail = song.thumbnail
        url = song.url
        queue_length = len(self.queue)

        embed = discord.Embed(title=f"**{title}**", url=url, color=0x00ff00)
        embed.set_thumbnail(url=thumbnail)

        if show_queue and ctx is not None:
            user = ctx.message.author
            embed.add_field(name=f"**Position in queue:** {queue_length}",
                            value="\u200b",
                            inline=True)

            embed.set_footer(text=f"{queue_length} song(s) in queue\n /play")
            embed.set_author(name="Added to queue",
                             icon_url=f"https://cdn.discordapp.com/avatars/"
                                      f"{user.id}/{user.avatar}.png?size=1024")
        else:
            embed.set_author(name="Now Playing")

        embed.add_field(name=f"**Duration:** {duration}",
                        value=f"\u200b",
                        inline=False)

        return embed

    @join.before_invoke
    async def connect_to_voice_channel(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                vc = ctx.author.voice.channel
                await vc.connect()
                await ctx.send(f"**Connected to {vc}**")
                self.bot_status = BotStatus.Connected
                print(f"Connected to {vc}")
            else:
                await ctx.send("**You are not connected to a voice channel.**")
                raise commands.CommandError("Author not connected "
                                            "to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    async def build_queue_embed(self):
        i = 1
        queue_embed = discord.Embed(
            title=f"**Songs in queue:** {len(self.queue)}",
            description="\u200b")
        if len(self.queue) > 0:
            for song in self.queue:
                duration = str(datetime.timedelta(seconds=int(song.duration)))
                if i == 1:
                    queue_embed.add_field(name=f"{i}. {song.title}",
                                          value=f"Duration:{duration}",
                                          inline=True)
                else:
                    queue_embed.add_field(name=f"{i}. {song.title}",
                                          value=f"Duration:{duration}",
                                          inline=False)
                i += 1
            return queue_embed
        else:
            queue_embed.add_field(name="**No songs in queue**",
                                  value='\u200b')
            return queue_embed

    async def clear_queue(self):
        self.queue.clear()

        for file in os.listdir(AUDIO_DIRECTORY):
            print(f"Removed {file}")
            os.remove(f"{AUDIO_DIRECTORY}/{file}")

        self.bot_status = BotStatus.Connected
        activity = discord.Activity(name="/help",
                                    type=discord.ActivityType.playing)
        # Set presence of bot
        await self.bot.change_presence(activity=activity)


def setup(bot):
    bot.add_cog(Music(bot))
