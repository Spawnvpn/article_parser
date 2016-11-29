import json
import scrapy

from scrapy import Request
from w3lib.html import remove_tags
from article_bot.items import ArticleParserItem


class ArticleSpider(scrapy.Spider):
    def __init__(self, *args, **kwargs):
        super(ArticleSpider, self).__init__(*args, **kwargs)
        # self.job = kwargs.get('_job')

    name = 'ArticleSpider'

    def start_requests(self):
        links = self.get_links()
        self.logger.info("LINKS: {}".format(", ".join(links)))
        for link in links:
            yield self.make_requests_from_url(link)

    def get_links(self):
        start_urls = ['https://news.ycombinator.com/newest', 'https://news.ycombinator.com/newest?n=31',
                      'https://news.ycombinator.com/newest?n=61', 'https://news.ycombinator.com/newest?n=91',
                      'https://news.ycombinator.com/newest?n=111']
        return start_urls

    def parse(self, response):
        self.logger.info(response)
        if response:
            article_urls = response.xpath('//*[@class="athing"]/td/a/@href').extract()
            for url in article_urls:
                yield Request(url='https://mercury.postlight.com/parser?url=%s' % url, callback=self.universal_hanlder, headers={'x-api-key': 'Wsfp1xDKbSbvRJhKg2ZaukFTkIKsY3vcePgyJ7IZ'})

    def universal_hanlder(self, response):
        item = ArticleParserItem()
        domain = json.loads(response.text).get('domain')
        url = json.loads(response.text).get('url')
        title = json.loads(response.text).get('title')
        content = json.loads(response.text).get('content')
        date_published = json.loads(response.text).get('date_published')
        item['domain'] = domain
        item['url'] = url
        item['title'] = title
        item['content'] = content
        item['date_published'] = date_published

        return item

    def github_handler(self, response):
        # self.logger.info(response)
        pass
