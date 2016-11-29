import os
import uuid
from article_bot.settings import BASE_PATH
from articles.models import Article


class ArticleParserPipeline(object):

    def process_item(self, item, spider):
        folder = "media/"

        try:
            os.mkdir(os.path.join(BASE_PATH, folder))
        except:
            pass

        if not Article.objects.filter(url=item['url']).exists() and item['content']:
            filename = str(uuid.uuid4()) + '.md'
            full_filename = os.path.join(BASE_PATH, folder, filename)

            with open(full_filename, "w") as text_file:
                text_file.write(item['content'])

            item['content'] = full_filename
            item.save()

        return item
