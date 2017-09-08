from django.db import models
from django.utils.text import Truncator


class Article(models.Model):
    feed = models.ForeignKey(
        'feeds.Feed',
        max_length=100,
        on_delete=models.CASCADE)
    img_url = models.CharField(max_length=250, null=True)
    date = models.DateTimeField('article post date')
    title = models.CharField(max_length=250, unique=True)
    permalink = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return "{}:  {}".format(self.title, self.feed)


class ArticleText(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, unique=True)
    text = models.TextField()

    def __str__(self):
        return "{}".format(Truncator(self.text).chars(75))
