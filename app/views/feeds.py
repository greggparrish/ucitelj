import datetime
from slugify import slugify
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_user import login_required, roles_required, current_user

from app import app, db
from app import images
from app.models.feeds import Feed, Subscription
from app.models.articles import Article
from app.forms.feeds import FeedForm

feed_bp = Blueprint('feeds', __name__)

@feed_bp.route('/')
def index():
    feeds = Feed.query.order_by(Feed.name)
    if current_user.is_authenticated:
        subs = Subscription.query.filter_by(user_id=current_user.id).all()
        user_subs = [ s.feed_id for s in subs ]
    else:
        user_subs = ''
        subs = Subscription.query.all()
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
@login_required
@roles_required('admin')
def new():
    form = FeedForm()
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
    return render_template('feeds/form.html', form=form)

@feed_bp.route('/edit/<int:feed_id>', methods=(['GET', 'POST']))
@login_required
@roles_required('admin')
def edit(feed_id):
    feed = Feed.query.get(feed_id)
    form = FeedForm(obj=feed)
    current_logo = feed.logo_filename
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
                body_tag=form.body_tag.data
                )
            try:
                db.session.commit()
                flash('Feed edited.')
            except Exception as e:
                flash('Error: Feed exists {}.'.format(e))
            return redirect(url_for('feeds.index'))
    return render_template('feeds/form.html', form=form, current_logo=current_logo)

@feed_bp.route('/subscriptions/', methods=['GET'])
@login_required
def subscription():
    feed_id = None
    sub_type=None
    if request.method == 'GET':
        feed_id = request.args.get('feed_id', type=int)
        sub_type = request.args.get('sub_type', type=str)
    if feed_id and sub_type:
        fid = Feed.query.get(feed_id)
        uid = current_user.id

        if sub_type == 'sub':
          sub = Subscription(user_id=uid,feed_id=fid.id)
          db.session.add(sub)
          db.session.commit()
          return jsonify('subbed')

        elif sub_type == 'unsub':
            sub = Subscription.query.filter_by(user_id=uid, feed_id=fid.id).first()
            if sub:
                db.session.delete(sub)
                db.session.commit()
                return jsonify('unsubbed')
            else:
                return jsonify('not subbed to this feed')
        else:
            return jsonify('bad formatting')
    else:
        return jsonify('bad formatting')
