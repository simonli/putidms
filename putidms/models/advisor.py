# -*- coding:utf-8 -*-
from putidms import db
from datetime import datetime


class Advisor(db.Model):
    __tablename__ = 'advisors'
    JOB_TYPES = {
        'A': u'辅导员',  # Advisor -> 辅导员
        'AA': u'辅助员',  # AssistantAdvisor -> 辅助员
        'IA': u'实习辅导员'  # InternshipAdvisor -> 实习辅导员
    }
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, index=True, unique=True)
    religiousname = db.Column(db.String(100))
    realname = db.Column(db.String(100))
    gender = db.Column(db.String(50))
    birthday = db.Column(db.Date)
    mobile = db.Column(db.String(50))
    email = db.Column(db.String(100))
    study_division = db.Column(db.String(255))
    study_department = db.Column(db.String(255))
    class_number = db.Column(db.String(100))
    job_type = db.Column(db.String(50), default='A')
    create_time = db.Column(db.DateTime)
    update_user = db.Column(db.String(100))
    update_time = db.Column(db.DateTime, default=datetime.utcnow)
