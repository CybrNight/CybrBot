import random

import aiohttp
from bs4 import BeautifulSoup


class Gelbooru:

    def __init__(self):
        self.URL = "https://gelbooru.com/"
        self.SEARCH = "https://gelbooru.com/index.php?page=post&s=list&tags="
        self.POST = "page=post&s=view&id="
        self.IMG = "https://simg3.gelbooru.com//samples/"
        self.AVATAR = "user_avatars"

    async def image_search(self, keywords):
        keywords = str(keywords).replace(" ", "+")
        url = self.SEARCH+keywords
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                text = await resp.text()

        bs = BeautifulSoup(text, "html.parser")
        posts = []
        for link in bs.find_all('a'):
            if link.has_attr('href'):
                lnk = link.attrs['href']
                if str(lnk).__contains__(self.POST) and not str(lnk).__contains__(self.AVATAR):
                    posts.append(self.URL + lnk)
        try:
            post = random.choice(posts)
            async with aiohttp.ClientSession() as session:
                async with session.get(post) as resp:
                    text = await resp.text()
            bs = BeautifulSoup(text, "html.parser")
            for link in bs.find_all('img'):
                if link.has_attr('src'):
                    lnk = link.attrs['src']
                    return lnk
        except Exception as e:
            print(e)
            return "```No Results Found :(```"
