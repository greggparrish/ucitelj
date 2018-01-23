from flask import redirect, url_for, request
from app import db, admin
from flask_user import login_required, roles_required, current_user
from flask_admin.contrib.sqla import ModelView

from app.models.users import User
from app.models.practice import Verb, Noun, Adjective, Adverb, VerbType, WordCase
from app.models.feeds import Feed
from app.models.articles import Article, ArticleText


class UciteljModelView(ModelView):
    def is_accessible(self):
        if not current_user.is_authenticated:
            return False
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('user.login', next=request.url))

class UserView(UciteljModelView):
    column_exclude_list = ['password_hash', 'confirmed_at']

# PRACTICE
class VerbTypeView(UciteljModelView):
    form_excluded_columns = ['verbs']

class VerbView(UciteljModelView):
    form_excluded_columns = ['verbs']

class VerbView(UciteljModelView):
    form_excluded_columns = ['verbs']

admin.add_view(UserView(User, db.session))
admin.add_view(VerbView(Verb, db.session))
admin.add_view(UciteljModelView(Noun, db.session))
admin.add_view(UciteljModelView(Adjective, db.session))
admin.add_view(UciteljModelView(Adverb, db.session))
admin.add_view(UciteljModelView(WordCase, db.session))
admin.add_view(VerbTypeView(VerbType, db.session))

# FEEDS & ARTICLES
class FeedView(UciteljModelView):
    column_list = ['name', 'feed_type', 'checked', 'country']
    column_exclude_list = ['confirmed_at', 'logo_filename']
    form_excluded_columns = ['users', 'articles']
class ArticleView(UciteljModelView):
    column_list = ['feed', 'title', 'date']
class ArticleTextView(UciteljModelView):
    column_list = ['article', 'title']
    column_searchable_list = ['article.title']

admin.add_view(FeedView(Feed, db.session))
admin.add_view(ArticleView(Article, db.session))
admin.add_view(ArticleTextView(ArticleText, db.session))
