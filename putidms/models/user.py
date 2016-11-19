# -*- coding:utf-8 -*-
from putidms import db
from flask_sqlalchemy import BaseQuery
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from putidms import login_manager
import datetime


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50),nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255),nullable=False, server_default=u'')
    realname = db.Column(db.String(255))
    email = db.Column(db.String(255),nullable=False)
    create_time = db.Column(db.DateTime)
    last_login_time = db.Column(db.DateTime, default=datetime.datetime.now())
    last_login_ip = db.Column(db.String(50))
    is_active = db.Column(db.Boolean,nullable=False, default=True)

    def __init__(self, username, password, **kwargs):
        super(User, self).__init__(**kwargs)
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

# callback function for  flask-login extension
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))