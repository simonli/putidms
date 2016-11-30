# -*- coding:utf-8 -*-
from putidms import db
from datetime import datetime


class Duty(db.Model):
    __tablename__ = 'duties'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False, index=True, unique=True)
    desc = db.Column(db.String(255))
    create_time = db.Column(db.DateTime)
    update_user = db.Column(db.Integer)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)
    counselors = db.relationship('Counselor', backref='duty', lazy='dynamic')

    @staticmethod
    def insert_duties():
        duties = {
            u'辅导员': (u'岗位：辅导员',),
            u'实习辅导员': (u'岗位：辅导员',),
            u'辅助员': (u'岗位：辅助员',)
        }
        for r in duties:
            duty = Duty.query.filter_by(name=r).first()
            if duty is None:
                duty = Duty(name=r)
            duty.desc = duty[r][0]
            duty.create_time = datetime.utcnow()
            duty.update_user = 'liq'
            duty.update_time = datetime.utcnow()
            db.session.add(duty)
        db.session.commit()


class Counselor(db.Model):
    __tablename__ = 'counselors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, index=True, unique=True)
    religiousname = db.Column(db.String(100))
    realname = db.Column(db.String(100))
    gender = db.Column(db.String(50))
    birthday = db.Column(db.Date)
    mobile = db.Column(db.String(50))
    email = db.Column(db.String(100))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    duty_id = db.Column(db.Integer, db.ForeignKey('duties.id'))  # 岗位
    create_time = db.Column(db.DateTime)
    update_user = db.Column(db.Integer)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)
    lead_class_records = db.relationship('LeadClassRecord', backref='counselor', lazy='dynamic')

    def __repr__(self):
        return '<Counselor %r>' % self.username if self.religiousname is None else self.religiousname


class LeadClassRecord(db.Model):
    __tablename__ = 'lead_class_records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    counselor_id = db.Column(db.Integer, db.ForeignKey('counselors.id'))
    date_start = db.Column(db.Date)
    date_end = db.Column(db.Date)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    current_duty_id = db.Column(db.Integer, db.ForeignKey('duties.id'))
    create_time = db.Column(db.DateTime)
    update_user = db.Column(db.Integer)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)


class TrainingRecord(db.Model):
    __tablename__ = 'training_records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    training_name = db.Column(db.String(255), nullable=False)
    locatiion = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    remark = db.Column(db.Text)
    counselor_id = db.Column(db.Integer, db.ForeignKey('counselors.id'))
    date_start = db.Column(db.Date)
    date_end = db.Column(db.Date)
    current_duty_id = db.Column(db.Integer, db.ForeignKey('duties.id'))
    create_time = db.Column(db.DateTime)
    update_user = db.Column(db.Integer)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)


class EvaluationRecord(db.Model):
    __tablename__ = 'evaluation_records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    evaluation_item = db.Column(db.String(255), nullable=False, index=True)
    evaluation_date = db.Column(db.Date, nullable=False)
    score = db.Column(db.String(100))
    counselor_id = db.Column(db.Integer, db.ForeignKey('counselors.id'))
    current_duty_id = db.Column(db.Integer, db.ForeignKey('duties.id'))
    create_time = db.Column(db.DateTime)
    update_user = db.Column(db.Integer)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)
