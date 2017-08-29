from django.db import models


class Feed(models.Model):
    logo = models.FileField(upload_to='static/img/feeds/', verbose_name="feed logo image", null=True, blank=True)
    name = models.CharField(max_length=200)
    rss = models.CharField(max_length=100)
    checked = models.DateTimeField('date last checked')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
