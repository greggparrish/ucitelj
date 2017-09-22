from django.db import models
from django.utils.text import Truncator

from bs4 import BeautifulSoup
from slugify import slugify
from time import mktime
import calendar
import feedparser
import psycopg2
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

    def update_articles(feeds=None):
        feeds = Feed.objects.all
        for f in feeds:
            posts = feedparser.parse(f.rss)
            for p in posts.entries:
                title = p.title
                date = datetime.fromtimestamp(mktime(p.published_parsed))
                url = p.link
                timestamp = calendar.timegm(p.published_parsed)
                slug = "{}_{}_{}".format(f[0], timestamp, slugify(title))
                new_text, add_date = Article.get_or_create(feed_id=f.id,title=title,date=date,url=url,slug=slug)

    def __str__(self):
        return "{}:  {}".format(self.title, self.feed)


class ArticleText(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, unique=True)
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
        new_text = ArticleText(article=article_id, text=text)
        new_text.save
        return new_text

    def __str__(self):
        return "{}".format(Truncator(self.text).chars(75))



