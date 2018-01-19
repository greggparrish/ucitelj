import sys
from flask import Blueprint, render_template, request, flash, redirect, abort, url_for, jsonify
from flask.views import MethodView
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

from app import db

admin_bp = Blueprint('admin', __name__)

# ADMIN CRUD PAGES
class CRUDView(MethodView):
    list_template = 'admin/list_view.html'
    detail_template = 'admin/detail_view.html'

    def __init__(self, model, endpoint, list_template=None, detail_template=None, exclude=None, filters=None):
        self.model = model
        self.endpoint = endpoint
        self.path = url_for(f'.{self.endpoint}')
        self.filters = filters or {}
        if list_template:
            self.list_template = list_template
        if detail_template:
            self.detail_template = detail_template
        self.obj_form = model_form(self.model, db.session, base_class=FlaskForm, exclude=exclude)

    def render_detail(self, **kwargs):
        return render_template(self.detail_template, path=self.path, **kwargs)

    def render_list(self, **kwargs):
        return render_template(self.list_template, path=self.path, filters=self.filters, **kwargs)

    def get(self, obj_id='', operation='', filter_name=''):
        if operation == 'new':
            form = self.obj_form()
            action = self.path
            return self.render_detail(form=form, action=action)
        if operation == 'delete':
            obj = self.model.query.get(obj_id)
            db.session.delete(obj)
            db.session.commit()
            return redirect(self.path)
        if operation == 'filter':
            func = self.filters.get(filter_name)
            obj = func(self.model)
            return self.render_list(obj=obj, filter_name=filter_name)
        if obj_id:
            obj = self.model.query.get(obj_id)
            obj_form = model_form(self.model, db.session)
            form = self.obj_form(obj=obj)
            action=request.path
            return self.render_detail(form=form, action=action)
        obj = self.model.query.order_by(self.model.id.desc()).all()
        return self.render_list(obj=obj)

    def post(self, obj_id='', operation=''):
        if obj_id:
            obj = self.model.query.get(obj_id)
        else:
            obj = self.model()
        obj_form = model_form(self.model, db.session, base_class=FlaskForm)
        form = self.obj_form(request.form)
        if form.validate_on_submit:
            form.populate_obj(obj)

            if operation == 'new':
                db.session.add(obj)
            db.session.commit()
        return redirect(self.path)


def register_crud(app, url, endpoint, model, decorators=[], **kwargs):
    view = CRUDView.as_view(endpoint, endpoint=endpoint, model=model, **kwargs)
    for decorator in decorators:
        view = decorator(view)

    app.add_url_rule(f'{ url }/', view_func=view, methods=['GET', 'POST'])
    app.add_url_rule(f'{ url }/<int:obj_id>/', view_func=view)
    app.add_url_rule(f'{ url }/<operation>/', view_func=view, methods=['GET','POST'])
    app.add_url_rule(f'{ url }/<operation>/<int:obj_id>/', view_func=view,
    methods=['GET'])
    app.add_url_rule(f'{ url }/<operation>/<filter_name>/', view_func=view,
    methods=['GET'])

from app.models.feeds import Feed
register_crud(admin_bp, '/feed', 'feed', Feed, exclude=['articles','users','checked','slug'])

from app.models.articles import Article
register_crud(admin_bp, '/article', 'article', Article)

from app.models.practice import WordCase, VerbType, Verb, Noun, Adjective, Adverb
register_crud(admin_bp, '/verb_type', 'verb_type', VerbType, exclude=['verbs',])
register_crud(admin_bp, '/word_case', 'word_case', WordCase)
register_crud(admin_bp, '/verb', 'verb', Verb)
register_crud(admin_bp, '/noun', 'noun', Noun)
register_crud(admin_bp, '/adjective', 'adjective', Adjective)
register_crud(admin_bp, '/adverb', 'adverb', Adverb)

