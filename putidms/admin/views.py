# -*- coding:utf-8 -*-
from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from putidms.models.org import Division, Department, Class, Duty
from putidms import db
from putidms.decorators import admin_required
from putidms.admin.forms import DivisionForm, DepartmentForm, ClassForm, DutyForm
from flask_login import current_user, login_required

mod = Blueprint('admin', __name__)


@mod.route('/_add_numbers', methods=['POST'])
def _add_numbers():
    a = request.form.get('a', 0, type=int)
    b = request.form.get('b', 0, type=int)
    return jsonify(d=a * b)


@mod.route('/division/list')
@login_required
@admin_required
def division_list():
    divs = Division.query.all()
    return render_template('admin/division_list.html', divs=divs)


@mod.route('/division/add', methods=['GET', 'POST'])
@login_required
@admin_required
def division_add():
    div = Division()
    form = DivisionForm(obj=div)
    if form.validate_on_submit():
        div.name = form.name.data
        div.desc = form.desc.data
        div.update_user = current_user.id
        db.session.add(div)
        db.session.commit()
        flash(u'成功添加修学处: %s!' % div.name, 'success')
        return redirect(url_for('admin.division_list'))
    return render_template('admin/division_add.html', form=form)


@mod.route('/division/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def division_edit(id):
    div = Division.query.get_or_404(id)
    form = DivisionForm(obj=div)
    if form.validate_on_submit():
        form.populate_obj(div)
        db.session.add(div)
        db.session.commit()
        flash(u'修学处 %s 编辑成功！' % div.name, 'success')
        return redirect(url_for('admin.division_list'))
    return render_template('admin/division_edit.html', form=form, div=div)


@mod.route('/division/delete/<int:id>', methods=['GET'])
@admin_required
def division_delete(id):
    pass


@mod.route('/department/list')
@admin_required
def department_list():
    depts = Department.query.all()
    return render_template('admin/department_list.html', depts=depts)


@mod.route('/department/add', methods=['GET', 'POST'])
@admin_required
def department_add():
    form = DepartmentForm()
    if form.validate_on_submit():
        dept = Department()
        dept.name = form.name.data
        dept.desc = form.desc.data
        dept.division = Division.query.get(form.division_id.data)
        dept.update_user = current_user.id
        db.session.add(dept)
        db.session.commit()
        flash(u'成功添加修学点: %s!' % dept.name, 'success')
        return redirect(url_for('admin.department_list'))
    return render_template('admin/department_add.html', form=form)


@mod.route('/department/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def department_edit(id):
    dept = Department.query.get_or_404(id)
    form = DepartmentForm(obj=dept)
    if form.validate_on_submit():
        form.populate_obj(dept)
        db.session.add(dept)
        db.session.commit()
        flash(u'修学点 %s 编辑成功！' % dept.name, 'success')
        return redirect(url_for('admin.department_list'))
    return render_template('admin/department_edit.html', form=form, dept=dept)


@mod.route('/department/delete/<int:id>', methods=['GET'])
@admin_required
def department_delete(id):
    pass


@mod.route('/class/list')
@admin_required
def class_list():
    classes = Class.query.all()
    return render_template('admin/class_list.html', classes=classes)


@mod.route('/class/add', methods=['GET', 'POST'])
def class_add():
    form = ClassForm()
    if form.validate_on_submit():
        c = Class()
        c.name = form.name.data
        c.desc = form.desc.data
        c.number = form.number.data
        c.department = Department.query.get(form.department_id.data)
        c.update_user = current_user.id
        db.session.add(c)
        db.session.commit()
        flash(u'成功添加班级: <b>%s - %s - %s</b>' % (c.department.division.name, c.department.name, c.name), 'success')
        return redirect(url_for('admin.class_list'))
    return render_template('admin/class_add.html', form=form)


@mod.route('/class/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def class_edit(id):
    c = Class.query.get(id)
    form = DivisionForm(obj=c)
    if form.validate_on_submit():
        form.populate_obj(c)
        db.session.add(c)
        db.session.commit()
        flash(u'班级 %s 编辑成功！' % c.name, 'success')
        return redirect(url_for('admin.class_list'))
    return render_template('admin/class_edit.html', form=form, cls=c)


@mod.route('/duty/list')
@admin_required
def duty_list():
    duties = Duty.query.all()
    return render_template('admin/duty_list.html', duties=duties)


@mod.route('/duty/add', methods=['GET', 'POST'])
@admin_required
def duty_add():
    form = DutyForm()
    if form.validate_on_submit():
        duty = Duty()
        duty.name = form.name.data
        duty.desc = form.desc.data
        duty.update_user = current_user.id
        db.session.add(duty)
        db.session.commit()
        flash(u'成功添加岗位: %s!' % duty.name, 'success')
        return redirect(url_for('admin.duty_list'))
    return render_template('admin/duty_add.html', form=form)


@mod.route('/duty/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def duty_edit(id):
    duty = Duty.query.get(id)
    form = DivisionForm(obj=duty)
    if form.validate_on_submit():
        form.populate_obj(duty)
        db.session.add(duty)
        db.session.commit()
        flash(u'岗位 %s 编辑成功！' % duty.name, 'success')
        return redirect(url_for('admin.duty_list'))
    return render_template('admin/duty_edit.html', form=form, duty=duty)


@mod.route('/_get_departments', methods=['POST'])
def _department_query():
    division_id = request.form.get('division_id', 0, type=int)
    depts = Department.query.filter_by(division_id=division_id).all()
    return jsonify(result=[d.to_json() for d in depts])


@mod.route('/_get_classes', methods=['POST'])
def _class_query():
    dept_id = request.form.get('department_id', 0, type=int)
    classes = Class.query.filter_by(department_id=dept_id).all()
    return jsonify(result=[c.to_json() for c in classes])
