import aiofiles
from ruia import AttrField, TextField, Item, Spider
import time

class FictionItem(Item):
    target_item = TextField(css_select="dd")
    title = TextField(css_select='a')
    url = AttrField(css_select='a', attr='href')

    async def clean_title(self, value):
        return value


class FictionSpider(Spider):
    start_urls = ['https://www.biquge5200.com/0_111/']

    async def parse(self, response):
        async for item in FictionItem.get_items(html=response.html):
            yield item

    async def process_item(self, item: FictionItem):
        """Ruia build-in method"""
        async with aiofiles.open('./fiction_chapter.txt', 'a') as f:
            await f.write(str(item.title) + "url:" + str(item.url) + '\n')
            await time.sleep(5)


if __name__ == '__main__':
    FictionSpider.start()