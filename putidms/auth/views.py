# -*- coding:utf-8 -*-
from flask import Blueprint, request, render_template, redirect, url_for, flash
from .forms import LoginForm, UserForm
from putidms.models.user import User
from flask_login import login_user, logout_user, login_required
from putidms import db
from datetime import datetime

mod = Blueprint('auth', __name__)


@mod.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print '@'*100
    if form.validate_on_submit():
        print '*'*100
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.verify_password(form.password.data):
                login_user(user)
                user.update_login_info(request.remote_addr)
                flash(u'登陆成功！欢迎回来，%s!' % user.realname, 'success')
                return redirect(request.args.get('next') or url_for('main.index'))
            else:
                flash(u'密码不正确。', 'danger')
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


@mod.route('/user/list')
def user_list():
    users = User.query.all()
    return render_template('auth/user_list.html', users=users)


@mod.route('/user/add', methods=['GET', 'POST'])
def user_add():
    form = UserForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.password = form.password.data
        user.realname = form.realname.data
        user.email = form.email.data
        user.last_login_ip = request.remote_addr
        user.role=User.ADMIN
        db.session.add(user)
        db.session.commit()
        flash(u'新增用户成功！', 'success')
        return redirect(url_for('auth.user_list'))
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('auth/user_add.html', form=form)
