from django.db import models
from django.utils.text import Truncator


class Article(models.Model):
    feed = models.ForeignKey('feeds.Feed', max_length=100, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    url = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return "{}:  {}".format(self.feed, self.word)


class ArticleText(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return "{}".format(Truncator(text).chars(75))
