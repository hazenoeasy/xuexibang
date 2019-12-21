# -*- coding:utf-8 -*-
__author__ = 'Jinyang Shao'

from flask_ckeditor import CKEditorField  # 富文本编辑器
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, IntegerField, \
    TextAreaField, SubmitField, MultipleFileField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, Email, Regexp, EqualTo

from extensions import db


class LoginForm(FlaskForm):
    # 使用render_kw来为表单项增加属性placeholder
    username = StringField('Username', validators=[DataRequired()], render_kw={'placeholder': 'username'})
    password = PasswordField('Password', validators=[DataRequired(), Length(3, 128)], render_kw={'placeholder': '>=3'})
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 254), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(3, 128), EqualTo('password2')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), Length(3, 128)])  # 未添加验证
    submit = SubmitField('Register')

    def validate_username(self, field):  # 防止用户名重复
        exist =  db.get_result({"function" : db.GET_UER_BY_NAME, "content": {
            "name" : field.data
        }})["content"]
        if exist:
            raise ValidationError('The username is already in use.')
# 之后再加个get_user_by_email


class HomeForm(FlaskForm):
    # 问题标题
    title = StringField('问题标题', validators=[DataRequired()])
    # 问题分类
    category = SelectField('问题种类', coerce=int, default=1)
    # 问题描述
    description = StringField('问题描述', validators=[DataRequired()])
    # 发布问题按钮
    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super(HomeForm, self).__init__(*args, **kwargs)
        categories = db.get_result({"function":db.GET_ALL_CATEGORY})
        self.category.choices = [(catid, catname)
                                 for catid, catname in categories["content"].iteritems()]


class AnswerForm(FlaskForm):
    # 回答问题文本框
    answer = TextAreaField('答案', validators=[DataRequired()], render_kw={'placeholder': 'please input the answer'})
    # 提交按钮
    submit = SubmitField('提交')


class CategoryForm(FlaskForm):  # 用于新增种类的表单
    name = StringField('Name', validators=[DataRequired(),  Length(1, 30)])
    submit = SubmitField('提交')

    def validate_name(self, field):   # 注意 不要写成validate_on_submit了
        ret = db.get_result({"function" : db.GET_CAT_BY_NAME, "content" : {
            "catname" : field.data
        }})
        if ret["content"]:
            raise ValidationError('The category name is already in use.')


class AdminForm(FlaskForm):   # 用于更改管理员密码
    password = PasswordField('New Password', validators=[DataRequired(), Length(3, 128), EqualTo('password2')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), Length(3, 128)])  # 未添加验证
    submit = SubmitField('ChangePass')