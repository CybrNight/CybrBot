import json
import os

with open("config.json", "r") as config:
    data = json.load(config)

BOT_PREFIX = data["prefix"]
TOKEN = os.environ.get("BOT_TOKEN")
print(TOKEN)

try:
    RELEASE_VERSION = os.environ.get("HEROKU_RELEASE_VERSION")
except Exception as e:
    print(e)
    RELEASE_VERSION = "2.0"
