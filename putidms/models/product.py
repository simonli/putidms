# -*- coding:utf-8 -*-
from putidms.extensions import db
from datetime import datetime


class Product(db.Model):
    __tablename__='medos_product'
    __tablename__ = "medos_product"
    id = db.Column(db.String(50), primary_key=True, autoincrement=False)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    
    seller_id = db.Column(db.Integer, db.ForeignKey("seller.id"))
    image = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    count = db.Column(db.Integer, nullable=False, default=0)
    sale_count = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String, nullable=False, default='')
    addresses = db.relationship('Address', backref='product', lazy='dynamic')
    orders = db.relationship('Order', backref='product', lazy='dynamic')
    lm_user = db.Column(db.String, nullable=False)
    lm_time = db.Column(db.DateTime, nullable=False, default=datetime.now())


class ProductMeta(db.Model):
    __tablename__ = 'medos_productexpand'
    id = db.Column(db.Integer, primary_key=True)



