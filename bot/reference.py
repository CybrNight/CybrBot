import json
import os
import discord


ROLES_CSV = os.getcwd() + "/resources/csv/roles.csv"
CHANNELS_CSV = os.getcwd() + "/resources/csv/channels.csv"

INSULT_CSV = os.getcwd()+"/resources/csv/insults.csv"
HAIKU_CSV = os.getcwd()+"/resources/csv/haiku.csv"
JPEG_DIRECTORY = os.getcwd()+"/download/jpeg"
FRY_DIRECTORY = os.getcwd()+"/download/deepfry"
IMG_DIRECTORY = os.getcwd()+"/resources/img"
AUDIO_DIRECTORY = os.getcwd() + "/resources/audio"
DOWNLOAD_DIRECTORY = os.getcwd()+"/download"
PRESENCE_JSON = os.getcwd()+"/resources/json/presence.json"
COMMAND_JSON = os.getcwd()+"/resources/json/commands.json"

RELEASE_VERSION = "3.0"


async def check_can_use(ctx, command=None):
    if isinstance(ctx.message.channel, discord.DMChannel):
        return True

    roles = []
    channels = []

    try:
        with open(ROLES_CSV, "r") as roles_csv:
            for role in roles_csv:
                roles.append(role)
    except Exception as e:
        print("Failed to load roles.csv")

    try:
        with open(CHANNELS_CSV, "r") as channels_csv:
            for channel in channels_csv:
                channels.append(channel)
    except Exception as e:
        print(e)
        print("Failed to channels.csv")

    try:
        with open(COMMAND_JSON, "r") as cmds:
            cmd = json.load(cmds)
    except Exception as e:
        print("Failed to load command.json")
        print(e)

    can_use = False
    # Check if commands exist
    for index, item in enumerate(cmd["commands"]):
        if item["name"] == command:
            for role in ctx.author.roles:
                for line in roles:
                    words = line.split(",")
                    if words[0] == role.name and int(words[1]) == role.id:
                        if int(words[2]) >= int(item["permission-level"]):
                            can_use = True
                            break

    for line in channels:
        channel = line.split(',')
        if channel[0] == ctx.message.channel.name and int(channel[0]) == ctx.message.channel.id:
            can_use = True
            break
        else:
            can_use = False

    cmds.close()

    if not can_use:
        await ctx.message.delete()

    return can_use

try:
    BOT_PREFIX = os.environ["BOT_PREFIX"]
    BOT_TOKEN = os.environ["BOT_TOKEN"]
    print(f"Loaded {BOT_TOKEN}, prefix is {BOT_PREFIX}")
except Exception as e:
    print(e)
    print("Unable to fetch BOT_TOKEN and BOT_PREFIX")
    BOT_TOKEN = "STOP"
