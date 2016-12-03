# -*- coding:utf-8 -*-
from wtforms import StringField, TextAreaField, validators, SelectField, RadioField, DateField, IntegerField, \
    ValidationError
from flask_wtf import FlaskForm
from putidms.models.counselor import Counselor, LeadClassRecord, TrainingRecord, EvaluationRecord
from putidms.models.org import Division, Department, Class


class CounselorForm(FlaskForm):
    username = StringField(u'姓名', validators=[validators.input_required(u'姓名不能为空。')])
    religiousname = StringField(u'法名')
    gender = RadioField(u'性别', coerce=str, choices=[('M', u'男'), ('F', u'女')], validators=[])
    birthday = DateField(u'生日', format='%Y-%m-%d')
    mobile = StringField(u'手机', validators=[validators.input_required(u'手机不能为空。')])
    email = StringField(u'Email')
    division_id = SelectField(u'修学处', coerce=int)
    department_id = SelectField(u'修学点', coerce=int)
    class_id = SelectField(u'班级', coerce=int)
    duty_id = SelectField(u'岗位', coerce=int)

    def __init__(self, *args, **kwargs):
        super(CounselorForm).__init__(*args, **kwargs)

        division_choices = [(r.id, r.name) for r in Division.query.order_by(Division.name).all()]
        division_choices.insert(0, (0, u'请选择所属修学处'))
        self.division_id.choices = division_choices

        self.counselor = kwargs.get('obj')
        if self.counselor:
            self.class_id.choices.default = self.counselor.cls.id
            self.department_id.default = self.counselor.department.id
            self.division_id.choices.default = self.counselor.department.division.id


class LeadClassRecordForm(FlaskForm):
    lead_class_id = SelectField(u'所带班级', coerce=int)
    lead_class_duty_id = SelectField(u'带班岗位', coerce=int)
    from_date = DateField(u'开始时间', format='%Y-%m-%d', validators=[validators.input_required(u'开始时间不能为空。')])
    to_date = DateField(u'结束时间', format='%Y-%m-%d', validators=[validators.input_required(u'结束时间不能为空。')])


class TrainingRecordForm(FlaskForm):
    training_name = StringField(u'培训名称', validators=[validators.input_required(u'姓名不能为空。')])
    location = StringField(u'培训地点', validators=[validators.input_required(u'姓名不能为空。')])
    content = TextAreaField(u'培训内容')
    remark = TextAreaField(u'备注')
    from_date = DateField(u'开始时间', format='%Y-%m-%d', validators=[validators.input_required(u'开始时间不能为空。')])
    to_date = DateField(u'结束时间', format='%Y-%m-%d', validators=[validators.input_required(u'结束时间不能为空。')])


class EvaluationRecordForm(FlaskForm):
    evaluation_item = StringField(u'考核项目', validators=[validators.input_required(u'姓名不能为空。')])
    evaluation_date = DateField(u'考核日期', format='%Y-%m-%d', validators=[validators.input_required(u'开始时间不能为空。')])
    score = IntegerField(u'考核得分', validators=[validators.input_required(u'姓名不能为空。')])
