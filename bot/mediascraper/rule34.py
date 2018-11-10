import random

import aiohttp
from bs4 import BeautifulSoup


class Rule34:

    def __init__(self):
        self.URL = "https://rule34.xxx/"
        self.SEARCH = "https://rule34.xxx/index.php?page=post&s=list&tags="
        self.POST = "?page=post&s=view"
        self.IMG = "https://img.rule34.xxx//images/"

    async def image_search(self, keywords):
        keywords = str(keywords).replace(" ", "+")

        async with aiohttp.ClientSession() as session:
            async with session.get(self.SEARCH+keywords) as resp:
                text = await resp.text()

        bs = BeautifulSoup(text, "html.parser")
        posts = []
        for link in bs.find_all('a'):
            if link.has_attr('href'):
                lnk = link.attrs['href']
                if str(lnk).__contains__(self.POST):
                    posts.append(self.URL + lnk)
        try:
            if posts.__len__() > 0: post = posts[random.randint(0, posts.__len__() - 1)]
            else: post = "```No Results Found :("

            async with aiohttp.ClientSession() as session:
                async with session.get(post) as resp:
                    text = await resp.text()

            bs = BeautifulSoup(text, "html.parser")
            for link in bs.find_all('img'):
                if link.has_attr('src'):
                    lnk = link.attrs['src']
                    img = lnk
                    if not img.__contains__("https:"):
                        img = "https:" + img
                    return img
        except ValueError:
            return "```No Results Found :(```"
