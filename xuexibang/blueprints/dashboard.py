#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Jinyang Shao'

'''
后台管理，主要负责 后台负责删除已经发布的问题，管理注册的用户
'''

from flask import render_template, Blueprint, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user

from xuexibang.main.forms import CategoryForm, AdminForm
from xuexibang.main.extensions import db
from xuexibang.main.utils import redirect_back
from database.models.model import UserInfo, Category
from xuexibang.main.utils import Page

import click


dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = AdminForm()
    if form.validate_on_submit():
        password = form.password.data
        new_admin = UserInfo(name=current_user.name, admin=True)
        new_admin.set_password(password)
        db.get_result({"function" : db.UPDATE_USER_PWD, "content": new_admin.to_dict()})
        flash("change the password success", "success")
    return render_template('dashboard/settings.html', form=form)


@dashboard_bp.route('/question/manage')
@login_required
def manage_questions():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['QUESTIONS_PER_PAGE']  # 每页显示的数量
    ret = db.get_result(
        {"function": db.GET_RECOMMEND_QUESTION, "content": {"number": per_page, "start": per_page * (page - 1)}})
    if ret["content"]:
        page_record = Page(page, per_page)
        if page <= 1:
            page_record.has_prev = False
        else:
            page_record.has_prev = True
        if len(ret["content"]) < per_page:
            page_record.is_last = True
    else:  # 啥都没有，说明最后了
        page_record = Page(page, per_page, True)
        page_record.has_prev = True
        page_record.is_last = True
    questions = ret["content"]
    return render_template('dashboard/manage_questions.html', questions=questions, page=page_record)


@dashboard_bp.route('/question/<int:question_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_questions(question_id):
    db.get_result({"function" : db.DELETE_QUESTION_BY_ID,
                   "content" : {"quid" : question_id}})
    flash('Question deleted.', 'success')
    return redirect_back()


@dashboard_bp.route('/category/new', methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        newcate = Category(catname=name)
        db.get_result({"function": db.INSERT_CATEGORY,
                       "content": newcate.to_dict()})
        flash("添加成功！", "success")
        return redirect(url_for('dashboard.manage_category'))
    return render_template('dashboard/new_category.html', form=form)


@dashboard_bp.route('/category/<string:cat_name>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(cat_name):
    form = CategoryForm()
    form.name(render_kw={'placeholder': cat_name})
    category = db.get_result({"function": db.GET_CAT_BY_NAME, "content": {
        "catname": cat_name
    }})["content"]
    if category["catid"] == 1:
        flash('You can not edit the default category.', 'warning')
        return redirect(url_for('front.index'))
    if form.validate_on_submit():
        '''需要数据库新功能'''
        db.get_result({"function": db.UPDATE_CAT_NAME_BY_ID, "content":{
            "catid": category["catid"],
            "catname": form.name.data
        }})
    return render_template('dashboard/edit_category.html', form=form)


@dashboard_bp.route('/category/<string:cat_name>/delete', methods=['POST'])
@login_required
def delete_category(cat_name):
    category = db.get_result({"function": db.GET_CAT_BY_NAME, "content":{
        "catname": cat_name
    }})['content']
    if category['catid'] == 1:
        flash('You can not delete the default category.', 'warning')
        return redirect(url_for('blog.index'))
    db.get_result({"function": db.DELETE_CATEGORY, "content":{
        "catid": category['catid']
    }})
    flash('Category deleted.', 'success')
    return redirect(url_for('.manage_category'))


@dashboard_bp.route('/category/manage', methods=['GET', 'POST'])
@login_required
def manage_category():
    return render_template('dashboard/manage_category.html')


@dashboard_bp.route('/users/manage', methods=['GET', 'POST'])
@login_required
def manage_users():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['USERS_PER_PAGE']
    start = per_page * (page - 1) + 1
    ret = db.get_result({"function": db.GET_USERS, "content":{
        "start": start,
        "number": per_page
    }})
    if ret["content"]:
        page_record = Page(page, per_page)
        if page <= 1:
            page_record.has_prev = False
        else:
            page_record.has_prev = True
        if len(ret["content"]) < per_page:
            page_record.is_last = True
    else:  # 啥都没有，说明最后了
        page_record = Page(page, per_page, True)
        page_record.has_prev = True
        page_record.is_last = True
    users = ret['content']
    return render_template('dashboard/manage_users.html', users=users, page=page_record)


@dashboard_bp.route('/users/<string:name>/delete', methods=['POST'])
@login_required
def delete_user(name):
    db.get_result({"function": db.DELETE_USER_BY_NAME, "content":{
        "name": name
    }})
    flash('User deleted.', 'success')
    return redirect(url_for('.manage_users'))


# 对未过目的问题进行管理
@dashboard_bp.route('/answers/manage', methods=['GET', 'POST'])
@login_required
def manage_answers():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ANSWERS_PER_PAGE']
    ret = db.get_result({"function": db.GET_UNREAD_ANSWER, "content":{
        "number": per_page,
        "start": per_page * (page - 1) + 1
    }})
    if ret["content"]:
        page_record = Page(page, per_page)
        if page <= 1:
            page_record.has_prev = False
        else:
            page_record.has_prev = True
        if len(ret["content"]) < per_page:
            page_record.is_last = True
    else:  # 啥都没有，说明最后了
        page_record = Page(page, per_page, True)
        page_record.has_prev = True
        page_record.is_last = True
    unread_answers = ret['content']
    return render_template('dashboard/manage_answers.html', answers=unread_answers, page=page_record)


@dashboard_bp.route('/answer/manage/read/<int:ans_id>', methods=['POST'])
@login_required
def read_answer(ans_id):
    db.get_result({"function": db.SET_ANSWER_READ, "content":{
        "ansid": ans_id
    }})
    flash('Answer readed', 'success')
    return redirect(url_for('.manage_answers'))