from flask import Flask, flash, redirect, url_for, request
from flask_assets import Environment, Bundle
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf.csrf import CSRFProtect

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "users.login"
mail = Mail()
images = UploadSet('feeds', IMAGES)


# INIT APP
app = Flask(__name__)
app.config.from_object(Config)

# INIT UTILS
db.init_app(app)
migrate.init_app(app, db)
login.init_app(app)
mail.init_app(app)
configure_uploads(app, images)
csrf = CSRFProtect(app)


# BLUEPRINTS
from app.views.static import static as static_bp  # noqa: E402
app.register_blueprint(static_bp)

from app.views.articles import article_bp  # noqa: E402
app.register_blueprint(article_bp, url_prefix='/articles')

from app.views.feeds import feed_bp  # noqa: E402
app.register_blueprint(feed_bp, url_prefix='/feeds')

from app.views.words import word_bp  # noqa: E402
app.register_blueprint(word_bp, url_prefix='/words')

from app.views.users import user_bp  # noqa: E402
from app.models.users import User  # noqa: E402
app.register_blueprint(user_bp, url_prefix='/users')

from app.views.grammar import grammar_bp  # noqa: E402
app.register_blueprint(grammar_bp, url_prefix='/grammar')

# ASSETS
assets = Environment(app)
assets.url = app.static_url_path
js = Bundle('js/base.js',
            filters='rjsmin',
            output='public/js/application.js')
css = Bundle('scss/application.scss',
             filters='pyscss',
             output='public/css/style.css',
             depends='scss/*/*.scss')
assets.register('js_all', js)
assets.register('css_all', css)


@login.unauthorized_handler
def handle_needs_login():
    flash("You have to be logged in to access this page.")
    return redirect(url_for('feed.index', next=request.endpoint))
