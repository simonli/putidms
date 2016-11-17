# -*- coding:utf-8 -*-
from putidms.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    realname = db.Column(db.String(255))
    create_time = db.Column(db.DateTime)
    last_login_time = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(50))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

    def get_user(self,username):
        pass
