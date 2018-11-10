import random

import aiohttp
from bs4 import BeautifulSoup

VIDEO = "http://hh.cx/files/"
TAG = "http://hentaihaven.org/tag/"
TAGS = "http://hentaihaven.org/?tdo_tag="
SEARCH = "http://hentaihaven.org/search/"


class HentaiHaven:

    def __init__(self):
        self.text = ""

    async def category_search(self, cats):
        cats = str(cats).replace(" ", "+")
        if str(cats).__contains__("+"):
            async with aiohttp.ClientSession() as session:
                async with session.get(TAGS + cats) as resp:
                    self.text = await resp.text()
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(TAGS + cats) as resp:
                    self.text = await resp.text()

        bs = BeautifulSoup(self.text, "html.parser")

        pages = []
        for link in bs.find_all('a'):
            if link.has_attr('href'):
                lnk = link.attrs['href']
                if lnk.__contains__("episode"):
                    pages.append(lnk)
        try:
            if pages.__len__() > 0: page = pages[random.randint(0, pages.__len__() - 1)]
            else: page = "```No Results Found :(```"
            return page
        except Exception as e:
            print(e)
            return "No Results Found :("

    async def random(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.hentaihaven.org") as resp:
                self.text = await resp.text()
        bs = BeautifulSoup(self.text, "html.parser")
        videos = []
        for link in bs.find_all('a'):
            if link.has_attr('href'):
                lnk = link.attrs['href']
                if lnk.__contains__("episode"):
                    videos.append(lnk)

        if videos.__len__() > 0: video = videos[random.randint(0, videos.__len__() - 1)]
        else: video = "```No Results Found :(```"

        return video
