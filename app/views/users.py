from sqlalchemy.orm import subqueryload
from flask import Blueprint, flash, render_template, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required

from app import db
from app.models.users import User, Role, UserRoles, Subscription, WordBank
from app.forms.users import LoginForm, RegistrationForm
from app.models.words import Definition, format_glossary


user_bp = Blueprint('users', __name__)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('users.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('feeds.index')
        return redirect(next_page)
    return render_template('users/login.html', title='Sign In', form=form)

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('feeds.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful')
        return redirect(url_for('feeds.index'))
    return render_template('users/register.html', title='Register', form=form)

@user_bp.route('/profile')
@login_required
def profile():
    user = User.query.get(3)
    subs = Subscription.query.options(subqueryload(Subscription.feeds)).filter_by(user_id=user.id).all()
    wbq = WordBank.query.with_entities(WordBank.hr_word_id).filter_by(user_id=user.id).all()
    wbl = Definition.query.options(subqueryload(Definition.hr_words)).filter(Definition.hr_word_id.in_(wbq)).all()
    wb = format_glossary(wbl)
    wbs = sorted(wb, key=lambda k: k['hr_word'])
    profile ={
            'user': user,
            'subs':subs,
            'wb':wbs
            }
    return render_template('users/profile.html', profile=profile)

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('static.home'))

