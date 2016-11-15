# -*- coding:utf-8 -*-
from __future__ import with_statement
from flask import Blueprint, request, render_template
from datetime import datetime

mod = Blueprint('home', __name__)


@mod.route('/')
def home():
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('D:/count.txt', 'a+') as fp:
        fp.write(date_str + "\n")
    return 'Hello World. - %s' % date_str


@mod.route('/test')
def test():
    return 'Hello World. testing'


@mod.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pass
    return render_template('login.html')
