from flask import redirect, url_for, request
from app import db, admin
from flask_user import login_required, roles_required, current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import ImageUploadField

from app.models.users import User
from app.models.grammar import Verb, Noun, Adjective, Adverb, WordCase, Preposition
from app.models.feeds import Feed
from app.models.articles import Article, ArticleText


class UciteljModelView(ModelView):
    def is_accessible(self):
        if not current_user.is_authenticated:
            return False
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('user.login', next=request.url))


# USER
class UserView(UciteljModelView):
    column_exclude_list = ['password_hash', 'confirmed_at']

admin.add_view(UserView(User, db.session))


# GRAMMAR
class VerbView(UciteljModelView):
    form_excluded_columns = ['verbs']
class VerbView(UciteljModelView):
    column_exclude_list = ['body',]
    form_excluded_columns = ['verbs']
class WordCaseView(UciteljModelView):
    column_exclude_list = ['table',]
    form_excluded_columns = ['verbs']

admin.add_view(VerbView(Verb, db.session))
admin.add_view(UciteljModelView(Noun, db.session))
admin.add_view(UciteljModelView(Adjective, db.session))
admin.add_view(UciteljModelView(Adverb, db.session))
admin.add_view(WordCaseView(WordCase, db.session))
admin.add_view(UciteljModelView(Preposition, db.session))


# FEEDS & ARTICLES
class FeedView(UciteljModelView):
    column_list = ['name', 'feed_type', 'checked', 'country']
    column_exclude_list = ['confirmed_at', 'logo_filename']
    form_excluded_columns = ['users', 'articles']
    logo_filename = ImageUploadField('logo_filename')
class ArticleView(UciteljModelView):
    column_list = ['feed', 'title', 'date']
class ArticleTextView(UciteljModelView):
    column_list = ['has_dict','article.date', 'article.feed.name', 'article.title']
    column_searchable_list = ['article.title']

admin.add_view(FeedView(Feed, db.session))
admin.add_view(ArticleView(Article, db.session))
admin.add_view(ArticleTextView(ArticleText, db.session))
