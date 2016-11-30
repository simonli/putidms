# -*- coding:utf-8 -*-
from wtforms import StringField, PasswordField, SubmitField,TextAreaField, \
    validators, SelectField, ValidationError
from flask_wtf import FlaskForm
from putidms.models.org import Division, Department


class DivisionForm(FlaskForm):
    name = StringField(u'修学处名称', validators=[validators.input_required(u'名称不能为空。')])
    desc = TextAreaField(u'简要描述')

    def __init__(self, *args, **kwargs):
        super(DivisionForm, self).__init__(*args, **kwargs)
        self.division = kwargs.get('obj')

    def validate_name(self, field):
        if field.data != self.division.name and \
                Division.query.filter_by(name=field.data).first():
            raise ValidationError(u'修学处名称已存在。')


class DepartmentForm(FlaskForm):
    division_id = SelectField(u'所属修学处', coerce=int)
    name = StringField(u'修学点名称', validators=[validators.input_required(u'名称不能为空。')])
    desc = TextAreaField(u'简要描述')

    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        division_choices = [(r.id, r.name) for r in Division.query.order_by(Division.name).all()]
        division_choices.insert(0, (0, u'请选择所属修学处'))
        self.division_id.choices = division_choices
        self.department = kwargs.get('obj')
        if self.department:
            self.division_id.default = self.department.division_id

    def validate_division_id(self, field):
        if field.data <= 0:
            raise ValidationError(u'请选择所属修学处。')

    def validate_name(self, field):
        if field.data != self.department.name and \
                Department.query.filter_by(name=field.data).first():
            raise ValidationError(u'修学点名称已存在。')


class ClassForm(FlaskForm):
    division_id = SelectField(u'所属修学处', coerce=int)
    department_id = SelectField(u'所属修学点', coerce=int)
    name = StringField(u'班级名称', validators=[validators.input_required(u'名称不能为空。')])
    number = StringField(u'班级编号', validators=[validators.input_required(u'名称不能为空。')]) # 班级编号
    desc = TextAreaField(u'简要描述')

    def __init__(self, *args, **kwargs):
        super(ClassForm, self).__init__(*args, **kwargs)
        division_choices = [(r.id, r.name) for r in Division.query.order_by(Division.name).all()]
        division_choices.insert(0, (0, u'请选择所属修学处'))
        self.division_id.choices = division_choices
        self.department = kwargs.get('obj')
        if self.department:
            self.division_id.default = self.department.division_id

    def validate_division_id(self, field):
        if field.data <= 0:
            raise ValidationError(u'请选择所属修学处。')

    def validate_name(self, field):
        if field.data != self.department.name and \
                Department.query.filter_by(name=field.data).first():
            raise ValidationError(u'修学点名称已存在。')
