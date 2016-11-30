# -*- coding:utf-8 -*-
from flask import Blueprint, request, render_template, redirect, url_for, flash
from putidms.models.org import Division, Department, Class
from putidms import db
from putidms.decorators import admin_required
from putidms.admin.forms import DivisionForm, DepartmentForm, ClassForm
from flask_login import current_user

mod = Blueprint('admin', __name__)


@mod.route('/divsion/add', methods=['GET', 'POST'])
def division_add():
    form = DivisionForm()
    if form.validate_on_submit():
        div = Division()
        div.name = form.name.data
        div.desc = form.desc.data
        div.update_user = current_user.id
        db.session.add(div)
        db.session.commit()
        flash(u'成功添加修学处: %s!' % div.name, 'success')
        return redirect(url_for('admin.division_list'))
    return render_template('admin/division_add.html', form=form)

@mod.route('/divsion/edit/<int:id>', methods=['GET', 'POST'])
def division_edit(id):
    div = Division.query.get(id)
    form = DivisionForm(obj=div)
    if form.validate_on_submit():
        form.populate_obj(div)
        db.session.add(div)
        db.session.commit()
        flash(u'修学处 %s 编辑成功！' % div.name, 'success')
        return redirect(url_for('admin.division_list'))
    return render_template('admin/division_edit.html',form=form, div=div)


@mod.route('/department/add', methods=['GET', 'POST'])
def division_add():
    form = DepartmentForm()
    if form.validate_on_submit():
        dept = Department()
        dept.name = form.name.data
        dept.desc = form.desc.data
        dept.update_user = current_user.id
        db.session.add(dept)
        db.session.commit()
        flash(u'成功添加修学点: %s!' % dept.name, 'success')
        return redirect(url_for('admin.department_list'))
    return render_template('admin/department_add.html', form=form)

@mod.route('/divsion/edit/<int:id>', methods=['GET', 'POST'])
def division_edit(id):
    div = Division.query.get(id)
    form = DivisionForm(obj=div)
    if form.validate_on_submit():
        form.populate_obj(div)
        db.session.add(div)
        db.session.commit()
        flash(u'修学处 %s 编辑成功！' % div.name, 'success')
        return redirect(url_for('admin.division_list'))
    return render_template('admin/division_edit.html',form=form, div=div)


@mod.route('/divsion/add', methods=['GET', 'POST'])
def division_add():
    form = DivisionForm()
    if form.validate_on_submit():
        div = Division()
        div.name = form.name.data
        div.desc = form.desc.data
        div.update_user = current_user.id
        db.session.add(div)
        db.session.commit()
        flash(u'成功添加修学处: %s!' % div.name, 'success')
        return redirect(url_for('admin.division_list'))
    return render_template('admin/division_add.html', form=form)

@mod.route('/divsion/edit/<int:id>', methods=['GET', 'POST'])
def division_edit(id):
    div = Division.query.get(id)
    form = DivisionForm(obj=div)
    if form.validate_on_submit():
        form.populate_obj(div)
        db.session.add(div)
        db.session.commit()
        flash(u'修学处 %s 编辑成功！' % div.name, 'success')
        return redirect(url_for('admin.division_list'))
    return render_template('admin/division_edit.html',form=form, div=div)