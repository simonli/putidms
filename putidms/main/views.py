# -*- coding:utf-8 -*-
from flask import current_app, Blueprint, request, render_template, redirect, url_for, flash, jsonify
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
    page = request.args.get('page', 1, type=int)
    pagination = Counselor.query.filter_by(is_delete=0).order_by(Counselor.update_time.desc()) \
        .paginate(page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False)
    counselors = pagination.items
    return render_template('main/counselor_list.html', counselors=counselors, pagination=pagination,
                           endpoint='.counselor_list')


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
        c.class_ = Class.query.get(form.class_id.data)  # 班级
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


@mod.route('/counselor/search', methods=['GET', 'POST'])
@login_required
def counselor_search():
    page = request.args.get('page', 1, type=int)
    cid = request.args.get('cid')
    if cid:
        keyword = int(cid)
        pagination = Counselor.query.filter_by(id=keyword).filter_by(is_delete=0).order_by(
            Counselor.update_time.desc()).paginate(page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False)
    else:
        keyword = request.form.get('keyword', '')
        query_str = '%' + keyword + '%'
        rule = db.or_(Counselor.id == query_str, Counselor.username.like(query_str),
                      Counselor.religiousname.like(query_str), \
                      Counselor.email.like(query_str), Counselor.mobile.like(query_str))
        pagination = Counselor.query.filter(rule).filter_by(is_delete=0).order_by(Counselor.update_time.desc()) \
            .paginate(page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False)
    counselors = pagination.items
    return render_template('main/counselor_list.html', counselors=counselors, keyword=keyword, pagination=pagination,
                           endpoint='.counselor_search')


@mod.route('/leadclass/list/<int:cid>')
@login_required
def leadclass_list(cid):
    page = request.args.get('page', 1, type=int)
    pagination = LeadClassRecord.query.filter_by(counselor_id=cid).order_by(LeadClassRecord.update_time.desc()) \
        .paginate(page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False)
    records = pagination.items
    return render_template('main/leadclass_list.html', records=records, pagination=pagination,
                           endpoint='.leadclass_list')


@mod.route('/leadclass/add/<int:cid>', methods=['GET', 'POST'])
@login_required
def leadclass_add(cid):
    c = Counselor.query.get(cid)
    if c is None:
        flash(u'该位辅导员/辅助员不存在。', 'danger')
        return redirect(url_for('.index'))
    form = LeadClassRecordForm()
    if form.validate_on_submit():
        r = LeadClassRecord()
        r.counselor_id = c.id
        r.duty_id = form.duty_id.data
        r.class_id = form.class_id.data
        r.from_date = form.from_date.data
        r.to_date = form.to_date.data
        db.session.add(r)
        db.session.commit()
        flash(u'带班记录添加成功。', 'success')
        return redirect(url_for('.leadclass_list', cid=cid))
    return render_template('main/leadclass_add.html', form=form, counselor=c)


@mod.route('/leadclass/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def leadclass_edit(id):
    r = LeadClassRecord.query.get_or_404(id)
    setattr(r, 'division_id', r.class_.department.division_id)
    setattr(r, 'department_id', r.class_.department_id)
    form = LeadClassRecordForm(obj=r)
    if form.validate_on_submit():
        form.populate_obj(r)
        db.session.add(r)
        db.session.commit()
        flash(u'带班记录编辑成功。', 'success')
        return redirect(url_for('.leadclass_list', cid=r.counselor_id))
    return render_template('main/leadclass_edit.html', form=form, record=r)


@mod.route('/leadclass/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def leadclass_delete():
    r = LeadClassRecord.query.get_or_404(id)
    db.session.remove(r)
    db.session.commit()
    flash(u'记录删除成功。', 'success')
    return redirect(url_for('.leadclass_list', cid=r.counselor_id))


@mod.route('/training/list/<int:cid>')
@login_required
def training_list(cid):
    page = request.args.get('page', 1, type=int)
    pagination = TrainingRecord.query.filter_by(counselor_id=cid).order_by(TrainingRecord.update_time.desc()) \
        .paginate(page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False)
    records = pagination.items
    return render_template('main/training_list.html', records=records, pagination=pagination, endpoint='.training_list')


@mod.route('/training/add/<int:cid>', methods=['GET', 'POST'])
@login_required
def training_add(cid):
    c = Counselor.query.get(cid)
    if c is None:
        flash(u'该位辅导员/辅助员不存在。', 'danger')
        return redirect(url_for('.index'))
    form = TrainingRecordForm()
    if form.validate_on_submit():
        r = TrainingRecord()
        r.counselor_id = cid
        r.name = form.name.data
        r.location = form.location.data
        r.content = form.content.data
        r.from_date = form.from_date.data
        r.to_date = form.to_date.data
        r.remark = form.remark.data
        r.counselor_id = c.id
        db.session.add(r)
        db.session.commit()
        flash(u'成功添加培训记录。', 'success')
        return redirect(url_for('.training_list', cid=c.id))
    return render_template('main/training_add.html', form=form, counselor=c)


@mod.route('/training/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def training_edit(id):
    r = TrainingRecord.query.get_or_404(id)
    form = TrainingRecordForm(obj=r)
    if form.validate_on_submit():
        form.populate_obj(r)
        db.session.add(r)
        db.session.commit()
        flash(u'编辑成功。', 'success')
        return redirect(url_for('.training_list', cid=r.counselor_id))
    return render_template('main/training_edit.html', form=form, record=r)


@mod.route('/training/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def training_delete(id):
    r = TrainingRecord.query.get_or_404(id)
    db.session.remove(r)
    db.session.commit()
    flash(u'删除成功。', 'success')
    return redirect(url_for('.training_list', cid=r.counselor_id))


@mod.route('/evaluation/list/<int:cid>')
@login_required
def evaluation_list(cid):
    page = request.args.get('page', 1, type=int)
    pagination = EvaluationRecord.query.filter_by(counselor_id=cid).order_by(EvaluationRecord.update_time.desc()) \
        .paginate(page, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False)
    records = pagination.items
    return render_template('main/evaluation_list.html', records=records, pagination=pagination,
                           endpoint='.evaluation_list')


@mod.route('/evaluation/add/<int:cid>', methods=['GET', 'POST'])
@login_required
def evaluation_add(cid):
    c = Counselor.query.get(cid)
    if c is None:
        flash(u'该位辅导员/辅助员不存在。', 'danger')
        return redirect(url_for('.index'))
    form = EvaluationRecordForm()
    if form.validate_on_submit():
        r = EvaluationRecord()
        r.counselor = c
        r.item = form.item.data
        r.shiftdate = form.shiftdate.data
        r.score = form.score.data
        db.session.add(r)
        db.session.commit()
        flash(u'添加成功。', 'success')
        return redirect(url_for('.evaluation_list', cid=c.id))
    return render_template('main/evaluation_add.html', form=form, counselor=c)


@mod.route('/evaluation/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def evaluation_edit(id):
    r = EvaluationRecord.query.get_or_404(id)
    form = EvaluationRecordForm(obj=r)
    if form.validate_on_submit():
        form.populate_obj(r)
        db.session.add(r)
        db.session.commit()
        flash(u'编辑成功。', 'success')
        return redirect(url_for('.evaluation_list', cid=r.counselor_id))
    return render_template('main/evaluation_edit.html', form=form, record=r)


@mod.route('/evaluation/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def evaluation_delete(id):
    r = EvaluationRecord.query.get_or_404(id)
    db.session.remove(r)
    db.session.commit()
    flash(u'删除成功。', 'success')
    return redirect(url_for('.evaluation_list', cid=r.counselor_id))
