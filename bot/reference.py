import json
import os
import discord
import asyncio


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
WAIFU_DIRECTORY = os.getcwd()+"/resources/json/waifu"
WISHLIST_DIRECTORY = os.getcwd()+"/resources/csv/wishlist"
WORD_BLACKLIST_JSON = os.getcwd()+"/resources/json/word_blacklist.json"

RELEASE_VERSION = "3.0"

roles = []
channels = []


async def check_can_use(ctx, command=None):
    return True

    roles.clear()
    channels.clear()

    if isinstance(ctx.message.channel, discord.DMChannel):
        return True

    try:
        with open(ROLES_CSV, "r") as roles_csv:
            for role in roles_csv:
                roles.append(role)
        roles_csv.close()
    except Exception as e:
        print(e)
        print("Failed to load roles.csv")

    try:
        with open(CHANNELS_CSV, "r") as channels_csv:
            for channel in channels_csv:
                channels.append(channel)
        channels_csv.close()
    except Exception as e:
        print(e)
        print("Failed to channels.csv")

    try:
        with open(COMMAND_JSON, "r") as cmds:
            commands = json.load(cmds)
    except Exception as e:
        print("Failed to load command.json")
        print(e)

    current_command = None

    can_use = False
    global valid_channel
    valid_channel = False
    global valid_role
    valid_role = False
    nsfw = None

    for line in channels:
        channel = line.split(',')

        for index, item in enumerate(commands["commands"]):
            if item["name"] == command:
                current_command = item

        if channel[0] == ctx.message.channel.name \
                and int(channel[1]) == int(ctx.message.channel.id):
            nsfw = channel[2]
            if current_command is not None:
                nsfw = nsfw.strip()
                if current_command["nsfw"] == "yes" and nsfw == "no":
                    print("Invalid command")
                    valid_channel = False
                    break
                else:
                    print("Valid command")
                    valid_channel = True
                    break

        if ctx.message.channel.name == "bot-commands" and nsfw == "no":
            return True

    # Check if role is valid
    role = "INVALID_CHANNEL"
    if valid_channel:
        # Find run command in commands.json
        for index, item in enumerate(commands["commands"]):
            if item["name"] == current_command["name"]:
                for user_role in ctx.author.roles:
                    for line in roles:
                        r = line.split(",")
                        if r[0] == user_role.name \
                                and int(r[1]) == user_role.id \
                                and not valid_role:
                            if int(r[2]) >= int(item["permission-level"]):
                                valid_role = True
                                break
                            elif not valid_role:
                                valid_role = False
                                role = user_role

    cmds.close()

    if not valid_role or not valid_channel:
        error = await ctx.send(f"**{ctx.message.author.mention} "
                               f"You do not have permission to use "
                               f"{command}**")
        can_use = False
        if not valid_role and role != "INVALID_CHANNEL":
            print(f"Command {command} used by invalid role {role}")
        if not valid_channel:
            print(f"Command {command} used in invalid channel "
                  f"{ctx.message.channel}")
        await asyncio.sleep(1.5)
        await error.delete()
        await ctx.message.delete()
    elif valid_role and valid_channel:
        can_use = True

    return can_use

try:
    BOT_PREFIX = os.environ["BOT_PREFIX"]
    BOT_TOKEN = os.environ["BOT_TOKEN"]
    print(f"Loaded {BOT_TOKEN}, prefix is {BOT_PREFIX}")
except Exception as e:
    print(e)
    print("Unable to fetch BOT_TOKEN and BOT_PREFIX")
    BOT_TOKEN = "STOP"
