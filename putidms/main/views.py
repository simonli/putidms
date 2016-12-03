# -*- coding:utf-8 -*-
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import datetime
from .forms import CounselorForm, LeadClassRecordForm, TrainingRecordForm, EvaluationRecordForm
from putidms.models.counselor import Counselor, LeadClassRecord, TrainingRecord, EvaluationRecord
from putidms.models.org import Class, Duty
from flask_login import current_user
from putidms import db

mod = Blueprint('main', __name__)


@mod.route('/')
@mod.route('/index')
def index():
    return render_template('main/index.html')


@mod.route('/counselor/list')
def counselor_list():
    counselors = Counselor.query.filter_by(is_delete=0).order_by(Counselor.update_time.desc()).all()
    return render_template('main/counselor_list.html', counselors=counselors)


@mod.route('/counselor/add', methods=['GET', 'POST'])
def counselor_add():
    form = CounselorForm()
    if form.validate_on_submit():
        c = Counselor()
        c.username = form.username.data
        c.religiousname = form.religiousname.data
        c.gender = form.gender.data
        c.birthday = form.birthday.data
        c.mobile = form.mobile.data
        c.email = form.email.data
        c.cls = Class.query.get(form.class_id.data)  # 班级
        c.duty = Duty.query.get(form.duty_id.data)
        c.create_user = current_user.id
        db.session.add(c)
        db.session.commit()
        flash(u'成功添加辅导/助员：%s' % c.username, 'success')
        return redirect(url_for('.counselor_list'))
    return render_template('main/counselor_add.html', form=form)


@mod.route('/counselor/edit/<int:id>', methods=['GET', 'POST'])
def counselor_edit(id):
    c = Counselor.query.get(id)
    form = CounselorForm(obj=c)
    if form.validate_on_submit():
        form.populate_obj(c)
        db.session.add(c)
        db.session.commit()
        flash(u'成功编辑辅导/助员: %s' % c.username, 'success')
        return redirect(url_for('.counselor_list'))
    return render_template('main/counselor_edit.html', form=form, counselor=c)


@mod.route('/counselor/delete/<int:id>')
def counselor_delete(id):
    c = Counselor.query.get(id)
    c.is_delete = 1
    db.session.add(c)
    db.session.commit()
    flash(u'成功删除辅导/助员：%s' % c.username, 'success')
    return redirect(url_for('.counselor_list'))


@mod.route('/counselor/query/<string:querystr>')
def counselor(querystr):
    pass
