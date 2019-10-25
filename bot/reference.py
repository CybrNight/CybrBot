import json
import os
import discord


INSULT_CSV = os.getcwd()+"/resources/csv/insults.csv"
HAIKU_CSV = os.getcwd()+"/resources/csv/haiku.csv"
JPEG_DIRECTORY = os.getcwd()+"/download/jpeg"
FRY_DIRECTORY = os.getcwd()+"/download/deepfry"
IMG_DIRECTORY = os.getcwd()+"/resources/img"
AUDIO_DIRECTORY = os.getcwd() + "/resources/audio"
DOWNLOAD_DIRECTORY = os.getcwd()+"/download"
PRESENCE_JSON = os.getcwd()+"/resources/json/presence.json"
COMMAND_JSON = os.getcwd()+"/resources/json/commands.json"
PERMISSIONS_JSON = os.getcwd() + "/resources/json/permissions.json"

RELEASE_VERSION = "3.0"


async def check_can_use(ctx, command=None):
    if isinstance(ctx.message.channel, discord.DMChannel):
        return True

    try:
        with open(PERMISSIONS_JSON, "r") as permissions:
            permission = json.load(permissions)
    except Exception as e:
        print("Failed to load permissions.json")

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
                if role.name in permission:
                    if int(permission[role.name]) >= int(item["permission-level"]):
                        can_use = True

    if ctx.author.id == 229773126936821760:
        can_use = True

    for index, item in enumerate(permission["allowed-channels"]):
        if item["name"] == ctx.message.channel.name:
            can_use = True
            break
        else:
            can_use = False

    permissions.close()
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
