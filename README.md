# Features
- Scraping of images and videos from various websites.
- Playing music from websites such as SoundCloud and YouTube
- More JPEG and deep fry images in chat
- Full permission system for command usage

# Usage
Install the required libraries using the command:
`pip install requirements.txt`

Hosting platforms such as Heroku should automatically do this for you on deployment.
If you are using Heroku you will need to install an OPUS buildpack for Heroku from [here.](https://github.com/xrisk/heroku-opus "here")
You are also going to need to install an FFMPEG buildpack from [here.](https://www.github.com/jonathangong/heroku-buildpack-ffmpeg-latest.git)

For a command list run `/help` in a channel labeled `#bot-commands`. This is the default channel the bot will work in.

Use `/register_channel <name>` to register a channel for command usage.
Use `/register_role <name> <permission-level>` to register a role for permissions.

# Libraries
- BeautifulSoup4 for website scraping
- PIL/Pillow for image processing (more JPEG and deep fry commands)
- Discord.py
- YouTube-DL
- AIOFiles for file handling
