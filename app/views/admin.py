from flask import Blueprint, render_template, redirect
from flask_user import login_required, roles_required, current_user

from app import app

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
def restrict_bp_to_admins():
    if not current_user.is_authenticated or not current_user.has_role('admin'):
        return redirect('/')

@admin_bp.route('/')
def index():
    t = current_user.__dict__
    return render_template('admin/index.html', t=t)

@admin_bp.route('/feeds/new/')
def new_feed():
    t = current_user.__dict__
    return render_template('admin/feed_new.html', t=t)

