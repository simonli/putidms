# -*- coding:utf-8 -*-
from wtforms import StringField, PasswordField, SubmitField, validators, SelectField, ValidationError
from flask_wtf import FlaskForm
from putidms.models.user import User

ROLE_CHOICES = [(v, User.get_description(k)) for (k, v) in User.ROLES.to_dict.items()]
ROLE_CHOICES.insert(0, (0, ''))


class LoginForm(FlaskForm):
    username = StringField(u'用户名', validators=[validators.input_required(u'用户名不能为空。')])
    password = PasswordField(u'密码', validators=[validators.input_required(u'密码不能为空。')])
    submit = SubmitField(u'登录')


class UserForm(FlaskForm):
    username = StringField(u'用户名', validators=[validators.input_required(u'用户名不能为空。')])
    password = PasswordField(u'密码', validators=[validators.input_required(u'密码不能为空。')])
    realname = StringField(u'真实名', validators=[validators.input_required(u'真实名或法名不能为空。')])
    email = StringField(u'邮件', validators=[validators.input_required(u'邮件地址不能为空。')])
    role = SelectField(u'角色', choices=ROLE_CHOICES, coerce=int)
    submit = SubmitField(u'添加')

    def validate_role(form, field):
        if field.data <= 0:
            raise ValidationError(u'请选择一个用户权限角色。')
