# -*- coding:utf-8 -*-
from medos.extensions import db
from datetime import datetime


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer())
    wechat_id = db.Column(db.String(200))

    pass
