import os
import calendar
from datetime import datetime
from time import mktime
import psycopg2
import feedparser
from slugify import slugify

def update_articles(feeds=None):
    '''  update articles '''
    db_name = os.environ['UCITELJ_DB_NAME']
    db_user = os.environ['UCITELJ_DB_USER']
    db_pass = os.environ['UCITELJ_DB_KEY']

    try:
        conn = psycopg2.connect(
            "dbname='{}' user='{}' host='localhost' password='{}'".format(
                db_name, db_user, db_pass))
    except BaseException:
        print("unable to connect to db")

    cur = conn.cursor()

    if feeds is None:
        cur.execute("SELECT id, rss FROM feeds_feed;")
        feeds = cur.fetchall()

    for f in feeds:
        posts = feedparser.parse(f[1])
        for p in posts.entries:
            title = p.title
            date = datetime.fromtimestamp(mktime(p.published_parsed))
            url = p.link
            timestamp = calendar.timegm(p.published_parsed)
            slug = "{}_{}_{}".format(f[0], timestamp, slugify(title))
            cur.execute(
                "INSERT INTO articles_article (feed_id,title,date,url,slug) VALUES (%s,%s,%s,%s,%s) ON CONFLICT (slug) DO NOTHING",
                (f[0],
                 title,
                 date,
                 url,
                 slug))
        conn.commit()
    conn.close()
