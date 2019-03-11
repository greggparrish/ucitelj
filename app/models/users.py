from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False, default='')
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    confirmed_at = db.Column(db.DateTime())
    first_name = db.Column(db.String(50), nullable=True, default='')
    last_name = db.Column(db.String(50), nullable=True, default='')
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))
    subscriptions = db.relationship("Subscription", backref='users')

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    def is_active(self):
        return self.is_enabled

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
        return User.query.get(int(id))


class Role(db.Model):
    '''
    User roles: admin, editor, public
    '''
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return '<Role: {}>'.format(self.name)


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return '<User role: {} {}>'.format(self.user.username, self.role.name)


class InviteCode(db.Model):
    __tablename__ = 'invite_codes'
    id = db.Column(db.Integer(), primary_key=True)
    code = db.Column(db.String(256), unique=True, nullable=False)


class Subscription(db.Model):
    '''
        M2M table linking users with feeds
    '''
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    feed_id = db.Column(db.Integer, db.ForeignKey('feeds.id', ondelete='CASCADE'), nullable=False)
    __table_args__ = (db.UniqueConstraint("feed_id", "user_id"),)

    def __repr__(self):
        return '<Sub: {}>'.format(self.feed.name)


class WordBank(db.Model):
    '''
        M2M table allowing users to save specific words
    '''
    __tablename__ = 'wordbanks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    hr_word_id = db.Column(db.Integer, db.ForeignKey('hr_words.id', ondelete='CASCADE'), nullable=False)
    __table_args__ = (db.UniqueConstraint("hr_word_id", "user_id"),)
