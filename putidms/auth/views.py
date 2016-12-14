# -*- coding:utf-8 -*-
from flask import Blueprint, request, render_template, redirect, url_for, flash
from .forms import LoginForm, UserForm
from putidms.models.user import User, Role
from flask_login import login_user, logout_user, login_required, current_user
from putidms import db
from datetime import datetime

mod = Blueprint('auth', __name__)


@mod.route('/login', methods=['GET', 'POST'])
def login():
    return_url = request.args.get("next") or request.form.get("next")
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.verify_password(form.password.data):
                login_user(user)
                user.update_login_info(request.remote_addr)
                flash(u'登陆成功！欢迎回来，%s!' % user.realname, 'success')
                return redirect(return_url or url_for('main.index'))
            else:
                flash(u'密码不正确。', 'danger')
        else:
            flash(u'用户不存在。', 'danger')
    if form.errors:
        flash(u'登陆失败，请尝试重新登陆.', 'danger')
    return render_template('auth/login.html', form=form, next=return_url)


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
    user = User()
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.password = form.password.data
        user.realname = form.realname.data
        user.email = form.email.data
        user.role = Role.query.get(form.role_id.data)
        user.create_time = datetime.utcnow()
        user.last_login_time = datetime.utcnow()
        user.last_login_ip = request.remote_addr
        db.session.add(user)
        db.session.commit()
        flash(u'新增用户成功！', 'success')
        return redirect(url_for('auth.user_list'))
    return render_template('auth/user_add.html', form=form)


@mod.route('/user/edit/<int:id>', methods=['GET', 'POST'])
def user_edit(id):
    user = User.query.get(id)
    form = UserForm(obj=user)
    del form.password
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        flash(u'编辑用户 %s 成功！' % user.realname, 'success')
        return redirect(url_for('auth.user_list'))
    return render_template('auth/user_edit.html', form=form, user=user)


@mod.route('/user/delete/<int:id>', methods=['GET'])
@login_required
def user_delete(id):
    user = User.query.get(id)
    user.is_delete = 1
    user.update_user = current_user.id
    db.session.add(user)
    db.session.commit()
    flash(u'删除用户 %s 成功！' % user.realname, 'success')
    return redirect(url_for('auth.user_list'))
