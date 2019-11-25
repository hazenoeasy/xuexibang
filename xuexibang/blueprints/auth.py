#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Jinyang Shao'

'''
用户注册认证后台管理
'''

from flask import render_template, Blueprint, redirect, flash, url_for

from xuexibang.main.forms import LoginForm, RegisterForm
from xuexibang.main.utils import redirect_back

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash('Welcome home, %s!' % username)
        return redirect(url_for('home'))
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
def logout():
    return redirect_back()


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        flash('新用户：%s, email: %s' % username, email)
        return redirect(url_for('home'))
    return render_template('auth/register.html', data=['data'], form=form)

