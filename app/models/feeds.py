import re
import requests

import feedparser
import requests
from requests.exceptions import ConnectionError
import calendar
from time import mktime
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from slugify import slugify
from flask_login import login_required

from app import app, db
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
    logo = db.Column(db.String(250))
    name = db.Column(db.String(250), nullable=False)
    rss = db.Column(db.String(250), unique=True, nullable=False)
    slug = db.Column(db.String(250), unique=True, nullable=False)

    def __repr__(self):
        return '<Feed: {}>'.format(self.name)


    def update_feed(self, feed):
        '''
        Updates feed content from rss feed, populates articles but not article_text
        Return: feed object
        '''
        try:
            feed_response = requests.get(feed.rss, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'})
            posts = feedparser.parse(feed_response)
            with app.app_context():
                db.create_all()
                for p in posts.entries:
                    title = p.title
                    date = datetime.fromtimestamp(mktime(p.published_parsed))
                    url = p.link
                    timestamp = calendar.timegm(p.published_parsed)
                    slug = "{}_{}_{}".format(feed.id, timestamp, slugify(title))
                    try:
                        new_text = Article(
                                permalink=url,
                                feed_id=feed.id,
                                title=title,
                                date=date,
                                slug=slug
                                )
                        db.session.add(new_text)
                    except IntegrityError:
                        db.session.rollback()
                feed.checked = datetime.now()
                db.session.commit()
        except ConnectionError:
            feed = False
        return feed


class Subscription(db.Model):
    '''
    M2M table linking users with feeds
    '''
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    feed_id = db.Column(db.Integer, db.ForeignKey('feeds.id', ondelete='CASCADE'), nullable=False)
    __table_args__ = (db.UniqueConstraint("feed_id", "user_id"),)

