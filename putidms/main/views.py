# -*- coding:utf-8 -*-
from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from datetime import datetime
from .forms import CounselorForm, LeadClassRecordForm, TrainingRecordForm, EvaluationRecordForm
from putidms.models.counselor import Counselor, LeadClassRecord, TrainingRecord, EvaluationRecord
from putidms.models.org import Class, Duty
from flask_login import current_user
from putidms import db
from flask_login import login_required

mod = Blueprint('main', __name__)


@mod.route('/')
@mod.route('/index')
def index():
    return render_template('main/index.html')


@mod.route('/testing')
def main():
    return render_template('main/main.html')


@mod.route('/_add_numbers')
def _add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)


@mod.route('/counselor/list')
@login_required
def counselor_list():
    counselors = Counselor.query.filter_by(is_delete=0).order_by(Counselor.update_time.desc()).all()
    return render_template('main/counselor_list.html', counselors=counselors)


@mod.route('/counselor/add', methods=['GET', 'POST'])
@login_required
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
@login_required
def counselor_edit(id):
    c = Counselor.query.get_or_404(id)
    form = CounselorForm(obj=c)
    if form.validate_on_submit():
        form.populate_obj(c)
        db.session.add(c)
        db.session.commit()
        flash(u'成功编辑辅导/助员: %s' % c.username, 'success')
        return redirect(url_for('.counselor_list'))
    return render_template('main/counselor_edit.html', form=form, counselor=c)


@mod.route('/counselor/delete/<int:id>')
@login_required
def counselor_delete(id):
    c = Counselor.query.get(id)
    c.is_delete = 1
    db.session.add(c)
    db.session.commit()
    flash(u'成功删除辅导/助员：%s' % c.username, 'success')
    return redirect(url_for('.counselor_list'))


@mod.route('/counselor/search', methods=['POST'])
def counselor_search():
    query_str = '%' + request.form.get('query_str') + '%'
    rule = db.or_(Counselor.username.like(query_str), Counselor.religiousname.like(query_str), \
                  Counselor.email.like(query_str), Counselor.mobile.like(query_str))
    counselors = Counselor.query.filter(rule).filter_by(is_delete=0).order_by(Counselor.update_time.desc()).all()
    return render_template('main/counselor_list.html', counselors=counselors, query_str=request.form.get('query_str'))
