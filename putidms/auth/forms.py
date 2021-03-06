# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import input_required as ir

from putidms.extensions import MySelectField
from putidms.models.org import Division
from putidms.models.user import User, Role


class LoginForm(FlaskForm):
    username = StringField(u'用户名', validators=[ir(u'用户名不能为空。')])
    password = PasswordField(u'密码', validators=[ir(u'密码不能为空。')])
    submit = SubmitField(u'登录')


class UserForm(FlaskForm):
    username = StringField(u'用户名', validators=[ir(u'用户名不能为空。')])
    password = PasswordField(u'密码', validators=[ir(u'密码不能为空。')])
    realname = StringField(u'真实姓名', validators=[ir(u'真实名或法名不能为空。')])
    email = StringField(u'邮件', validators=[ir(u'邮件地址不能为空。')])
    role_id = MySelectField(u'权限', coerce=int)
    division_id = MySelectField(u'所属修学处', coerce=int)
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.user = kwargs.get('obj')

        role_choices = [(r.id, r.show_name) for r in Role.query.order_by(Role.name).all()]
        role_choices.insert(0, (0, u'请选择权限'))
        self.role_id.choices = role_choices

        division_choices = [(r.id, r.name) for r in Division.query.order_by(Division.name).all()]
        division_choices.insert(0, (0, u'请选择所属修学处'))
        self.division_id.choices = division_choices

        if self.user:
            self.role_id.default = self.user.role_id
            self.division_id.default = self.user.division_id

    def validate_role_id(self, field):
        if field.data <= 0:
            raise ValidationError(u'请选择用户权限。')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已经存在。')

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError(u'Email地址已经存在。')
