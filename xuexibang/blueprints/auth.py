#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Jinyang Shao'

'''
用户注册认证后台管理
'''

from flask import render_template, Blueprint, redirect, flash, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
#login_user用于后续的管理员登录
from xuexibang.main.forms import LoginForm, RegisterForm
from xuexibang.main.utils import redirect_back
from xuexibang.main.extensions import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    from database.models.model import UserInfo
    if current_user.is_authenticated:
        return redirect((url_for('front.home')))
    form = LoginForm()
    if form.validate_on_submit():
        username_input = form.username.data
        password_input = form.password.data
        remember = form.remember.data
        userinfo = db.get_result({"function": db.GET_UER_BY_NAME, "content": {
            "name" : username_input
        }})['content']

        if userinfo:
            user = UserInfo(uid=userinfo['uid'], name=userinfo['name'], email=userinfo['email'], admin=userinfo['admin'],
                         password_hash=userinfo['password_hash'])
            if user.validate_password(password_input):
                login_user(user, remember)
                flash('欢迎回来, %s!' % username_input)
                return redirect_back()
        else:
            flash('No account.', 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout success .', 'info')
    return redirect((url_for('front.home')))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    from database.models.model import UserInfo
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data.lower()
        password = form.password.data
        ret = db.get_result({"function" : db.GET_UER_BY_NAME, "content" : {
            "name" : username
        }})
        if ret["content"] is None:
            user = UserInfo(name=username, email=email, admin=False)
            user.set_password(password)
            ret = db.get_result({"function": db.INSERT_USER, "content": user.to_dict()})
            if ret["success"]:
                flash('注册%s！请登录' % ret["success"])
                return redirect(url_for('auth.login'))
            else:
                flash('注册失败')
                return redirect(url_for('auth.register'))
        else:
            flash('用户名已存在！重新注册')
            return redirect(url_for('auth.register'))
    return render_template('auth/register.html', form=form)

