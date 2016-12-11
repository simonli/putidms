# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, IntegerField, SubmitField
from wtforms import ValidationError
from wtforms.validators import Regexp
from wtforms.validators import input_required as ir, email
from putidms import db
from putidms.models.counselor import Counselor
from putidms.models.org import Division, Department, Class, Duty


class CounselorForm(FlaskForm):
    username = StringField(u'姓名', validators=[ir(u'姓名不能为空。')])
    religiousname = StringField(u'法名')
    gender = SelectField(u'性别', coerce=str, choices=[('M', u'男'), ('F', u'女')], validators=[])
    birthday = DateField(u'生日', format='%Y-%m-%d', validators=[ir(u'生日不能为空。')])
    mobile = StringField(u'手机', validators=[ir(u'手机号码不能为空。'), Regexp('^1[34578]\d{9}$', message=u'手机号码格式不正确。')])
    email = StringField(u'Email', validators=[email(u'Email格式不正确')])
    division_id = SelectField(u'修学处', coerce=int)
    department_id = SelectField(u'修学点', coerce=int)
    class_id = SelectField(u'班级', coerce=int)
    duty_id = SelectField(u'岗位', coerce=int)
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(CounselorForm, self).__init__(*args, **kwargs)

        division_choices = [(r.id, r.name) for r in Division.query.order_by(Division.name).all()]
        division_choices.insert(0, (0, u'请选择所属修学处'))
        self.division_id.choices = division_choices

        department_choices = [(r.id, r.name) for r in Department.query.order_by(Department.name).all()]
        if self.division_id.data:
            department_choices = [(r.id, r.name) for r in
                                  Department.query.filter_by(division_id=self.division_id.data).order_by(
                                      Department.name).all()]
        department_choices.insert(0, (0, u'请选择所属修学点'))
        self.department_id.choices = department_choices

        class_choices = [(r.id, r.name) for r in Class.query.order_by(Class.name).all()]
        if self.department_id.data:
            class_choices = [(r.id, r.name) for r in
                             Class.query.filter_by(department_id=self.department_id.data).order_by(Class.name).all()]
        class_choices.insert(0, (0, u'请选择所属班级'))
        self.class_id.choices = class_choices

        duty_choices = [(r.id, r.name) for r in Duty.query.order_by(Duty.name).all()]
        duty_choices.insert(0, (0, u'请选择岗位'))
        self.duty_id.choices = duty_choices

        self.counselor = kwargs.get('obj')
        if self.counselor:
            self.class_id.default = self.counselor.class_id
            print '8'*100
            print self.counselor.cls.department_id
            print '9'*100
            self.department_id.default = 1#self.counselor.cls.department_id
            self.division_id.default = self.counselor.cls.department.division_id
            self.duty_id.default = self.counselor.duty_id

    def validate_division_id(self, field):
        if field.data <= 0:
            raise ValidationError(u'请选择修学处。')

    def validate_department_id(self, field):
        if field.data <= 0:
            raise ValidationError(u'请选择修学点')

    def validate_class_id(self, field):
        if field.data <= 0:
            raise ValidationError(u'请选择班级')

    def validate_duty_id(self, field):
        if field.data <= 0:
            raise ValidationError(u'请选择岗位')

    def validate_username(self, field):
        if self.counselor:
            pass
        else:
            cs = db.session.query(db.func.count(Counselor.username)).filter_by(username=self.username.data).filter_by(
                religiousname=self.religiousname.data).scalar()
            if cs > 0:
                raise ValidationError(u'用用户+法名 重复，请改变后重新提交')

    def validate_email(self, field):
        if self.counselor:
            if self.counselor.email != field.data and \
                    Counselor.query.filter_by(email=field.data).first():
                raise ValidationError(u'Email地址已存在。')
        else:
            if Counselor.query.filter_by(email=field.data).first():
                raise ValidationError(u'Email地址已存在。')


class LeadClassRecordForm(FlaskForm):
    lead_class_id = SelectField(u'所带班级', coerce=int)
    lead_class_duty_id = SelectField(u'带班岗位', coerce=int)
    from_date = DateField(u'开始时间', format='%Y-%m-%d', validators=[ir(u'开始时间不能为空。')])
    to_date = DateField(u'结束时间', format='%Y-%m-%d', validators=[ir(u'结束时间不能为空。')])
    submit = SubmitField(u'添加')


class TrainingRecordForm(FlaskForm):
    training_name = StringField(u'培训名称', validators=[ir(u'姓名不能为空。')])
    location = StringField(u'培训地点', validators=[ir(u'姓名不能为空。')])
    content = TextAreaField(u'培训内容')
    remark = TextAreaField(u'备注')
    from_date = DateField(u'开始时间', format='%Y-%m-%d', validators=[ir(u'开始时间不能为空。')])
    to_date = DateField(u'结束时间', format='%Y-%m-%d', validators=[ir(u'结束时间不能为空。')])
    submit = SubmitField(u'添加')


class EvaluationRecordForm(FlaskForm):
    evaluation_item = StringField(u'考核项目', validators=[ir(u'姓名不能为空。')])
    evaluation_date = DateField(u'考核日期', format='%Y-%m-%d', validators=[ir(u'开始时间不能为空。')])
    score = IntegerField(u'考核得分', validators=[ir(u'姓名不能为空。')])
    submit = SubmitField(u'添加')
