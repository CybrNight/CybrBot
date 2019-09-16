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

RELEASE_VERSION = "3.0"

ROLES = {
    "Sauce Provider": 20,
    "Sauce Creators": 15,
    "Sauce Enforcers": 10,
    "Nitro Booster": 5,
    "Sauce": 5,
    "Premium Sauce": 5,
}


async def can_use(ctx, command=None):
    try:
        with open(COMMAND_JSON, "r") as cmds:
            cmd = json.load(cmds)
            can_use = False
            # Check if commands exist
            for index, item in enumerate(cmd["commands"]):
                if item["name"] == command:
                    for role in ctx.author.roles:
                        if role.name in ROLES:
                            if ROLES[role.name] >= int(item["permission-level"]):
                                can_use = True

            if ctx.author.id == "229773126936821760":
                can_use = True

            if ctx.message.channel.name is not "bot_commands":
                can_use = False

            cmds.close()

            if not can_use:
                await ctx.message.delete()

            return can_use
    except Exception as e:
        print("Failed to load command.json")
        print(e)

try:
    BOT_PREFIX = os.environ["BOT_PREFIX"]
    BOT_TOKEN = os.environ["BOT_TOKEN"]
    print(f"Loaded {BOT_TOKEN}, prefix is {BOT_PREFIX}")
except Exception as e:
    print(e)
    print("Unable to fetch BOT_TOKEN and BOT_PREFIX")
    BOT_TOKEN = "STOP"
