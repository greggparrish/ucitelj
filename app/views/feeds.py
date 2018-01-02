import datetime
from slugify import slugify
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_user import login_required, roles_required, current_user

from app import app, db
from app import images
from app.models.feeds import Feed, Subscription
from app.models.articles import Article
from app.forms.feeds import NewFeedForm

feed_bp = Blueprint('feeds', __name__)

@feed_bp.route('/')
def index():
    feeds = Feed.query.order_by(Feed.name)
    subs = Subscription.query.filter_by(user_id=current_user.id).all()
    user_subs = [ s.feed_id for s in subs ]
    return render_template('feeds/index.html', feeds=feeds, user_subs=user_subs)

@feed_bp.route('/<feed_slug>')
def show(feed_slug):
    f = Feed.query.filter(Feed.slug==feed_slug).first()
    five_hours_ago = datetime.datetime.now() - datetime.timedelta(hours=5)
    if f.checked < five_hours_ago:
        Feed().update_feed(f)
    fa = Article.query.filter(Article.feed_id == f.id).order_by(Article.date.desc())
    return render_template('feeds/show.html', f=f, fa=fa)

@feed_bp.route('/new', methods=(['GET', 'POST']))
def new():
    form = NewFeedForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            filename = images.save(request.files['logo'])
            feed = Feed(
                name=form.name.data,
                rss=form.rss.data,
                country=form.country.data,
                feed_type=form.feed_type.data,
                about=form.about.data,
                logo_filename=filename,
                slug = slugify(form.name.data),
                checked='2017-06-30 14:22:42.150367',
                body_tag=form.body_tag.data
                )
            try:
                db.session.add(feed)
                db.session.commit()
                flash('Feed added.')
            except Exception as e:
                flash('Error: Feed exists {}.'.format(e))
            return redirect(url_for('feeds.index'))
    return render_template('feeds/new.html', form=form)

