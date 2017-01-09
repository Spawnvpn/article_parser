import json
import os
import uuid
import csv
from textwrap import dedent
from hdfs import InsecureClient
from article_bot.settings import BASE_PATH
from article_parser.settings import HDFS_ADRESS
from articles.models import Article
from w3lib.html import remove_tags


class ArticleParserPipeline(object):

    def process_item(self, item, spider):
        folder = "media/"

        try:
            os.mkdir(os.path.join(BASE_PATH, folder))
        except:
            pass

        # if not Article.objects.filter(url=item['url']).exists() and item['content']:
        if item['content']:
            content = remove_tags(item['content'], which_ones=('script', 'noscript', 'iframe', 'pre', 'link', 'frame',
                                                               'meta', 'form'))
            content = dedent(content)
            # content = content.replace('</pre>', '')
            content = content.replace('</article>', '')
            # content = content.replace('<', '&lt;')
            while '\n\n' in content:
                content = content.replace('\n\n', '\n')

            # filename = item['url'].replace('/', '_') + '.md'
            filename = str(uuid.uuid4()) + '.md'
            full_filename = os.path.join(BASE_PATH, folder, filename)

            with open(full_filename, "w") as text_file:
                text_file.write(content.encode('utf8'))
            spark_data = {'content': item.get('content', ''), 'domain': item.get('domain', ''),
                          'url': item.get('url', ''), 'title': item.get('title', ''), }
            item['content'] = full_filename
            item.save()

            client = InsecureClient(HDFS_ADRESS, user='bogdan')
            with client.write(str(uuid.uuid4()) + '.json', encoding='utf-8') as writer:
                writer.write(json.dumps(spark_data))

        return item
