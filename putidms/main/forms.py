# -*- coding:utf-8 -*-
from wtforms import StringField, TextAreaField, validators, SelectField, ValidationError
from flask_wtf import FlaskForm
from putidms.models.counselor import Counselor, LeadClassRecord, TrainingRecord, EvaluationRecord

class CounselorForm(FlaskForm):
    pass

