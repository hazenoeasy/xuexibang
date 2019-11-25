#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Jinyang Shao'

'''
后台管理，主要负责 dashboard.html 的数据处理,后台负责删除已经发布的问题，管理注册的用户
'''

from flask import render_template, Blueprint

from xuexibang.main.utils import redirect_back
from database.api.main_base import *

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/manager')
def settings():
    o = Operator()
    admin = o.get_result()
    return render_template('dashboard/dashboard.html')