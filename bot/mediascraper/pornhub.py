import random
import aiohttp
from bs4 import BeautifulSoup

VIDEO = "/view_video.php?viewkey"
SEARCH = "https://www.pornhub.com/video/search?search="


class PornHub:

    def __init__(self):
        print()

    @staticmethod
    async def video_search(keywords):
        async with aiohttp.ClientSession() as session:
            async with session.get(SEARCH+keywords) as resp:
                text = await resp.text()
                bs = BeautifulSoup(text, "html.parser")
                videos = []
                for link in bs.find_all('a'):
                    if link.has_attr('href'):
                        lnk = link.attrs['href']
                        if str(lnk).__contains__(VIDEO):
                            if not str(lnk).__contains__("https://www.pornhub.com"):
                                lnk = "https://www.pornhub.com"+lnk
                            videos.append(lnk)
                if videos.__len__() > 0:
                    video = random.choice(videos)
                else:
                    video = "```No Results Found :(```"
                return video
