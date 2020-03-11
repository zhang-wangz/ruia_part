from ruia import Request, Spider
from spiderExample.item import HackerNewsItem
from spiderExample.middlewares import middleware
from spiderExample.db import MotorBase


class HackerNewsSpider(Spider):
    start_urls = ['https://news.ycombinator.com']
    concurrency = 3

    async def parse(self, response):
        self.mongo_db = MotorBase().get_db('ruia_test')
        urls = ['https://news.ycombinator.com/news?p=1', 'https://news.ycombinator.com/news?p=2']
        for index, url in enumerate(urls):
            yield Request(
                url,
                callback=self.parse_item,
                metadata={'index': index}
            )

    async def parse_item(self, response):
        async for item in HackerNewsItem.get_items(html=response.html):
            yield item

    async def process_item(self, item):
        try:
            await self.mongo_db.news.update_one({
                'url': item.url
            }, {
                '$set': {'url': item.url, 'title': item.title}
            },
                upsert=True)
        except Exception as e:
            self.logger.exception(e)


if __name__ == '__main__':
    HackerNewsSpider.start(middleware=middleware)
