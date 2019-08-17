import sys

from discord.ext.commands import Bot

from bot.reference import *

bot = Bot(command_prefix=BOT_PREFIX)
bot.remove_command("help")
cogs_dir = "cogs"
print(f"Running Python {sys.version}")


@bot.event
async def on_ready():
    if not os.path.isdir(DOWNLOAD_DIRECTORY):
        try:
            os.mkdir(DOWNLOAD_DIRECTORY)
            print("Created download directory")
        except Exception as e:
            print(e)
    if not os.path.isdir(JPEG_DIRECTORY):
        try:
            os.mkdir(JPEG_DIRECTORY)
            print("Created JPEG directory")
        except Exception as e:
            print(e)
    if not os.path.isdir(FRY_DIRECTORY):
        try:
            os.mkdir(FRY_DIRECTORY)
            print("Created deep fry directory")
        except Exception as e:
            print(e)
    if not os.path.isdir(AUDIO_DIRECTORY):
        try:
            os.mkdir(AUDIO_DIRECTORY)
            print("Created audio directory")
        except Exception as e:
            print(e)
    print(f"Logged in as {bot.user.name}")

cogs = os.listdir(cogs_dir)

if __name__ == "__main__":
    for extension in [f.replace('.py', '') for f in os.listdir(cogs_dir) if os.path.isfile(os.path.join(cogs_dir, f))]:
        try:
            bot.load_extension(f"{cogs_dir}.{extension}")
        except Exception as e:
            print(e)
            print(f'Failed to load extension {extension}.')
    bot.run(TOKEN)
