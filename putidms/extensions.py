# -*- coding:utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from wtforms import SelectField

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = u'欢迎使用菩提书院辅导员管理系统，请登录后访问该页面！'
login_manager.login_message_category = "warning"


class MySelectField(SelectField):
    def iter_choices(self):
        for value, label in self.choices:
            if self.default:
                yield (value, label, self.coerce(value) == self.coerce(self.default))
            else:
                yield (value, label, self.coerce(value) == self.data)
