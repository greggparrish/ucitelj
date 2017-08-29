from django.db import models


class Article(models.Model):
    feed = models.ForeignKey('feeds.Feed', max_length=100, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    url = models.CharField(max_length=200, unique=True)
    text = models.TextField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return "%s:  %s" % (self.feed, self.word)
