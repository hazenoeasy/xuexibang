#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Jinyang Shao'

'''
这个负责网站主页前台的数据传送和获取
'''

from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, abort, make_response

# from xuexibang.main.email import *
# from xuexibang.main.extensions import *
#  from xuexibang.main.forms import QuestionForm

front_bp = Blueprint('front', __name__)


class current_user:
    is_authenticated = False


@front_bp.route('/home')  # test
def home():
    return render_template('front/home.html', data=['some', 'data', 'from', 'the', 'back', 'end'])


@front_bp.route('/')
def index():
    per_page = current_app.config['QUESTION_POST_PER_PAGE']
    # question = o.getresult(10,sdfsa)
    question = "data"
    return render_template('front/home.html', question=question)


@front_bp.route('/myquestion')
def myquestion():
    question = "data"
    return render_template('front/myquestion.html', question=question)


@front_bp.route('/qna', methods=['GET', 'POST'])
def qna():  # 回答相应的问题
    return render_template('front/qna.html')