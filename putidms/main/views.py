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
@login_required
def counselor_search():
    query_str = '%' + request.form.get('query_str') + '%'
    rule = db.or_(Counselor.username.like(query_str), Counselor.religiousname.like(query_str), \
                  Counselor.email.like(query_str), Counselor.mobile.like(query_str))
    counselors = Counselor.query.filter(rule).filter_by(is_delete=0).order_by(Counselor.update_time.desc()).all()
    return render_template('main/counselor_list.html', counselors=counselors, query_str=request.form.get('query_str'))


@mod.route('/leadclass_list')
@login_required
def leadclass_list():
    lcrs = LeadClassRecord.query.order_by(LeadClassRecord.update_time.desc()).all()
    return render_template('main/leadclass_list.html', records=lcrs)


@mod.route('/leadclass/add/<int:cid>', methods=['GET', 'POST'])
@login_required
def leadclass_add(cid):
    form = LeadClassRecordForm()
    if form.validate_on_submit():
        c = Counselor.query.get_or_404(cid)
        r = LeadClassRecord()
        r.counselor_id = c.id
        r.lead_class_duty_id = form.lead_class_duty_id.data
        r.lead_class_id = form.lead_class_id.data
        r.from_date = form.from_date.data
        r.to_date = form.to_date.data
        db.session.add(r)
        db.session.commit()
        flash(u'带班记录添加成功。')
        return redirect(url_for('.leadclass_list', cid=cid))
    return render_template('main/leadclass_add.html', form=form, cid=cid)


@mod.route('/leadclass/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def leadclass_edit(id):
    r = LeadClassRecord.query.get_or_404(id)
    form = LeadClassRecordForm(obj=r)
    if form.validate_on_submit():
        form.populate_obj(r)
        db.session.add(r)
        db.session.commit()
        flash(u'带班记录编辑成功。')
        return redirect(url_for('.leadclass_list', cid=r.counselor_id))
    return render_template('main/leadclass_edit.html', form=form, record=r)


@mod.route('/leadclass/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def leadclass_delete():
    r = LeadClassRecord.query.get_or_404(id)
    db.session.remove(r)
    db.session.commit()
    flash(u'记录删除成功。')
    return redirect(url_for('.leadclass_list', cid=r.counselor_id))


@mod.route('/training/list')
@login_required
def training_list():
    r = TrainingRecord.query.order_by(TrainingRecord.update_time.desc()).all()
    return render_template('main/training_list.html', record=r)


@mod.route('/training/add/<int:cid>', methods=['GET', 'POST'])
@login_required
def training_add(cid):
    form = TrainingRecordForm()
    if form.validate_on_submit():
        c = Counselor.query.get_or_404(cid)
        r = TrainingRecord()
        r.training_name = form.training_name.data
        r.location = form.location.data
        r.content = form.content.data
        r.from_date = form.from_date.data
        r.to_date = form.to_date.data
        r.remark = form.remark.data
        r.counselor_id = c.id
        db.session.add(r)
        db.session.commit()
        flash(u'成功添加培训记录。')
        return redirect(url_for('.training_list', cid=c.id))
    return render_template('main/training_add.html', form=form)


@mod.route('/training/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def training_edit(id):
    r = TrainingRecord.query.get_or_404(id)
    form = TrainingRecordForm(obj=r)
    if form.validate_on_submit():
        form.populate_obj(r)
        db.session.add(r)
        db.session.commit()
        flash(u'编辑成功。')
        return redirect(url_for('.training_list', cid=r.counselor_id))
    return render_template('main/training_edit.html', form=form, record=r)


@mod.route('/training/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def training_delete(id):
    r = TrainingRecord.query.get_or_404(id)
    db.session.remove(r)
    db.session.commit()
    flash(u'删除成功。')
    return redirect(url_for('.training_list', cid=r.counselor_id))


@mod.route('/evaluation/list')
@login_required
def evaluation_list():
    r = EvaluationRecord.query.order_by(EvaluationRecord.update_time.desc()).all()
    return render_template('main/evaluation_list.html', record=r)


@mod.route('/evaluation/add/<int:cid>', methods=['GET', 'POST'])
@login_required
def evaluation_add(cid):
    form = EvaluationRecordForm()
    if form.validate_on_submit():
        r = EvaluationRecord()
        r.evaluation_item = form.evaluation_item.data
        r.evaluation_date = form.evaluation_date.data
        r.score = form.score.data
        db.session.add(r)
        db.session.commit()
        flash(u'添加成功。')
    return render_template('main/evaluation_add.html', form=form)


@mod.route('/evaluation/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def evaluation_edit(id):
    r = EvaluationRecord.query.get_or_404(id)
    form = EvaluationRecordForm(obj=r)
    if form.validate_on_submit():
        form.populate_obj(r)
        db.session.add(r)
        db.session.commit()
        flash(u'编辑成功。')
        return redirect(url_for('.evaluation_list', cid=r.counselor_id))
    return render_template('main/evaluation_edit.html', form=form, record=r)


@mod.route('/evaluation/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def evaluation_delete(id):
    r = EvaluationRecord.query.get_or_404(id)
    db.session.remove(r)
    db.session.commit()
    flash(u'删除成功。')
    return redirect(url_for('.evaluation_list', cid=r.counselor_id))
