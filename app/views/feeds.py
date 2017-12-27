import datetime

from app import app
from app.models.feeds import Feed
from app.models.articles import Article
from flask import Blueprint, render_template

feed_bp = Blueprint('feeds', __name__)

@feed_bp.route('/')
def index(page=1):
    feeds = Feed.query.order_by(Feed.name)
    return render_template('feeds/index.html', feeds=feeds)

@feed_bp.route('/<feed_slug>')
def show(feed_slug):
    f = Feed.query.filter(Feed.slug==feed_slug).first()
    five_hours_ago = datetime.datetime.now() - datetime.timedelta(hours=5)
    if f.checked < five_hours_ago:
      Feed().update_feed(f)
    fa = Article.query.filter(Article.feed_id == f.id).order_by(Article.date.desc())
    return render_template('feeds/show.html', f=f, fa=fa)

