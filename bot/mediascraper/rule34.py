import random

import aiohttp
from bs4 import BeautifulSoup


class Rule34:

    def __init__(self):
        self.URL = "https://rule34.xxx/"
        self.SEARCH = "https://rule34.xxx/index.php?page=post&s=list&tags="
        self.POST = "?page=post&s=view"
        self.IMG = "https://us.rule34.xxx//images/"
        self.PATREON = "p.png"

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
            post = random.choice(posts)

            async with aiohttp.ClientSession() as session:
                async with session.get(post) as resp:
                    text = await resp.text()

            bs = BeautifulSoup(text, "html.parser")
            for link in bs.find_all('img'):
                if link.has_attr('src'):
                    lnk = link.attrs['src']
                    img = lnk
                    if not img.__contains__(self.PATREON) and not img.__contains__("icame.png") \
                            and not img.__contains__("r34chibi.png"):
                        if not img.__contains__("https:"):
                            img = "https:" + img
                        return img
            return "```No Results Found :(```"
        except Exception as e:
            print(e)
            return "```No Results Found :(```"
