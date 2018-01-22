import logging
import os

from flask import Flask, render_template
from flask_admin import Admin, AdminIndexView
from flask_assets import Environment, Bundle
from flask_babel import Babel, lazy_gettext as _l
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_user import current_user, login_required, UserManager, UserMixin, SQLAlchemyAdapter
from flask_wtf.csrf import CSRFProtect

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "users.login"
mail = Mail()
babel = Babel()
images = UploadSet('feeds', IMAGES)


# INIT APP
app = Flask(__name__)
app.config.from_object(Config)

# INIT UTILS
db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
mail.init_app(app)
babel.init_app(app)
configure_uploads(app, images)
csrf = CSRFProtect(app)


# BLUEPRINTS
from app.views.static import static as static_bp
app.register_blueprint(static_bp)

from app.views.articles import article_bp
app.register_blueprint(article_bp, url_prefix='/articles')

from app.views.feeds import feed_bp
app.register_blueprint(feed_bp, url_prefix='/feeds')

from app.views.words import word_bp
app.register_blueprint(word_bp, url_prefix='/words')

from app.views.users import user_bp
from app.models.users import User
app.register_blueprint(user_bp, url_prefix='/users')

from app.views.practice import practice_bp
app.register_blueprint(practice_bp, url_prefix='/practice')

# USER MGMT
db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, app)


# ADMIN
class UciteljAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if not current_user.is_authenticated:
            return False
        return current_user.has_role('admin')

admin = Admin(app, name='Učitelj', index_view=UciteljAdminIndexView(), template_mode='bootstrap3')
from app import admin_views

# ASSETS
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
        depends='scss/*/*.scss')
assets.register('js_all', js)
assets.register('css_all', css)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def handle_needs_login():
    flash("You have to be logged in to access this page.")
    return redirect(url_for('feed.index', next=request.endpoint))
