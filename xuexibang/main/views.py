#-*- coding: utf-8 -*-
import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

from flask import flash, redirect, url_for, render_template

from xuexibang import app  # , db
from xuexibang.main.forms import LoginForm, RegisterForm, HomeForm
# app.config['SECRET_KEY'] = '123456'

# 对于URL http://localhost:5000/
@app.route('/')
def hello():
    return redirect(url_for('home'))


@app.route('/home')
def home():
    form = HomeForm()
    if form.validate_on_submit():
        title=form.title.data
        description=form.description.data
        return redirect(url_for('home'))
    return render_template('home.html', data=['data'],form=form)


@app.route('/register')
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        flash('新用户：%s, email: %s' % username, email)
        return redirect(url_for('home'))
    return render_template('register.html', data=['data'], form=form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash('Welcome home, %s!' % username)
        return redirect(url_for('home'))
    return render_template('signin.html', data=['data'], form=form)


@app.route('/myquestion')
def myquestion():
    return render_template('myquestion.html', data=['data'])


@app.route('/qna')
def qna():
    return render_template('qna.html', data=['data'])