import sys
from flask import Blueprint, render_template, request, flash, redirect, abort, url_for, jsonify
from flask.views import MethodView
from wtforms.ext.sqlalchemy.orm import model_form

from app import db

admin_bp = Blueprint('admin', __name__)

# ADMIN CRUD PAGES
class CRUDView(MethodView):
    list_template = 'admin/list_view.html'
    detail_template = 'admin/detail_view.html'

    def __init__(self, model, endpoint, list_template=None, detail_template=None, exclude=None):
        self.model = model
        self.endpoint = endpoint
        self.path = url_for(f'.{self.endpoint}')
        if list_template:
            self.list_template = list_template
        if detail_template:
            self.detail_template = detail_template
        self.obj_form = model_form(self.model, db.session, exclude=exclude)

    def render_detail(self, **kwargs):
        return render_template(self.detail_template, path=self.path, **kwargs)

    def render_list(self, **kwargs):
        return render_template(self.list_template, path=self.path, **kwargs)

    def get(self, obj_id='', operation=''):
        if operation == 'new':
            form = self.obj_form()
            action = self.path
            return self.render_detail(form=form, action=action)
        if operation == 'delete':
            obj = self.model.query.get(obj_id)
            db.session.delete(obj)
            db.session.commit()
            return redirect(self.path)
        if obj_id:
            obj = self.model.query.get(obj_id)
            obj_form = model_form(self.model, db.session)
            form = self.obj_form(obj=obj)
            action=request.path
            return self.render_detail(form=form, action=action)
        obj = self.model.query.order_by(self.model.id.desc()).all()
        return self.render_list(obj=obj)

from app.models.feeds import Feed
view = CRUDView.as_view('feed', Feed, endpoint='feed')
admin_bp.add_url_rule('/feed/', view_func=view, methods=['GET', 'POST'])
admin_bp.add_url_rule('/feed/<operation>/<int:obj_id>/', view_func=view, methods=['GET', 'POST'])
admin_bp.add_url_rule('/feed/<int:obj_id>/', view_func=view, methods=['GET', 'POST'])

from app.models.articles import Article
view = CRUDView.as_view('article', Article, endpoint='article')
admin_bp.add_url_rule('/article/', view_func=view, methods=['GET', 'POST'])
admin_bp.add_url_rule('/article/<operation>/<int:obj_id>/', view_func=view, methods=['GET', 'POST'])
admin_bp.add_url_rule('/article/<int:obj_id>/', view_func=view, methods=['GET', 'POST'])


from app.models.practice import VerbType
view = CRUDView.as_view('verb_type', VerbType, endpoint='verb_type', exclude='verbs')
admin_bp.add_url_rule('/verb_type/', view_func=view, methods=['GET', 'POST'])
admin_bp.add_url_rule('/verb_type/<operation>/<int:obj_id>/', view_func=view, methods=['GET', 'POST'])
admin_bp.add_url_rule('/verb_type/<int:obj_id>/', view_func=view, methods=['GET', 'POST'])

