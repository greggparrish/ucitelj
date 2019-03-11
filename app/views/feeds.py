import datetime
from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user, login_required

from app import db
from app.models.feeds import Feed
from app.models.users import Subscription
from app.models.articles import Article

feed_bp = Blueprint('feeds', __name__)


@feed_bp.route('/')
def index():
    feeds = Feed.query.order_by(Feed.name)
    if current_user.is_authenticated:
        subs = Subscription.query.filter_by(user_id=current_user.id).all()
        user_subs = [s.feed_id for s in subs]
    else:
        user_subs = ''
        subs = Subscription.query.all()
    return render_template('feeds/index.html', feeds=feeds, user_subs=user_subs)


@feed_bp.route('/<feed_slug>')
def show(feed_slug):
    f = Feed.query.filter(Feed.slug == feed_slug).first()
    five_hours_ago = datetime.datetime.now() - datetime.timedelta(hours=5)
    if f.checked < five_hours_ago:
        Feed().update_feed(f)
    fa = Article.query.filter(Article.feed_id == f.id).order_by(Article.date.desc())
    return render_template('feeds/show.html', f=f, fa=fa)


@feed_bp.route('/subscriptions/', methods=['GET'])
@login_required
def subscription():
    feed_id = None
    sub_type = None
    if request.method == 'GET':
        feed_id = request.args.get('feed_id', type=int)
        sub_type = request.args.get('sub_type', type=str)
    if feed_id and sub_type:
        fid = Feed.query.get(feed_id)
        uid = current_user.id

        if sub_type == 'sub':
            sub = Subscription(user_id=uid, feed_id=fid.id)
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
