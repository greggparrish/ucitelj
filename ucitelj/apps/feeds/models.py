from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from datetime import datetime
import feedparser
import calendar
from time import mktime
from slugify import slugify

from ..articles.models import Article

class Feed(models.Model):
    GENRE_CHOICES = (
        (5, 'catholic'),
        (0, 'news'),
        (1, 'horror'),
        (4, 'politics'),
        (2, 'pop culture'),
        (6, 'regional'),
        (3, 'scifi'),
    )
    COUNTRY_CHOICES = (
        (0, 'HR'),
        (1, 'RS')
    )
    logo = models.FileField(upload_to='static/img/feeds/', verbose_name="feed logo image", null=True, blank=True)
    feedtype = models.IntegerField(choices=GENRE_CHOICES, blank=True, null=True)
    country = models.IntegerField(choices=COUNTRY_CHOICES, blank=True, null=True)
    name = models.CharField(max_length=200)
    about = models.TextField()
    rss = models.CharField(max_length=100)
    checked = models.DateTimeField('date last checked')
    body_tag = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def update_feed(feed):
        posts = feedparser.parse(feed.rss, agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
        for p in posts.entries:
            title = p.title
            date = datetime.fromtimestamp(mktime(p.published_parsed))
            url = p.link
            timestamp = calendar.timegm(p.published_parsed)
            slug = "{}_{}_{}".format(feed.id, timestamp, slugify(title))
            new_text, add_date = Article.objects.get_or_create(permalink=url, defaults={'feed_id':feed.id,'title':title,'date':date,'slug':slug})
        feed.checked = timezone.now()
        feed.save()

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'feed',)
