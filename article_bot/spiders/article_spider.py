import json
import urlparse
import scrapy
from scrapy import Request
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
        start_urls = ['https://news.ycombinator.com/newest']
        return start_urls

    def parse(self, response):
        self.logger.info(response)
        if response:
            article_urls = response.xpath('//*[@class="athing"]/td/a/@href').extract()
            for url in article_urls:
                try:
                    yield Request(url=url, callback=self.universal_hanlder)
                except:
                    pass

    def universal_hanlder(self, response):
        item = ArticleParserItem()
        # domain = json.loads(response.text).get('domain')
        # url = json.loads(response.text).get('url')
        # title = json.loads(response.text).get('title')
        # content = json.loads(response.text).get('content')
        # date_published = json.loads(response.text).get('date_published')
        item['domain'] = self.get_domain(response)
        item['url'] = self.get_url(response)
        item['title'] = self.get_title(response)
        item['content'] = self.get_content(response)
        # item['date_published'] = date_published

        return item

    def github_handler(self, response):
        # self.logger.info(response)
        pass

    def get_title(self, response):
        title = response.xpath('//title/text()').extract()[0]
        return title

    def get_content(self, response):
        content = ''
        selectors = ['//*[contains(@class, "content")]', '//*[contains(@class, "site-content")]',
                     '//*[contains(@class, "content-main")]', '//*[contains(@class,"article")]', '//*[@id="content-main"]',
                     '//*[@id="content"]', '//*[@id="site-content"]', '//*[@id="article"]', '//article']
        for selector in selectors:
            if response.xpath(selector).extract():
                data = response.xpath(selector).extract()
                if len(data) > 1:
                    for i in range(len(data) - 1):
                        if len(data[i]) < len(data[i + 1]):
                            content = data[i + 1]
                        else:
                            content = data[i]
                else:
                    content = data[0]
        return content.encode('utf8')

    def get_author(self):
        pass

    def get_domain(self, response):
        domain = urlparse.urlparse(response.url).hostname
        return domain

    def get_url(self, response):
        url = response.url
        return url

    def get_date_published(self):
        pass
