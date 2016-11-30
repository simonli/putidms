# -*- coding:utf-8 -*-
from putidms import db
from datetime import datetime


class Division(db.Model):
    __tablename__ = 'divisions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), index=True, unique=True, nullable=False)
    desc = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.utcfromtimestamp)
    departments = db.relationship('Department', backref='division', lazy='dynamic')
    update_user = db.Column(db.Integer)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Division %r>' % self.name


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    division_id = db.Column(db.Integer, db.ForeignKey('divisions.id'))
    name = db.Column(db.String(255), index=True, unique=True, nullable=False)
    desc = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    update_user = db.Column(db.Integer)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)
    counselors = db.relationship('Counselor', backref='department', lazy='dynamic')
    classes = db.relationship('Class', backref='department', lazy='dynamic')

    def __repr__(self):
        return '<Department %r>' % self.name


class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    name = db.Column(db.String(255), index=True, unique=True, nullable=False)
    number = db.Column(db.String(255), nullable=False, index=True) #班级编号
    desc = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    update_user = db.Column(db.Integer)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Class %r>' % self.name
