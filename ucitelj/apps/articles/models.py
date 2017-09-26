from django.db import models
from django.utils.text import Truncator

import re

from bs4 import BeautifulSoup
from slugify import slugify
import requests


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
    article = models.OneToOneField('Article', on_delete=models.CASCADE)
    text = models.TextField()

    def get_article_content(article):
        r = requests.get(article.permalink)
        soup = BeautifulSoup(r.content, 'lxml')
        at = []
        e,n = re.split('\.|#', article.feed.body_tag)
        s = '#' if '#' in article.feed.body_tag else '.'
        if '#' in article.feed.body_tag:
          bt = soup.find(e, id=n)
        else:
          bt = soup.find(e, class_=n)
        ps = bt.find_all('p')
        for p in ps:
            if p.text != '':
                at.append("<p>{}</p>".format(p.text.strip()))
        new_text = ArticleText(article=article, text=at)
        new_text.save
        return at

    def __str__(self):
        return "{}".format(Truncator(self.text).chars(75))
