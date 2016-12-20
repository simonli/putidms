# -*- coding:utf-8 -*-
from datetime import datetime

from putidms import db


class Division(db.Model):
    __tablename__ = 'divisions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), index=True, unique=True, nullable=False)
    desc = db.Column(db.Text)
    update_user = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)
    departments = db.relationship('Department', backref='division', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super(Division, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Division %r>' % self.name


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), index=True, unique=True, nullable=False)
    desc = db.Column(db.Text)
    update_user = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)

    division_id = db.Column(db.Integer, db.ForeignKey('divisions.id'))
    classes = db.relationship('Class', backref='department', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super(Department, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Department %r>' % self.name

    def to_json(self):
        return {'id': self.id, 'name': self.name, 'desc': self.desc}


class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), index=True, unique=True, nullable=False)
    number = db.Column(db.String(255), unique=True, nullable=False, index=True)  # 班级编号
    desc = db.Column(db.Text)
    update_user = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    counselors = db.relationship('Counselor', backref='class_', lazy='dynamic')
    lead_class_records = db.relationship('LeadClassRecord', backref='class_', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super(Class, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<Class %r>' % self.name

    def to_json(self):
        return {'id': self.id, 'name': self.name, 'desc': self.desc, 'number': self.number}


class Duty(db.Model):
    __tablename__ = 'duties'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), index=True, unique=True, nullable=False)
    desc = db.Column(db.Text)
    update_user = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)
    counselors = db.relationship('Counselor', backref='duty', lazy='dynamic')
    lead_class_records = db.relationship('LeadClassRecord', backref='duty', lazy='dynamic')

    def __init__(self, *args, **kwargs):
        super(Duty, self).__init__(*args, **kwargs)

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
            duty.desc = duties[r][0]
            duty.create_time = datetime.utcnow()
            duty.update_time = datetime.utcnow()
            db.session.add(duty)
        db.session.commit()
