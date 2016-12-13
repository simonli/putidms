# -*- coding:utf-8 -*-
from putidms import db
from datetime import datetime


class Counselor(db.Model):
    __tablename__ = 'counselors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, index=True)
    religiousname = db.Column(db.String(100))
    gender = db.Column(db.String(50))
    birthday = db.Column(db.Date)
    mobile = db.Column(db.String(50))
    email = db.Column(db.String(100))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    duty_id = db.Column(db.Integer, db.ForeignKey('duties.id'))  # 岗位
    is_delete = db.Column(db.Integer, default=0)
    create_user = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    update_user = db.Column(db.Integer)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)
    lead_class_records = db.relationship('LeadClassRecord', backref='counselor', lazy='dynamic')
    training_records = db.relationship('TrainingRecord', backref='counselor', lazy='dynamic')
    evaluation_records = db.relationship('EvaluationRecord', backref='counselor', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super(Counselor, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Counselor %r>' % self.username if self.religiousname is None else self.religiousname


class LeadClassRecord(db.Model):
    __tablename__ = 'lead_class_records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    from_date = db.Column(db.Date)
    to_date = db.Column(db.Date)
    counselor_id = db.Column(db.Integer, db.ForeignKey('counselors.id'))
    lead_class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    lead_class_duty_id = db.Column(db.Integer, db.ForeignKey('duties.id'))
    update_user = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super(LeadClassRecord, self).__init__(*args, **kwargs)


class TrainingRecord(db.Model):
    __tablename__ = 'training_records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    training_name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    remark = db.Column(db.Text)
    from_date = db.Column(db.Date)
    to_date = db.Column(db.Date)
    counselor_id = db.Column(db.Integer, db.ForeignKey('counselors.id'))
    update_user = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super(TrainingRecord, self).__init__(*args, **kwargs)


class EvaluationRecord(db.Model):
    __tablename__ = 'evaluation_records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    evaluation_item = db.Column(db.String(255), nullable=False, index=True)
    evaluation_date = db.Column(db.Date, nullable=False)
    score = db.Column(db.Integer)
    counselor_id = db.Column(db.Integer, db.ForeignKey('counselors.id'))
    update_user = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super(EvaluationRecord, self).__init__(*args, **kwargs)
