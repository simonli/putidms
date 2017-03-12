# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, ValidationError
from wtforms.validators import input_required as ir

from putidms.extensions import MySelectField
from putidms.models.org import Division, Department, Class, Duty


class DivisionForm(FlaskForm):
    name = StringField(u'修学处名称', validators=[ir(u'名称不能为空。')])
    desc = TextAreaField(u'简要描述')
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(DivisionForm, self).__init__(*args, **kwargs)
        self.division = kwargs.get('obj')

    def validate_name(self, field):
        if field.data != self.division.name and \
                Division.query.filter_by(name=field.data).first():
            raise ValidationError(u'修学处名称已存在。')


class DepartmentForm(FlaskForm):
    division_id = MySelectField(u'所属修学处', coerce=int)
    name = StringField(u'修学点名称', validators=[ir(u'名称不能为空。')])
    desc = TextAreaField(u'简要描述')
    submit = SubmitField(u'提交')

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
        if self.department:
            if field.data != self.department.name and \
                    Department.query.filter_by(name=field.data).first():
                raise ValidationError(u'修学点名称已存在。')
        else:
            if Department.query.filter_by(name=field.data).first():
                raise ValidationError(u'修学点名称已存在。')


class ClassForm(FlaskForm):
    division_id = MySelectField(u'所属修学处', coerce=int)
    department_id = MySelectField(u'所属修学点', coerce=int)
    name = StringField(u'班级名称', validators=[ir(u'名称不能为空。')])
    number = StringField(u'班级编号', validators=[ir(u'班级编号不能为空。')])  # 班级编号
    desc = TextAreaField(u'简要描述')
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(ClassForm, self).__init__(*args, **kwargs)
        self.class_ = kwargs.get('obj')

        division_choices = [(r.id, r.name) for r in Division.query.all()]
        division_choices.insert(0, (0, u'请选择所属修学处'))
        self.division_id.choices = division_choices

        if self.class_:
            dept_choices = [(r.id, r.name) for r in Department.query \
                .filter_by(division_id=self.division_id.data).all()]
        else:
            dept_choices = [(r.id, r.name) for r in Department.query.all()]
        dept_choices.insert(0, (0, u'请选择所属修学点'))
        self.department_id.choices = dept_choices

        if self.class_:
            self.department_id.default = self.class_.department_id
            self.division_id.default = self.class_.department.division_id

    def validate_division_id(self, field):
        if field.data <= 0:
            raise ValidationError(u'请选择所属修学处。')

    def validate_department_id(self, field):
        if field.data <= 0:
            raise ValidationError(u'请选择所属修学点。')

    def validate_name(self, field):
        if self.class_:
            if field.data != self.class_.name and \
                    Class.query.filter_by(name=field.data).first():
                raise ValidationError(u'班级名称已存在。')
        else:
            if Class.query.filter_by(name=field.data).first():
                raise ValidationError(u'班级名称已存在。')

    def validate_number(self, field):
        if self.class_:
            if field.data != self.class_.number and \
                    Class.query.filter_by(number=field.data).first():
                raise ValidationError(u'班级编号已存在。')
        else:
            if Class.query.filter_by(number=field.data).first():
                raise ValidationError(u'班级编号已存在。')


class DutyForm(FlaskForm):
    name = StringField(u'岗位名称', validators=[ir(u'名称不能为空。')])
    desc = TextAreaField(u'简要描述')
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(DutyForm, self).__init__(*args, **kwargs)
        self.duty = kwargs.get('obj')

    def validate_name(self, field):
        if field.data != self.duty.name and \
                Duty.query.filter_by(name=field.data).first():
            raise ValidationError(u'岗位名称已存在。')
