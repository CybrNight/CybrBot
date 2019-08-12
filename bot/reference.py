import json
import os


with open(os.getcwd()+"/resources/config.json", "r") as config:
    data = json.load(config)

RELEASE_VERSION = "3.0"
BOT_PREFIX = data["prefix"]
TOKEN = os.environ.get("BOT_TOKEN")
