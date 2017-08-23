from django.db import models


class Feed(models.Model):
    name = models.CharField(max_length=200)
    rss = models.CharField(max_length=100)
    checked = models.DateTimeField('date last checked')
    def __str__(self):
        return self.name
