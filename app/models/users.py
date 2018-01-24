import jwt
from flask_user import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False, default='')
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    confirmed_at = db.Column(db.DateTime())
    is_enabled = db.Column(db.Boolean(), nullable=False, default=False)
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

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

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

class InviteCode(db.Model, UserMixin):
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
