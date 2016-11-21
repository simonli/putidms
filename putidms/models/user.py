# -*- coding:utf-8 -*-
from putidms import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from putidms import login_manager
from datetime import datetime
from putidms.helper import enum


class User(UserMixin, db.Model):
    __tablename__ = 'putidms_users'

    # MEMBER = 100 修学处档案义工权限
    # ADMIN = 200   辅导委档案义工权限
    # SUPER_ADMIN = 999  超级管理员，可以添加User和Admin
    ROLES = enum(MEMBER=100, ADMIN=200, SUPER_ADMIN=999)
    ROLES_NAMES = {100:u'修学处档案义工',200:u'辅导委档案义工',999:u'超级管理员'}


    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True, index=True)
    _password_hash = db.Column('password', db.String(255), nullable=False, server_default=u'')
    realname = db.Column(db.String(255))
    email = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())
    last_login_time = db.Column(db.DateTime, default=datetime.now())
    last_login_ip = db.Column(db.String(50), default='')
    login_count = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    role = db.Column(db.Integer, nullable=False, default=ROLES.MEMBER)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self._password_hash = generate_password_hash(password)

    @property
    def is_super_admin(self):
        return self.role == self.ROLES.SUPER_ADMIN

    @property
    def is_admin(self):
        return self.role == self.ROLES.ADMIN

    @property
    def is_member(self):
        return self.role == self.ROLES.MEMBER

    def verify_password(self, password):
        return check_password_hash(self._password_hash, password)

    def update_login_info(self, last_login_ip):
        self.last_login_ip = last_login_ip
        self.last_login_time = datetime.now()
        self.login_count += 1
        db.session.add(self)
        db.session.commit()

    def get_role_name(self, role_type):
        return self.ROLES_NAMES.get(role_type)

    # callback function for  flask-login extension
    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


