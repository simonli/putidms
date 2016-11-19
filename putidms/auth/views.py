# -*- coding:utf-8 -*-
from __future__ import with_statement
from flask import Blueprint, request, render_template, redirect, url_for, flash
from .forms import LoginForm
from putidms.models.user import User
from flask_login import login_user, logout_user, login_required

mod = Blueprint('auth', __name__)


@mod.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.verify_password(form.password.data):
                login_user(user)  # Flask-Login login_user
                flash(u'登陆成功！欢迎回来，%s!' % user.username, 'success')
                return redirect(request.args.get('next') or url_for('main.index'))
            else:
                flash('密码不正确。', 'danger')
        else:
            flash(u'用户不存在。', 'danger')
    if form.errors:
        flash(u'登陆失败，请尝试重新登陆.', 'danger')
    return render_template('auth/login.html', form=form)


@mod.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'您已退出登陆。', 'success')
    return redirect(url_for('main.index'))
