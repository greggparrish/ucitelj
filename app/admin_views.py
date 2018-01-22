from flask import redirect, url_for, request
from app import db, admin
from flask_user import login_required, roles_required, current_user
from flask_admin.contrib.sqla import ModelView

from app.models.users import User
from app.models.practice import Verb, Noun, Adjective, Adverb, VerbType, WordCase


class UciteljModelView(ModelView):
    def is_accessible(self):
        if not current_user.is_authenticated:
            return False
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('user.login', next=request.url))

class UserView(UciteljModelView):
    column_exclude_list = ['password_hash', 'confirmed_at']

class VerbTypeView(UciteljModelView):
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
