# -*- coding:utf-8 -*-
from wtforms import Form, StringField, PasswordField, validators

class LoginForm(Form):
    username = StringField(u'用户名', validators=[validators.input_required(u'用户名不能为空'),validators.data_required()])
    password = PasswordField(u'密码', validators=[validators.input_required(u'密码不能为空')])
