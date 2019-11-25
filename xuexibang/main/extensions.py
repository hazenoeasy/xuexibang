#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Jinyang Shao'

'''
一些全局变量：数据库、富文本编辑器、时间戳
'''
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_mail import Mail
from flask_moment import Moment
from database.api.main_base import *

bootstrap = Bootstrap()
db = Operator()
mail = Mail()
ckeditor = CKEditor()
moment = Moment()
