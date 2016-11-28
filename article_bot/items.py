import django
import scrapy
from scrapy_djangoitem import DjangoItem

django.setup()

from articles.models import Article


class ArticleParserItem(DjangoItem):
    django_model = Article
    domain = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    date_published = scrapy.Field()
