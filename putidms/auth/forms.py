# -*- coding:utf-8 -*-
from wtforms import Form, StringField, PasswordField, SubmitField, validators
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    username = StringField(u'用户名', validators=[validators.input_required(u'用户名不能为空。')])
    password = PasswordField(u'密码', validators=[validators.input_required(u'密码不能为空。')])
    submit = SubmitField(u'登录')


class UserForm(FlaskForm):
    username = StringField(u'用户名', validators=[validators.input_required(u'用户名不能为空。')])
    password = PasswordField(u'密码', validators=[validators.input_required(u'密码不能为空。')])
    realname = StringField(u'真实名', validators=[validators.input_required(u'真实名或法名不能为空。')])
    email = StringField(u'邮件', validators=[validators.input_required(u'邮件地址不能为空。')])
    # role = StringField(u'角色', validators=[validators.input_required(u'角色不能为空。')])
    submit = SubmitField(u'登录')
