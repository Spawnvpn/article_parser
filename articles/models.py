from __future__ import unicode_literals

from django.db import models


class Article(models.Model):
    domain = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    date_published = models.CharField(max_length=255, null=True)
    date_stored = models.DateTimeField(auto_now=True)
    content = models.FileField(upload_to='media', max_length=255)

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
