import json
import os


INSULT_CSV = os.getcwd()+"/resources/csv/insults.csv"
HAIKU_CSV = os.getcwd()+"/resources/csv/haiku.csv"
JPEG_DIRECTORY = os.getcwd()+"/download/jpeg"
FRY_DIRECTORY = os.getcwd()+"/download/deepfry"
IMG_DIRECTORY = os.getcwd()+"/resources/img"
AUDIO_DIRECTORY = os.getcwd()+"/resources/audio"
DOWNLOAD_DIRECTORY = os.getcwd()+"/download"
CONFIG_JSON = os.getcwd()+"/resources/json/config.json"
PRESENCE_JSON = os.getcwd()+"/resources/json/presence.json"
COMMAND_JSON = os.getcwd()+"/resources/json/commands.json"

with open(CONFIG_JSON, "r") as config:
    data = json.load(config)

RELEASE_VERSION = "3.0"
BOT_PREFIX = data["prefix"]
TOKEN = os.environ.get("BOT_TOKEN")