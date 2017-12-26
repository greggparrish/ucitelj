import logging
import os

from flask import Flask, render_template
from flask_assets import Environment, Bundle
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

""" INIT APP """
app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

""" INIT UTILS """
db.init_app(app)
migrate.init_app(app, db)
login.init_app(app)

""" BLUEPRINTS """
from app.views.static import static as static_bp
app.register_blueprint(static_bp)

from app.views.words import word_bp
app.register_blueprint(word_bp, url_prefix='/words')

from app.views.articles import article_bp
app.register_blueprint(article_bp, url_prefix='/articles')

from app.views.feeds import feed_bp
app.register_blueprint(feed_bp, url_prefix='/feeds')

from app.views.users import user_bp
app.register_blueprint(user_bp, url_prefix='/users')


""" ASSETS """
assets = Environment(app)
assets.url = app.static_url_path
js = Bundle(
        'js/base.js',
        filters='rjsmin',
        output='public/js/application.js')
css = Bundle(
        'scss/application.scss',
        filters='pyscss',
        output='public/css/style.css',
        depends='scss/partials/*.scss')
assets.register('js_all', js)
assets.register('css_all', css)
