import os
from datetime import datetime
import re

from bs4 import BeautifulSoup
from slugify import slugify
from time import mktime
import calendar
import feedparser
import psycopg2
import requests

db_name = os.environ['UCITELJ_DB_NAME']
db_user = os.environ['UCITELJ_DB_USER']
db_pass = os.environ['UCITELJ_DB_KEY']


class dbconn():
    def __init__(self):
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = psycopg2.connect( "dbname='{}' user='{}' host='localhost' password='{}'".format( db_name, db_user, db_pass))
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_class, exc, traceback):
        self.conn.commit()
        self.conn.close()


def update_articles(feeds=None):
    with dbconn() as c:
        if feeds is None:
            c.execute("SELECT id, rss FROM feeds_feed;")
            feeds = c.cursor.fetchall()
        for f in feeds:
            posts = feedparser.parse(f[1])
            for p in posts.entries:
                title = p.title
                date = datetime.fromtimestamp(mktime(p.published_parsed))
                url = p.link
                timestamp = calendar.timegm(p.published_parsed)
                slug = "{}_{}_{}".format(f[0], timestamp, slugify(title))
                c.execute(
                    "INSERT INTO articles_article (feed_id,title,date,url,slug) VALUES (%s,%s,%s,%s,%s) ON CONFLICT (slug) DO NOTHING",
                    (f[0], title, date, url, slug))

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
    with dbconn() as c:
            c.execute(
                "INSERT INTO articles_articletext (article_id,text) VALUES (%s,%s) ON CONFLICT (article_id) DO NOTHING",
                    (article.id,at))
    return at
