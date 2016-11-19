# -*- coding:utf-8 -*-
from __future__ import with_statement
from flask import Blueprint, request, render_template, redirect, url_for, flash
import datetime

mod = Blueprint('main', __name__)


@mod.route('/')
@mod.route('/index')
def index():
    return datetime.datetime.now()
