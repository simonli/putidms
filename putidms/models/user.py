# -*- coding:utf-8 -*-
from putidms import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from putidms import login_manager
from datetime import datetime


class Permission:
    USER = 0x01
    MODERATOR = 0x02
    ADMIN = 0xff


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True, index=True)
    show_name = db.Column(db.String(100))
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super(Role, self).__init__(*args, **kwargs)

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.USER, True, u'修学处义工'),  # 修学处义工权限
            'Moderator': (Permission.MODERATOR, False, u'辅导委义工'),  # 辅导委义工权限
            'Admin': (Permission.ADMIN, False, u'管理员')  # 超级管理员权限
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            role.show_name = roles[r][2]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True, index=True)
    _password_hash = db.Column('password', db.String(255), nullable=False, server_default=u'')
    realname = db.Column(db.String(255))
    email = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    last_login_time = db.Column(db.DateTime, default=datetime.now)
    last_login_ip = db.Column(db.String(50), default='')
    login_count = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self._password_hash = generate_password_hash(password)

    @property
    def is_admin(self):
        return self.can(Permission.ADMIN)

    @property
    def is_moderator(self):
        return self.can(Permission.MODERATOR)

    def verify_password(self, password):
        return check_password_hash(self._password_hash, password)

    def can(self, permissions):
        return self.role is not None and (self.role.permissions | permissions) == permissions

    def update_login_info(self, last_login_ip):
        self.last_login_ip = last_login_ip
        self.last_login_time = datetime.now()
        self.login_count += 1
        db.session.add(self)
        db.session.commit()

    # callback function for  flask-login extension
    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
