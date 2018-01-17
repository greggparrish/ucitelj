import re
import requests
import sys

import feedparser
import requests
from requests.exceptions import ConnectionError
import calendar
from time import mktime
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from slugify import slugify
from flask_login import login_required

from app import db
from app.models.articles import Article

TYPE_CHOICES = ('culture', 'news', 'politics', 'regional', 'religious')
COUNTRY_CHOICES = ('Croatia', 'Serbia')


class Feed(db.Model):
    '''
    RSS feeds: Parent to articles, classified by TYPE_CHOICES and COUNTRY_CHOICES
    to allow filtering/use of HR or RS dictionaries
    '''
    __tablename__ = 'feeds'

    id = db.Column(db.Integer, primary_key=True)
    articles = db.relationship('Article', backref='feed', lazy='dynamic')
    about = db.Column(db.Text)
    body_tag = db.Column(db.String(250), nullable=False)
    checked = db.Column(db.DateTime)
    country = db.Column(db.Enum(*COUNTRY_CHOICES, name="country"))
    feed_type = db.Column(db.Enum(*TYPE_CHOICES, name="feed_type"))
    logo_filename = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    rss = db.Column(db.String(250), unique=True, nullable=False)
    users = db.relationship("Subscription", backref='feeds')
    slug = db.Column(db.String(250), unique=True, nullable=False)

    def country_choices(self):
        return [ (c, c) for c in COUNTRY_CHOICES ]

    def type_choices(self):
        return [ (c, c) for c in TYPE_CHOICES ]

    def __repr__(self):
        return '<Feed: {}>'.format(self.name)

    def update_feed(self, feed):
        '''
        Updates feed content from rss feed, populates articles but not article_text
        Return: feed object
        '''
        try:
            feed_response = requests.get(feed.rss, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}, timeout=2)
        except Exception as e:
          return False
        if feed_response.status_code == 200:
            posts = feedparser.parse(feed_response.content)
            for p in posts.entries:
                title = p.title
                date = datetime.fromtimestamp(mktime(p.published_parsed))
                url = p.link
                timestamp = calendar.timegm(p.published_parsed)
                slug = "{}_{}_{}".format(feed.id, timestamp, slugify(title))
                if date > feed.checked:
                    new_text = Article(
                            permalink=url,
                            feed_id=feed.id,
                            title=title,
                            date=date,
                            slug=slug
                            )
                    try:
                        db.session.add(new_text)
                        db.session.commit()
                    except IntegrityError:
                        ''' Article already exists '''
                        db.session.rollback()
            feed.checked = datetime.now()
            db.session.commit()
            return feed


