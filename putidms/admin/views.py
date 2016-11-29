# -*- coding:utf-8 -*-
from flask import Blueprint, request, render_template, redirect, url_for, flash
from putidms.models import User
from flask_login import login_user, logout_user, login_required
from putidms import db

mod = Blueprint('admin', __name__)