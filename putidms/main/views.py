# -*- coding:utf-8 -*-
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import datetime

mod = Blueprint('main', __name__)


@mod.route('/')
@mod.route('/index')
def index():
    return render_template('main/index.html')
