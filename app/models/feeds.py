import re
import requests

import feedparser
import calendar
from time import mktime
from datetime import datetime
from slugify import slugify

from app import app, db
from app.models.users import User

TYPE_CHOICES = ('culture', 'news', 'politics', 'regional', 'religious')
COUNTRY_CHOICES = ('Croatia', 'Serbia')


class Feed(db.Model):
    __tablename__ = 'feeds'

    id = db.Column(db.Integer, primary_key=True)
    articles = db.relationship('Article', backref='feed', lazy='dynamic', order_by="desc(Article.date)")
    about = db.Column(db.Text)
    body_tag = db.Column(db.String(250))
    checked = db.Column(db.DateTime)
    country = db.Column(db.Enum(*COUNTRY_CHOICES, name="country"))
    feed_type = db.Column(db.Enum(*TYPE_CHOICES, name="feed_type"))
    logo = db.Column(db.String(250))
    name = db.Column(db.String(250))
    rss = db.Column(db.String(250))
    slug = db.Column(db.String(250), unique=True)

    def __repr__(self):
        return '<Feed: {}>'.format(self.name)


    def update_feed(self, feed):
        posts = feedparser.parse(feed.rss, agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
        with app.app_context():
            db.create_all()
            for p in posts.entries:
                title = p.title
                date = datetime.fromtimestamp(mktime(p.published_parsed))
                url = p.link
                timestamp = calendar.timegm(p.published_parsed)
                slug = "{}_{}_{}".format(feed.id, timestamp, slugify(title))
                try:
                    with db.session.begin_nested():
                        new_text = Article(permalink=url, defaults={'feed_id':feed.id,'title':title,'date':date,'slug':slug})
                        db.session.add(new_text)
                except IntegrityError:
                    #Article text already exists
                    new_text = Article.query.filter(permalink=url).first()
            feed.checked = timezone.now()
            db.session.add(feed)
            db.session.commit()
        return feed


class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    feed_id = db.Column(db.Integer, db.ForeignKey(Feed.id))
    __table_args__ = (db.UniqueConstraint("feed_id", "user_id"),)

