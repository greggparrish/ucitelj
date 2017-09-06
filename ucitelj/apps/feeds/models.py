from django.db import models
from django.contrib.auth.models import User


class Feed(models.Model):
    GENRE_CHOICES = (
        (0, 'news'),
        (1, 'horror'),
        (4, 'politics'),
        (2, 'pop culture'),
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

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'feed',)
