# -*- coding:utf-8 -*-
from __future__ import with_statement
from flask import Blueprint
from datetime import datetime


mod = Blueprint('account', __name__)


@mod.route('/')
def home():
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('count.txt','a+') as fp:
        fp.write(date_str+"\n")
    return 'Hello World. - %s' % date_str+"....."