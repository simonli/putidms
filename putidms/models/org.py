# -*- coding:utf-8 -*-
from putidms import db
from datetime import datetime

class StudyDiv(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(255), index=True,unique=True,nullable=False)
    desc = db.Column(db.Text)
    create_time = db.Column(db.DateTime,default=datetime.utcfromtimestamp)
