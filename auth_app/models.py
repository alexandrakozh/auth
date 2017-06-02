from flask.ext.login import UserMixin
from app import db
from datetime import datetime
from six import text_type
import uuid
from passlib.apps import custom_app_context as pwd


class AuthenticationError(Exception):
    """
    Class for base error during authentication
    """
    pass


class User(db.Model, UserMixin):
    """
    Simple User model
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(100), unique=True)
    image = db.relationship('Image', backref='user', lazy='dynamic')
    created_on = db.Column('created_on', db.DateTime)

    def __init__(self, username=None, user_id=None, email=None):
        if not user_id:
            self.id = uuid.uuid4().hex[:5]
        else:
            self.id = user_id
        self.username = username
        self.password_hash = None
        self.email = email
        self.created_on = datetime.now()

    def hash_password(self, password):
        self.password_hash = pwd.encrypt(password)

    def verify_password(self, password):
        return pwd.verify(password, self.password_hash)

    def get_id(self):
        try:
            return text_type(self.id)
        except:
            raise AuthenticationError('User id is not valid')

    def __repr__(self):
        return '<User %r>' % self.username


class Image(db.Model):
    id = db.Column('image_id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
