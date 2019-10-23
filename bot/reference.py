import json
import os


INSULT_CSV = os.getcwd()+"/resources/csv/insults.csv"
HAIKU_CSV = os.getcwd()+"/resources/csv/haiku.csv"
JPEG_DIRECTORY = os.getcwd()+"/download/jpeg"
FRY_DIRECTORY = os.getcwd()+"/download/deepfry"
IMG_DIRECTORY = os.getcwd()+"/resources/img"
AUDIO_DIRECTORY = os.getcwd() + "/resources/audio"
DOWNLOAD_DIRECTORY = os.getcwd()+"/download"
PRESENCE_JSON = os.getcwd()+"/resources/json/presence.json"
COMMAND_JSON = os.getcwd()+"/resources/json/commands.json"
ALLOWED_CHANNELS_JSON = os.getcwd()+"/resources/json/allowed_channels.json"

RELEASE_VERSION = "3.0"

ALLOWED_CHANNELS = ["bot-commands", "bot-commands-nsfw", "bot-commands-sfw"]

ROLES = {
    "Trusted": 99,
    "Sauce Provider": 20,
    "Sauce Creators": 15,
    "Sauce Enforcers": 10,
    "Nitro Booster": 5,
    "Sauce": 5,
    "Premium Sauce": 5,
}


async def check_can_use(ctx, command=None):
    try:
        with open(ALLOWED_CHANNELS_JSON, "r") as channels:
            channel = json.load(channels)
    except Exception as e:
        print("Failed to load allowed_channels.json")

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
                if role.name in ROLES:
                    if ROLES[role.name] >= int(item["permission-level"]):
                        can_use = True

    if ctx.author.id == 229773126936821760:
        can_use = True

    for index, item in enumerate(channel["allowed-channels"]):
        if item["name"] == ctx.message.channel.name:
            can_use = True
            break
        else:
            can_use = False

    channels.close()
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
