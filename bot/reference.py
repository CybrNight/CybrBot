import json
import os


with open("config.json", "r") as config:
    data = json.load(config)

RELEASE_VERSION = "2.5"
BOT_PREFIX = data["prefix"]
TOKEN = os.environ.get("BOT_TOKEN")
